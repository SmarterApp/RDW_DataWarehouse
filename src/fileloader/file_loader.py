import datetime
import csv
import fileloader.prepare_queries as queries
import random
import argparse
from sqlalchemy.exc import NoSuchTableError
import udl2.message_keys as mk
from udl2_util.measurement import measure_cpu_plus_elasped_time
from udl2_util.database_util import execute_queries, execute_query_with_result, connect_db


DBDRIVER = "postgresql"


@measure_cpu_plus_elasped_time
def check_setup(staging_table, engine, conn):
    # check if staging table is defined or not
    if not engine.dialect.has_table(conn, staging_table):
        print("There is no staging table -- ", staging_table)
        raise NoSuchTableError


@measure_cpu_plus_elasped_time
def extract_csv_header(csv_file):
    '''
    Extract header names and types from input csv file
    '''
    print(csv_file)
    with open(csv_file) as csv_obj:
        reader = csv.reader(csv_obj)
        header_names = next(reader)
        header_types = ['text'] * len(header_names)
    formatted_header_names = [canonicalize_header_field(name) for name in header_names]

    return formatted_header_names, header_types


@measure_cpu_plus_elasped_time
def canonicalize_header_field(field_name):
    '''
    Canonicalize input field_name
    '''
    # TODO: rules TBD
    return field_name.replace('-', '_').replace(' ', '_').replace('#', '')


@measure_cpu_plus_elasped_time
def create_fdw_tables(conn, header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    create_csv_ddl = queries.create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server)
    drop_csv_ddl = queries.drop_ddl_csv_query(csv_schema, csv_table)
    execute_queries(conn, [drop_csv_ddl, create_csv_ddl], 'Exception in creating fdw tables --', 'file_loader', 'create_fdw_tables')


@measure_cpu_plus_elasped_time
def get_fields_map(conn, header_names, header_types, ref_table, csv_lz_table, batch_id, csv_file, staging_schema, staging_table):

    """
    Getting field mapper, which maps the column in staging table, and columns in csv table
    """
    # get column mapping from ref table
    get_column_mapping_query = queries.get_column_mapping_query(staging_schema, ref_table, csv_lz_table)
    column_mapping = execute_query_with_result(conn, get_column_mapping_query,
                                               'Exception in creating insertion query to stg table -- ',
                                               'file_loader', 'get_fields_map')
    csv_table_columns = ['\'' + str(batch_id) + '\'', 'nextval(\'{seq_name}\')']
    stg_asmt_outcome_columns = ['batch_id', 'record_sid']
    transformation_rules = ['', '']
    if column_mapping:
        for mapping in column_mapping:
            csv_table_columns.append(mapping[0])
            stg_asmt_outcome_columns.append(mapping[1])
            transformation_rules.append(mapping[2])
    """
    # pick the columns from the 2nd to the last 2nd
    stg_asmt_outcome_columns = [column_info[0] for column_info in UDL_METADATA['TABLES']['STG_SBAC_ASMT_OUTCOME']['columns'][1:-1]]
    # map first column in staging table to batch_id, map second column in staging table to the expression of using sequence
    csv_table_columns = header_names[:]
    csv_table_columns.insert(0, '\'' + str(batch_id) + '\'')
    csv_table_columns.insert(1, 'nextval(\'{seq_name}\')')
    """
    return stg_asmt_outcome_columns, csv_table_columns, transformation_rules


@measure_cpu_plus_elasped_time
def import_via_fdw(conn, stg_asmt_outcome_columns, csv_table_columns, transformation_rules, header_types,
                   batch_id, apply_rules, staging_schema, staging_table, csv_schema, csv_table, start_seq):
    # create sequence name, use table_name and a random number combination
    seq_name = (csv_table + '_' + str(random.choice(range(1, 10)))).lower()
    create_sequence = queries.create_sequence_query(staging_schema, seq_name, start_seq)
    insert_into_staging_table = queries.create_inserting_into_staging_query(stg_asmt_outcome_columns, apply_rules, csv_table_columns, header_types,
                                                                            staging_schema, staging_table, csv_schema, csv_table, start_seq, seq_name,
                                                                            transformation_rules)
    drop_sequence = queries.drop_sequence_query(staging_schema, seq_name)
    # print('@@@@@@@', insert_into_staging_table)
    execute_queries(conn, [create_sequence, insert_into_staging_table, drop_sequence], 'Exception in loading data -- ', 'file_loader', 'import_via_fdw')


@measure_cpu_plus_elasped_time
def drop_fdw_tables(conn, csv_schema, csv_table):
    drop_csv_ddl = queries.drop_ddl_csv_query(csv_schema, csv_table)
    execute_queries(conn, [drop_csv_ddl], 'Exception in drop fdw table -- ', 'file_loader', 'drop_fdw_tables')


@measure_cpu_plus_elasped_time
def load_data_process(conn, conf):
    # read headers from header_file
    # TODO: decide: extract from csv or read from ref table. Maybe reading from csv is better for creating fdw
    # since it keeps same order of headers in csv
    header_names, header_types = extract_csv_header(conf[mk.HEADERS])

    # create FDW table
    create_fdw_tables(conn, header_names, header_types, conf[mk.FILE_TO_LOAD], conf[mk.CSV_SCHEMA], conf[mk.CSV_TABLE], conf[mk.FDW_SERVER])

    # get field map
    stg_asmt_outcome_columns, csv_table_columns, transformation_rules = get_fields_map(conn, header_names, header_types,
                                                                                       conf[mk.REF_TABLE], conf[mk.CSV_LZ_TABLE], conf[mk.BATCH_ID], conf[mk.FILE_TO_LOAD],
                                                                                       conf[mk.TARGET_DB_SCHEMA], conf[mk.TARGET_DB_TABLE])

    # load the data from FDW table to staging table
    start_time = datetime.datetime.now()
    import_via_fdw(conn, stg_asmt_outcome_columns, csv_table_columns, transformation_rules, header_types,
                   conf[mk.BATCH_ID], conf[mk.APPLY_RULES], conf[mk.TARGET_DB_SCHEMA], conf[mk.TARGET_DB_TABLE],
                   conf[mk.CSV_SCHEMA], conf[mk.CSV_TABLE], conf[mk.ROW_START])
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)

    # drop FDW table
    drop_fdw_tables(conn, conf[mk.CSV_SCHEMA], conf[mk.CSV_TABLE])

    return time_as_seconds


@measure_cpu_plus_elasped_time
def load_file(conf):
    '''
    Main function to initiate file loader
    '''
    # log for start the file loader
    # print("I am the file loader, about to load file %s" % extract_file_name(conf[mk.FILE_TO_LOAD]))

    # connect to database
    conn, engine = connect_db(DBDRIVER, conf[mk.TARGET_DB_USER], conf[mk.TARGET_DB_PASSWORD],
                              conf[mk.TARGET_DB_HOST], conf[mk.TARGET_DB_PORT], conf[mk.TARGET_DB_NAME])

    # check staging tables
    check_setup(conf[mk.TARGET_DB_TABLE], engine, conn)

    # start loading file process
    time_for_load_as_seconds = load_data_process(conn, conf)

    # close db connection
    conn.close()

    # log for end the file loader
    # print("I am the file loader, loaded file %s in %.3f seconds" % (extract_file_name(conf[mk.FILE_TO_LOAD]), time_for_load_as_seconds))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='source_csv', required=True, help="path to the source file")
    parser.add_argument('-m', dest='header_csv', required=True, help="path to the header file")
    args = parser.parse_args()

    conf = {
            'csv_file': args.source_csv,
            'header_file': args.header_csv,
            'csv_table': 'csv_table_for_file_loader',
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'udl2',
            'db_name': 'udl2',
            'db_password': 'udl2abc1234',
            'csv_schema': 'udl2',
            'fdw_server': 'udl2_fdw_server',
            'staging_schema': 'udl2',
            'staging_table': 'STG_SBAC_ASMT_OUTCOME',
            'apply_rules': False,
            'start_seq': 10,
            'batch_id': 100
    }
    start_time = datetime.datetime.now()
    load_file(conf)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time --", spend_time)
