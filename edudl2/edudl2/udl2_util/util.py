from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from sqlalchemy.sql.expression import select
from edudl2.json_util.json_util import get_value_from_json
import json
from edcore.database.utils.query import update_udl_stats_by_batch_guid
from email.mime.text import MIMEText
from jinja2 import Template
import pkg_resources
import smtplib
from email.mime.multipart import MIMEMultipart
__author__ = 'sravi'

import os
from edudl2.udl2_util.file_util import convert_path_to_list
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2.constants import Constants


def get_tenant_name(incoming_file):
    """
    Given the incoming files path return the name of the tenant
    :param incoming_file: the path to the incoming file
    :return: A string containing the tenant name or None
    """
    zones_config = udl2_conf.get(Constants.ZONES)
    if zones_config:
        arrivals_dir_path = zones_config.get(Constants.ARRIVALS)
    if arrivals_dir_path and incoming_file.startswith(arrivals_dir_path):
        relative_file_path = os.path.relpath(incoming_file, arrivals_dir_path)
        folders = convert_path_to_list(relative_file_path)
        return folders[0] if len(folders) > 0 else None
    return None


def merge_to_udl2stat_notification(batch_id, notification_data):
    '''
    merge notification data with given new data in udl2_stat table
    :param batch_id: batch id to be updated
    :param notification_data: new notification data to be included
    '''
    with StatsDBConnection() as connector:
        udl_status_table = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = select([udl_status_table.c.notification], from_obj=[udl_status_table]).where(udl_status_table.c.batch_guid == batch_id)
        batches = connector.get_result(query)

    # there should be one record.
    for batch in batches:
        notification = batch.get(UdlStatsConstants.NOTIFICATION, '{}')
        notification_dict = json.loads(notification if notification is not None else '{}')
        notification_dict.update(notification_data)
        update_udl_stats_by_batch_guid(batch_id, {UdlStatsConstants.NOTIFICATION: json.dumps(notification_dict)})


def get_assessment_type(json_file_dir):
    """
    Get the assessment type for the UDL job from the json file
    @param json_file_dir: A directory that houses the json file
    @return: UDL job assessment type
    @rtype: string
    """
    assessment_types = Constants.ASSESSMENT_TYPES()
    assessment_type = get_value_from_json(json_file_dir, Constants.ASSESSMENT_TYPE_KEY)
    if assessment_type not in assessment_types:
        raise ValueError('No valid load type specified in json file --')
    return assessment_type


def send_email_from_template(substitutions=None):
    if substitutions is None:
        substitutions = {}
    settings = udl2_conf['mail']['udl_fail']
    enabled = settings.get('enabled', False)
    if enabled:
        template_dir = pkg_resources.resource_filename("edudl2", "templates")
        template_filename = os.path.join(template_dir, settings["template_filename"])
        with open(template_filename) as fh:
            template_text = fh.read()

        template = Template(template_text)
        email_text = template.render(substitutions)
        message = MIMEText(email_text)
        message['From'] = settings['from']
        message['To'] = settings['to']
        message['Subject'] = settings['subject']
        send_email(message)


def send_email(mime_message):
    settings = udl2_conf['mail']
    mail_hostname = settings['server_host']
    mail_port = settings.get('server_port', 465)
    aws_mail_username = settings.get('smtp_username')
    aws_mail_password = settings.get('smtp_password')
    if type(mail_port) is str:
        mail_port = int(mail_port)

    if mail_port == 25:
        with smtplib.SMTP(mail_hostname, mail_port) as mail:
            mail.send_message(mime_message)
            mail.quit()
    else:
        with smtplib.SMTP_SSL(mail_hostname, mail_port) as mail:
            mail.login(aws_mail_username, aws_mail_password)
            mail.send_message(mime_message)
            mail.quit()
