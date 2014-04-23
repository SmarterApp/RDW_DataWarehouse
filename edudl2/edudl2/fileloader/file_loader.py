import datetime
import csv
import edudl2.fileloader.prepare_queries as queries
import random
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.sql.expression import select
import edudl2.udl2.message_keys as mk
from edudl2.udl2_util.database_util import execute_udl_queries
from edudl2.udl2.constants import Constants
import logging
from edudl2.database.udl2_connector import get_udl_connection


DATA_TYPE_IN_FDW_TABLE = 'text'
logger = logging.getLogger(__name__)


def check_setup(staging_table, engine, conn):
    '''
    Function to check if the given staging table exists or not
    If the given staging table does not exist, raise NoSuchTableError
    '''
    # check if staging table is defined or not
    if not engine.dialect.has_table(conn, staging_table):
        logger.error("There is no staging table -- %s " % staging_table)
        raise NoSuchTableError


def extract_csv_header(conn, staging_schema, ref_table, csv_lz_table, csv_header_file):
    '''
    Extract header names and header types from input csv file,
    and also compare the header names in csv_header_file and ref_table.
    If any of header does not match, raise ValueError.
    By default, the header type for all columns is 'text'.
    '''
    # get ordered header names from input csv_header_file
    with open(csv_header_file) as csv_obj:
        reader = csv.reader(csv_obj)
        header_names_in_header_file = next(reader)
        header_types = [DATA_TYPE_IN_FDW_TABLE] * len(header_names_in_header_file)

    #Case insensitive
    lowered_headers_in_file = [header.lower() for header in header_names_in_header_file]
    # verify headers in csv header file also exist in ref_table
    header_names_in_ref_table = get_csv_header_names_in_ref_table(conn, staging_schema, ref_table, csv_lz_table)
    # if there are columns which exist at header file, but not defined in ref table, raise exception
    diff_item = set(lowered_headers_in_file) - set(header_names_in_ref_table)
    if len(diff_item) > 0:
        raise ValueError('Column %s does not match between header file and mapping defined in ref table %s' % (str(diff_item), ref_table))
    formatted_header_names = [canonicalize_header_field(name) for name in lowered_headers_in_file]
    return formatted_header_names, header_types


def get_csv_header_names_in_ref_table(conn, staging_schema, ref_table_name, csv_lz_table):
    '''
    Function to get header names in the given ref_table
    '''
    header_names_in_ref_table = []
    ref_table = conn.get_table(ref_table_name)
    ref_table_columns_query = select([ref_table.c.source_column]).where(ref_table.c.source_table == csv_lz_table)
    csv_columns_in_ref_table = conn.execute(ref_table_columns_query)
    if csv_columns_in_ref_table:
        header_names_in_ref_table = [name[0] for name in csv_columns_in_ref_table]
    return header_names_in_ref_table


def canonicalize_header_field(field_name):
    '''
    Canonicalize input field_name
    '''
    # TODO: rules TBD
    return field_name.replace('-', '_').replace(' ', '_').replace('#', '')


def create_fdw_tables(conn, header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    '''
    Create one foreign table which maps to the given csv_file on the given fdw_server
    '''
    create_csv_ddl = queries.create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server)
    drop_csv_ddl = queries.drop_ddl_csv_query(csv_schema, csv_table)
    # First drop the fdw table if exists, then create a new one
    execute_udl_queries(conn, [drop_csv_ddl, create_csv_ddl], 'Exception in creating fdw tables --', 'file_loader', 'create_fdw_tables')


def get_fields_map(conn, ref_table_name, csv_lz_table, guid_batch, csv_file, staging_schema, header_file):
    '''
    Getting field mapping, which maps the columns in staging table, and columns in csv table
    The mapping is defined in the given ref_table except for guid_batch and src_file_rec_num
    @return: stg_asmt_outcome_columns - list of columns in staging table
             csv_table_columns - list of corresponding columns in csv table
             transformation_rules - list of transformation rules for corresponding columns
    '''
    # get column mapping from ref table
    ref_table = conn.get_table(ref_table_name)
    column_mapping_query = select([ref_table.c.source_column,
                                   ref_table.c.target_column,
                                   ref_table.c.stored_proc_name],
                                  from_obj=ref_table).where(ref_table.c.source_table == csv_lz_table)
    column_mapping_result = conn.execute(column_mapping_query)
    op_column_present = check_header_contains_op(header_file)

    # column guid_batch and src_file_rec_num are in staging table, but not in csv_table
    csv_table_columns = ['\'' + str(guid_batch) + '\'', 'nextval(\'{seq_name}\')']
    stg_columns = ['guid_batch', 'src_file_rec_num']
    transformation_rules = ['', '']
    if column_mapping_result:
        for mapping in column_mapping_result:
            if mapping[1] == Constants.OP_COLUMN_NAME and not op_column_present:
                continue
            csv_table_columns.append(mapping[0])
            stg_columns.append(mapping[1])
            transformation_rules.append(mapping[2])
    return stg_columns, csv_table_columns, transformation_rules


def import_via_fdw(conn, stg_columns, csv_table_columns, transformation_rules,
                   apply_rules, staging_schema, staging_table, csv_schema, csv_table, start_seq):
    '''
    Load data from foreign table to staging table
    '''
    # create sequence name, use table_name and a random number combination. This sequence is used for column src_file_rec_num
    seq_name = (csv_table + '_' + str(random.choice(range(1, 10)))).lower()

    # query 1 -- create query to create sequence
    create_sequence = queries.create_sequence_query(staging_schema, seq_name, start_seq)
    # query 2 -- create query to load data from fdw to staging table
    insert_into_staging_table = queries.create_inserting_into_staging_query(stg_columns, apply_rules, csv_table_columns,
                                                                            staging_schema, staging_table, csv_schema, csv_table, seq_name,
                                                                            transformation_rules)
    # query 3 -- create query to drop sequence
    drop_sequence = queries.drop_sequence_query(staging_schema, seq_name)
    # logger.debug('@@@@@@@', insert_into_staging_table)

    # execute 3 queries in order
    execute_udl_queries(conn, [create_sequence, insert_into_staging_table, drop_sequence], 'Exception in loading data -- ', 'file_loader', 'import_via_fdw')


def drop_fdw_tables(conn, csv_schema, csv_table):
    '''
    Drop foreign table
    '''
    drop_csv_ddl = queries.drop_ddl_csv_query(csv_schema, csv_table)
    execute_udl_queries(conn, [drop_csv_ddl], 'Exception in drop fdw table -- ', 'file_loader', 'drop_fdw_tables')


def load_data_process(conn, conf):
    '''
    Load data from csv to staging table. The database connection and configuration information are provided
    '''
    # read headers from header_file
    header_names, header_types = extract_csv_header(conn, conf[mk.TARGET_DB_SCHEMA], conf[mk.REF_TABLE], conf[mk.CSV_LZ_TABLE], conf[mk.HEADERS])

    # create FDW table
    create_fdw_tables(conn, header_names, header_types, conf[mk.FILE_TO_LOAD], conf[mk.CSV_SCHEMA], conf[mk.CSV_TABLE], conf[mk.FDW_SERVER])

    # get field map
    stg_columns, csv_table_columns, transformation_rules = get_fields_map(conn, conf[mk.REF_TABLE], conf[mk.CSV_LZ_TABLE],
                                                                          conf[mk.GUID_BATCH], conf[mk.FILE_TO_LOAD],
                                                                          conf[mk.TARGET_DB_SCHEMA], conf[mk.HEADERS])

    # load the data from FDW table to staging table
    start_time = datetime.datetime.now()
    import_via_fdw(conn, stg_columns, csv_table_columns, transformation_rules,
                   conf[mk.APPLY_RULES], conf[mk.TARGET_DB_SCHEMA], conf[mk.TARGET_DB_TABLE],
                   conf[mk.CSV_SCHEMA], conf[mk.CSV_TABLE], conf[mk.ROW_START])
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)

    # drop FDW table
    drop_fdw_tables(conn, conf[mk.CSV_SCHEMA], conf[mk.CSV_TABLE])

    return time_as_seconds


def check_header_contains_op(csv_file):
    """Open the csv file and determine if the file contains the OP column

    :param csv_file: the name of the csv file
    :returns True if the file contains the 'op' column, False otherwise
    """
    with open(csv_file, 'r') as fp:
        csv_reader = csv.reader(fp)
        header = next(csv_reader)
        return Constants.OP_COLUMN_NAME in header


def load_file(conf):
    '''
    Main function to initiate file loader
    '''
    logger.info("Starting data load from csv to staging")
    with get_udl_connection() as conn:
        # start loading file process
        time_for_load_as_seconds = load_data_process(conn, conf)
    logger.info("Data Loaded from csv to Staging in %s seconds" % time_for_load_as_seconds)
