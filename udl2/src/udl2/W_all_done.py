'''
Created on Sep 10, 2013

@author: swimberly
'''
import datetime

from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from udl2 import message_keys as mk
from udl2.celery import celery
from udl2_util.measurement import BatchTableBenchmark
from udl2.udl2_base_task import Udl2BaseTask
from udl2.status import insert_udl_daily_stats
from udl2.constants import UdlStatsConstants


logger = get_task_logger(__name__)


def report_udl_batch_metrics_to_log(msg, end_time, pipeline_status):
    logger.info('UDL Batch Summary:')
    logger.info('Batch Guid: ' + msg[mk.GUID_BATCH])
    logger.info('Batch Status: ' + pipeline_status)
    logger.info('Start time: ' + str(msg[mk.START_TIMESTAMP]))
    logger.info('End time: ' + str(end_time))
    if mk.INPUT_FILE_SIZE in msg:
        logger.info('Input file size: ' + str(round(msg[mk.INPUT_FILE_SIZE] / (1024 * 1024.0), 3)) + 'MB')
    if mk.FACT_ROWS_LOADED in msg:
        logger.info('Total Records Processed: ' + str(msg[mk.FACT_ROWS_LOADED]))


def report_batch_to_udl_daily_stats(msg, end_time):
    logger.info('Reporting to UDL daily stats')
    #Fact rows are not updated for student registration yet
    fact_rows_loaded = 0
    if mk.FACT_ROWS_LOADED in msg:
        fact_rows_loaded = msg[mk.FACT_ROWS_LOADED]
    udl_batch_stats = {
        UdlStatsConstants.BATCH_GUID: msg[mk.GUID_BATCH],
        UdlStatsConstants.STATE_CODE: msg[mk.TENANT_NAME],
        UdlStatsConstants.FILE_ARRIVED: msg[mk.START_TIMESTAMP],
        UdlStatsConstants.TENANT: msg[mk.TENANT_NAME],
        UdlStatsConstants.RECORD_LOADED_COUNT: fact_rows_loaded,
        UdlStatsConstants.UDL_START: msg[mk.START_TIMESTAMP],
        UdlStatsConstants.UDL_END: end_time
    }
    insert_udl_daily_stats(udl_batch_stats)


@celery.task(name='udl2.W_all_done.task', base=Udl2BaseTask)
def task(msg):
    start_time = msg[mk.START_TIMESTAMP]
    end_time = datetime.datetime.now()
    load_type = msg[mk.LOAD_TYPE]
    guid_batch = msg[mk.GUID_BATCH]

    # infer overall pipeline_status based on previous pipeline_state
    pipeline_status = mk.FAILURE if mk.PIPELINE_STATE in msg and msg[mk.PIPELINE_STATE] == 'error' else mk.SUCCESS

    benchmark = BatchTableBenchmark(guid_batch, load_type, 'UDL_COMPLETE',
                                    start_time, end_time, udl_phase_step_status=pipeline_status)
    benchmark.record_benchmark()

    # record batch stats to udl daily stats table
    # this will be used by migration script to move the data from pre-prod to prod
    report_batch_to_udl_daily_stats(msg, end_time)

    # report the batch metrics in Human readable format to the UDL log
    report_udl_batch_metrics_to_log(msg, end_time, pipeline_status)
    return msg
