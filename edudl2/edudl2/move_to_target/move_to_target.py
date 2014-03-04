from edudl2.udl2_util.database_util import execute_udl_queries, execute_udl_query_with_result
from collections import OrderedDict
from edudl2.udl2 import message_keys as mk
import datetime
import logging
from edcore.utils.utils import compile_query_to_sql_text
from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
from config.ref_table_data import op_table_conf
from edudl2.udl2.udl2_connector import TargetDBConnection, UDL2DBConnection, ProdDBConnection
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.move_to_target.move_to_target_setup import get_column_and_type_mapping
from edudl2.move_to_target.create_queries import (select_distinct_asmt_guid_query, select_distinct_asmt_rec_id_query,
                                                  enable_trigger_query, create_insert_query, update_foreign_rec_id_query,
                                                  create_information_query, create_select_columns_in_table_query,
                                                  create_delete_query, create_sr_table_select_insert_query,
                                                  update_matched_fact_asmt_outcome_row, find_deleted_fact_asmt_outcome_rows,
                                                  match_delete_fact_asmt_outcome_row_in_prod)
from edudl2.move_to_target.query_helper import QueryHelper


DBDRIVER = "postgresql"
FAKE_REC_ID = -1
logger = logging.getLogger(__name__)


def explode_data_to_fact_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to explode data from integration table INT_SBAC_ASMT_OUTCOME to star schema table fact_asmt_outcome
    The basic steps are:
    0. Get three foreign keys: asmt_rec_id, student_rec_id and section_rec_id
    1. Disable trigger of table fact_asmt_outcome
    2. Insert data from INT_SBAC_ASMT_OUTCOME to fact_asmt_outcome. But for columns inst_hier_rec_id and student_rec_id ,
       put the temporary value as -1
    3. Update foreign key inst_hier_rec_id by comparing district_guid, school_guid and state_code
    4. Update foreign key student_rec_id by comparing student_guid, batch_guid
    5. Enable trigger of table fact_asmt_outcome
    '''
    asmt_rec_id_info = conf[mk.MOVE_TO_TARGET]['asmt_rec_id']
    # get asmt_rec_id, which is one foreign key in fact table
    asmt_rec_id, asmt_rec_id_column_name = get_asmt_rec_id(conf, asmt_rec_id_info['guid_column_name'], asmt_rec_id_info['guid_column_in_source'],
                                                           asmt_rec_id_info['rec_id'], asmt_rec_id_info['target_table'], asmt_rec_id_info['source_table'])

    # get section_rec_id, which is one foreign key in fact table. We set to a fake value
    section_rec_id_info = conf[mk.MOVE_TO_TARGET]['section_rec_id_info']
    section_rec_id = section_rec_id_info['value']
    section_rec_id_column_name = section_rec_id_info['rec_id']

    # update above 2 foreign keys in column mapping
    column_mapping[asmt_rec_id_column_name] = str(asmt_rec_id)
    column_mapping[section_rec_id_column_name] = str(section_rec_id)

    # get list of queries to be executed
    queries = create_queries_for_move_to_fact_table(conf, source_table, target_table, column_mapping, column_types)

    # create database connection (connect to target)
    with TargetDBConnection(conf[mk.TENANT_NAME]) as conn:

        # execute above four queries in order, 2 parts
        # First part: Disable Trigger & Load Data
        start_time_p1 = datetime.datetime.now()
        for query in queries[0:2]:
            logger.info(query)
        affected_rows_first = execute_udl_queries(conn,
                                                  queries[0:2],
                                                  'Exception -- exploding data from integration to fact table part 1',
                                                  'move_to_target',
                                                  'explode_data_to_fact_table')
        finish_time_p1 = datetime.datetime.now()

        # Record benchmark
        benchmark = BatchTableBenchmark(conf[mk.GUID_BATCH], conf[mk.LOAD_TYPE],
                                        'udl2.W_load_from_integration_to_star.explode_to_fact',
                                        start_time_p1, finish_time_p1,
                                        working_schema=conf[mk.TARGET_DB_SCHEMA],
                                        udl_phase_step='Disable Trigger & Load Data')
        benchmark.record_benchmark()

        # The second part: Update Inst Hier Rec Id FK, Update Student Rec Id FK
        start_time_p2 = datetime.datetime.now()
        execute_udl_queries(conn,
                            queries[2:5],
                            'Exception -- exploding data from integration to fact table part 2',
                            'move_to_target',
                            'explode_data_to_fact_table')
        finish_time_p2 = datetime.datetime.now()

        # Record benchmark
        benchmark = BatchTableBenchmark(conf[mk.GUID_BATCH], conf[mk.LOAD_TYPE],
                                        'udl2.W_load_from_integration_to_star.explode_to_fact',
                                        start_time_p2, finish_time_p2,
                                        working_schema=conf[mk.TARGET_DB_SCHEMA],
                                        udl_phase_step='Update Inst Hier Rec Id FK & Re-enable Trigger')
        benchmark.record_benchmark()

    # returns the number of rows that are inserted into fact table. It maps to the second query result
    return affected_rows_first[1]


def get_asmt_rec_id(conf, guid_column_name_in_target, guid_column_name_in_source, rec_id_column_name,
                    target_table_name, source_table_name):
    '''
    Main function to get asmt_rec_id in dim_asmt table
    Steps:
    1. Get guid_amst from integration table INT_SBAC_ASMT
    2. Select asmt_rec_id from dim_asmt by the same guid_amst got from 1. It should have 1 value
    '''
    # connect to integration table, to get the value of guid_asmt
    with UDL2DBConnection() as conn_to_source_db:
        query_to_get_guid = select_distinct_asmt_guid_query(conf[mk.SOURCE_DB_SCHEMA],
                                                            source_table_name,
                                                            guid_column_name_in_source, conf[mk.GUID_BATCH])
        # print(query_to_get_guid)
        guid_column_value = execute_query_get_one_value(conn_to_source_db, query_to_get_guid,
                                                        guid_column_name_in_source)

    # connect to target table, to get the value of asmt_rec_id
    with TargetDBConnection(conf[mk.TENANT_NAME]) as conn_to_target_db:
        query_to_get_rec_id = select_distinct_asmt_rec_id_query(conf[mk.TARGET_DB_SCHEMA],
                                                                target_table_name,
                                                                rec_id_column_name,
                                                                guid_column_name_in_target,
                                                                guid_column_value)
        # print(query_to_get_rec_id)
        asmt_rec_id = execute_query_get_one_value(conn_to_target_db, query_to_get_rec_id, rec_id_column_name)

    return asmt_rec_id, rec_id_column_name


def execute_query_get_one_value(conn, query, column_name):
    '''
    This is the function to execute one query, and return one correct value returned by the query
    '''
    one_value_result = []
    try:
        result = conn.execute(query)
        for row in result:
            one_value_result.append(row[0])
    except Exception as exception:
        logger.exception(exception)
    if len(one_value_result) != 1:
        # raise Exception('Rec id of %s has more/less than 1 record for batch %s' % (column_name, guid_batch))
        logger.info('Rec id of %s has more/less than 1 record, length is %d ' % (column_name, len(one_value_result)))
        if len(one_value_result) > 1:
            one_value_result = str(one_value_result[0])
        else:
            one_value_result = ['-1']
    return one_value_result[0]


def create_queries_for_move_to_fact_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to create four queries(in order) for moving data from integration table
    INT_SBAC_ASMT_OUTCOME to star schema table fact_asmt_outcome.
    These four queries are corresponding to four steps described in method explode_data_to_fact_table().
    @return: list of four queries
    '''
    # disable foreign key in fact table
    disable_trigger_query = enable_trigger_query(conf[mk.TARGET_DB_SCHEMA], target_table, False)

    # create insertion insert_into_fact_table_query
    insert_into_fact_table_query = create_insert_query(conf, source_table, target_table, column_mapping, column_types,
                                                       False)
    logger.info(insert_into_fact_table_query)

    # update inst_hier_query back
    update_inst_hier_rec_id_fk_query = update_foreign_rec_id_query(conf[mk.TARGET_DB_SCHEMA], FAKE_REC_ID,
                                                                   conf[mk.MOVE_TO_TARGET]['update_inst_hier_rec_id_fk'])

    # update student query back
    update_student_rec_id_fk_query = update_foreign_rec_id_query(conf[mk.TARGET_DB_SCHEMA], FAKE_REC_ID,
                                                                 conf[mk.MOVE_TO_TARGET]['update_student_rec_id_fk'])

    # enable foreign key in fact table
    enable_back_trigger_query = enable_trigger_query(conf[mk.TARGET_DB_SCHEMA], target_table, True)

    return [disable_trigger_query, insert_into_fact_table_query, update_inst_hier_rec_id_fk_query,
            update_student_rec_id_fk_query,
            enable_back_trigger_query]


def explode_data_to_dim_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to move data from source table to target tables.
    Source table can be INT_SBAC_ASMT, and INT_SBAC_ASMT_OUTCOME. Target table can be any dim tables in star schema.
    @param conf: one dictionary which has database settings, and guid_batch
    @param source_table: name of the source table where the data comes from
    @param target_table: name of the target table where the data should be moved to
    @param column_mapping: list of tuple of:
                           column_name_in_target, column_name_in_source
    @param column_types: data types of all columns in one target table
    '''
    # create database connection to target
    with TargetDBConnection(conf[mk.TENANT_NAME]) as conn:

        # create insertion query
        # TODO: find out if the affected rows, time can be returned, so that the returned info can be put in the log
        # send only data that is needed to be inserted (such insert, update) to dimenstion table
        query = create_insert_query(conf, source_table, target_table, column_mapping, column_types, True,
                                    'C' if source_table in op_table_conf else None)

            #query = create_insert_query(conf, source_table, target_table, column_mapping, column_types, True, None)
        logger.info(compile_query_to_sql_text(query))

        # execute the query
        affected_rows = execute_udl_queries(conn, [query],
                                            'Exception -- exploding data from integration to target ' +
                                            '{target_table}'.format(target_table=target_table),
                                            'move_to_target', 'explode_data_to_dim_table')

    return affected_rows


def calculate_spend_time_as_second(start_time, finish_time):
    '''
    Main function to calculate period distance as seconds
    '''
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)
    return time_as_seconds


def match_deleted_records(conf, match_conf):
    '''
    Match production database in fact_asmt_outcome. and get fact_asmt_outcome primary rec id
    in prodution tables.
    return a list of rec_id to delete reocrds
    '''
    candidates = []
    matched_results = []
    logger.info('in match_deleted_records')
    with TargetDBConnection(conf[mk.TENANT_NAME]) as target_conn:

        query = find_deleted_fact_asmt_outcome_rows(conf[mk.TARGET_DB_SCHEMA],
                                                    match_conf['target_table'],
                                                    conf[mk.GUID_BATCH],
                                                    match_conf['find_deleted_fact_asmt_outcome_rows'])
        candidates = execute_udl_query_with_result(target_conn, query,
                                                   'Exception -- Failed at execute find_deleted_fact_asmt_outcome_rows query',
                                                   'move_to_target',
                                                   'matched_deleted_records')
    with ProdDBConnection(conf[mk.TENANT_NAME]) as prod_conn:
        for candidate in candidates.fetchall():
            query = match_delete_fact_asmt_outcome_row_in_prod(conf[mk.PROD_DB_SCHEMA],
                                                               match_conf['prod_table'],
                                                               match_conf['match_delete_fact_asmt_outcome_row_in_prod'],
                                                               dict(zip(match_conf['find_deleted_fact_asmt_outcome_rows']['columns'],
                                                                        candidate)))
            matched = execute_udl_query_with_result(prod_conn, query,
                                                    'Exception -- Failed at match_delete_fact_asmt_outcome_row_in_prod query',
                                                    'move_to_target',
                                                    'matched_deleted_records')
            if matched.rowcount > 0:
                for row in matched.fetchall():
                    matched_results.append(dict(zip(match_conf['match_delete_fact_asmt_outcome_row_in_prod']['columns'],
                                                    row)))
    return matched_results


def update_or_delete_duplicate_record(tenant_name, guid_batch, match_conf):
    affected_rows = 0
    with TargetDBConnection(tenant_name) as target_conn, ProdDBConnection(tenant_name) as prod_conn:
        # TODO rename QueryHelper
        target_db_helper = QueryHelper(target_conn, guid_batch, match_conf)
        prod_db_helper = QueryHelper(prod_conn, guid_batch, match_conf)
        for record in target_db_helper.find_all():
            matched = prod_db_helper.find_by_natural_key(record)
            if not matched:
                continue
            identical = target_db_helper.is_identical(matched, record)
            if not identical:
                # TODO update dim & fact table?
                # TODO what if student_rec_id already exists?
                target_db_helper.update_to_match(matched)
            else:
                # TODO what about fact_asmt_outcome?
                # TODO constraint in fact
                target_db_helper.delete_by_guid(record)
            affected_rows += 1
    return affected_rows


def check_mismatched_deletions(conf, match_conf):
    '''
    check if any deleted record is not in target database. if yes. return True,
    so we will raise error for this udl batch
    '''
    logger.info('check_mismatched_deletions')
    with TargetDBConnection(conf[mk.TENANT_NAME]) as conn:
        query = find_deleted_fact_asmt_outcome_rows(conf[mk.TARGET_DB_SCHEMA],
                                                    match_conf['target_table'],
                                                    conf[mk.GUID_BATCH],
                                                    match_conf['find_deleted_fact_asmt_outcome_rows'])
        mismatches = execute_udl_query_with_result(conn, query,
                                                   'Exception -- Failed at execute find_deleted_fact_asmt_outcome_rows query',
                                                   'move_to_target',
                                                   'checked_mismatched_deletions')
    mismatched_rows = []
    if mismatches.rowcount > 0:
        for mismatch in mismatches:
            mismatched_rows.append(dict(zip(match_conf['find_deleted_fact_asmt_outcome_rows']['columns'], mismatch)))
        raise DeleteRecordNotFound(conf[mk.GUID_BATCH],
                                   mismatched_rows,
                                   "{schema}.{table}".format(schema=conf[mk.PROD_DB_SCHEMA],
                                                             table=match_conf['prod_table']))


def update_deleted_record_rec_id(conf, match_conf, matched_values):
    '''
    update rows in the batch that have a match in prod with correct deletion status for migration.
    and update the asmnt_outcome_rec_id in pre-prod to prod value so migration can work faster
    '''
    logger.info('update_deleted_record_rec_id')
    with TargetDBConnection(conf[mk.TENANT_NAME]) as conn:
        for matched_value in matched_values:
            query = update_matched_fact_asmt_outcome_row(conf[mk.TARGET_DB_SCHEMA],
                                                         match_conf['target_table'],
                                                         conf[mk.GUID_BATCH],
                                                         match_conf['update_matched_fact_asmt_outcome_row'],
                                                         matched_value)
            try:
                execute_udl_queries(conn, [query],
                                    'Exception -- Failed at execute find_deleted_fact_asmt_outcome_rows query',
                                    'move_to_target',
                                    'update_deleted_record_rec_id')
            except Exception:
                pass


def move_data_from_int_tables_to_target_table(conf, task_name, source_tables, target_table):
    '''
    Move student registration data from source integration tables to target table.
    Source tables are INT_STU_REG and INT_STU_REG_META. Target table is student_registration.

    @param conf: Configuration for particular load type (assessment or studentregistration)
    @param task_name: Name of the celery task invoking this method
    @param source_tables: Names of the source tables from where the data comes
    @param target_table: Name of the target table to where the data should be moved

    @return: Number of inserted rows
    '''

    with UDL2DBConnection() as conn_to_source_db:

        column_and_type_mapping = get_column_and_type_mapping(conf, conn_to_source_db, task_name,
                                                              target_table, source_tables)

        delete_criteria = get_current_stu_reg_delete_criteria(conn_to_source_db, conf[mk.GUID_BATCH],
                                                              conf[mk.SOURCE_DB_SCHEMA], conf[mk.SOURCE_DB_TABLE])

    with TargetDBConnection(conf[mk.TENANT_NAME]) as conn_to_target_db:

        # Cleanup any existing records with matching registration system id and academic year.
        delete_query = create_delete_query(conf[mk.TARGET_DB_SCHEMA], target_table, delete_criteria)
        deleted_rows = execute_udl_queries(conn_to_target_db, [delete_query],
                                           'Exception -- deleting data from target {target_table}'.format(target_table=target_table),
                                           'move_to_target', 'move_data_from_int_tables_to_target_table')
        logger.info('{deleted_rows} deleted from {target_table}'.format(deleted_rows=deleted_rows[0], target_table=target_table))

        insert_query = create_sr_table_select_insert_query(conf, target_table, column_and_type_mapping)
        logger.info(insert_query)
        affected_rows = execute_udl_queries(conn_to_target_db, [insert_query],
                                            'Exception -- moving data from integration {int_table} to target {target_table}'
                                            .format(int_table=source_tables[0], target_table=target_table),
                                            'move_to_target', 'move_data_from_int_tables_to_target_table')

    return affected_rows


def get_current_stu_reg_delete_criteria(conn, batch_guid, source_db_schema, source_table):
    '''
    Get the delete criteria for current stident registration job

    @param conn: Connection to source database
    @param batch_guid: Batch ID to be used in criteria to select correct table row
    @param source_db_schema: Names of the source database schema
    @param source_table: Source table containing the delete criteria information

    @return: Criteria for deletion from target table for current batch job
    '''

    select_columns = ['test_reg_id', 'academic_year']
    criteria = {'guid_batch': batch_guid}
    query = create_select_columns_in_table_query(source_db_schema, source_table, select_columns, criteria)

    result = execute_udl_query_with_result(conn, query, 'Bad Query')
    reg_system_id, academic_year = result.fetchone()

    return {'reg_system_id': reg_system_id, 'academic_year': str(academic_year)}
