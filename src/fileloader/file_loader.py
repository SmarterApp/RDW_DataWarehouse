import datetime
import csv
import fileloader.prepare_queries as queries
import random
from udl2.database import UDL_TABLE_METADATA
from udl2.field_mapper import field_mapper_dict
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.engine import create_engine


DBDRIVER = "postgresql+pypostgresql"

# temporary assumption: extra columns in staging tables, but not in csv file
extra_header_names = ['src_row_number', 'row_rec_id']
extra_header_types = ['bigint', 'serial primary key']


def get_db_conf():
    '''
    Get database conf parameters in configuration file
    '''
    # TODO: need to get conf options from conf file
    return conf


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
    # TODO:might add checking if fdw is defined or not


def set_fdw(conn, conf):
    '''
    Function to set fdw, including extension, server and functions
    '''
    # reference: http://www.postgresql.org/docs/9.2/static/file-fdw.html
    try:
        # set fdw extension
        conn.execute(queries.create_fdw_extension_query(conf['csv_schema']))

        # set fdw server
        conn.execute(queries.create_fdw_server_query(conf['fdw_server']))

        # run functions. read from .sql file
        statement = open("transformation_rules.sql").read()
        # print(statement.strip())
        conn.execute(statement)

    except Exception as e:
        print('Exception -- ', e)
        # conn.rollback()


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
    # This is to create one fake staging table
    # add extra columns in header
    header_names_copy = header_names[:]
    header_types_copy = header_types[:]
    header_names_copy.extend(extra_header_names)
    header_types_copy.extend(extra_header_types)

    create_staging_table = queries.create_staging_tables_query(header_types_copy, header_names_copy, csv_file, staging_schema, staging_table)
    # drop_staging_table = queries.drop_staging_tables_query(staging_schema, staging_table)
    # print(create_staging_table)
    execute_queries(conn, [create_staging_table], 'Exception in getting staging table -- ')
    """

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
    # hard-code for test:
    import_via_fdw(conn, stg_asmt_outcome_columns, conf['batch_id'], conf['apply_rules'], csv_table_columns, header_types, conf['staging_schema'], conf['staging_table'], conf['csv_schema'], conf['csv_table'], conf['start_seq'])
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)
    print("\nSpend time for loading file %s (seconds) -- %f" % (conf['csv_file'], time_as_seconds))

    # drop FDW table
    drop_fdw_tables(conn, conf['csv_schema'], conf['csv_table'])

    return spend_time


def load_file(conf):
    '''
    Main function to initiate file loader
    '''

    # connect to database
    conn, engine = connect_db(conf)

    # check staging tables
    check_setup(conf['staging_table'], engine, conn)

    # start loading file process
    time_for_load = load_data_process(conn, conf)

    # close db connection
    conn.close()

"""
if __name__ == '__main__':
    conf = {
            'csv_file': '/Users/lichen/Documents/Edware/sandboxes/ejen/US14726/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-realdata.csv',
            'metadata_file': '/Users/lichen/Documents/Edware/sandboxes/ejen/US14726/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-metadata.csv',
            'csv_table': 'UDL_test_data_block_of_100_records_with_datatype_errors_v3',

            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'abrien',
            'db_name': 'fdw_test',
            'db_password': '',
            'csv_schema': 'public',
            'fdw_server': 'udl_import',
            'staging_schema': 'public',
            'staging_table': 'tmp',
            'apply_rules': False,
            'start_seq': 10,
            'batch_id': 100
    }
    start_time = datetime.datetime.now()
    load_file(conf)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time --", spend_time)
"""
