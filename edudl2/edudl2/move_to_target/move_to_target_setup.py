from edudl2.database.udl2_connector import get_target_connection
__author__ = 'swimberly'
from collections import OrderedDict, namedtuple
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.move_to_target.create_queries import (get_dim_table_mapping_query, get_column_mapping_query,
                                                  create_information_query)
from edudl2.udl2_util.database_util import execute_udl_query_with_result, get_db_connection_params
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.udl2.constants import Constants

Column = namedtuple('Column', ['src_col', 'type'])


def get_table_and_column_mapping(conf, task_name, table_name_prefix=None):
    '''
    The main function to get the table mapping and column mapping from reference table
    @param conf: configuration dictionary
    @param table_name_prefix: the prefix of the table name
    '''
    with get_udl_connection() as conn_source:
        table_map = get_table_mapping(conn_source, task_name, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], table_name_prefix)
        column_map = get_column_mapping_from_int_to_star(conn_source, task_name, conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.PHASE], list(table_map.keys()))

    return table_map, column_map


def get_table_mapping(conn, task_name, schema_name, table_name, phase_number, table_name_prefix=None):
    # TODO: refactor this to get results and query in one
    table_mapping_query = get_dim_table_mapping_query(schema_name, table_name, phase_number)
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
    # TODO: refactor this to get results and query in one
    column_map = {}
    for dim_table in dim_tables:
        # get column map for this dim_table
        column_mapping_query = get_column_mapping_query(schema_name, table_name, dim_table)
        column_mapping_result = execute_udl_query_with_result(conn, column_mapping_query, 'Exception -- getting column mapping',
                                                              task_name, 'get_column_mapping')
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


def get_column_and_type_mapping(conf, conn, task_name, target_table, source_tables):
    '''
    Get the column and type mapping for the target table.

    @param conf: Configuration for particular load type (assessment or studentregistration)
    @param conn: Connection to the source database containing the reference table
    @param task_name: Name of the celery task invoking this method
    @param target_table: Table into which to insert data
    @param source_tables: Iinclude columns from these tables

    @return: An ordered dictionary containing the column and type mapping
    '''

    column_and_type_mapping = OrderedDict()

    for source_table in source_tables:

        column_mapping_query = get_column_mapping_query(conf[mk.SOURCE_DB_SCHEMA], conf[mk.REF_TABLE], target_table, source_table)
        column_mapping_result = execute_udl_query_with_result(conn, column_mapping_query, 'Exception -- getting column mapping',
                                                              task_name, 'get_column_mapping')
        column_mapping_list = []

        if column_mapping_result:

            # We'll fill in the types in a bit....
            column_mapping = OrderedDict()
            for mapping in column_mapping_result:
                target_column = mapping[0]
                source_column = mapping[1]
                column_mapping.update({target_column: source_column})

            types = get_table_column_types(conf, target_table, column_mapping.keys())

            for target_column, source_column in column_mapping.items():
                type = types[target_column]
                column = (target_column, Column(source_column, type))

                # This is the primary key; need to put the pair in front.
                if source_column is not None and 'nextval' in source_column:
                    column_mapping_list.insert(0, column)
                else:
                    column_mapping_list.append(column)

        column_and_type_mapping[source_table] = OrderedDict(column_mapping_list)

    return column_and_type_mapping


def get_table_column_types(conf, target_table, column_names):
    '''
    Main function to get column types of a table by querying the table
    @return a dictionary, which has same ordered keys in the input column_names.
    The values are column types with maximum length if it is defined in table.
    The pattern of the value is: <column_name data_type(length)> or <column_name data_type>
    '''

    column_types = OrderedDict([(column_name, '') for column_name in column_names])
    tenant = conf[mk.TENANT_NAME]

    with get_target_connection(tenant, conf[mk.GUID_BATCH]) as conn:
        query = create_information_query(target_table)

        try:
            result = conn.execute(query)
            for row in result:
                column_name = row[0]
                data_type = row[1]
                character_maximum_length = row[2]

                if column_name in column_types.keys():
                    return_value = column_name + " " + data_type
                    if character_maximum_length:
                        return_value += "(" + str(character_maximum_length) + ")"
                    column_types[column_name] = return_value
        except Exception as e:
            print('Exception in getting type', e)

    return column_types


def generate_conf(guid_batch, phase_number, load_type, tenant_code, target_schema):
    """
    Return all needed configuration information
    :param guid_batch: the guid for the batch
    :param phase_number: the current number of the phase
    :param load_type: type of load. ie. assessment
    :param tenant_code: the tenants 2 letter code
    :return: A dictionary of the config details
    """
    tenant_prod_db_info = get_tenant_prod_db_information(tenant_code)
    db_params_tuple = get_db_connection_params(udl2_conf['udl2_db_conn']['url'])

    conf = {
        # add guid_batch from msg
        mk.GUID_BATCH: guid_batch,
        # source schema
        mk.SOURCE_DB_SCHEMA: udl2_conf['udl2_db_conn']['db_schema'],
        # source database setting
        mk.SOURCE_DB_DRIVER: db_params_tuple[0],
        mk.SOURCE_DB_USER: db_params_tuple[1],
        mk.SOURCE_DB_PASSWORD: db_params_tuple[2],
        mk.SOURCE_DB_HOST: db_params_tuple[3],
        mk.SOURCE_DB_PORT: db_params_tuple[4],
        mk.SOURCE_DB_NAME: db_params_tuple[5],

        mk.SOURCE_DB_TABLE: Constants.UDL2_JSON_INTEGRATION_TABLE(load_type),

        mk.TARGET_DB_SCHEMA: target_schema,
        mk.REF_TABLE: Constants.UDL2_REF_MAPPING_TABLE(load_type),
        mk.PHASE: int(phase_number),
        mk.LOAD_TYPE: load_type,
        mk.TENANT_NAME: tenant_code if udl2_conf['multi_tenant']['active'] else udl2_conf['multi_tenant']['default_tenant'],
    }
    conf.update(tenant_prod_db_info)

    return conf


def get_tenant_prod_db_information(tenant_code):
    """
    If multi-tenancy is on look in the Master metadata table to pull out
    information about this tenant, otherwise get the target db info from udl2_conf
    :param tenant_code: The code (2 char name) for the give tenant
    :return: A dictionary containing the relevant connection information
    """
    tenant_code = tenant_code if udl2_conf['multi_tenant']['active'] else udl2_conf['multi_tenant']['default_tenant']

    return {mk.PROD_DB_SCHEMA: udl2_conf['prod_db_conn'][tenant_code]['db_schema']}
