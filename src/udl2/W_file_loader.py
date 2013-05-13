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
    csv_file_path = msg['file_to_load']
    header_file_path = msg['header_file']
    start_seq = msg['row_start']
    landing_zone_file = msg['landing_zone_file']
    work_zone = msg['work_zone']
    history = msg['history']
    logger.info(task.name)
    logger.info('Loading file %s...' % csv_file_path)
    conf = generate_conf_for_loading(csv_file_path, header_file_path, start_seq, landing_zone_file, work_zone, history)
    load_file(conf)
   
#    if udl2_stages[task.name]['next'] is not None:
#        next_msg = [file_name + ' passed after ' + task.name]
#        exec("task_instance = " + udl2_stages[task.name]['next']['task'])
#        task_instance.apply_async(next_msg,
#                                  udl2_queues[task.name]['queue'],
#                                  udl2_stages[task.name]['routing_key'])
    udl2.W_final_cleanup.task.apply_async([conf], queue='Q_final_cleanup', routing_key='udl2')
    return msg


def generate_conf_for_loading(csv_file_path, header_file_path, start_seq, landing_zone_file, work_zone, history):
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
            'db_user': 'postgres',
            'db_name': 'fdw_test',
            'db_password': '3423346',
            'csv_schema': 'public',
            'fdw_server': 'udl_import',
            'staging_schema': 'public',
            'staging_table': 'tmp',
            'apply_rules': False,
            'landing_zone_file': landing_zone_file,
            'work_zone': work_zone,
            'history': history
    }
    return conf


@celery.task(name="udl2.W_file_loader.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
