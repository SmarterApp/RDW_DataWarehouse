from __future__ import absolute_import
import datetime

from udl2.celery import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from udl2 import message_keys as mk
from move_to_target.move_to_target import (explode_data_to_dim_table, explode_data_to_fact_table,
                                           get_table_column_types, calculate_spend_time_as_second)
from celery import group
from udl2_util.measurement import BatchTableBenchmark
from move_to_target.move_to_target_setup import get_table_and_column_mapping, generate_conf, create_group_tuple
from udl2.udl2_base_task import Udl2BaseTask

logger = get_task_logger(__name__)


#*************implemented via group*************
@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_dims', base=Udl2BaseTask)
def explode_to_dims(msg):
    '''
    This is the celery task to move data from integration tables to dim tables.
    In the input batch object, guid_batch is provided.
    '''
    start_time = datetime.datetime.now()
    conf = generate_conf(msg[mk.GUID_BATCH], msg[mk.PHASE], msg[mk.LOAD_TYPE], msg[mk.TENANT_NAME])
    table_map, column_map = get_table_and_column_mapping(conf, 'dim_')
    grouped_tasks = create_group_tuple(explode_data_to_dim_table_task,
                                       [(conf, source_table, dim_table, column_map[dim_table], get_table_column_types(conf, dim_table, list(column_map[dim_table].keys())))
                                        for dim_table, source_table in table_map.items()])
    result_uuid = group(*grouped_tasks)()
    msg['dim_tables'] = result_uuid.get()

    total_affected_rows = 0
    for dim_table_result in msg['dim_tables']:
        total_affected_rows += dim_table_result[mk.SIZE_RECORDS]

    end_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(msg[mk.GUID_BATCH], msg[mk.LOAD_TYPE], explode_to_dims.name, start_time, end_time,
                                    size_records=total_affected_rows, task_id=str(explode_to_dims.request.id), working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()
    return msg


@celery.task(name="udl2.W_load_from_integration_to_star.explode_data_to_dim_table_task", base=Udl2BaseTask)
def explode_data_to_dim_table_task(conf, source_table, dim_table, column_mapping, column_types):
    """
    This is the celery task to move data from one integration table to one dim table.
    :param conf:
    :param source_table:
    :param dim_table:
    :param column_mapping:
    :param column_types:
    :return:
    """
    logger.info('LOAD_FROM_INT_TO_STAR: migrating source table <%s> to <%s>' % (source_table, dim_table))
    start_time = datetime.datetime.now()
    affected_rows = explode_data_to_dim_table(conf, source_table, dim_table, column_mapping, column_types)
    finish_time = datetime.datetime.now()
    _time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)

    # Create benchmark object ant record benchmark
    udl_phase_step = 'INT --> DIM:' + dim_table
    benchmark = BatchTableBenchmark(conf[mk.GUID_BATCH], conf[mk.LOAD_TYPE], explode_data_to_dim_table_task.name, start_time, finish_time,
                                    udl_phase_step=udl_phase_step, size_records=affected_rows[0], task_id=str(explode_data_to_dim_table_task.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], udl_leaf=True)
    benchmark.record_benchmark()
    return benchmark.get_result_dict()


@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_fact', base=Udl2BaseTask)
def explode_to_fact(msg):
    '''
    This is the celery task to move data from integration table to fact table.
    In batch, guid_batch is provided.
    '''
    logger.info('LOAD_FROM_INT_TO_STAR: Migrating fact_assessment_outcome from Integration to Star.')
    start_time = datetime.datetime.now()
    guid_batch = msg[mk.GUID_BATCH]
    phase_number = msg[mk.PHASE]
    load_type = msg[mk.LOAD_TYPE]
    tenant_name = msg[mk.TENANT_NAME]
    conf = generate_conf(guid_batch, phase_number, load_type, tenant_name)
    # get fact table column mapping
    fact_table_map, fact_column_map = get_table_and_column_mapping(conf, 'fact_')
    fact_table = list(fact_table_map.keys())[0]
    source_table_for_fact_table = list(fact_table_map.values())[0]
    fact_column_types = get_table_column_types(conf, fact_table, list(fact_column_map[fact_table].keys()))

    affected_rows = explode_data_to_fact_table(conf, source_table_for_fact_table, fact_table, fact_column_map[fact_table], fact_column_types)

    finish_time = datetime.datetime.now()
    _time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)

    # Create benchmark object ant record benchmark
    udl_phase_step = 'INT --> FACT TABLE'
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], explode_to_fact.name, start_time, finish_time,
                                    udl_phase_step=udl_phase_step, size_records=affected_rows, task_id=str(explode_to_fact.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({mk.FACT_ROWS_LOADED: affected_rows})
    return outgoing_msg

