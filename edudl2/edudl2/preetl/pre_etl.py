import logging
import datetime
from uuid import uuid4
from edudl2.udl2 import message_keys as mk
from edudl2.exceptions.errorcodes import ErrorCode
from edudl2.udl2_util.measurement import BatchTableBenchmark

logger = logging.getLogger('pre_etl')


def pre_etl_job(udl2_conf, load_type='Unknown', batch_guid_forced=None):
    '''
    PRE ETL function: create a new guid_batch and insert into batch table
    @param udl2_conf: udl2 config, which is got from udl.udl2_conf
    @param log_file: name of the log_file, by default is None, and it will be set to the value in config file
    @param load_type: load type of the current job. The default value is 'Unknown'
    @param batch_guid_forced: forced batch_guid to be used for this UDL process. If not provided batch_guid will be generated
    '''
    try:
        start_time = datetime.datetime.now()
        # generate a guid_batch for the current UDL batch if batch_guid is not forced
        guid_batch = str(uuid4()) if batch_guid_forced is None else batch_guid_forced

        # record the pre_etl step to udl batch table
        benchmark = BatchTableBenchmark(guid_batch=guid_batch, load_type=load_type,
                                        udl_phase='PRE ETL', start_timestamp=start_time,
                                        working_schema=udl2_conf['udl2_db']['db_schema'],
                                        udl_leaf=str(False), udl_phase_step_status=mk.SUCCESS)
        benchmark.record_benchmark()
        return guid_batch
    except Exception as e:
        logger.error(ErrorCode.BATCH_REC_FAILED + ': ' + str(e))
        return None
