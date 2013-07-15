from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from udl2 import message_keys as mk
import move_to_target.column_mapping as col_map
from move_to_target.move_to_target import explode_data_to_dim_table, explode_data_to_fact_table, get_table_column_types, calculate_spend_time_as_second
from celery import group
import datetime
from udl2_util.measurement import measure_cpu_plus_elasped_time


logger = get_task_logger(__name__)


#*************implemented via group*************
@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_dims')
@measure_cpu_plus_elasped_time
def explode_to_dims(msg):
    '''
    This is the celery task to move data from integration tables to dim tables.
    In the input batch object, guid_batch is provided.
    '''
    conf = generate_conf(msg[mk.GUID_BATCH])
    column_map = col_map.get_column_mapping()
    grouped_tasks = create_group_tuple(explode_data_to_dim_table_task,
                                       [(conf, source_table, dim_table, column_map[dim_table], get_table_column_types(conf, dim_table, list(column_map[dim_table].keys())))
                                        for dim_table, source_table in col_map.get_target_tables_parallel().items()])
    result_uuid = group(*grouped_tasks)()
    msg['dim_tables'] = result_uuid.get()
    return msg


@celery.task(name="udl2.W_load_from_integration_to_star.explode_data_to_dim_table_task")
@measure_cpu_plus_elasped_time
def explode_data_to_dim_table_task(conf, source_table, dim_table, column_mapping, column_types):
    '''
    This is the celery task to move data from one integration table to one dim table.
    '''
    logger.info('LOAD_FROM_INT_TO_STAR: migrating source table <%s> to <%s>' % (source_table, dim_table))
    start_time = datetime.datetime.now()
    explode_data_to_dim_table(conf, source_table, dim_table, column_mapping, column_types)
    finish_time = datetime.datetime.now()
    time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)
    # print('I am the exploder, moved data from %s into dim table %s in %.3f seconds' % (source_table, dim_table, time_as_seconds))


@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_fact')
@measure_cpu_plus_elasped_time
def explode_to_fact(msg):
    '''
    This is the celery task to move data from integration table to fact table.
    In batch, guid_batch is provided.
    '''
    logger.info('LOAD_FROM_INT_TO_STAR: Migrating fact_assessment_outcome from Integration to Star.')
    start_time = datetime.datetime.now()
    guid_batch = msg[mk.GUID_BATCH]
    conf = generate_conf(guid_batch)
    # get column mapping
    column_map = col_map.get_column_mapping()
    fact_table = col_map.get_target_table_callback()[0]
    source_table_for_fact_table = col_map.get_target_table_callback()[1]
    column_types = get_table_column_types(conf, fact_table, list(column_map[fact_table].keys()))

    explode_data_to_fact_table(conf, source_table_for_fact_table, fact_table, column_map[fact_table], column_types)

    finish_time = datetime.datetime.now()
    time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)
    # print('I am the exploder, copied data from staging table into fact table in %.3f seconds' % time_as_seconds)
    return guid_batch


@celery.task(name="udl2.W_load_from_integration_to_star.error_handler")
@measure_cpu_plus_elasped_time
def error_handler(uuid):
    '''
    This is the error handler task
    '''
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


@measure_cpu_plus_elasped_time
def create_group_tuple(task_name, arg_list):
    '''
    Create task call as a tuple
    Example: task_name = add, arg_list = [(2,2), (2,4)]
             returns: (add.s(2,4), add.s(2,4))
    '''
    grouped_tasks = [task_name.s(*arg) for arg in arg_list]
    return tuple(grouped_tasks)


@measure_cpu_plus_elasped_time
def generate_conf(guid_batch):
    '''
    Return all needed configuration information
    '''
    conf = {
             # add guid_batch from msg
            mk.GUID_BATCH: guid_batch,

            # source schema
            mk.SOURCE_DB_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
            # source database setting
            mk.SOURCE_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],

            # target schema
            mk.TARGET_DB_SCHEMA: udl2_conf['target_db']['db_schema'],
            # target database setting
            mk.TARGET_DB_HOST: udl2_conf['target_db']['db_host'],
            mk.TARGET_DB_PORT: udl2_conf['target_db']['db_port'],
            mk.TARGET_DB_USER: udl2_conf['target_db']['db_user'],
            mk.TARGET_DB_NAME: udl2_conf['target_db']['db_database'],
            mk.TARGET_DB_PASSWORD: udl2_conf['target_db']['db_pass'],
    }
    return conf
