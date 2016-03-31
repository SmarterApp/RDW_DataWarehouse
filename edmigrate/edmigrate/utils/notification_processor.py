# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Sep 15, 2014

@author: tosako
'''
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from sqlalchemy.sql.expression import select, and_, or_
from edcore.notification.constants import Constants
from edcore.notification.notification import send_notification


def get_batch_for_notification():
    '''
    get records to send notification from udl_stat table
    '''
    with StatsDBConnection() as connector:
        udl_status_table = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = \
            select([udl_status_table.c.rec_id,
                    udl_status_table.c.batch_guid,
                    udl_status_table.c.load_type,
                    udl_status_table.c.load_status,
                    udl_status_table.c.notification,
                    udl_status_table.c.notification_status],
                   from_obj=[udl_status_table]).\
            where(udl_status_table.c.load_status.in_([UdlStatsConstants.UDL_STATUS_FAILED, UdlStatsConstants.MIGRATE_FAILED, UdlStatsConstants.MIGRATE_INGESTED]))
        query = query.where(and_(or_(udl_status_table.c.notification_status.is_(None), udl_status_table.c.notification_status == ''))).order_by(udl_status_table.c.file_arrived)
        batches = connector.get_result(query)
    return batches


def send_notifications(mail_server, mail_sender):
    '''
    send notifications to call_back and/or mail
    :param mail_server: email server
    :param mail_sender: email sender
    '''
    batches = get_batch_for_notification()
    for batch in batches:
        batch[Constants.MAIL_SERVER] = mail_server
        batch[Constants.MAIL_SENDER] = mail_sender
        send_notification(batch)
