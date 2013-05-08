

def create_fdw_extension_query(csv_schema):
    return "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA {csv_schema}".format(csv_schema=csv_schema)


def create_fdw_server_query(fdw_server):
    return "CREATE SERVER {fdw_server} FOREIGN DATA WRAPPER file_fdw".format(fdw_server=fdw_server)


def create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    # TODO: if the csv_file does not have header row, need to set header = false in the OPTINOS
    ddl_parts = ["CREATE FOREIGN TABLE IF NOT EXISTS %s.%s ( " % (csv_schema, csv_table),
                 ','.join([header_names[i] + ' ' + header_types[i] + ' ' for i in range(len(header_names))]),
                 ") SERVER %s " % fdw_server,
                 "OPTIONS (filename '%s', format '%s', header '%s')" % (csv_file, 'csv', 'true')]
    ddl_parts = "".join(ddl_parts)
    return ddl_parts


def drop_ddl_csv_query(csv_schema, csv_table):
    ddl = "DROP FOREIGN TABLE IF EXISTS {csv_schema}.{csv_table} ".format(csv_schema=csv_schema, csv_table=csv_table)
    return ddl


def create_staging_tables_query(header_types, header_names, csv_file, csv_schema, csv_table):
    # TODO: need to be replaced by importing from staging table definition
    ddl_parts = ["CREATE TABLE IF NOT EXISTS %s.%s ( " % (csv_schema, csv_table),
                 ','.join([header_names[i] + ' ' + header_types[i] + ' ' for i in range(len(header_names))]),
                 ") "]
    return "".join(ddl_parts)


def drop_staging_tables_query(csv_schema, csv_table):
    ddl = "DROP TABLE IF EXISTS {csv_schema}.{csv_table}".format(csv_schema=csv_schema, csv_table=csv_table)
    return ddl


def create_inserting_into_staging_query(apply_rules, header_names, header_types, staging_schema, staging_table, csv_schema, csv_table):
    trim_column_names = apply_transformation_rules(apply_rules, header_types, header_names)
    insert_sql = ["insert into %s.%s (select " % (staging_schema, staging_table),
                  "".join([i for i in trim_column_names]),
                  " from %s.%s)" % (csv_schema, csv_table),
                  ]
    insert_sql = "".join(insert_sql)
    return insert_sql


def set_sequence_query(staging_table, start_seq):
    return "SELECT pg_catalog.setval(pg_get_serial_sequence('{staging_table}', 'src_row_number'), {start_seq}, false)".format(staging_table=staging_table, start_seq=start_seq)


def apply_transformation_rules(apply_rules, header_types, header_names):
    '''
    The function apply the some transformation rules
    '''
    header_with_rules = []
    for i in range(len(header_names)):
        header_name = header_names[i]

        if apply_rules:
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
