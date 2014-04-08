from __future__ import absolute_import
import datetime

from edudl2.udl2.celery import celery
from celery.utils.log import get_task_logger
from edudl2.udl2 import message_keys as mk
from celery import group
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.move_to_target.move_to_target_setup import get_table_and_column_mapping, generate_conf,\
    create_group_tuple, get_table_column_types, get_move_to_target_conf
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.move_to_target.move_to_target import explode_data_to_dim_table, calculate_spend_time_as_second,\
    explode_data_to_fact_table, match_deleted_records, update_deleted_record_rec_id, check_mismatched_deletions,\
    handle_duplicates_in_dimensions, create_target_schema_for_batch

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_load_from_integration_to_star.create_target_schema', base=Udl2BaseTask)
def create_target_schema(msg):
    """
    Task to create target star schema
    """
    start_time = datetime.datetime.now()
    conf = _get_conf(msg)
    create_target_schema_for_batch(conf)
    end_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(msg[mk.GUID_BATCH], msg[mk.LOAD_TYPE], create_target_schema.name, start_time, end_time,
                                    task_id=str(create_target_schema.request.id), working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()
    return msg


#*************implemented via group*************
@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_dims', base=Udl2BaseTask)
def explode_to_dims(msg):
    '''
    This is the celery task to move data from integration tables to dim tables.
    In the input batch object, guid_batch is provided.
    '''
    start_time = datetime.datetime.now()
    conf = _get_conf(msg)
    table_map, column_map = get_table_and_column_mapping(conf, explode_to_dims.name, 'dim_')
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


@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_facts', base=Udl2BaseTask)
def explode_to_facts(msg):
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

    conf = _get_conf(msg)
    # get fact table column mapping
    fact_table_map, fact_column_map = get_table_and_column_mapping(conf, explode_to_facts.name, 'fact_')

    affected_rows = 0
    for fact_table, source_table_for_fact_table in fact_table_map.items():
        fact_column_types = get_table_column_types(conf, fact_table, list(fact_column_map[fact_table].keys()))

        affected_rows += explode_data_to_fact_table(conf, source_table_for_fact_table, fact_table,
                                                    fact_column_map[fact_table], fact_column_types)

    finish_time = datetime.datetime.now()
    _time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)

    # Create benchmark object ant record benchmark
    udl_phase_step = 'INT --> FACT TABLE'
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], explode_to_facts.name, start_time, finish_time,
                                    udl_phase_step=udl_phase_step, size_records=affected_rows, task_id=str(explode_to_facts.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({mk.TOTAL_ROWS_LOADED: affected_rows})
    return outgoing_msg


@celery.task(name='udl2.W_load_from_integration_to_star.handle_deletions', base=Udl2BaseTask)
def handle_deletions(msg):
    '''
    This is the celery task to match production database to find out deleted records in a batch
    exists.
    In batch, guid_batch is provided.
    '''
    logger.info('LOAD_FROM_INT_TO_STAR: Handle deletions in target tables.')
    start_time = datetime.datetime.now()
    guid_batch = msg[mk.GUID_BATCH]
    phase_number = msg[mk.PHASE]
    load_type = msg[mk.LOAD_TYPE]
    tenant_name = msg[mk.TENANT_NAME]
    # pass down the affected row from previous stage
    affected_rows = msg[mk.TOTAL_ROWS_LOADED]
    udl_phase_step = 'HANDLE DELETION IN FACT'

    conf = _get_conf(msg)
    conf[mk.UDL_PHASE_STEP] = udl_phase_step
    conf[mk.WORKING_SCHEMA] = msg['dim_tables'][0][mk.WORKING_SCHEMA]
    match_conf = get_move_to_target_conf()['handle_deletions']
    matched_results = match_deleted_records(conf, match_conf)
    update_deleted_record_rec_id(conf, match_conf, matched_results)
    check_mismatched_deletions(conf, match_conf)

    finish_time = datetime.datetime.now()
    _time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], handle_deletions.name, start_time, finish_time,
                                    udl_phase_step=udl_phase_step, size_records=affected_rows,
                                    task_id=str(handle_deletions.request.id), working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({mk.TOTAL_ROWS_LOADED: affected_rows})
    return outgoing_msg


@celery.task(name='udl2.W_load_from_integration_to_star.handle_record_upsert', base=Udl2BaseTask)
def handle_record_upsert(msg):
    '''
    Match records in current batch with production database, such that
    existing records only get updated to avoid duplication.
    '''
    logger.info('LOAD_FROM_INT_TO_STAR: detect duplications in target tables.')
    start_time = datetime.datetime.now()
    conf = _get_conf(msg)
    affected_rows = handle_duplicates_in_dimensions(conf[mk.TENANT_NAME], conf[mk.GUID_BATCH])
    finish_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    udl_phase_step = 'Delete duplicate record in dim tables'
    benchmark = BatchTableBenchmark(msg[mk.GUID_BATCH], msg[mk.LOAD_TYPE], handle_record_upsert.name, start_time, finish_time,
                                    udl_phase_step=udl_phase_step, size_records=affected_rows, task_id=str(handle_record_upsert.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()

    return msg


def _get_conf(msg):
    guid_batch = msg[mk.GUID_BATCH]
    phase_number = msg[mk.PHASE]
    load_type = msg[mk.LOAD_TYPE]
    tenant_name = msg[mk.TENANT_NAME]
    # if target schema name is specifically injected use that else use batch_guid as the schema name always
    target_schema = msg[mk.TARGET_DB_SCHEMA] if mk.TARGET_DB_SCHEMA in msg else msg[mk.GUID_BATCH]
    conf = generate_conf(guid_batch, phase_number, load_type, tenant_name, target_schema)
    return conf
