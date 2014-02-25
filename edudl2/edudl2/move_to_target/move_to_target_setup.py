__author__ = 'swimberly'

from collections import OrderedDict

from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.move_to_target import create_queries as queries
from edudl2.udl2_util.database_util import execute_udl_query_with_result
from edudl2. udl2.udl2_connector import UDL2DBConnection
from edudl2.move_to_target.move_to_target_conf import get_move_to_target_conf


def get_table_and_column_mapping(conf, task_name, table_name_prefix=None):
    '''
    The main function to get the table mapping and column mapping from reference table
    @param conf: configuration dictionary
    @param table_name_prefix: the prefix of the table name
    '''

    with UDL2DBConnection() as conn_source:
        table_map = get_table_mapping(conn_source, task_name, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], table_name_prefix)
        column_map = get_column_mapping_from_int_to_star(conn_source, task_name, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], list(table_map.keys()))

    return table_map, column_map


def get_table_mapping(conn, task_name, schema_name, table_name, phase_number, table_name_prefix=None):
    table_mapping_query = queries.get_dim_table_mapping_query(schema_name, table_name, phase_number)
    table_mapping_result = execute_udl_query_with_result(conn, table_mapping_query, 'Exception -- getting table mapping', task_name, 'get_table_mapping')
    table_mapping_dict = {}
    if table_mapping_result:
        for mapping in table_mapping_result:
            # mapping[0]: target_table, mapping[1]: source_table
            if table_name_prefix:
                if mapping[0].startswith(table_name_prefix):
                    table_mapping_dict[mapping[0]] = mapping[1]
            else:
                table_mapping_dict[mapping[0]] = mapping[1]
    return table_mapping_dict


def get_column_mapping_from_int_to_star(conn, task_name, schema_name, table_name, phase_number, dim_tables):
    column_map = {}
    for dim_table in dim_tables:
        column_map[dim_table] = get_column_mapping_from_int_to_target(conn, task_name, schema_name, table_name, phase_number, dim_table)
    return column_map


def get_column_mapping_from_int_to_target(conn, task_name, schema_name, reference_table, phase_number, target_table, source_table=None):
    # Get column map for this target table.
    column_mapping_query = queries.get_column_mapping_query(schema_name, reference_table, phase_number, target_table, source_table)
    column_mapping_result = execute_udl_query_with_result(conn, column_mapping_query, 'Exception -- getting column mapping',
                                                          task_name, 'get_column_mapping_from_int_to_target')
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

    return OrderedDict(column_mapping_list)


def create_group_tuple(task_name, arg_list):
    '''
    Create task call as a tuple
    Example: task_name = add, arg_list = [(2,2), (2,4)]
             returns: (add.s(2,4), add.s(2,4))
    '''
    grouped_tasks = [task_name.s(*arg) for arg in arg_list]
    return tuple(grouped_tasks)


def generate_conf(guid_batch, phase_number, load_type, tenant_code):
    """
    Return all needed configuration information
    :param guid_batch: the guid for the batch
    :param phase_number: the current number of the phase
    :param load_type: type of load. ie. assessment
    :param tenant_code: the tenants 2 letter code
    :return: A dictionary of the config details
    """
    tenant_target_db_info = get_tenant_target_db_information(tenant_code)
    tenant_prod_db_info = get_tenant_prod_db_information(tenant_code)

    conf = {
        # add guid_batch from msg
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
        mk.SOURCE_DB_TABLE: udl2_conf['udl2_db']['json_integration_tables'][load_type],

        mk.REF_TABLE: udl2_conf['udl2_db']['ref_tables'][load_type],
        mk.PHASE: int(phase_number),
        mk.MOVE_TO_TARGET: get_move_to_target_conf(),
        mk.LOAD_TYPE: load_type,
        mk.TENANT_NAME: tenant_code if udl2_conf['multi_tenant']['active'] else udl2_conf['multi_tenant']['default_tenant'],
    }

    conf.update(tenant_target_db_info)
    conf.update(tenant_prod_db_info)

    return conf


def get_tenant_target_db_information(tenant_code):
    """
    If multi-tenancy is on look in the Master metadata table to pull out
    information about this tenant, otherwise get the target db info from udl2_conf
    :param tenant_code: The code (2 char name) for the give tenant
    :return: A dictionary containing the relevant connection information
    """
    tenant_code = tenant_code if udl2_conf['multi_tenant']['active'] else udl2_conf['multi_tenant']['default_tenant']

    return {
        mk.TARGET_DB_NAME: udl2_conf['target_db_conn'][tenant_code]['db_database'],
        mk.TARGET_DB_USER: udl2_conf['target_db_conn'][tenant_code]['db_user'],
        mk.TARGET_DB_SCHEMA: udl2_conf['target_db_conn'][tenant_code]['db_schema'],
        mk.TARGET_DB_PASSWORD: udl2_conf['target_db_conn'][tenant_code]['db_pass'],
    }


def get_tenant_prod_db_information(tenant_code):
    """
    If multi-tenancy is on look in the Master metadata table to pull out
    information about this tenant, otherwise get the target db info from udl2_conf
    :param tenant_code: The code (2 char name) for the give tenant
    :return: A dictionary containing the relevant connection information
    """
    tenant_code = tenant_code if udl2_conf['multi_tenant']['active'] else udl2_conf['multi_tenant']['default_tenant']

    return {
        mk.PROD_DB_NAME: udl2_conf['prod_db_conn'][tenant_code]['db_database'],
        mk.PROD_DB_USER: udl2_conf['prod_db_conn'][tenant_code]['db_user'],
        mk.PROD_DB_SCHEMA: udl2_conf['prod_db_conn'][tenant_code]['db_schema'],
        mk.PROD_DB_PASSWORD: udl2_conf['prod_db_conn'][tenant_code]['db_pass'],
    }
