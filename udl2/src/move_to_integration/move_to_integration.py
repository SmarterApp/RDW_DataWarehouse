import datetime
from udl2_util.database_util import connect_db, execute_udl_queries, get_table_columns_info, execute_udl_query_with_result
from udl2 import message_keys as mk
import fileloader.prepare_queries as queries
import logging

from udl2.udl2_connector import UDL2DBConnection

logger = logging.getLogger(__name__)


def move_data_from_staging_to_integration(conf):
    '''
    map sql data type in configuration file into what SQLAlchemy type is.
    @param conf: configration dictionary, the format is defined in W_load_to_integration_table.py
           note: udl2_conf is the udl2_conf dictionary that stores all configuration settings
    '''
    with UDL2DBConnection() as conn:

        #(conn, _engine) = connect_db(conf[mk.SOURCE_DB_DRIVER],
        #                             conf[mk.SOURCE_DB_USER],
        #                             conf[mk.SOURCE_DB_PASSWORD],
        #                             conf[mk.SOURCE_DB_HOST],
        #                             conf[mk.SOURCE_DB_PORT],
        #                             conf[mk.SOURCE_DB_NAME])
        # get the column mapping from ref table
        target_columns, source_columns_with_tran_rule = get_column_mapping_from_stg_to_int(conn, conf[mk.REF_TABLE], conf[mk.SOURCE_DB_TABLE],
                                                                                           conf[mk.TARGET_DB_TABLE], conf[mk.SOURCE_DB_SCHEMA])
        sql_query = create_migration_query(conf[mk.SOURCE_DB_SCHEMA], conf[mk.SOURCE_DB_TABLE], conf[mk.TARGET_DB_SCHEMA],
                                           conf[mk.TARGET_DB_TABLE], conf[mk.ERROR_DB_SCHEMA], 'ERR_LIST', conf[mk.GUID_BATCH],
                                           target_columns, source_columns_with_tran_rule)
        logger.debug(sql_query)
        except_msg = "problem when load data from staging table to integration table"
        query_result = execute_udl_queries(conn, [sql_query], except_msg, 'move_to_integration', 'move_data_from_staging_to_integration')
    return query_result[0]


def get_column_mapping_from_stg_to_int(conn, ref_table, staging_table, integration_table, schema_name):
    '''
    Getting column mapping, which maps the columns in staging table, and columns in integration table
    The mapping is defined in the given ref_table
    @return: target_columns - list of columns in integration table
             source_columns_with_tran_rule - list of source columns with the corresponding transformation rules
    '''
    # get the column length of all target columns. Returns a dictionary, the key is the column name in target/integration table, and the value is the column length
    column_name_length_dict = get_varchar_column_name_and_length(conn, integration_table)
    # get column mapping from ref table, returns a list of tuple. The tuple has 3 items(source_column, target_column, stored_proc_exp)
    get_column_mapping_query = queries.get_column_mapping_query(schema_name, ref_table, staging_table)
    column_mapping = execute_udl_query_with_result(conn, get_column_mapping_query,
                                               'Exception in getting column mapping between csv_table and staging table -- ',
                                               'file_loader', 'get_fields_map')

    target_columns = []
    source_columns_with_tran_rule = []
    if column_mapping:
        for mapping in column_mapping:
            source_column = mapping[0]
            target_column = mapping[1]
            stored_proc_exp = mapping[2]
            source_column_with_query_prefix = ', '.join(['A.' + sub_srouce_column.strip() for sub_srouce_column in source_column.split(',')])

            # if this target column has the length information we got before
            if stored_proc_exp is not None:
                if target_column in column_name_length_dict.keys():
                    stored_proc_exp = stored_proc_exp.format(src_column=source_column_with_query_prefix, length=column_name_length_dict[target_column])
                else:
                    stored_proc_exp = stored_proc_exp.format(src_column=source_column_with_query_prefix)
            else:
                stored_proc_exp = source_column_with_query_prefix
            target_columns.append(target_column)
            source_columns_with_tran_rule.append(stored_proc_exp)
    return target_columns, source_columns_with_tran_rule


def get_varchar_column_name_and_length(conn, integration_table):
    '''
    Getting the column length of all varchar columns in integration table
    '''
    column_info = get_table_columns_info(conn, integration_table)
    column_name_length_dict = {}
    for column_info_tuple in column_info:
        # only varchar needs the length information
        if column_info_tuple[1] == 'character varying':
            column_name_length_dict[column_info_tuple[0]] = column_info_tuple[2]
    return column_name_length_dict


def create_migration_query(source_schema, source_table, target_schema, target_table,
                           error_schema, error_table, guid_batch, target_columns, source_columns_with_tran_rule):
    '''
    Create migration script in SQL text template. It will be a tech debt to migrate it to SQLAlchemy
    equivalent. Also the code may require updates after metadata definition are finalized

    @param source_shema: schema name where the staging table resides
    @param source_table: table name for staging data that are cleaned
    @param target_schema: schema name where the target table resides
    @param target_table: table name for integration table that holds only correct results
    @param error_schema: schema name where error table resides
    @param error_table: table name for error tables
    @param mapping: mapping between columns in staging table, target table and rules for type conversion
    @param guid_batch: batch id for specific type.
    '''
    target_columns_expand = ", ".join(target_columns)
    source_columns_expand = ", ".join(source_columns_with_tran_rule)

    sql_template = """
    INSERT INTO "{target_schema}"."{target_table}"
         ({target_columns})
    SELECT {source_columns}
        FROM "{source_schema}"."{source_table}" AS A LEFT JOIN
        "{error_schema}"."{error_table}" AS B ON (A.record_sid = B.record_sid )
        WHERE B.record_sid IS NULL AND A.guid_batch = \'{guid_batch}\'
    """
    sql = sql_template.format(target_schema=target_schema,
                              target_table=target_table,
                              target_columns=target_columns_expand,
                              source_columns=source_columns_expand,
                              source_schema=source_schema,
                              source_table=source_table,
                              error_schema=error_schema,
                              error_table=error_table,
                              guid_batch=guid_batch)
    return sql


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    # place holder for execute the code as shell script
    end_time = datetime.datetime.now()
