import logging
from edudl2.udl2_util.database_util import execute_udl_queries, get_table_columns_info
from edudl2.udl2 import message_keys as mk
from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql.expression import select, and_
from sqlalchemy.orm import aliased

logger = logging.getLogger(__name__)


def move_data_from_staging_to_integration(conf):
    '''
    map sql data type in configuration file into what SQLAlchemy type is.
    @param conf: configration dictionary, the format is defined in W_load_to_integration_table.py
           note: udl2_conf is the udl2_conf dictionary that stores all configuration settings
    '''
    source_table_name = conf[mk.SOURCE_DB_TABLE]
    target_table_name = conf[mk.TARGET_DB_TABLE]
    err_list_table_name = conf[mk.ERR_LIST_TABLE]
    guid_batch = conf[mk.GUID_BATCH]
    ref_table = conf[mk.REF_TABLE]
    with get_udl_connection() as conn:
        # get the column mapping from ref table
        target_columns, source_columns_with_tran_rule = get_column_mapping_from_stg_to_int(conn,
                                                                                           ref_table,
                                                                                           source_table_name,
                                                                                           target_table_name)
    try:
        success = move_data_from_staging_to_integration_all(source_table_name, target_table_name, err_list_table_name,
                                                            guid_batch, target_columns, source_columns_with_tran_rule)
        return success, 0
    except:
        return move_data_from_staging_to_integration_one_by_one(source_table_name, target_table_name, err_list_table_name,
                                                                guid_batch, target_columns, source_columns_with_tran_rule)


def move_data_from_staging_to_integration_all(source_table_name, target_table_name, err_list_table_name, guid_batch, target_columns, source_columns_with_tran_rule, record_sid=None):
    with get_udl_connection() as conn:

        sql_query = create_migration_query(conn, source_table_name, target_table_name,
                                           err_list_table_name, guid_batch, target_columns,
                                           source_columns_with_tran_rule, record_sid=record_sid)
        except_msg = "problem when load data from staging table to integration table"
        query_result = execute_udl_queries(conn, [sql_query], except_msg, 'move_to_integration', 'move_data_from_staging_to_integration', tries=-1)
    return query_result[0]


def move_data_from_staging_to_integration_one_by_one(source_table_name, target_table_name, err_list_table_name, guid_batch, target_columns, source_columns_with_tran_rule):
    success = 0
    fail = 0
    with get_udl_connection() as conn:
        source_table = conn.get_table(source_table_name)
        select_source_table = select([source_table.c.record_sid.label('record_sid')], from_obj=[source_table]).where(source_table.c.guid_batch == guid_batch)
        results = conn.get_result(select_source_table)
        for result in results:
            try:
                record_sid = result.get('record_sid')
                query_result = move_data_from_staging_to_integration_all(source_table_name, target_table_name, err_list_table_name,
                                                                         guid_batch, target_columns, source_columns_with_tran_rule,
                                                                         record_sid=record_sid)
                success += query_result
            except:
                logger.error('Failed to integrate record: batch_guid[' + guid_batch + '] record_sid[' + record_sid + ']')
                fail += 1
    return success, fail


def get_column_mapping_from_stg_to_int(conn, ref_table_name, staging_table, integration_table_name):
    '''
    Getting column mapping, which maps the columns in staging table, and columns in integration table
    The mapping is defined in the given ref_table
    @return: target_columns - list of columns in integration table
             source_columns_with_tran_rule - list of source columns with the corresponding transformation rules
    '''
    # get the column length of all target columns. Returns a dictionary,
    # the key is the column name in target/integration table, and the value is the column length
    column_name_length_dict = get_varchar_column_name_and_length(conn, integration_table_name)
    # get column mapping from ref table
    ref_table = conn.get_table(ref_table_name)
    column_mapping_query = select([ref_table.c.source_column,
                                   ref_table.c.target_column,
                                   ref_table.c.stored_proc_name],
                                  from_obj=ref_table).where(ref_table.c.source_table == staging_table)
    column_mapping = conn.execute(column_mapping_query)
    integration_table = conn.get_table(integration_table_name)
    target_column_ordered = [column.name for column in integration_table.c]
    column_mapping_dict = {}
    if column_mapping:
        for mapping in column_mapping:
            target_column_name = mapping[1]
            column_mapping_dict[target_column_name] = mapping
    target_columns = []
    source_columns_with_tran_rule = []
    for column in target_column_ordered:
        if column in column_mapping_dict.keys():
            mapping = column_mapping_dict[column]
            source_column = mapping[0]
            target_column = mapping[1]
            stored_proc_exp = mapping[2]
            source_column_with_query_prefix = ', '.join(['"A".' + sub_source_column.strip()
                                                         for sub_source_column in source_column.split(',')])

            # if this target column has the length information we got before
            if stored_proc_exp is not None:
                if target_column in column_name_length_dict.keys():
                    stored_proc_exp = stored_proc_exp.format(src_column=source_column_with_query_prefix,
                                                             length=column_name_length_dict[target_column])
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


def create_migration_query(conn, source_table_name, target_table_name, error_table_name,
                           guid_batch, target_columns, source_columns_with_tran_rule, record_sid=None):
    '''
    Create migration script in SQL text template. It will be a tech debt to migrate it to SQLAlchemy
    equivalent. Also the code may require updates after metadata definition are finalized

    @param source_table_name: table name for staging data that are cleaned
    @param target_table_name: table name for integration table that holds only correct results
    @param error_table_name: table name for error tables
    @param guid_batch: batch id for specific type
    @param target_columns: target table columns
    @param source_columns_with_tran_rule: source table columns with translation rules added
    '''
    integration_table = conn.get_table(target_table_name)
    staging_table = aliased(conn.get_table(source_table_name), name='A')
    error_table = aliased(conn.get_table(error_table_name), name='B')

    select_query = select(source_columns_with_tran_rule,
                          from_obj=[staging_table
                                    .outerjoin(error_table,
                                               and_(error_table.c.record_sid == staging_table.c.record_sid))])
    select_query = select_query.where(and_(staging_table.c.guid_batch == guid_batch,
                                           error_table.c.record_sid.is_(None)))
    if record_sid is not None:
        select_query = select_query.where(and_(staging_table.c.record_sid == record_sid))
    query = integration_table.insert(inline=True).from_select(target_columns, select_query)
    return query
