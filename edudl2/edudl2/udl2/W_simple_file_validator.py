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
from celery.utils.log import get_task_logger
import datetime
import os
from edudl2.udl2.celery import udl2_conf, celery
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.sfv.simple_file_validator import SimpleFileValidator
from edudl2.udl2_util.measurement import BatchTableBenchmark

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_validator.task", base=Udl2BaseTask)
def task(incoming_msg):
    start_time = datetime.datetime.now()
    guid_batch = incoming_msg[mk.GUID_BATCH]
    load_type = incoming_msg[mk.LOAD_TYPE]

    tenant_directory_paths = incoming_msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]

    sfv = SimpleFileValidator(load_type)
    error_map = {}
    for file_name in os.listdir(expanded_dir):
        error_map[file_name] = sfv.execute(expanded_dir, file_name, guid_batch)

    # TODO: Add logic that checks error list and writes to a log/db/etc
    for input_file in error_map.keys():
        errors = error_map[input_file]
        if len(errors) == 0:
            logger.info('FILE VALIDATOR: Validated file <%s> and found no errors.' % (os.path.join(expanded_dir, input_file)))
        else:
            # TODO: Jump to ERROR_TASK
            for error in errors:
                logger.error('ERROR: ' + str(error))
            raise Exception('simple file validator error: %s' % errors)

    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, incoming_msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id),
                                    tenant=incoming_msg[mk.TENANT_NAME])
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file splitter
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    return outgoing_msg


# TODO: Actually implement get_number_of_parts()
def get_number_of_parts():
    return 4
