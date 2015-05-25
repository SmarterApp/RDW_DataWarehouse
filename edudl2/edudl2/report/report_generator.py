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
from edcore.utils.utils import archive_files, run_cron_job
from hpz_client.frs.file_registration import register_file
from hpz_client.frs.http_file_upload import http_file_upload
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import csv
import pkg_resources
from jinja2 import Template
import datetime
import argparse
import time
import copy

STUDENT_ID = 'student_id'
ASMT_GUID = 'asmt_guid'
INGESTED_RECORDS = 'ingested_records'

DAILY = 'daily'
WEEKLY = 'weekly'
UDL_REPORT_UID = 'report.uid'
UDL_REPORT_MAIL_TO = 'report.mail_to'
UDL_REPORT_SUBJECT = 'report.subject'
UDL_REPORT_MAIL_FROM = 'report.mail_from'


def generate_report(uid, email_to, start_date, end_date=None, email_from='noreply@smarterbalanced.org', subject='my subject'):
    '''
    generate report by batch
    '''
    report_data = create_report_data(start_date, end_date)
    registration_id, download_url, web_download_url = register_file(uid, email_to)
    summary = {'hpz_web_url': web_download_url, 'start_date': start_date}
    if end_date is not None:
        summary['end_date'] = end_date
    reports = []
    # register
    if report_data:
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = os.path.join(tmp, 'data')
            os.mkdir(data_dir)
            csv_file = os.path.join(data_dir, 'report.csv')
            export_to_csv(csv_file, report_data)
            summary['records'] = len(report_data)
            report_file = os.path.join(tmp, 'report.zip')
            # archive
            archive_files(data_dir, report_file)
            # create email content
            mail_content = create_email_content(summary)
            http_file_upload(report_file, registration_id, email_from=email_from, email_subject=subject, email_content=mail_content)
    else:
        # create email content
        mail_content = create_email_content(summary, web_download_url)
        # send
        http_file_upload(None, registration_id, email_from=email_from, email_subject=subject, email_content=mail_content)
    return


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
    report = []
    report_data = {}
    udl_stats_results = get_udl_stats_by_date(start_date, end_date=end_date)
    for udl_stats_result in udl_stats_results:
        batch_guid = udl_stats_result[UdlStatsConstants.BATCH_GUID]
        load_status = udl_stats_result[UdlStatsConstants.LOAD_STATUS]
        tenant = udl_stats_result[UdlStatsConstants.TENANT]
        if load_status == UdlStatsConstants.MIGRATE_INGESTED:
            records = get_udl_record_by_batch_guid(batch_guid, tenant)
            for record in records:
                report_data[record[STUDENT_ID] + record[ASMT_GUID]] = {STUDENT_ID: record[STUDENT_ID], ASMT_GUID: record[ASMT_GUID]}
    for key in sorted(report_data.keys()):
        report.append(report_data[key])
    return report


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
    generate_report(settings['uid'], settings['mail_to'], settings['start_date'], settings['end_date'], settings['mail_from'], settings['subject'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate udl report')
    parser.add_argument('-c', '--config', help='Set the path to ini file', default=UDL2_DEFAULT_CONFIG_PATH_FILE)
    args = parser.parse_args()

    config_path_file = args.config
    # get udl2 configuration as nested and flat dictionary
    # TODO: Refactor to use either flat or map structure
    udl2_conf, udl2_flat_conf = read_ini_file(config_path_file)
    initialize_all_db(udl2_conf, udl2_flat_conf)

    uid = udl2_conf.get(UDL_REPORT_UID)
    email_to = udl2_conf.get(UDL_REPORT_MAIL_TO)
    subject = udl2_conf.get(UDL_REPORT_SUBJECT)
    mail_from = udl2_conf.get(UDL_REPORT_MAIL_FROM)
    today = datetime.date.today()
    end = None
    start = today
    generate_report_settings = {'report.enable': 'True',
                                'report.schedule.cron.hour': '1',
                                'report.schedule.cron.minute': '0',
                                'report.schedule.cron.second': '0',
                                'uid': uid,
                                'mail_to': email_to,
                                'subject': subject,
                                'mail_from': mail_from,
                                'start_date': start,
                                'end_date': None}
    run_cron_job(copy.deepcopy(generate_report_settings), 'report.', generate_report_for_cron)

    one_week = datetime.timedelta(weeks=1)
    start = today - one_week
    end = today
    generate_report_settings['report.schedule.cron.day_of_week'] = '6'
    generate_report_settings['report.schedule.cron.hour'] = '2'
    generate_report_settings['end_date'] = end
    run_cron_job(generate_report_settings, 'report.', generate_report_for_cron)

    while True:
        time.sleep(1)
