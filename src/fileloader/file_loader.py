import datetime
import os
import csv
import prepare_queries as queries
from sqlalchemy.engine import create_engine
from sqlalchemy import Table, Column, Index
from sqlalchemy.schema import MetaData


DBDRIVER = "postgresql+pypostgresql"


def get_db_conf():
    '''
    Get database conf parameters in configuration file
    '''
    # TODO: need to get conf options from conf file
    conf = {
            'csv_file': '/Users/lichen/Documents/Edware/sandboxes/ejen/US14726/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-realdata.csv',
            'metadata_file': '/Users/lichen/Documents/Edware/sandboxes/ejen/US14726/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-metadata.csv',
            'csv_table': 'UDL_test_data_block_of_100_records_with_datatype_errors_v1',
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'postgres',
            'db_name': 'fdw_test',
            'db_password': '3423346',
            'csv_schema': 'public',
            'fdw_server': 'udl_import',
            'staging_schema': 'public',
            'staging_table': 'tmp'
    }
    return conf


def connect_db(conf_args=get_db_conf()):
    '''
    Connect to database via sqlalchemy
    '''
    # TODO:define conf_args content
    db_string = DBDRIVER + '://{db_user}:{db_password}@{db_host}/{db_name}'.format(**conf_args)
    print('*********', db_string)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    return db_connection, engine


def check_setup(staging_table, engine, conn):
    # check if staging table is defined or not
    if not engine.dialect.has_table(conn, staging_table):
        return False
    # TODO:check if fdw is defined or not
    return True


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
        conn.text(statement)

    except Exception as e:
        print('Exception -- ', e)
        conn.rollback()


def extract_csv_header(csv_file):
    '''
    Extract header names and types from input csv file
    '''
    with open(csv_file) as csv_obj:
        reader = csv.reader(csv_obj)
        header_names = next(reader)
        header_types = ['text'] * len(header_names)
    # same role as fields mapping?
    formatted_header_names = [canonicalize_header_field(name) for name in header_names]
    print("formatter header names -- ", formatted_header_names)
    print("header types           -- ", header_types)
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
    except:
        print()


def get_staging_tables(conn):
    # can be replaced by get staging definition from other place
    create_staging_table = queries.create_staging_tables_query()
    drop_staging_table = queries.drop_staging_tables_query()
    # execute queries
    conn.execute(drop_staging_table)
    conn.execute(create_staging_table)


def import_via_fdw(conn, apply_rules, header_types, formatted_header_names, pre_staging_schema, pre_staging_table, csv_file_with_type_errors, csv_schema, csv_table_with_type_errors):
    insert_into_staging_table = queries.create_inserting_into_staging_query()
    try:
        conn.execute(insert_into_staging_table)
    except Exception as e:
        print('Exception -- ', e)
        conn.rollback()


def load_data_process(conn, conf):
    header_names, header_types = extract_csv_header(conf['csv_file'])

    # create FDW table
    # prepare queries
    create_fdw_tables(conn, header_names, header_types, conf['csv_file'], conf['csv_schema'], conf['csv_table'], conf['fdw_server'])
    return
    # get staging tables
    # TODO:need to define the approach to get the staging table definition
    staging_table = get_staging_tables()

    # do transform and import
    start_time = datetime.datetime.now()
    import_via_fdw(staging_table)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time for loading file --", spend_time)
    return spend_time


def load_file(conf):
    '''
    Main function to initiate file loader
    '''

    # connect to database
    conn, engine = connect_db()

    # check staging tables
    valid_setup = check_setup(conf['staging_table'], engine, conn)

    if valid_setup:
        # start loading file process
        time_for_load = load_data_process(conn, conf)
    else:
        # error handle
        print('error in setup')

    # close db connection
    conn.close()

    # records the time
    return time_for_load


if __name__ == '__main__':
    conf = {
            'csv_file': '/Users/lichen/Documents/Edware/sandboxes/ejen/US14726/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-realdata.csv',
            'metadata_file': '/Users/lichen/Documents/Edware/sandboxes/ejen/US14726/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-metadata.csv',
            'csv_table': 'UDL_test_data_block_of_100_records_with_datatype_errors_v1',
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'postgres',
            'db_name': 'fdw_test',
            'db_password': '3423346',
            'csv_schema': 'public',
            'fdw_server': 'udl_import',
            'staging_schema': 'public',
            'staging_table': 'tmp'
    }
    start_time = datetime.datetime.now()
    load_file(conf)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time --", spend_time)
