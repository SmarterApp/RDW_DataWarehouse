import csv
import psycopg2
import os
import datetime


def connect_db(db_host, db_port, db_name, db_user, db_password):
    conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (db_name, db_user, db_password, db_host, db_port))
    return conn


def set_fdw_extension(conn, csv_schema='public'):
    set_fdw_extension_sql = "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA %s" % csv_schema
    cursor = conn.cursor()
    cursor.execute(set_fdw_extension_sql)
    conn.commit()
    cursor.close()


def set_fdw_server(conn, fdw_server):
    try:
        set_fdw_server_sql = "CREATE SERVER %s FOREIGN DATA WRAPPER file_fdw" % fdw_server
        cursor = conn.cursor()
        cursor.execute(set_fdw_server_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()


def load_data_process(need_type, conn, apply_rules, csv_file, metadata_file, csv_schema, csv_table, fdw_server, staging_schema, staging_table):
    header_names, formatted_header_names, header_types = extract_csv_header2(metadata_file)
    # print('header names in csv file              -- ', header_names)
    # print('header names in staging and FDW table -- ', formatted_header_names)
    # print('header types in csv file              -- ', header_types)
    assert(len(header_names) == len(formatted_header_names) and len(formatted_header_names) == len(header_types))
#     # get the required type of all columns
#     if need_type:
#         # TODO: write a function to get column types
#         # For now, use as 'text' for all columns
#         header_types = ['text' for _i in range(len(header_names))]
#     else:
#         header_types = ['text' for _i in range(len(header_names))]

    # create FDW
    create_csv_ddl = generate_create_ddl_csv(header_types, formatted_header_names, csv_file, csv_schema, csv_table, fdw_server)
    drop_csv_ddl = generate_drop_ddl_csv(csv_schema, csv_table)
    define_table(conn, csv_schema, drop_csv_ddl, create_csv_ddl)

    # create staging table
    create_staging_table = generate_create_staging_table(header_types, formatted_header_names, csv_file, staging_schema, staging_table)
    drop_staging_table = generate_drop_staging_table(staging_schema, staging_table)
    define_table(conn, staging_schema, drop_staging_table, create_staging_table)

    # do transform and import
    start_time = datetime.datetime.now()
    import_via_fdw(conn, apply_rules, header_types, formatted_header_names, staging_schema, staging_table, csv_file, csv_schema, csv_table)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time for loading file --", spend_time)
    return spend_time


def canonicalize_header_field(field_name):
    return field_name.replace('-', '_').replace(' ', '_').replace('#', '')


def extract_csv_header(csv_file):
    '''
    This method returns two lists
    First list  : header_names contains all header names in the input csv_file
    Second list : formatted_header_names contains all header names which will be used in FDW and staging table
    '''
    header_names = []
    header_types = []
    with open(csv_file) as csv_obj:
        reader = csv.reader(csv_obj)
        header_names = next(reader)
        # header_types = next(reader)
        header_types = ['text'] * len(header_names)
    # same role as fields mapping?
    formatted_header_names = [canonicalize_header_field(name) for name in header_names]
    return header_names, formatted_header_names, header_types


def extract_csv_header2(metadata_file):
    '''
    This method returns two lists
    First list  : header_names contains all header names in the input metadata_file
    Second list : formatted_header_names contains all header names which will be used in FDW and staging table
    '''
    header_names = []
    header_types = []
    with open(metadata_file) as csv_obj:
        reader = csv.reader(csv_obj)
        next(reader)
        for row in reader:
            header_names.append(row[0])
            header_types.append(row[1])
    # same role as fields mapping?
    formatted_header_names = [canonicalize_header_field(name) for name in header_names]
    return header_names, formatted_header_names, header_types


def generate_drop_ddl_csv(csv_schema, csv_table_with_type_errors):
    ddl = "DROP FOREIGN TABLE IF EXISTS %s.%s " % (csv_schema, csv_table_with_type_errors)
    return ddl


def generate_drop_staging_table(csv_schema, csv_table_with_type_errors):
    ddl = "DROP TABLE IF EXISTS %s.%s " % (csv_schema, csv_table_with_type_errors)
    return ddl


def generate_create_staging_table(header_types, formatted_header_names, csv_file_with_type_errors, csv_schema, csv_table_with_type_errors):
    ddl_parts = ["CREATE TABLE IF NOT EXISTS %s.%s ( " % (csv_schema, csv_table_with_type_errors) ,
                 ','.join([formatted_header_names[i] + ' ' + header_types[i] + ' ' for i in range(len(formatted_header_names))]),
                 ") "]
    return "".join(ddl_parts)


def generate_create_ddl_csv(header_types, formatted_header_names, csv_file_with_type_errors, csv_schema, csv_table_with_type_errors, fdw_server):
    ddl_parts = ["CREATE FOREIGN TABLE IF NOT EXISTS %s.%s ( " % (csv_schema, csv_table_with_type_errors) ,
                 ','.join([formatted_header_names[i] + ' ' + header_types[i] + ' ' for i in range(len(formatted_header_names))]),
                 ") SERVER %s " % fdw_server ,
                 "OPTIONS (filename '%s', format '%s', header '%s')" % (csv_file_with_type_errors, 'csv', 'true')]
    ddl_parts = "".join(ddl_parts)
    return ddl_parts


def define_table(conn, schema, drop_ddl, create_ddl):
    # print('\ndefine table -- ')
    try:
        cursor = conn.cursor()
        # print(drop_ddl)
        # print(create_ddl)
        cursor.execute(drop_ddl)
        cursor.execute(create_ddl)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()


def apply_transformation_rules(apply_rules, header_types, header_names):
    '''
    The function apply the some transformation rules
    '''
    header_with_rules = []
    for i in range(len(header_names)):
        header_name = header_names[i]

        if apply_rules.lower() == 'true':
            header_type = header_types[i]
            # test for function map_gender. Hard code as a temporary solution
            if header_name.lower() in ['gender_1', 'gender_2', 'gender_3', 'gender_4']:
                header_name = 'map_gender(' + header_name + ')'
                # test for function map_yn. Hard code as a temporary solution
            elif header_name.lower() in ['y_or_n_1', 'y_or_n_2', 'y_or_n_3', 'y_or_n_4']:
                header_name = 'map_yn(' + header_name + ')'
            elif header_type.lower() == 'text':
                header_name = "trim(replace(upper(" + header_name + "), CHR(13), ''))"

        if i < len(header_names) - 1:
            header_name += ', '
        header_with_rules.append(header_name)
    return header_with_rules


def create_sql_functions(conn):
    # print('\ncreating functions --')
    try:
        cursor = conn.cursor()
        statement = open("transformation_rules.sql").read()
        cursor.execute(statement)
        conn.commit()
    except Exception as e:
        print('Exception -- ', e)
        conn.rollback()
    finally:
        cursor.close()


def import_via_fdw(conn, apply_rules, header_types, formatted_header_names, pre_staging_schema, pre_staging_table, csv_file_with_type_errors, csv_schema, csv_table_with_type_errors):
    # print('\nimport data from FDW into staging table --')
    trim_column_names = apply_transformation_rules(apply_rules, header_types, formatted_header_names)
    insert_sql = ["insert into %s.%s (select " % (pre_staging_schema, pre_staging_table) ,
                  "".join([ i for i in trim_column_names]),
                  " from %s.%s)" % (csv_schema, csv_table_with_type_errors),
                  ]
    insert_sql = "".join(insert_sql)

    try:
        # print(insert_sql)
        cursor = conn.cursor()
        cursor.execute(insert_sql)
        conn.commit()
    except Exception as e:
        print('Exception -- ', e)
        conn.rollback()
    finally:
        cursor.close()


def test_import(conf):
    conn = connect_db(conf['db_host'], conf['db_port'], conf['db_name'], conf['db_user'], conf['db_password'])

    set_fdw_extension(conn)
    set_fdw_server(conn, conf['fdw_server'])

    # create functions (e.g. transformation rules)
    create_sql_functions(conn)

    time_for_load = load_data_process(False, conn, conf['apply_transformation_rules'], conf['csv_file'], conf['metadata_file'], conf['csv_schema'], conf['csv_table'], conf['fdw_server'], conf['staging_schema'], conf['staging_table'])

    conn.close()

    return time_for_load

if __name__ == '__main__':
    conf = {
            'csv_file': os.getcwd() + '/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-realdata.csv',
            'metadata_file': os.getcwd() + '/UDL-test-data-Block-of-100-records-WITHOUT-datatype-errors-v3-metadata.csv',
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
    test_import(conf)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time --", spend_time)
