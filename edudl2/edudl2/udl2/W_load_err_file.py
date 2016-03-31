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

from __future__ import absolute_import

import json

from celery.utils.log import get_task_logger

from edcore.notification.constants import Constants

from edudl2.udl2 import message_keys as mk
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2_util import file_util
from edudl2.udl2_util.util import merge_to_udl2stat_notification

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_err_file.task", base=Udl2BaseTask)
def task(incoming_msg):
    '''
    This is the celery task to load err file
    '''
    guid_batch = incoming_msg.get(mk.GUID_BATCH)
    # Outgoing message to be piped to the file expander
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    tenant_directory_paths = incoming_msg.get(mk.TENANT_DIRECTORY_PATHS)
    expanded_dir = tenant_directory_paths.get(mk.EXPANDED)
    err_file = file_util.get_file_type_from_dir('.err', expanded_dir)
    if err_file is not None:
        with file_util.open_udl_file(err_file) as f:
            json_data = f.read()
            error_json = json.loads(json_data)
            content = error_json['content']
            if content == 'error':
                tsb_error = error_json['tsb_error']
                outgoing_msg['tsb_error'] = tsb_error
                notification_data = {'tsb_error': tsb_error}
                notification_data[Constants.ERROR_DESC] = 'tsb error'
                merge_to_udl2stat_notification(guid_batch, notification_data)

    return outgoing_msg
