'''
Created on Sep 20, 2013

@author: swimberly
'''
import argparse
import os
from datetime import date
from sqlalchemy.sql import select
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2.udl2_pipeline import get_pipeline_chain
from edudl2.udl2.celery import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from edudl2.udl2_util.database_util import connect_db, get_sqlalch_table_object
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2.constants import Constants


FILES = ['BENCHMARK_RECORDS_10K.tar.gz.asc', 'BENCHMARK_RECORDS_50K.tar.gz.asc', 'BENCHMARK_RECORDS_100K.tar.gz.asc', 'BENCHMARK_RECORDS_500K.tar.gz.asc', 'BENCHMARK_RECORDS_2M.tar.gz.asc', 'BENCHMARK_RECORDS_5M.tar.gz.asc']
#CSV_FILES = ['REALDATA_RECORDS_10K.csv', 'REALDATA_RECORDS_50K.csv', 'REALDATA_RECORDS_100K.csv',
#             'REALDATA_RECORDS_500K.csv', 'REALDATA_RECORDS_2M.csv', 'REALDATA_RECORDS_5M.csv']
#JSON_FILES = ['METADATA_RECORDS_10K.json', 'METADATA_RECORDS_50K.json', 'METADATA_RECORDS_100K.json',
#              'METADATA_RECORDS_500K.json', 'METADATA_RECORDS_2M.json', 'METADATA_RECORDS_5M.json']
HISTORY_TABLE = 'HISTORY_TABLE'
BATCH_TABLE = 'UDL_BATCH'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
logger = get_task_logger(__name__)

config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE

conf_tup = read_ini_file(config_path_file)
udl2_conf = conf_tup[0]


def start_test(directory_path, memory, cpu, hist_db, hist_schema, port, user, passwd, host):
    '''
    kick off the tests by scheduling the task with celery
    '''
    run_pipeline.apply_async(({'directory': directory_path, 'memory': memory, 'cpu': cpu, 'hist_db': hist_db,
                               'hist_schema': hist_schema, 'port': port, 'user': user, 'passwd': passwd, 'host': host}, ))


@celery.task(name='benchmarking.run_benchmarking.run_pipeline')
def run_pipeline(msg):
    '''
    Run the pipeline for the current file and use this task as a callback for future tasks
    '''
    file_index = 0

    # if this is not the first run record the data from the previous run in the database
    # and increment the file index
    if msg.get('batch_guid'):
        record_benchmark_info(msg['batch_guid'], msg['hist_schema'], msg['user'], msg['passwd'],
                              msg['host'], msg['port'], msg['hist_db'], msg['memory'], msg['cpu'])
        file_index = msg['file_index'] + 1

    # Exit if all tests have completed
    if file_index >= len(FILES):
        logger.info('All Tests Complete')
        return

    logger.info('**Running Pipeline test %d**' % file_index)

    # Construct new message
    directory = msg['directory']
    new_msg = dict(list(msg.items()) + list({'file_index': file_index, 'callback': run_pipeline}.items()))

    # define csv and json file
    #csv_file = os.path.join(directory, CSV_FILES[file_index])
    #json_file = os.path.join(directory, JSON_FILES[file_index])
    files = os.path.join(directory, FILES[file_index])

    # run pipeline with the two files and the newly constructed message
    #start_pipeline(csv_file, json_file, udl2_conf, batch_guid_forced=None, **new_msg)
    get_pipeline_chain(files, udl2_conf, batch_guid_forced=None, **new_msg)


@celery.task(name="benchmarking.run_benchmarking.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


def record_benchmark_info(batch_guid, history_schema_name, hist_user, hist_pass, hist_host, hist_port, hist_db, memory, cpu):
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

    # Get relevant data from the udl_batch table
    batch_table = get_sqlalch_table_object(engine, udl2_conf['udl2_db']['db_schema'], Constants.UDL2_BATCH_TABLE)
    batch_table_res = get_data_from_batch_table(batch_guid, conn, batch_table)
    conn.close()

    # pull out total time and total count from results
    tot_time, tot_count = get_total_time_and_records_from_results(batch_table_res)

    # Connect to history table
    (hist_conn, hist_engine) = connect_db(udl2_conf['udl2_db']['db_driver'], hist_user, hist_pass, hist_host, hist_port, hist_db)

    # Get sqlalchemy table objects
    history_table = get_sqlalch_table_object(hist_engine, history_schema_name, HISTORY_TABLE)
    hist_batch_table = get_sqlalch_table_object(hist_engine, history_schema_name, BATCH_TABLE)

    # Population history tables
    copy_batch_results_to_history_schema(batch_table_res, batch_table, history_schema_name, hist_batch_table, hist_conn)
    add_data_to_history_table(hist_conn, history_table, cpu, memory, date.today(), tot_time, tot_count)


def get_data_from_batch_table(batch_guid, db_conn, batch_table):
    '''
    select all the records from the batch table with the given batch_guid
    '''
    batch_select = select([batch_table]).where(batch_table.c.guid_batch == batch_guid)
    return db_conn.execute(batch_select).fetchall()


def copy_batch_results_to_history_schema(results, batch_table, hist_schema, hist_batch_table, db_conn):
    '''
    copy the result from the udl batch table to the history udl_batch table
    '''
    res_list_of_dicts = convert_results_to_dict(results, batch_table)
    db_conn.execute(hist_batch_table.insert(), res_list_of_dicts)


def add_data_to_history_table(connect_db, hist_table, cpu_info, memory_info, last_UDL_run_date, UDL_completion_duration, file_size):
    '''
    take the relevant information and write the data to the history table
    '''
    connect_db.execute(hist_table.insert().values(cpu_info=cpu_info, memory_info=memory_info, last_UDL_run_date=last_UDL_run_date,
                                                  UDL_completion_duration=UDL_completion_duration, file_size=file_size))


def get_total_time_and_records_from_results(row_list):
    '''
    Given a list of result tuples from sqlalchemy query retrieve the total time of the run and
    retrieve the number of records.
    '''
    # search values
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
    return [{columns[i]: row[i] for i in range(len(columns)) if columns[i] != 'batch_sid'} for row in results]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run the benchmarking for several file sizes")
    parser.add_argument('-d', '--directory', default=None,
                        help='the location of directory containing the files to use for testing')
    parser.add_argument('-m', '--memory', required=True,
                        help='the amount of memory in the system as a string (ie. "16GB")')
    parser.add_argument('-c', '--cpu', required=True,
                        help='the number of cpus and/or type of cpus on the system (ie. 4 cores 1.9GHz)')
    parser.add_argument('--host', default='127.0.0.1',
                        help='the host where the db is located. default: 127.0.0.1')
    parser.add_argument('-b', '--history-database', default='',
                        help='the name of the database that the history schema is in')
    parser.add_argument('-s', '--history-schema', default='',
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
    host = args.host
    print('params', directory, memory, cpu, hist_db, hist_schema, port, user, passwd, host)
    start_test(directory, memory, cpu, hist_db, hist_schema, port, user, passwd, host)
