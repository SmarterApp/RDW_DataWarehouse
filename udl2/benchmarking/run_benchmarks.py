'''
Created on Sep 20, 2013

@author: swimberly
'''
import argparse
import imp
import os

from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from scripts.driver import start_pipeline
from udl2.celery import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger


CSV_FILES = ['REALDATA_RECORDS_10K.csv', 'REALDATA_RECORDS_50K.csv', 'REALDATA_RECORDS_100K.csv',
             'REALDATA_RECORDS_500K.csv', 'REALDATA_RECORDS_2M.csv', 'REALDATA_RECORDS_5M.csv']
JSON_FILES = ['METADATA_RECORDS_10K.json', 'METADATA_RECORDS_50K.json', 'METADATA_RECORDS_100K.json',
              'METADATA_RECORDS_500K.json', 'METADATA_RECORDS_2M.json', 'METADATA_RECORDS_5M.json']

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
logger = get_task_logger(__name__)

config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE

udl2_conf = imp.load_source('udl2_conf', config_path_file)
from udl2_conf import udl2_conf


def start_test(directory_path):
    '''
    kick off the tests by scheduling the task with celery
    '''
    run_pipeline.apply_async(({'directory': directory_path}, ))


@celery.task(name='benchmarking.run_benchmarking.run_pipeline')
def run_pipeline(msg):
    '''
    Run the pipeline for the current file and use this task as a callback for future tasks
    '''
    file_index = 0
    if msg.get('batch_guid'):
        record_benchmark_info(msg['batch_guid'])
        file_index = msg['file_index'] + 1

    if file_index >= len(CSV_FILES):
        logger.info('All Tests Complete')
        return

    logger.info('**Running Pipeline test %d**' % file_index)
    directory = msg.get('directory', __location__)

    csv_file = os.path.join(directory, CSV_FILES[file_index])
    json_file = os.path.join(directory, JSON_FILES[file_index])
    start_pipeline(csv_file, json_file, udl2_conf, callback=run_pipeline, file_index=file_index, directory=directory)


@celery.task(name="benchmarking.run_benchmarking.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


def record_benchmark_info(batch_guid):
    '''
    Record the benchmarking information in the table
    '''
    logger.info('Writing Benchmark to database')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default=None,
                        help='the location of directory containing the files to use for testing')

    args = parser.parse_args()
    directory = args.directory if args.directory else __location__
    start_test(directory)
