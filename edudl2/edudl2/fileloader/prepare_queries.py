from edudl2.udl2_util.database_util import create_filtered_sql_string


def create_fdw_extension_query(csv_schema):
    return create_filtered_sql_string("CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA {csv_schema}",
                                      csv_schema=csv_schema)


def create_fdw_server_query(fdw_server):
    return create_filtered_sql_string("CREATE SERVER {fdw_server} FOREIGN DATA WRAPPER file_fdw",
                                      fdw_server=fdw_server)


def create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    # bug, when csv_file name is longer than 63 chars, it causes foreign data wrapper fails to create mapping.
    ddl_parts = ['CREATE FOREIGN TABLE IF NOT EXISTS "{csv_schema}"."{csv_table}" (',
                 ', '.join([header_names[i] + ' ' + header_types[i] for i in range(len(header_names))]),
                 ") SERVER {fdw_server} ",
                 "OPTIONS (filename '{csv_file}', format 'csv', header 'false')"]
    return create_filtered_sql_string("".join(ddl_parts),
                                      csv_schema=csv_schema, csv_table=csv_table, fdw_server=fdw_server, csv_file=csv_file)


def drop_ddl_csv_query(csv_schema, csv_table):
    return create_filtered_sql_string('DROP FOREIGN TABLE IF EXISTS "{csv_schema}"."{csv_table}"',
                                      csv_schema=csv_schema, csv_table=csv_table)


def drop_staging_tables_query(csv_schema, csv_table):
    return create_filtered_sql_string('DROP TABLE IF EXISTS "{csv_schema}"."{csv_table}"',
                                      csv_schema=csv_schema, csv_table=csv_table)


def create_inserting_into_staging_query(stg_asmt_outcome_columns, apply_rules, csv_table_columns, staging_schema,
                                        staging_table, csv_schema, csv_table, seq_name, transformation_rules):
    column_names_with_proc = apply_transformation_rules(apply_rules, csv_table_columns, transformation_rules)
    # TODO: This needs to be changed to SQLAlchemy query
    insert_sql = ['INSERT INTO "{staging_schema}"."{staging_table}"(',
                  ', '.join(stg_asmt_outcome_columns),
                  ') SELECT ',
                  ', '.join(column_names_with_proc),
                  ' FROM "{csv_schema}"."{csv_table}"',
                  ]
    # note: seq_name is used in the expression of column record_sid in stg_asmt_outcome_columns
    return create_filtered_sql_string("".join(insert_sql),
                                      seq_name=seq_name, staging_schema=staging_schema, staging_table=staging_table,
                                      csv_schema=csv_schema, csv_table=csv_table)


def set_sequence_query(staging_table, start_seq):
    return create_filtered_sql_string("SELECT pg_catalog.setval(pg_get_serial_sequence('{staging_table}', 'src_row_number'), {start_seq}, false)",
                                      staging_table=staging_table, start_seq=start_seq)


def create_sequence_query(staging_schema, seq_name, start_seq):
    return create_filtered_sql_string('CREATE SEQUENCE "{staging_schema}"."{seq_name}" START {start_seq}',
                                      staging_schema=staging_schema, seq_name=seq_name, start_seq=start_seq)


def drop_sequence_query(staging_schema, seq_name):
    return create_filtered_sql_string('DROP SEQUENCE "{staging_schema}"."{seq_name}"',
                                      staging_schema=staging_schema, seq_name=seq_name)


def apply_transformation_rules(apply_rules, csv_table_columns, transformation_rules):
    '''
    The function apply the some transformation rules
    '''
    header_with_rules = []
    for i in range(len(csv_table_columns)):
        header_name = csv_table_columns[i]
        rule = transformation_rules[i]
        column_with_rule = header_name
        if apply_rules:
            if rule is not None and rule != '':
                column_with_rule = ''.join([rule, '(', header_name, ')'])
        header_with_rules.append(column_with_rule)
    return header_with_rules


def get_column_mapping_query(staging_schema, ref_table, source_table):
    # TODO: This needs to be changed to SQLAlchemy query
    return create_filtered_sql_string('SELECT source_column, target_column, stored_proc_name FROM "{staging_schema}"."{ref_table}" WHERE source_table=\'{source_table}\'',
                                      staging_schema=staging_schema, ref_table=ref_table, source_table=source_table)
