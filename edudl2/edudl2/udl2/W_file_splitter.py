from __future__ import absolute_import
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
import datetime
from edudl2.udl2_util.file_util import get_file_type_from_dir
from edudl2.filesplitter.file_splitter import split_file
from edudl2.udl2_util.measurement import BatchTableBenchmark
from celery.utils.log import get_task_logger
from edcore.notification.constants import Constants as NotificationConstants,\
    Constants
from edudl2.udl2_util.util import merge_to_udl2stat_notification


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_splitter.task", base=Udl2BaseTask)
def task(incoming_msg):
    '''
    This is the celery task for splitting file
    '''
    start_time = datetime.datetime.now()
    guid_batch = incoming_msg[mk.GUID_BATCH]
    parts = incoming_msg[mk.PARTS]
    load_type = incoming_msg[mk.LOAD_TYPE]
    tenant_directory_paths = incoming_msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]
    csv_file = get_file_type_from_dir('.csv', expanded_dir)

    subfiles_dir = tenant_directory_paths[mk.SUBFILES]

    # do actual work of splitting file
    split_file_tuple_list, header_file_path, \
        totalrows, filesize = split_file(csv_file, parts=parts, output_dir=subfiles_dir)

    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time

    logger.info(task.name)
    logger.info("FILE_SPLITTER: Split <%s> into %i sub-files in %s" % (csv_file, parts, spend_time))

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, finish_time,
                                    size_records=totalrows, size_units=filesize, udl_phase_step_status=NotificationConstants.SUCCESS,
                                    task_id=str(task.request.id), tenant=incoming_msg[mk.TENANT_NAME])
    benchmark.record_benchmark()
    # update udl_stat for notification
    merge_to_udl2stat_notification(guid_batch, {Constants.UDL_PHASE_STEP_STATUS: NotificationConstants.SUCCESS})
    # Outgoing message to be piped to the parallel file loader
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({mk.SPLIT_FILE_LIST: split_file_tuple_list,
                         mk.HEADER_FILE_PATH: header_file_path,
                         mk.SIZE_RECORDS: totalrows
                         })
    return outgoing_msg
