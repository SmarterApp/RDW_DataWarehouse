from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
import udl2.W_final_cleanup
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from fileloader.file_loader import load_file
import os


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_loader.task")
def task(msg):
    csv_file_path = msg['input_file']
    header_file_path = msg['header_file']
    start_seq = msg['row_start']
    logger.info(task.name)
    logger.info('Loading file %s...' % csv_file_path)
    conf = generate_conf_for_loading(csv_file_path, header_file_path, start_seq)
    load_file(conf)
   
#    if udl2_stages[task.name]['next'] is not None:
#        next_msg = [file_name + ' passed after ' + task.name]
#        exec("task_instance = " + udl2_stages[task.name]['next']['task'])
#        task_instance.apply_async(next_msg,
#                                  udl2_queues[task.name]['queue'],
#                                  udl2_stages[task.name]['routing_key'])
    udl2.W_final_cleanup.task.apply_async([csv_file_path + ' passed after ' + task.name],
                                           queue='Q_final_cleanup',
                                           routing_key='udl2')
    return msg


def generate_conf_for_loading(csv_file_path, header_file_path, start_seq):
    csv_file_name_and_ext = os.path.splitext(os.path.basename(csv_file_path))
    csv_file_name = csv_file_name_and_ext[0]
    csv_table = csv_file_name
    conf = {
            'csv_file': csv_file_path,
            'start_seq': start_seq,
            'header_file': header_file_path,
            'csv_table': csv_table,
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'udl2',
            'db_name': 'udl2',
            'db_password': 'udl2abc1234',
            'csv_schema': 'udl2',
            'fdw_server': 'udl_import',
            'staging_schema': 'udl2',
            'staging_table': 'STG_SBAC_ASMT_OUTCOME',
            'apply_rules': False,
            # need to replace by passing from file splitter
            'batch_id': 200

    }
    return conf


@celery.task(name="udl2.W_file_loader.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
