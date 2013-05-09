import datetime
import csv
import prepare_queries as queries
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.engine import create_engine


DBDRIVER = "postgresql+pypostgresql"

# temporary assumption: extra columns in staging tables, but not in csv file
extra_header_names = ['src_row_number', 'row_rec_id']
extra_header_types = ['text', 'serial primary key']


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
    print(db_string)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    return db_connection, engine


def check_setup(staging_table, engine, conn):
    # check if staging table is defined or not
    if not engine.dialect.has_table(conn, staging_table):
        print("There is no staging table -- ", staging_table)
        raise NoSuchTableError
    # TODO:check if fdw is defined or not


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
    # execute queries
    try:
        conn.execute(drop_csv_ddl)
        conn.execute(create_csv_ddl)
    except Exception as e:
        print('Exception in creating fdw tables --', e)
        # add rollback here


def get_staging_tables(conn, header_names, header_types, csv_file, staging_schema, staging_table):
    # can be replaced by get staging definition from other place
    # add extra columns in header
    header_names_copy = header_names[:]
    header_types_copy = header_types[:]
    header_names_copy.extend(extra_header_names)
    header_types_copy.extend(extra_header_types)

    create_staging_table = queries.create_staging_tables_query(header_types_copy, header_names_copy, csv_file, staging_schema, staging_table)
    drop_staging_table = queries.drop_staging_tables_query(staging_schema, staging_table)
    print(create_staging_table)
    # execute queries
    try:
        # conn.execute(drop_staging_table)
        conn.execute(create_staging_table)
    except Exception as e:
        print('Exception in getting staging table--', e)
        # add rollback here


def import_via_fdw(conn, apply_rules, header_names, header_types, staging_schema, staging_table, csv_schema, csv_table, start_seq):
    insert_into_staging_table = queries.create_inserting_into_staging_query(apply_rules, header_names, header_types, staging_schema, staging_table, csv_schema, csv_table, start_seq)
    print('@@@@@@@', insert_into_staging_table)
    try:
        conn.execute(insert_into_staging_table)
    except Exception as e:
        print('Exception -- ', e)
        # conn.rollback()


def load_data_process(conn, conf):
    # TODO: need to change if the header is not in the csv_file
    header_names, header_types = extract_csv_header(conf['csv_file'])

    # create FDW table
    # prepare queries
    create_fdw_tables(conn, header_names, header_types, conf['csv_file'], conf['csv_schema'], conf['csv_table'], conf['fdw_server'])

    # get staging tables
    # TODO: need to define the approach to get the staging table definition.
    # temporary: hard code to create one if not here
    get_staging_tables(conn, header_names, header_types, conf['csv_file'], conf['staging_schema'], conf['staging_table'])

    # do transform and import
    start_time = datetime.datetime.now()
    import_via_fdw(conn, conf['apply_rules'], header_names, header_types, conf['staging_schema'], conf['staging_table'], conf['csv_schema'], conf['csv_table'], conf['start_seq'])
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)
    print("\nSpend time for loading file(seconds) --", time_as_seconds)
    return spend_time


def load_file(conf):
    '''
    Main function to initiate file loader
    '''

    # connect to database
    conn, engine = connect_db(conf)

    # check staging tables
    # Note: currently, we do not have staging table defined.
    # If we want to run this script without staging table defined at first,
    # please comment out the following line.
    # in method load_data_process(), then in get_staging_tables(), it will create staging table as a temporary solution
    # check_setup(conf['staging_table'], engine, conn)
    # start loading file process
    time_for_load = load_data_process(conn, conf)
    print("Time for load file", time_for_load)

    # close db connection
    conn.close()

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
            'start_seq': 20
    }
    start_time = datetime.datetime.now()
    load_file(conf)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time --", spend_time)
