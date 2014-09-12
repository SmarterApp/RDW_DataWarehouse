from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from sqlalchemy.sql.expression import select
import json
from edcore.database.utils.query import update_udl_stats_by_batch_guid
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
        query = select([udl_status_table.c.notification], from_obj=[udl_status_table]).where(udl_status_table.c.batch_guid == UdlStatsConstants.UDL_STATUS_INGESTED)
        batches = connector.get_result(query)

    # there should be one record.
    for batch in batches:
        notification = batch[UdlStatsConstants.NOTIFICATION]
        notification_dict = json.loads(notification)
        notification_dict.update(notification_data)
        update_udl_stats_by_batch_guid(batch_id, {UdlStatsConstants.NOTIFICATION: json.dumps(notification_dict)})
