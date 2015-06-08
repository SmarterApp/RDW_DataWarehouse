'''
Created on May 12, 2015

@author: tosako
'''

from edcore.database.utils.query import get_udl_stats_by_date
from edcore.database.utils.constants import UdlStatsConstants
from sqlalchemy.sql.expression import select, and_
from edudl2.database.udl2_connector import get_udl_connection, initialize_all_db, \
    get_prod_connection
from edudl2.udl2.constants import Constants
import tempfile
import os
from edcore.utils.utils import archive_files, run_cron_job, create_daemon
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import csv
import pkg_resources
from jinja2 import Template
import datetime
import argparse
import time
import copy
import re
from email.mime.text import MIMEText
from edudl2.udl2_util.util import send_email
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from email.mime.base import MIMEBase
from email import encoders

STUDENT_ID = 'student_id'
ASMT_GUID = 'asmt_guid'
INGESTED_RECORDS = 'ingested_records'

DAILY = 'daily'
WEEKLY = 'weekly'
UDL_REPORT_ENABLED = 'mail.udl_report.enabled'
UDL_REPORT_UID = 'mail.udl_report.uid'
UDL_REPORT_MAIL_TO = 'mail.udl_report.to'
UDL_REPORT_SUBJECT = 'mail.udl_report.subject'
UDL_REPORT_MAIL_FROM = 'mail.udl_report.from'


def generate_report(email_to, start_date, end_date=None, email_from='noreply@smarterbalanced.org', subject='my subject'):
    '''
    generate report by batch
    '''
    reports_data = create_report_data(start_date, end_date)
    summary = {'start_date': start_date}
    if end_date is not None:
        summary['end_date'] = end_date
    if reports_data:
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = os.path.join(tmp, 'data')
            os.mkdir(data_dir)
            results = []
            for datestamp in reports_data.keys():
                report_data = reports_data[datestamp]
                csv_file = os.path.join(data_dir, 'report_' + datestamp + '.csv')
                export_to_csv(csv_file, report_data)
                results.append({'datestamp': datestamp, 'counts': len(report_data)})
            summary['results'] = results
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            report_file = os.path.join(tmp, 'report_' + today + '.zip')
            # archive
            archive_files(data_dir, report_file)
            # create email content
            mail_content = create_email_content(summary)
            send_report(email_to, email_from, subject, mail_content, report_file=report_file)
    else:
        # create email content
        mail_content = create_email_content(summary)
        send_report(email_to, email_from, subject, mail_content, report_file=None)
        # send
    return


def send_report(email_to, email_from, subject, mail_content, report_file=None):
    text_message = MIMEText(mail_content)
    if report_file is None:
        text_message['From'] = email_from
        text_message['To'] = email_to
        text_message['Subject'] = subject
        send_email(text_message)
    else:
        message = MIMEMultipart()
        message['From'] = email_from
        message['To'] = email_to
        message['Subject'] = subject
        mime = MIMEBase('application', "octet-stream")
        message.attach(text_message)
        with open(report_file, 'rb') as f:
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            mime.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(report_file))
            message.attach(mime)
        send_email(message)


def create_email_content(summary):
    template_filename = os.path.join(pkg_resources.resource_filename('edudl2', 'templates'), "udl_report.j2")
    with open(template_filename) as fh:
        template_text = fh.read()

        template = Template(template_text)
        mail_content = template.render(summary)
    return mail_content


def export_to_csv(file_path, report_data):
    with open(file_path, 'w') as f:
        fieldnames = [STUDENT_ID, ASMT_GUID]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(report_data)


def create_report_data(start_date, end_date=None):
    '''
    Find migrate ingested batch from edware_stats
    '''
    reports = {}
    udl_stats_results = get_udl_stats_by_date(start_date, end_date=end_date)
    for udl_stats_result in udl_stats_results:
        batch_guid = udl_stats_result[UdlStatsConstants.BATCH_GUID]
        load_status = udl_stats_result[UdlStatsConstants.LOAD_STATUS]
        tenant = udl_stats_result[UdlStatsConstants.TENANT]
        if load_status == UdlStatsConstants.MIGRATE_INGESTED:
            records = get_udl_record_by_batch_guid(batch_guid, tenant)
            report_data = {}
            for record in records:
                '''
                remove any duplicated records
                '''
                report_data[record[STUDENT_ID] + record[ASMT_GUID]] = {STUDENT_ID: record[STUDENT_ID], ASMT_GUID: record[ASMT_GUID]}
            file_name = get_intput_file(batch_guid)
            m = re.search('(\d+-\d+-\d+)', file_name)
            if m:
                datestamp = m.group(0)
            else:
                datestamp = 'UNKNOWN_DATE'
            report = reports.get(datestamp, [])
            if not report:
                '''
                if report is just initialized, dict does not have ref to report variable.
                '''
                reports[datestamp] = report
            for key in sorted(report_data.keys()):
                report.append(report_data[key])
    return reports


def get_udl_record_by_batch_guid(batch_guid, tenant):
    records = []
    with get_prod_connection(tenant=tenant) as connection:
        fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
        fact_block_asmt_outcome = connection.get_table('fact_block_asmt_outcome')
        select_fao = select([fact_asmt_outcome.c.student_id.label(STUDENT_ID), fact_asmt_outcome.c.asmt_guid.label(ASMT_GUID)]).where(and_(fact_asmt_outcome.c.batch_guid == batch_guid, fact_asmt_outcome.c.rec_status == 'C'))
        select_fbao = select([fact_block_asmt_outcome.c.student_id.label(STUDENT_ID), fact_block_asmt_outcome.c.asmt_guid.label(ASMT_GUID)]).where(and_(fact_block_asmt_outcome.c.batch_guid == batch_guid, fact_block_asmt_outcome.c.rec_status == 'C'))
        records = connection.get_result(select_fao.union(select_fbao))
    return records


def get_intput_file(batch_guid):
    input_file = ''
    with get_udl_connection() as connector:
        batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
        s = select([batch_table.c.input_file.label('input_file')]).where(and_(batch_table.c.udl_phase == 'udl2.W_file_arrived.task', batch_table.c.guid_batch == batch_guid))
        results = connector.get_result(s)
        if results:
            input_file = results[0]['input_file']
    return input_file


try:
    config_path_file = os.environ['UDL2_CONF']
except Exception:
    config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE


def generate_report_for_cron(settings):
    report_hour = settings['hour']
    today = datetime.datetime.today().strftime('%Y-%m-%d ' + str(report_hour) + ':00:00')
    start_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:00:00')
    end_date = today
    generate_report(settings['mail_to'], start_date, end_date, settings['mail_from'], settings['subject'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate udl report')
    parser.add_argument('-i', dest='ini_file', help='Set the path to ini file', default=UDL2_DEFAULT_CONFIG_PATH_FILE)
    parser.add_argument('--hour', dest='hour', help='hour to run this script', default='10')
    parser.add_argument('-r', dest='report_hour', help='report hour, e.g. yesterday 10am to today 10am', default='10')
    parser.add_argument('-p', dest='pidfile', default='/opt/edware/run/edudl2-report.pid',
                        help="pid file for edudl2 trigger daemon")
    parser.add_argument('-d', dest='daemon', action='store_true', default=False,
                        help="daemon mode for udl report")
    args = parser.parse_args()

    config_path_file = args.ini_file
    hour = args.hour
    report_hour = args.report_hour
    daemon_mode = args.daemon
    pid_file = args.pidfile
    if daemon_mode:
        create_daemon(pid_file)
    # get udl2 configuration as nested and flat dictionary
    udl2_conf, udl2_flat_conf = read_ini_file(config_path_file)
    initialize_all_db(udl2_conf, udl2_flat_conf)

    email_to = udl2_flat_conf.get(UDL_REPORT_MAIL_TO)
    subject = udl2_flat_conf.get(UDL_REPORT_SUBJECT)
    email_from = udl2_flat_conf.get(UDL_REPORT_MAIL_FROM)
    enabled = udl2_flat_conf.get(UDL_REPORT_ENABLED)
    start_date = today = datetime.datetime.today().strftime('%Y-%m-%d %H:00:00')
    if enabled is not None and enabled.lower() == 'True':
        generate_report_settings = {'report.enable': 'True',
                                    'report.schedule.cron.hour': hour,
                                    'report.schedule.cron.minute': '0',
                                    'report.schedule.cron.second': '0',
                                    'hour': report_hour,
                                    'mail_to': email_to,
                                    'subject': subject,
                                    'mail_from': email_from}
        run_cron_job(copy.deepcopy(generate_report_settings), 'report.', generate_report_for_cron)

        while True:
            time.sleep(1)
