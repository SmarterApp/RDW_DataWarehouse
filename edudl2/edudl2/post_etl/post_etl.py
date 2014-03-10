import logging
import os
import shutil
import edudl2.udl2.message_keys as mk
from edudl2.udl2.celery import udl2_conf
from edcore.utils.cleanup import cleanup_all_tables
from edudl2.udl2.udl2_connector import get_udl_connection

__author__ = 'sravi'

logger = logging.getLogger(__name__)


def get_work_zone_directories_to_cleanup(msg):
    tenant_directory_paths = msg[mk.TENANT_DIRECTORY_PATHS]
    work_zone_directories_to_cleanup = {
        mk.ARRIVED: tenant_directory_paths[mk.ARRIVED],
        mk.DECRYPTED: tenant_directory_paths[mk.DECRYPTED],
        mk.EXPANDED: tenant_directory_paths[mk.EXPANDED],
        mk.SUBFILES: tenant_directory_paths[mk.SUBFILES]
    }
    return work_zone_directories_to_cleanup


def cleanup_work_zone(work_zone_directories_to_cleanup):
    """
    Remove all the directories in the given dict
    :param work_zone_directories_to_cleanup: a dictionary of directories
    :return:
    """
    for directory in work_zone_directories_to_cleanup.values():
        # cleanup the entire directory recursively
        if os.path.exists(directory):
            shutil.rmtree(directory)
    return True


def cleanup_udl_tables(guid_batch):
    """
    """
    with get_udl_connection() as connector:
        schema_name = udl2_conf['udl2_db']['db_schema']
        cleanup_all_tables(connector=connector, schema_name=schema_name,
                           column_name='guid_batch', value=guid_batch, batch_delete=True, table_name_prefix='int_')
        cleanup_all_tables(connector=connector, schema_name=schema_name,
                           column_name='guid_batch', value=guid_batch, batch_delete=True, table_name_prefix='stg_')


def cleanup(msg):
    """
    UDL batch cleanup up operation

    :param msg: Pipeline message passed down from the task
    """
    work_zone_directories_to_cleanup = get_work_zone_directories_to_cleanup(msg)
    guid_batch = msg[mk.GUID_BATCH]

    # cleanup workzone
    cleanup_work_zone(work_zone_directories_to_cleanup)

    # cleanup udl tables
    cleanup_udl_tables(guid_batch)
