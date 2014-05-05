'''
Created on Sep 10, 2013

@author: swimberly
'''
import datetime
from celery.utils.log import get_task_logger
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.celery import celery
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edcore.database.utils.constants import UdlStatsConstants, LoadType
from edcore.database.utils.query import update_udl_stats
import json


logger = get_task_logger(__name__)


def report_udl_batch_metrics_to_log(msg, end_time, pipeline_status):
    logger.info('UDL Batch Summary:')
    logger.info('Batch Guid: ' + msg[mk.GUID_BATCH])
    logger.info('Batch Status: ' + pipeline_status)
    logger.info('Start time: ' + str(msg[mk.START_TIMESTAMP]))
    logger.info('End time: ' + str(end_time))
    if mk.INPUT_FILE_SIZE in msg:
        logger.info('Input file size: ' + str(round(msg[mk.INPUT_FILE_SIZE] / (1024 * 1024.0), 3)) + 'MB')
    if mk.TOTAL_ROWS_LOADED in msg:
        logger.info('Total Records Processed: ' + str(msg[mk.TOTAL_ROWS_LOADED]))


def _create_stats_row(msg, end_time, status):
    stats = {}
    stats[UdlStatsConstants.LOAD_END] = end_time
    stats[UdlStatsConstants.RECORD_LOADED_COUNT] = msg[mk.TOTAL_ROWS_LOADED] if mk.TOTAL_ROWS_LOADED in msg else 0

    if status is mk.SUCCESS:
        stats[UdlStatsConstants.LOAD_STATUS] = UdlStatsConstants.UDL_STATUS_INGESTED
        if msg[mk.LOAD_TYPE] == LoadType.STUDENT_REGISTRATION:
            stats[UdlStatsConstants.BATCH_OPERATION] = UdlStatsConstants.SNAPSHOT
            snapshot_criteria = {}
            snapshot_criteria['reg_system_id'] = msg[mk.REG_SYSTEM_ID]
            snapshot_criteria['academic_year'] = msg[mk.ACADEMIC_YEAR]
            stats[UdlStatsConstants.SNAPSHOT_CRITERIA] = json.dumps(snapshot_criteria)
    else:
        stats[UdlStatsConstants.LOAD_STATUS] = UdlStatsConstants.UDL_STATUS_FAILED

    return stats


def report_batch_to_udl_stats(msg, end_time, status):
    logger.info('Reporting to UDL daily stats')
    stats = _create_stats_row(msg, end_time, status)

    update_udl_stats(msg[mk.UDL_STATS_REC_ID], stats)


@celery.task(name='udl2.W_all_done.task', base=Udl2BaseTask)
def task(msg):
    start_time = msg[mk.START_TIMESTAMP]
    end_time = datetime.datetime.now()
    load_type = msg[mk.LOAD_TYPE]
    guid_batch = msg[mk.GUID_BATCH]

    # infer overall pipeline_status based on previous pipeline_state
    pipeline_status = mk.FAILURE if mk.PIPELINE_STATE in msg and msg[mk.PIPELINE_STATE] == 'error' else mk.SUCCESS

    benchmark = BatchTableBenchmark(guid_batch, load_type, 'UDL_COMPLETE',
                                    start_time, end_time, udl_phase_step_status=pipeline_status, tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()

    # record batch stats to udl stats table
    # this will be used by migration script to move the data from pre-prod to prod
    report_batch_to_udl_stats(msg, end_time, pipeline_status)
    # report the batch metrics in Human readable format to the UDL log
    report_udl_batch_metrics_to_log(msg, end_time, pipeline_status)
    return msg
