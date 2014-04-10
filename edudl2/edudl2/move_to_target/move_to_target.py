from edudl2.udl2_util.database_util import execute_udl_queries
from sqlalchemy.exc import IntegrityError
from edudl2.udl2 import message_keys as mk
import datetime
import logging
from edschema.metadata.util import get_tables_starting_with
from edcore.utils.utils import compile_query_to_sql_text
from edudl2.exceptions.errorcodes import ErrorSource
from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound, UDLDataIntegrityError
from config.ref_table_data import op_table_conf
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.move_to_target.move_to_target_setup import get_column_and_type_mapping
from edudl2.database.udl2_connector import get_target_connection, get_udl_connection,\
    get_prod_connection
from edudl2.move_to_target.handle_upsert_helper import HandleUpsertHelper
from edschema.metadata_generator import generate_ed_metadata
import edschema.metadata.util as edschema_util
from sqlalchemy import update
from sqlalchemy.sql.expression import text, select, and_, tuple_
from edcore.database.utils.utils import create_schema
from edcore.database.utils.constants import Constants
from edschema.metadata.util import get_primary_key_columns, get_natural_key, get_natural_key_columns
from edudl2.move_to_target.create_queries import enable_trigger_query,\
    create_insert_query, update_foreign_rec_id_query,\
    create_sr_table_select_insert_query,\
    create_delete_query, update_matched_fact_asmt_outcome_row,\
    get_delete_candidates, match_delete_record_against_prod

FAKE_REC_ID = -1
logger = logging.getLogger(__name__)


def create_target_schema_for_batch(conf):
    """
    creates the target star schema needed for this batch
    """
    with get_target_connection(conf[mk.TENANT_NAME]) as conn:
        schema_name = conf[mk.TARGET_DB_SCHEMA]
        create_schema(conn, generate_ed_metadata, schema_name)
        conn.set_metadata_by_reflect(schema_name)
        drop_foreign_keys_on_fact_asmt_outcome(conn, schema_name)


def drop_foreign_keys_on_fact_asmt_outcome(conn, schema):
    '''
    drop foreign key constraints of fact_asmt_outcome table in target db.
    :param target_db: The configuration dictionary for
    '''
    constraints = ['fact_asmt_outcome_student_rec_id_fkey', 'fact_asmt_outcome_asmt_rec_id_fkey', 'fact_asmt_outcome_inst_hier_rec_id_fkey']
    for constraint in constraints:
        sql = text('ALTER TABLE "{schema}".{table} DROP CONSTRAINT {constraint}'.format(schema=schema,
                                                                                        table='fact_asmt_outcome',
                                                                                        constraint=constraint))
        conn.execute(sql)


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
    # get asmt_rec_id, which is one foreign key in fact table
    asmt_rec_id_info = conf[mk.MOVE_TO_TARGET]['asmt_rec_id']
    asmt_rec_id_column_name = asmt_rec_id_info['rec_id']
    asmt_rec_id = get_asmt_rec_id(conf[mk.GUID_BATCH], conf[mk.TENANT_NAME], asmt_rec_id_info)

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
    with get_target_connection(conf[mk.TENANT_NAME], conf[mk.GUID_BATCH]) as conn:
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


def get_asmt_rec_id(guid_batch, tenant_name, asmt_rec_id_info):
    '''
    Returns asmt_rec_id from dim_asmt table
    Steps:
    1. Get guid_asmt from integration table INT_SBAC_ASMT
    2. Select asmt_rec_id from dim_asmt by the same guid_amst got from 1. It should have 1 value
    '''
    source_table_name = asmt_rec_id_info['source_table']
    guid_column_name_in_source = asmt_rec_id_info['guid_column_in_source']
    target_table_name = asmt_rec_id_info['target_table']
    guid_column_name_in_target = asmt_rec_id_info['guid_column_name']
    rec_id_column_name = asmt_rec_id_info['rec_id']

    # connect to integration table, to get the value of guid_asmt
    with get_udl_connection() as udl_conn:
        int_table = udl_conn.get_table(source_table_name)
        query = select([int_table.c[guid_column_name_in_source]], from_obj=int_table, limit=1)
        query = query.where(int_table.c['guid_batch'] == guid_batch)
        results = udl_conn.get_result(query)
        if results:
            guid_column_value = results[0][guid_column_name_in_source]

    # connect to target table, to get the value of asmt_rec_id
    with get_target_connection(tenant_name, guid_batch) as target_conn:
        dim_asmt = target_conn.get_table(target_table_name)
        query = select([dim_asmt.c[rec_id_column_name]], from_obj=dim_asmt, limit=1)
        query = query.where(dim_asmt.c[guid_column_name_in_target] == guid_column_value)
        query = query.where(and_(dim_asmt.c['batch_guid'] == guid_batch))
        results = target_conn.get_result(query)
        if results:
            asmt_rec_id = results[0][rec_id_column_name]

    return asmt_rec_id


def create_queries_for_move_to_fact_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to create four queries(in order) for moving data from integration table
    INT_SBAC_ASMT_OUTCOME to star schema table fact_asmt_outcome.
    These four queries are corresponding to four steps described in method explode_data_to_fact_table().
    @return: list of four queries
    '''
    # disable foreign key in fact table
    queries = [enable_trigger_query(conf[mk.TARGET_DB_SCHEMA], target_table, False)]

    # create insertion insert_into_fact_table_query
    insert_into_fact_table_query = create_insert_query(conf, source_table, target_table, column_mapping, column_types,
                                                       False)
    logger.info(insert_into_fact_table_query)
    queries.append(insert_into_fact_table_query)

    # update inst_hier_query back
    with get_target_connection(conf[mk.TENANT_NAME], conf[mk.TARGET_DB_SCHEMA]) as conn:
        trg_tbl = conn.get_table(target_table)
        for fk in edschema_util.get_foreign_key_reference_columns(trg_tbl):
            queries.extend(update_foreign_rec_id_query(fk))

    # enable foreign key in fact table
    queries.append(enable_trigger_query(conf[mk.TARGET_DB_SCHEMA], target_table, True))

    return queries


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
    with get_target_connection(conf[mk.TENANT_NAME], conf[mk.GUID_BATCH]) as conn:
        # create insertion query
        # TODO: find out if the affected rows, time can be returned, so that the returned info can be put in the log
        # send only data that is needed to be inserted (such insert, update) to dimenstion table
        query = create_insert_query(conf, source_table, target_table, column_mapping, column_types, True,
                                    'C' if source_table in op_table_conf else None)

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
    return (finish_time - start_time).total_seconds()


def get_columns_names_to_pick_for_delete(table):
    '''
    returns column names to be picked for handling the delete

    :param table: SQLAlchemy table object
    '''
    pk = get_primary_key_columns(table)
    nk = get_natural_key(table)
    nk = nk if nk is not None else []
    return [c.name for c in pk + nk]


def get_records_marked_for_deletion(conf, target_conn, table_name):
    table = target_conn.get_table(table_name)
    column_names = get_columns_names_to_pick_for_delete(table)
    columns_to_select = [table.c[column_name] for column_name in column_names]
    query = select(columns_to_select, from_obj=table).where(and_(table.c.batch_guid == conf[mk.GUID_BATCH],
                                                                 table.c.rec_status == Constants.STATUS_WIP))
    result = target_conn.get_result(query)
    return result


def yield_records_to_be_deleted(conf, prod_conn, table_name, records_marked_for_deletion, batch_size=100):
    '''
    Yield records to  marked as deleted from pre-prod table

    The methods yields records marked for delete('W') from the pre-prod database table

    :param conf: udl configuration object
    :param target_conn: connection object to pre-prod database
    :param batch_size: batch size to yield results
    '''
    table = prod_conn.get_table(table_name)
    natural_keys = get_natural_key_columns(table)
    columns_to_select = [table.c[column_name] for column_name in get_columns_names_to_pick_for_delete(table)]
    key_columns = [table.columns[key] for key in natural_keys]
    key_values = [[row[key] for key in natural_keys] for row in records_marked_for_deletion]
    query = select(columns_to_select, from_obj=table).where(and_(table.c.rec_status == Constants.STATUS_CURRENT,
                                                                 tuple_(*key_columns).in_(key_values)))
    result = prod_conn.execute(query, stream_results=True)
    rows = result.fetchmany(batch_size)
    while len(rows) > 0:
        yield rows
        rows = result.fetchmany(batch_size)


def update_rec_id_for_records_to_delete(conf, target_conn, table_name, prod_records_matched):
    table = target_conn.get_table(table_name)
    columns = table.c
    for record in prod_records_matched:
        values = {columns[pk_column]: record[pk_column] for pk_column in table.primary_key.columns.keys()}
        values[columns[Constants.REC_STATUS]] = Constants.STATUS_DELETE
        criteria = [table.c[nk_column] == record[nk_column] for nk_column in get_natural_key_columns(table)]
        criteria.append(table.c.batch_guid == conf[mk.GUID_BATCH])
        criteria.append(table.c.rec_status == Constants.STATUS_WIP)
        query = update(table).values(values).where(and_(*criteria))
        try:
            target_conn.execute(query)
        except IntegrityError as ie:
            e = UDLDataIntegrityError(conf[mk.GUID_BATCH], ie,
                                      "{schema}.{table}".format(schema=conf[mk.PROD_DB_SCHEMA], table=table_name),
                                      ErrorSource.DELETE_FACT_ASMT_OUTCOME_RECORD_MORE_THAN_ONCE,
                                      conf[mk.UDL_PHASE_STEP],
                                      conf[mk.WORKING_SCHEMA])
            failure_time = datetime.datetime.now()
            e.insert_err_list(failure_time)


def check_mismatched_deletions(conf, target_conn, table_name):
    '''
    check if any deleted record is not in target database
    so we will raise error for this udl batch
    '''
    logger.info('check_mismatched_deletions')
    mismatches = get_records_marked_for_deletion(conf, target_conn, table_name)
    if mismatches:
        raise DeleteRecordNotFound(conf[mk.GUID_BATCH],
                                   mismatches,
                                   "{schema}.{table}".format(schema=conf[mk.PROD_DB_SCHEMA],
                                                             table=table_name),
                                   ErrorSource.MISMATCHED_FACT_ASMT_OUTCOME_RECORD,
                                   conf[mk.UDL_PHASE_STEP],
                                   conf[mk.WORKING_SCHEMA])


def process_records_to_be_deleted(conf, target_conn, prod_conn, table_name):
    '''
    process records to be deleted
    '''
    records_marked_for_deletion = get_records_marked_for_deletion(conf, target_conn, table_name)
    if len(records_marked_for_deletion) > 0:
        proxy_rows = yield_records_to_be_deleted(conf, prod_conn, table_name, records_marked_for_deletion)
        for prod_rows in proxy_rows:
            update_rec_id_for_records_to_delete(conf, target_conn, table_name, prod_rows)
        check_mismatched_deletions(conf, target_conn, table_name)
    else:
        logger.info('No records found marked for deletion in {schema_name}.'
                    '{target_table}'.format(schema_name=conf[mk.GUID_BATCH], target_table=table_name))


def handle_updates_and_deletes(conf):
    '''
    Main handler for updates and deletes
    '''
    with get_target_connection(conf[mk.TENANT_NAME], conf[mk.TARGET_DB_SCHEMA]) as target_conn, get_prod_connection(conf[mk.TENANT_NAME]) as prod_conn:
        tables = get_tables_starting_with(target_conn.get_metadata(), Constants.FACT_TABLES_PREFIX)
        for table_name in tables:
            process_records_to_be_deleted(conf, target_conn, prod_conn, table_name)


def handle_duplicates_in_dimensions(tenant_name, guid_batch):
    '''
    Handle duplicate records in dimensions by marking them as deleted

    Steps:
    1. Soft delete records (Mark rec_status as 'S') in pre-prod dimensions that are already existing in production database
       The match is done based on natural_key columns of the table and some other key columns listed
    2. Update the rec_id of the record marked for delete with the id of the matching record found in prod. This is needed for
       step which updates foreign keys in fact asmt outcome

    :param tenant_name: tenant name, to get target database connection
    :param guid_batch:  batch buid
    '''
    affected_rows = 0
    with get_target_connection(tenant_name, guid_batch) as target_conn, get_prod_connection(tenant_name) as prod_conn:

        tables = get_tables_starting_with(target_conn.get_metadata(), Constants.DIM_TABLES_PREFIX)
        for table_name in tables:
            target_db_helper = HandleUpsertHelper(target_conn, guid_batch, table_name)
            prod_db_helper = HandleUpsertHelper(prod_conn, guid_batch, table_name)
            for record in target_db_helper.find_all():
                matched = prod_db_helper.find_by_natural_key(record)
                if not matched:
                    continue
                # soft delete the record and set its pk as the pk of the matched record
                target_db_helper.soft_delete_and_update(record, matched)
                affected_rows += 1
    return affected_rows


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
    with get_udl_connection() as conn_to_source_db:

        column_and_type_mapping = get_column_and_type_mapping(conf, conn_to_source_db, task_name,
                                                              target_table, source_tables)

        delete_criteria = get_current_stu_reg_delete_criteria(conf[mk.GUID_BATCH], conf[mk.SOURCE_DB_TABLE])

    with get_target_connection(conf[mk.TENANT_NAME], conf[mk.GUID_BATCH]) as conn_to_target_db:
        # Cleanup any existing records with matching registration system id and academic year.
        # TODO: get query and execute in one
        delete_query = create_delete_query(conf[mk.TENANT_NAME], conf[mk.TARGET_DB_SCHEMA], target_table, delete_criteria)
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


def get_current_stu_reg_delete_criteria(batch_guid, source_table):
    '''
    Get the delete criteria for current stident registration job

    @param conn: Connection to source database
    @param batch_guid: Batch ID to be used in criteria to select correct table row
    @param source_db_schema: Names of the source database schema
    @param source_table: Source table containing the delete criteria information

    @return: Criteria for deletion from target table for current batch job
    '''
    with get_udl_connection() as conn:
        int_metadata_table = conn.get_table(source_table)
        query = select([int_metadata_table.c.test_reg_id,
                        int_metadata_table.c.academic_year],
                       from_obj=int_metadata_table).where(int_metadata_table.c.guid_batch == batch_guid)
        result = conn.get_result(query)
        return {'reg_system_id': result[0]['test_reg_id'], 'academic_year': str(result[0]['academic_year'])}
