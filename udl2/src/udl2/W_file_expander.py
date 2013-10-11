from __future__ import absolute_import
import os

from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2_util import file_util
from fileexpander.file_expander import expand_file
import udl2.message_keys as mk

__author__ = 'abrien'

'''
This task takes a zipped file in landing_zone/work/GUID_BATCH/arrived/
and unpacks into landing_zone/work/GUID_BATCH/expanded
'''

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_expander.task")
def task(incoming_msg):

    # Retrieve parameters from the incoming message
    file_to_expand = incoming_msg[mk.FILE_TO_EXPAND]
    guid_batch = incoming_msg[mk.GUID_BATCH]
    tenant_directory_paths = incoming_msg[mk.TENANT_DIRECTORY_PATHS]
    expand_to_dir = tenant_directory_paths['expanded']

    logger.info('W_FILE_EXPANDER: expand file <%s> with guid_batch = <%s> to directory <%s>' % (file_to_expand, guid_batch, expand_to_dir))
    file_contents = expand_file(file_to_expand, expand_to_dir)
    logger.info('W_FILE_EXPANDER: expanded files:  <%s> and <%s>' % (file_contents[0], file_contents[1]))

    # Outgoing message to be piped to the file expander
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({
        mk.JSON_FILENAME: file_contents[0],
        mk.CSV_FILENAME: file_contents[1]
        })
    return outgoing_msg


def unpack_json_file(file_to_expand, expanded_dir, json_filepath):
    # TODO: Remove 3rd param and actually implement this method
    if file_util.copy_file(json_filepath, expanded_dir):
        return os.path.join(expanded_dir, os.path.basename(json_filepath))
    return None


def unpack_csv_file(file_to_expand, expanded_dir, csv_filename):
    # TODO: Remove 3rd param and actually implement this method
    if file_util.copy_file(csv_filename, expanded_dir):
        return os.path.join(expanded_dir, os.path.basename(csv_filename))
    return None
