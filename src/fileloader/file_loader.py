import datetime
import csv
import fileloader.prepare_queries as queries
import random
import argparse
from udl2.database import UDL_TABLE_METADATA
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.engine import create_engine
from udl2_util.file_util import extract_file_name


DBDRIVER = "postgresql+pypostgresql"


def connect_db(conf_args):
    '''
    Connect to database via sqlalchemy
    '''

    # TODO:define conf_args content
    db_string = DBDRIVER + '://{db_user}:{db_password}@{db_host}/{db_name}'.format(**conf_args)
    # print(db_string)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    return db_connection, engine


def check_setup(staging_table, engine, conn):
    # check if staging table is defined or not
    if not engine.dialect.has_table(conn, staging_table):
        print("There is no staging table -- ", staging_table)
        raise NoSuchTableError


def extract_csv_header(csv_file):
    '''
    Extract header names and types from input csv file
    '''
    with open(csv_file) as csv_obj:
        reader = csv.reader(csv_obj)
        header_names = next(reader)
        header_types = ['text'] * len(header_names)
    formatted_header_names = [canonicalize_header_field(name) for name in header_names]
    # print("formatter header names -- ", formatted_header_names)
    # print("header types           -- ", header_types)

    return formatted_header_names, header_types


def canonicalize_header_field(field_name):
    '''
    Canonicalize input field_name
    '''
    # TODO: rules TBD
    return field_name.replace('-', '_').replace(' ', '_').replace('#', '')


def create_fdw_tables(conn, header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    create_csv_ddl = queries.create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server)
    drop_csv_ddl = queries.drop_ddl_csv_query(csv_schema, csv_table)
#     print(create_csv_ddl)
    execute_queries(conn, [drop_csv_ddl, create_csv_ddl], 'Exception in creating fdw tables --')


def execute_queries(conn, list_of_queries, except_msg):
    trans = conn.begin()
    # execute queries
    try:
        for query in list_of_queries:
            conn.execute(query)
        trans.commit()
    except Exception as e:
        print(except_msg, e)
        trans.rollback()


def get_fields_map(conn, header_names, header_types, batch_id, csv_file, staging_schema, staging_table):

    """
    Getting field mapper, which maps the column in staging table, and columns in csv table
    """
    # pick the columns from the 2nd to the last 2nd
    stg_asmt_outcome_columns = [column_info[0] for column_info in UDL_TABLE_METADATA['STG_SBAC_ASMT_OUTCOME']['columns'][1:-1]]
    # map first column in staging table to batch_id, map second column in staging table to the expression of using sequence
    csv_table_columns = header_names[:]
    csv_table_columns.insert(0, str(batch_id))
    csv_table_columns.insert(1, 'nextval(\'{seq_name}\')')
    return stg_asmt_outcome_columns, csv_table_columns


def import_via_fdw(conn, stg_asmt_outcome_columns, batch_id, apply_rules, csv_table_columns, header_types, staging_schema, staging_table, csv_schema, csv_table, start_seq):
    # create sequence name, use table_name and a random number combination
    seq_name = csv_table + '_' + str(random.choice(range(1, 10)))
    create_sequence = queries.create_sequence_query(staging_schema, seq_name, start_seq)
    insert_into_staging_table = queries.create_inserting_into_staging_query(stg_asmt_outcome_columns, batch_id, apply_rules, csv_table_columns, header_types, staging_schema, staging_table, csv_schema, csv_table, start_seq, seq_name)
    drop_sequence = queries.drop_sequence_query(staging_schema, seq_name)
    # print('@@@@@@@', create_sequence)
    execute_queries(conn, [create_sequence, insert_into_staging_table, drop_sequence], 'Exception in loading data -- ')


def drop_fdw_tables(conn, csv_schema, csv_table):
    drop_csv_ddl = queries.drop_ddl_csv_query(csv_schema, csv_table)
    execute_queries(conn, [drop_csv_ddl], 'Exception in drop fdw table -- ')


def load_data_process(conn, conf):
    # read headers from header_file
    header_names, header_types = extract_csv_header(conf['header_file'])

    # create FDW table
    create_fdw_tables(conn, header_names, header_types, conf['csv_file'], conf['csv_schema'], conf['csv_table'], conf['fdw_server'])

    # get field map
    stg_asmt_outcome_columns, csv_table_columns = get_fields_map(conn, header_names, header_types, conf['batch_id'], conf['csv_file'], conf['staging_schema'], conf['staging_table'])

    # load the data from FDW table to staging table
    start_time = datetime.datetime.now()
    import_via_fdw(conn, stg_asmt_outcome_columns, conf['batch_id'], conf['apply_rules'], csv_table_columns, header_types, conf['staging_schema'], conf['staging_table'], conf['csv_schema'], conf['csv_table'], conf['start_seq'])
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)

    # drop FDW table
    drop_fdw_tables(conn, conf['csv_schema'], conf['csv_table'])

    return time_as_seconds


def load_file(conf):
    '''
    Main function to initiate file loader
    '''
    # log for start the file loader
    print("I am the file loader, about to load file %s" % extract_file_name(conf['csv_file']))

    # connect to database
    conn, engine = connect_db(conf)

    # check staging tables
    check_setup(conf['staging_table'], engine, conn)

    # start loading file process
    time_for_load_as_seconds = load_data_process(conn, conf)

    # close db connection
    conn.close()

    # log for end the file loader
    print("I am the file loader, loaded file %s in %f seconds" % (extract_file_name(conf['csv_file']), time_for_load_as_seconds))

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
            'fdw_server': 'udl_import',
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
