

def create_fdw_extension_query(csv_schema):
    return "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA {csv_schema}".format(csv_schema=csv_schema)


def create_fdw_server_query(fdw_server):
    return "CREATE SERVER {fdw_server} FOREIGN DATA WRAPPER file_fdw".format(fdw_server=fdw_server)


def create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    ddl_parts = ["CREATE FOREIGN TABLE IF NOT EXISTS %s.%s ( " % (csv_schema, csv_table),
                 ','.join([header_names[i] + ' ' + header_types[i] + ' ' for i in range(len(header_names))]),
                 ") SERVER %s " % fdw_server,
                 "OPTIONS (filename '%s', format '%s', header '%s')" % (csv_file, 'csv', 'true')]
    ddl_parts = "".join(ddl_parts)
    return ddl_parts


def drop_ddl_csv_query(csv_schema, csv_table):
    ddl = "DROP FOREIGN TABLE IF EXISTS {csv_schema}.{csv_table} ".format(csv_schema=csv_schema, csv_table=csv_table)
    return ddl


def create_staging_tables_query(header_types, formatted_header_names, csv_file_with_type_errors, csv_schema, csv_table_with_type_errors):
    # TODO: need to be replaced by importing from staging table definition
    ddl_parts = ["CREATE TABLE IF NOT EXISTS %s.%s ( " % (csv_schema, csv_table_with_type_errors),
                 ','.join([formatted_header_names[i] + ' ' + header_types[i] + ' ' for i in range(len(formatted_header_names))]),
                 ") "]
    return "".join(ddl_parts)


def drop_staging_tables_query(csv_schema, csv_table_with_type_errors):
    ddl = "DROP TABLE IF EXISTS {csv_schema}.{csv_table_with_type_errors}".format(csv_schema=csv_schema, csv_table_with_type_errors=csv_table_with_type_errors)
    return ddl


def create_inserting_into_staging_query(conn):
    trim_column_names = apply_transformation_rules(apply_rules, header_types, formatted_header_names)
    insert_sql = ["insert into %s.%s (select " % (pre_staging_schema, pre_staging_table) ,
                  "".join([ i for i in trim_column_names]),
                  " from %s.%s)" % (csv_schema, csv_table_with_type_errors),
                  ]
    insert_sql = "".join(insert_sql)
    return insert_sql
