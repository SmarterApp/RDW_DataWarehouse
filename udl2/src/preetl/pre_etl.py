from uuid import uuid4
import preetl.create_queries as queries
from udl2_util.database_util import connect_db, execute_queries
import logging
from celery.utils.log import get_task_logger
import datetime


def pre_etl_job(udl2_conf, load_type='Assessment'):
    '''
    PRE ETL function: create a new guid_batch and insert one row into batch table
    @param udl2_conf: udl2 config, which is got from udl.udl2_conf
    @param load_type: load type of the current job. The default value is 'Assessment'
    '''
    logger = get_logger(udl2_conf, for_error=True)
    try:
        # generate guid_batch
        guid_batch = str(uuid4())

        # prepare content to be inserted into batch table
        parm = {'guid_batch': guid_batch,
                'load_type': load_type,
                'working_schema': udl2_conf['udl2_db']['staging_schema'],
                'udl_phase': 'PRE ETL',
                'udl_leaf': str(False),
                }

        schema = parm['working_schema']
        batch_table = udl2_conf['udl2_db']['batch_table_name']

        # create the insertion query
        insert_query = queries.insert_batch_row_query(schema, batch_table, **parm)

        # create database connection
        (conn, _engine) = connect_db(udl2_conf['udl2_db']['db_driver'],
                                     udl2_conf['udl2_db']['db_user'],
                                     udl2_conf['udl2_db']['db_pass'],
                                     udl2_conf['udl2_db']['db_host'],
                                     udl2_conf['udl2_db']['db_port'],
                                     udl2_conf['udl2_db']['db_database'])
        # insert into batch table
        execute_queries(conn, [insert_query], 'Exception in pre_etl, execute query to insert into batch table', 'pre_etl', 'pre_etl_job')
        conn.close()

        return guid_batch

    except Exception as e:
        logger.error(str(e))


def get_logger(udl2_conf, for_error=False):
    '''
    Get/create a logger object. The created logger object will record log message into log file
    @param udl2_conf: udl2 config, which is got from udl.udl2_conf. It has the log file path
    @param for_error: if it is true, log file will be the 'error' log file, otherwise, the log file is the 'audit' log file
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(udl2_conf['logging']['level'])
    log_file_key = 'error' if for_error is True else 'audit'
    fh = logging.FileHandler(udl2_conf['logging'][log_file_key])
    # set the log format same as the as one in celery logger
    fh.setFormatter(logging.Formatter("[%(asctime)s: %(levelname)s/PreEtl] %(message)s"))
    logger.addHandler(fh)
    return logger
