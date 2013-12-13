__author__ = 'swimberly'

from collections import OrderedDict
from sqlalchemy.sql import select

from udl2.celery import udl2_conf
from udl2 import message_keys as mk
from move_to_target import create_queries as queries
from udl2_util.database_util import connect_db, execute_udl_query_with_result, get_sqlalch_table_object
from udl2.udl2_connector import UDL2DBConnection


def get_table_and_column_mapping(conf, table_name_prefix=None):
    '''
    The main function to get the table mapping and column mapping from reference table
    @param conf: configuration dictionary
    @param table_name_prefix: the prefix of the table name
    '''

    with UDL2DBConnection() as conn_source:
        table_map = get_table_mapping(conn_source, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], table_name_prefix)
        column_map = get_column_mapping_from_int_to_star(conn_source, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], list(table_map.keys()))

    return table_map, column_map


def get_table_mapping(conn, schema_name, table_name, phase_number, table_name_prefix=None):
    table_mapping_query = queries.get_dim_table_mapping_query(schema_name, table_name, phase_number)
    table_mapping_result = execute_udl_query_with_result(conn, table_mapping_query, 'Exception -- getting table mapping', 'W_load_from_integration_to_star', 'get_table_mapping')
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


def get_column_mapping_from_int_to_star(conn, schema_name, table_name, phase_number, dim_tables):
    column_map = {}
    for dim_table in dim_tables:
        # get column map for this dim_table
        column_mapping_query = queries.get_dim_column_mapping_query(schema_name, table_name, phase_number, dim_table)
        column_mapping_result = execute_udl_query_with_result(conn, column_mapping_query, 'Exception -- getting column mapping', 'W_load_from_integration_to_star', 'get_column_mapping_from_int_to_star')
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
    tenant_db_info = get_tenant_target_db_information(tenant_code)
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

        mk.REF_TABLE: udl2_conf['udl2_db']['ref_table_name'],
        mk.PHASE: int(phase_number),
        mk.MOVE_TO_TARGET: udl2_conf['move_to_target'],
        mk.LOAD_TYPE: load_type,
        mk.TENANT_NAME: tenant_code if udl2_conf['multi_tenant']['on'] else udl2_conf['multi_tenant']['default_tenant'],
    }

    conf.update(tenant_db_info)

    return conf


def get_tenant_target_db_information(tenant_code):
    """
    If multi-tenancy is on look in the Master metadata table to pull out
    information about this tenant, otherwise get the target db info from udl2_conf
    :param tenant_code: The code (2 char name) for the give tenant
    :return: A dictionary containing the relevant connection information
    """
    tenant_code = tenant_code if udl2_conf['multi_tenant']['on'] else udl2_conf['multi_tenant']['default_tenant']
    #if udl2_conf['multi_tenant']['on']:
    #    with UDL2DBConnection() as conn:
    #        mast_meta_table = conn.get_table(udl2_conf['udl2_db']['master_metadata_table'])
    #
    #        select_object = select([mast_meta_table]).where(mast_meta_table.c.tenant_code == tenant_code)
    #        (_, _, _, _, db_host, db_name, schema, port, user, passwd, _) = conn.execute(select_object).fetchone()
    #    db_name = udl2_conf['target_db'][tenant_code]['db_database']
    #    passwd = udl2_conf['target_db'][tenant_code]['db_pass']
    #    user = udl2_conf['target_db'][tenant_code]['db_user']
    #else:
    #    db_host = udl2_conf['target_db']['db_host']
    #    port = udl2_conf['target_db']['db_port']
    #    user = udl2_conf['target_db']['db_user']
    #    db_name = udl2_conf['target_db']['db_database']
    #    schema = udl2_conf['target_db']['db_schema']
    #    passwd = udl2_conf['target_db']['db_pass']

    return {
        #mk.TARGET_DB_HOST: db_host,
        mk.TARGET_DB_NAME: udl2_conf['target_db_conn'][tenant_code]['db_database'],
        #mk.TARGET_DB_PORT: port,
        mk.TARGET_DB_USER: udl2_conf['target_db_conn'][tenant_code]['db_user'],
        mk.TARGET_DB_SCHEMA: udl2_conf['target_db']['db_schema'],
        mk.TARGET_DB_PASSWORD: udl2_conf['target_db_conn'][tenant_code]['db_pass'],
    }

