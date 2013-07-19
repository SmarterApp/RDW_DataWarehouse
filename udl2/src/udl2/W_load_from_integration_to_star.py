from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from udl2 import message_keys as mk
from move_to_target.move_to_target import explode_data_to_dim_table, explode_data_to_fact_table, get_table_column_types, calculate_spend_time_as_second
from celery import group
import datetime
from udl2_util.measurement import measure_cpu_plus_elasped_time
from move_to_target import create_queries as queries
from udl2_util.database_util import connect_db, execute_query_with_result
from collections import OrderedDict


logger = get_task_logger(__name__)


#*************implemented via group*************
@celery.task(name='udl2.W_load_from_integration_to_star.explode_to_dims')
@measure_cpu_plus_elasped_time
def explode_to_dims(msg):
    '''
    This is the celery task to move data from integration tables to dim tables.
    In the input batch object, guid_batch is provided.
    '''
    conf = generate_conf(msg[mk.GUID_BATCH], msg[mk.PHASE])
    table_map, column_map = get_table_and_column_mapping(conf, 'dim_')
    grouped_tasks = create_group_tuple(explode_data_to_dim_table_task,
                                       [(conf, source_table, dim_table, column_map[dim_table], get_table_column_types(conf, dim_table, list(column_map[dim_table].keys())))
                                        for dim_table, source_table in table_map.items()])
    result_uuid = group(*grouped_tasks)()
    msg['dim_tables'] = result_uuid.get()
    return msg


@measure_cpu_plus_elasped_time
def get_table_and_column_mapping(conf, table_name_prefix=None):
    '''
    The main function to get the table mapping and column mapping from reference table
    @param conf: configuration dictionary
    @param table_name_prefix: the prefix of the table name
    '''
    (conn_source, _engine) = connect_db(conf[mk.SOURCE_DB_DRIVER],
                                        conf[mk.SOURCE_DB_USER],
                                        conf[mk.SOURCE_DB_PASSWORD],
                                        conf[mk.SOURCE_DB_HOST],
                                        conf[mk.SOURCE_DB_PORT],
                                        conf[mk.SOURCE_DB_NAME])
    table_map = get_table_mapping(conn_source, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], table_name_prefix)
    column_map = get_column_mapping_from_int_to_star(conn_source, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], list(table_map.keys()))
    conn_source.close()
    return table_map, column_map


@measure_cpu_plus_elasped_time
def get_table_mapping(conn, schema_name, table_name, phase_number, table_name_prefix=None):
    table_mapping_query = queries.get_dim_table_mapping_query(schema_name, table_name, phase_number)
    table_mapping_result = execute_query_with_result(conn, table_mapping_query, 'Exception -- getting table mapping', 'W_load_from_integration_to_star', 'get_table_mapping')
    table_mapping_dict = {}
    if table_mapping_result:
        for mapping in table_mapping_result:
            if table_name_prefix:
                if mapping[0].startswith(table_name_prefix):
                    table_mapping_dict[mapping[0]] = mapping[1]
            else:
                table_mapping_dict[mapping[0]] = mapping[1]
    return table_mapping_dict


@measure_cpu_plus_elasped_time
def get_column_mapping_from_int_to_star(conn, schema_name, table_name, phase_number, dim_tables):
    column_map = {}
    for dim_table in dim_tables:
        # get column map for this dim_table
        column_mapping_query = queries.get_dim_column_mapping_query(schema_name, table_name, phase_number, dim_table)
        column_mapping_result = execute_query_with_result(conn, column_mapping_query, 'Exception -- getting column mapping', 'W_load_from_integration_to_star', 'get_column_mapping_from_int_to_star')
        column_mapping_list = []
        if column_mapping_result:
            for mapping in column_mapping_result:
                # mapping[0]: target_column, mapping[1]: source_column
                target_column = mapping[0]
                source_column = mapping[1]
                target_source_pair = (target_column, source_column)
                # this is the primary key, need to put the pair in front
                if source_column is not None and 'nextval' in source_column:
                    column_mapping_list.insert(0, target_source_pair)
                else:
                    column_mapping_list.append(target_source_pair)
        column_map[dim_table] = OrderedDict(column_mapping_list)
    return column_map


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
    _time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)
    # print('I am the exploder, moved data from %s into dim table %s in %.3f seconds' % (source_table, dim_table, _time_as_seconds))


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
    phase_number = msg[mk.PHASE]
    conf = generate_conf(guid_batch, phase_number)
    # get fact table column mapping
    fact_table_map, fact_column_map = get_table_and_column_mapping(conf, 'fact_')
    fact_table = list(fact_table_map.keys())[0]
    source_table_for_fact_table = list(fact_table_map.values())[0]
    fact_column_types = get_table_column_types(conf, fact_table, list(fact_column_map[fact_table].keys()))

    explode_data_to_fact_table(conf, source_table_for_fact_table, fact_table, fact_column_map[fact_table], fact_column_types)

    finish_time = datetime.datetime.now()
    _time_as_seconds = calculate_spend_time_as_second(start_time, finish_time)
    # print('I am the exploder, copied data from staging table into fact table in %.3f seconds' % _time_as_seconds)
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
def generate_conf(guid_batch, phase_number):
    '''
    Return all needed configuration information
    '''
    conf = {  # add guid_batch from msg
              mk.GUID_BATCH: guid_batch,

              # db driver
              mk.SOURCE_DB_DRIVER: udl2_conf['udl2_db']['db_driver'],

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
              mk.REF_TABLE: udl2_conf['udl2_db']['ref_table_name'],
              mk.PHASE: int(phase_number),
              mk.MOVE_TO_TARGET: udl2_conf['move_to_target']
    }
    return conf
