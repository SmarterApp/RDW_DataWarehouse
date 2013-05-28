from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import move_to_target.column_mapping as col_map
from move_to_target.move_to_target import explode_data_to_dim_table, explode_data_to_fact_table, get_table_column_types, calculate_spend_time_as_second
from celery import group
import datetime


logger = get_task_logger(__name__)


#*************implemented via group*************
@celery.task(name='udl2.W_move_to_target.explode_to_dims')
def explode_to_dims(batch):
    '''
    This is the celery task to move data from integration tables to dim tables.
    In the input batch object, batch_id is provided.
    '''
    conf = generate_conf(batch)
    column_map = col_map.get_column_mapping()
    grouped_tasks = create_group_tuple(explode_data_to_dim_table_task,
                                       [(conf, source_table, dim_table, column_map[dim_table], get_table_column_types(conf, dim_table, list(column_map[dim_table].keys())))
                                        for dim_table, source_table in col_map.get_target_tables_parallel().items()])
    result_uuid = group(*grouped_tasks)()
    batch['dim_tables'] = result_uuid.get()
    return batch


@celery.task(name="udl2.W_move_to_target.explode_to_signle_dim")
def explode_data_to_dim_table_task(conf, source_table, dim_table, column_mapping, column_types):
    '''
    This is the celery task to move data from one integration table to one dim table.
    '''
    print('I am the exploder, about to copy data from %s into dim table %s ' % (source_table, dim_table))
    start_time = datetime.datetime.now()
    explode_data_to_dim_table(conf, source_table, dim_table, column_mapping, column_types)
    finish_time = datetime.datetime.now()
    time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)
    print('I am the exploder, moved data from %s into dim table %s in %.3f seconds' % (source_table, dim_table, time_as_seconds))


@celery.task(name='udl2.W_move_to_target.explode_to_fact')
def explode_to_fact(batch):
    '''
    This is the celery task to move data from integration table to fact table.
    In batch, batch_id is provided.
    '''
    print('I am the exploder, about to copy fact table')
    start_time = datetime.datetime.now()

    conf = generate_conf(batch)
    # get column mapping
    column_map = col_map.get_column_mapping()
    fact_table = col_map.get_target_table_callback()[0]
    source_table_for_fact_table = col_map.get_target_table_callback()[1]
    column_types = get_table_column_types(conf, fact_table, list(column_map[fact_table].keys()))

    explode_data_to_fact_table(conf, source_table_for_fact_table, fact_table, column_map[fact_table], column_types)

    finish_time = datetime.datetime.now()
    time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)
    print('I am the exploder, copied data from staging table into fact table in %.3f seconds' % time_as_seconds)
    return batch


@celery.task(name="udl2.W_move_to_target.error_handler")
def error_handler(uuid):
    '''
    This is the error handler task
    '''
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


def create_group_tuple(task_name, arg_list):
    '''
    Create task call as a tuple
    Example: task_name = add, arg_list = [(2,2), (2,4)]
             returns: (add.s(2,4), add.s(2,4))
    '''
    grouped_tasks = [task_name.s(*arg) for arg in arg_list]
    return tuple(grouped_tasks)


def generate_conf(msg):
    '''
    Return all needed configuration information
    '''
    conf = {
             # add batch_id from msg
            'batch_id': msg['batch_id'],

            # source schema
            'source_schema': udl2_conf['udl2_db']['integration_schema'],
            # source database setting
            'db_host': udl2_conf['postgresql']['db_host'],
            'db_port': udl2_conf['postgresql']['db_port'],
            'db_user': udl2_conf['postgresql']['db_user'],
            'db_name': udl2_conf['postgresql']['db_database'],
            'db_password': udl2_conf['postgresql']['db_pass'],

            # target schema
            'target_schema': udl2_conf['target_db']['db_schema'],
            # target database setting
            'db_host_target': udl2_conf['target_db']['db_host'],
            'db_port_target': udl2_conf['target_db']['db_port'],
            'db_user_target': udl2_conf['target_db']['db_user'],
            'db_name_target': udl2_conf['target_db']['db_database'],
            'db_password_target': udl2_conf['target_db']['db_pass'],
    }
    return conf
