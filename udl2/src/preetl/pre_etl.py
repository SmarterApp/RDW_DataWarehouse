from uuid import uuid4
from preetl import create_queries as queries
from udl2_util.database_util import connect_db, execute_queries
import logging
from udl2.errorcodes import BATCH_REC_FAILED
from udl2 import message_keys as mk


def pre_etl_job(udl2_conf, log_file=None, load_type='Unknown', batch_guid_forced=None):
    '''
    PRE ETL function: create a new guid_batch and insert one row into batch table
    @param udl2_conf: udl2 config, which is got from udl.udl2_conf
    @param log_file: name of the log_file, by default is None, and it will be set to the value in config file
    @param load_type: load type of the current job. The default value is 'Unknown'
    '''
    logger = get_logger(udl2_conf, udl2_conf['logging']['error'] if log_file is None else log_file)

    try:
        # generate a guid_batch
        guid_batch = str(uuid4()) if batch_guid_forced is None else batch_guid_forced

        # prepare content to be inserted into batch table
        parm = {mk.GUID_BATCH: guid_batch,
                mk.LOAD_TYPE: load_type,
                mk.WORKING_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
                mk.UDL_PHASE: 'PRE ETL',
                mk.UDL_LEAF: str(False),
                mk.UDL_PHASE_STEP_STATUS: mk.SUCCESS
                }

        schema = parm[mk.WORKING_SCHEMA]
        batch_table = udl2_conf['udl2_db']['batch_table']

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
        logger.error(BATCH_REC_FAILED + ': ' + str(e))
        return None


def get_logger(udl2_conf, log_file):
    '''
    Get/create a logger object. The created logger object will record log message into the log file
    @param udl2_conf: udl2 config, which is got from udl.udl2_conf. It has the log file path
    @param log_file: name of the log_file
    '''
    logger = logging.getLogger(__name__)
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter('[%(asctime)s: %(levelname)s/%(module)s] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
