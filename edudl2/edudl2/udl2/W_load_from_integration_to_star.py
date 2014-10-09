from __future__ import absolute_import
import datetime

from edudl2.udl2.celery import celery
from celery.utils.log import get_task_logger
from edudl2.udl2 import message_keys as mk
from celery import group
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.move_to_target.move_to_target_setup import get_table_and_column_mapping, generate_conf,\
    get_table_column_types
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.move_to_target.move_to_target import explode_data_to_dim_table, calculate_spend_time_as_second,\
    explode_data_to_fact_table, handle_duplicates_in_dimensions, create_target_schema_for_batch, handle_updates_and_deletes
from celery.canvas import chord
from edudl2.udl2.W_tasks_utils import handle_group_results
from edudl2.udl2.constants import Constants
logger = get_task_logger(__name__)


@celery.task(name='udl2.W_load_from_integration_to_star.prepare_target_schema', base=Udl2BaseTask)
def prepare_target_schema(msg):
    """
    Task to create target star schema
    """
    start_time = datetime.datetime.now()
    conf = _get_conf(msg)
    tenant = conf[mk.TENANT_NAME]
    schema = conf[mk.TARGET_DB_SCHEMA]

    create_target_schema_for_batch(tenant, schema)

    end_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(msg[mk.GUID_BATCH], msg[mk.LOAD_TYPE], prepare_target_schema.name, start_time, end_time,
                                    task_id=str(prepare_target_schema.request.id), working_schema=schema, tenant=tenant)
    benchmark.record_benchmark()
    return msg


def get_explode_to_tables_tasks(msg, prefix):
    '''
    Returns a chord of tasks to migrate to pre-prod tables
    '''
    task_map = {'dim': explode_data_to_dim_table_task,
                'fact_asmt': explode_data_to_fact_table_task,
                'fact_block': explode_data_to_fact_table_task}
    task_name = task_map.get(prefix)
    conf = _get_conf(msg)
    table_map, column_map = get_table_and_column_mapping(conf, 'explode to ' + prefix, prefix + '_')
    grouped_tasks = []
    for table, source_table in table_map.items():
        grouped_tasks.append(task_name.subtask(args=[conf, source_table, table, column_map[table], get_table_column_types(conf, table, list(column_map[table].keys()))]))
    # TODO: This breaks local dev debugging for some reason
    #return chord(group(grouped_tasks), handle_group_results.s())
    return group(grouped_tasks)


@celery.task(name="udl2.W_load_from_integration_to_star.explode_data_to_dim_table_task", base=Udl2BaseTask)
def explode_data_to_dim_table_task(msg, conf, source_table, dim_table, column_mapping, column_types):
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
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], udl_leaf=True, tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()
    return msg


@celery.task(name="udl2.W_load_from_integration_to_star.explode_data_to_fact_table_task", base=Udl2BaseTask)
def explode_data_to_fact_table_task(msg, conf, source_table, fact_table, column_mapping, column_types):
    """
    This is the celery task to move data from one integration table to one fact table.
    :param conf:
    :param source_table:
    :param fact_table:
    :param column_mapping:
    :param column_types:
    :return:
    """
    logger.info('LOAD_FROM_INT_TO_STAR: migrating source table <%s> to <%s>' % (source_table, fact_table))
    start_time = datetime.datetime.now()
    affected_rows = explode_data_to_fact_table(conf, source_table, fact_table, column_mapping, column_types)
    finish_time = datetime.datetime.now()

    benchmark = BatchTableBenchmark(conf[mk.GUID_BATCH], conf[mk.LOAD_TYPE], explode_data_to_fact_table_task.name,
                                    start_time, finish_time, udl_phase_step='INT --> FACT:' + fact_table, size_records=affected_rows,
                                    task_id=str(explode_data_to_fact_table_task.request.id), tenant=msg[mk.TENANT_NAME],
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], udl_leaf=True)
    benchmark.record_benchmark()
    return msg


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
    # pass down the affected row from previous stage
    udl_phase_step = 'HANDLE DELETION IN FACT'
    conf = _get_conf(msg)
    conf[mk.UDL_PHASE_STEP] = udl_phase_step

    # handle updates and deletes
    handle_updates_and_deletes(conf)
    finish_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], handle_deletions.name, start_time, finish_time,
                                    udl_phase_step=udl_phase_step, tenant=msg[mk.TENANT_NAME],
                                    task_id=str(handle_deletions.request.id), working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(msg)
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
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()

    return msg


def _get_conf(msg):
    guid_batch = msg[mk.GUID_BATCH]
    phase_number = Constants.INT_TO_STAR_PHASE
    load_type = msg[mk.LOAD_TYPE]
    tenant_name = msg[mk.TENANT_NAME]
    target_schema = msg[mk.GUID_BATCH]
    conf = generate_conf(guid_batch, phase_number, load_type, tenant_name, target_schema)
    return conf
