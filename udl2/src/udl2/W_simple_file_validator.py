from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from sfv.simple_file_validator import SimpleFileValidator
from udl2_util.file_util import get_expanded_dir
import os
import udl2.message_keys as mk
from udl2_util.measurement import measure_cpu_plus_elasped_time, benchmarking_udl2

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_validator.task")
@benchmarking_udl2
def task(msg):
    lzw = msg[mk.LANDING_ZONE_WORK_DIR]
    guid_batch = msg[mk.GUID_BATCH]

    expanded_dir = get_expanded_dir(lzw, guid_batch)

    sfv = SimpleFileValidator()
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
                print('ERROR: ' + str(error))

    # benchmark
    benchmark = {mk.TASK_ID: str(task.request.id)}
    return benchmark


# TODO: Actually implement get_number_of_parts()
@measure_cpu_plus_elasped_time
def get_number_of_parts():
    return 4
