

def create_fdw_extension_query(csv_schema):
    return "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA {csv_schema}".format(csv_schema=csv_schema)


def create_fdw_server_query(fdw_server):
    return "CREATE SERVER {fdw_server} FOREIGN DATA WRAPPER file_fdw".format(fdw_server=fdw_server)


def create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server):
    # bug, when csv_file name is longer than 63 chars, it causes foreign data wrapper fails to create mapping.
    ddl_parts = ['CREATE FOREIGN TABLE IF NOT EXISTS "{csv_schema}"."{csv_table}" (',
                 ', '.join([header_names[i] + ' ' + header_types[i] for i in range(len(header_names))]),
                 ") SERVER {fdw_server} ",
                 "OPTIONS (filename '{csv_file}', format 'csv', header 'false')"]
    ddl_parts = "".join(ddl_parts).format(csv_schema=csv_schema, csv_table=csv_table, fdw_server=fdw_server, csv_file=csv_file)
    # print(ddl_parts)
    return ddl_parts


def drop_ddl_csv_query(csv_schema, csv_table):
    ddl = 'DROP FOREIGN TABLE IF EXISTS "{csv_schema}"."{csv_table}"'.format(csv_schema=csv_schema, csv_table=csv_table)
    return ddl


def drop_staging_tables_query(csv_schema, csv_table):
    ddl = 'DROP TABLE IF EXISTS "{csv_schema}"."{csv_table}"'.format(csv_schema=csv_schema, csv_table=csv_table)
    return ddl


def create_inserting_into_staging_query(stg_asmt_outcome_columns, apply_rules, csv_table_columns, staging_schema,
                                        staging_table, csv_schema, csv_table, seq_name, transformation_rules):
    column_names_with_proc = apply_transformation_rules(apply_rules, csv_table_columns, transformation_rules)
    insert_sql = ['INSERT INTO "{staging_schema}"."{staging_table}"(',
                  ', '.join(stg_asmt_outcome_columns),
                  ') SELECT ',
                  ', '.join(column_names_with_proc),
                  ' FROM "{csv_schema}"."{csv_table}"',
                  ]
    # note: seq_name is used in the expression of column record_sid in stg_asmt_outcome_columns
    insert_sql = "".join(insert_sql).format(seq_name=seq_name, staging_schema=staging_schema, staging_table=staging_table,
                                            csv_schema=csv_schema, csv_table=csv_table)
    return insert_sql


def set_sequence_query(staging_table, start_seq):
    return "SELECT pg_catalog.setval(pg_get_serial_sequence('{staging_table}', 'src_row_number'), {start_seq}, false)".format(staging_table=staging_table,
                                                                                                                              start_seq=start_seq)


def create_sequence_query(staging_schema, seq_name, start_seq):
    return 'CREATE SEQUENCE "{staging_schema}"."{seq_name}" START {start_seq}'.format(staging_schema=staging_schema,
                                                                                      seq_name=seq_name,
                                                                                      start_seq=start_seq)


def drop_sequence_query(staging_schema, seq_name):
    return 'DROP SEQUENCE "{staging_schema}"."{seq_name}"'.format(staging_schema=staging_schema,
                                                                  seq_name=seq_name)


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
    return 'SELECT source_column, target_column, stored_proc_name FROM "{staging_schema}"."{ref_table}" WHERE source_table=\'{source_table}\''.format(staging_schema=staging_schema,
                                                                                                                                                      ref_table=ref_table,
                                                                                                                                                      source_table=source_table)