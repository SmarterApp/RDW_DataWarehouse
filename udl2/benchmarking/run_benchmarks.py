'''
Created on Sep 20, 2013

@author: swimberly
'''
import argparse
import imp
import os

from sqlalchemy.sql import select

from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from scripts.driver import start_pipeline
from udl2.celery import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from udl2_util.database_util import connect_db, get_schema_metadata


CSV_FILES = ['REALDATA_RECORDS_10K.csv', 'REALDATA_RECORDS_50K.csv', 'REALDATA_RECORDS_100K.csv',
             'REALDATA_RECORDS_500K.csv', 'REALDATA_RECORDS_2M.csv', 'REALDATA_RECORDS_5M.csv']
JSON_FILES = ['METADATA_RECORDS_10K.json', 'METADATA_RECORDS_50K.json', 'METADATA_RECORDS_100K.json',
              'METADATA_RECORDS_500K.json', 'METADATA_RECORDS_2M.json', 'METADATA_RECORDS_5M.json']

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
logger = get_task_logger(__name__)

config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE

udl2_conf = imp.load_source('udl2_conf', config_path_file)
from udl2_conf import udl2_conf


def start_test(directory_path, memory, cpu, hist_db, hist_schema, port, user, passwd):
    '''
    kick off the tests by scheduling the task with celery
    '''
    run_pipeline.apply_async(({'directory': directory_path, 'memory': memory, 'cpu': cpu, 'hist_db': hist_db,
                               'hist_schema': hist_schema, 'port': port, 'user': user, 'passwd': passwd}, ))


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


def record_benchmark_info(batch_guid, history_schema_name, history_table_name):
    '''
    Record the benchmarking information in the table
    '''
    logger.info('Writing Benchmark to database')
    (conn, engine) = connect_db(udl2_conf['udl2_db']['db_driver'],
                                 udl2_conf['udl2_db']['db_user'],
                                 udl2_conf['udl2_db']['db_pass'],
                                 udl2_conf['udl2_db']['db_host'],
                                 udl2_conf['udl2_db']['db_port'],
                                 udl2_conf['udl2_db']['db_database'])
    metadata = get_schema_metadata(engine, udl2_conf['udl2_db']['db_schema'])
    batch_table = metadata.tables[udl2_conf['udl2_db']['batch_table']]

    batch_table_res = get_data_from_batch_table(batch_guid, conn, metadata, batch_table)
    conn.close()

    tot_time, tot_count = get_total_time_and_records_from_results(batch_table_res)
    copy_batch_results_to_history_schema(batch_table_res, batch_table)


def get_data_from_batch_table(batch_guid, db_conn, metadata, batch_table):
    '''
    select all the records from the batch table with the given batch_guid
    '''
    batch_select = select([batch_table]).where(batch_table.c.guid_batch == batch_guid)
    return db_conn.execute(batch_select).fetchall()


def copy_batch_results_to_history_schema(results, batch_table, hist_schema, hist_batch_table, db_conn):
    '''
    '''
    res_list_of_dicts = convert_results_to_dict(results, batch_table)
    db_conn.execute(hist_batch_table.insert(), res_list_of_dicts)


def get_total_time_and_records_from_results(row_list):
    '''
    Given a list of result tuples from sqlalchemy query retrieve the total time of the run and
    retrieve the number of records.
    '''
    duration_col = 12
    phase_col = 4
    phase_step_col = 5
    size_records_col = 8
    stage_string = 'INT --> FACT TABLE'
    complete_string = 'UDL_COMPLETE'

    duration = [row[duration_col] for row in row_list if row[phase_col] == complete_string][0]
    size_records = [row[size_records_col] for row in row_list if row[phase_step_col] == stage_string][0]

    return duration, size_records


def convert_results_to_dict(results, table):
    '''
    Take the list of results and the sqlalchemy table object and create a list of dictionaries
    containing all the results
    '''
    columns = table.columns.keys()
    return [{columns[i]: row[i] for i in range(len(columns))} for row in results]


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default=None,
                        help='the location of directory containing the files to use for testing')
    parser.add_argument('-m', '--memory', required=True,
                        help='the amount of memory in the system as a string (ie. "16GB")')
    parser.add_argument('-c', '--cpu', required=True,
                        help='the number of cpus and/or type of cpus on the system (ie. 4 cores 1.9GHz)')
    parser.add_argument('-d', '--history-database', defualt='',
                        help='the name of the database that the history schema is in')
    parser.add_argument('-s', '--history-schema', defualt='',
                        help='the name of the schema where the history table is located')
    parser.add_argument('--port', default=5432,
                        help='the port, default: 5432')
    parser.add_argument('-u', '--user', default='',
                        help='the username to use to connect to the database. default: ')
    parser.add_argument('-p', '--passwd', default='',
                        help='the password to use in connecting to the database')

    args = parser.parse_args()
    directory = args.directory if args.directory else __location__
    memory = args.memory
    cpu = args.cpu
    hist_db = args.history_database
    hist_schema = args.history_schema
    port = args.port
    user = args.user
    passwd = args.passwd
    start_test(directory, memory, cpu, hist_db, hist_schema, port, user, passwd)
