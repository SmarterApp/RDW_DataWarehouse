from __future__ import absolute_import
import udl2.celery
import udl2.W_final_cleanup
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from fileloader.file_loader import load_file


logger = get_task_logger(__name__)


@udl2.celery.celery.task(name="udl2.W_file_loader.task")
def task(msg):
    csv_file_path = msg['input_file']
    header_file_path = msg['header_file']
    logger.info(task.name)
    logger.info('Loading file %s...' % csv_file_path)
    conf = generate_conf_for_loading(csv_file_path, header_file_path)
    load_file(conf)
    udl2.W_final_cleanup.task.apply_async([csv_file_path + ' passed after ' + task.name],
                                           queue='Q_final_cleanup',
                                           routing_key='udl2')
    return msg


def generate_conf_for_loading(csv_file_path, header_file_path):
    conf = {
            'csv_file': csv_file_path,
            'header_file': header_file_path,
            'csv_table': 'UDL_test_data_block_of_100_records_with_datatype_errors_v3',
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'postgres',
            'db_name': 'fdw_test',
            'db_password': '3423346',
            'csv_schema': 'public',
            'fdw_server': 'udl_import',
            'staging_schema': 'public',
            'staging_table': 'tmp',
            'apply_rules': False
    }
    return conf


@udl2.celery.celery.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
