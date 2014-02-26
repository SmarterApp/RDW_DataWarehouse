import re
from edudl2.udl2 import message_keys as mk


def select_distinct_asmt_guid_query(schema_name, table_name, column_name, guid_batch):
    '''
    Create query to find distict asmt_guid for a given batch in source table
    @schema_name:
    @table_name:
    @column_name:
    @guid_batch
    '''
    sql_template = "SELECT DISTINCT {guid_column_name_in_source} " + \
                   "FROM {source_schema_and_table} " + \
                   "WHERE guid_batch=\'{guid_batch}\'"
    return sql_template.format(guid_column_name_in_source=column_name,
                               source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                               guid_batch=guid_batch)


def select_distinct_asmt_rec_id_query(schema_name, target_table_name, rec_id_column_name, guid_column_name_in_target,
                                      guid_column_value):
    '''
    Create query to find distict asmt_rec_id for a given batch in source table

    '''
    sql_template = "SELECT DISTINCT {rec_id_column_name} " + \
                   "FROM {source_schema_and_table} " + \
                   "WHERE {guid_column_name_in_target}=\'{guid_column_value_got}\'"
    return sql_template.format(rec_id_column_name=rec_id_column_name,
                               source_schema_and_table=combine_schema_and_table(schema_name, target_table_name),
                               guid_column_name_in_target=guid_column_name_in_target,
                               guid_column_value_got=guid_column_value)


def create_select_columns_in_table_query(schema_name, table_name, column_names, criteria=None):
    if (criteria):
        select_query = "SELECT DISTINCT " + ",".join(column_names) + \
            " FROM " + combine_schema_and_table(schema_name, table_name) + \
            " WHERE " + " and ".join(list(key + "='" + value + "'" for key, value in criteria.items()))
    else:
        select_query = "SELECT DISTINCT " + ",".join(column_names) + \
            " FROM " + combine_schema_and_table(schema_name, table_name)
    return select_query


def create_insert_query(conf, source_table, target_table, column_mapping, column_types, need_distinct, op=None):
    '''
    Main function to create query to insert data from source table to target table
    The query will be executed on the database where target table exists
    Since the source tables and target tables can be existing on different databases/servers,
    dblink is used here to get data from source database in the select clause
    '''
    distinct_expression = 'DISTINCT ' if need_distinct else ''
    seq_expression = list(column_mapping.values())[0].replace("'", "''")

    # TODO:if guid_batch is changed to uuid, need to add quotes around it
    if op is None:
        insert_sql = ["INSERT INTO {target_schema_and_table}(",
                      ",".join(list(column_mapping.keys())),
                      ")  SELECT * FROM " +
                      "dblink(\'host={host} port={port} dbname={db_name} user={db_user} password={db_password}\', " +
                      "\'SELECT {seq_expression}, * FROM (SELECT {distinct_expression}",
                      ",".join(value.replace("'", "''") for value in list(column_mapping.values())[1:]),
                      " FROM {source_schema_and_table} " +
                      "WHERE guid_batch=\'\'{guid_batch}\'\') as y\') AS t(",
                      ",".join(list(column_types.values())),
                      ");"]
    else:
        insert_sql = ["INSERT INTO {target_schema_and_table}(",
                      ",".join(list(column_mapping.keys())),
                      ")  SELECT * FROM " +
                      "dblink(\'host={host} port={port} dbname={db_name} user={db_user} password={db_password}\', " +
                      "\'SELECT {seq_expression}, * FROM (SELECT {distinct_expression}",
                      ",".join(value.replace("'", "''") for value in list(column_mapping.values())[1:]),
                      " FROM {source_schema_and_table} " +
                      "WHERE op = \'\'{op}\'\' AND guid_batch=\'\'{guid_batch}\'\') as y\') AS t(",
                      ",".join(list(column_types.values())),
                      ");"]
    insert_sql = "".join(insert_sql).format(target_schema_and_table=combine_schema_and_table(conf[mk.TARGET_DB_SCHEMA],
                                                                                             target_table),
                                            host=conf[mk.SOURCE_DB_HOST],
                                            port=conf[mk.SOURCE_DB_PORT],
                                            db_name=conf[mk.SOURCE_DB_NAME],
                                            db_user=conf[mk.SOURCE_DB_USER],
                                            db_password=conf[mk.SOURCE_DB_PASSWORD],
                                            seq_expression=seq_expression,
                                            distinct_expression=distinct_expression,
                                            source_schema_and_table=combine_schema_and_table(conf[mk.SOURCE_DB_SCHEMA],
                                                                                             source_table),
                                            op=op,
                                            guid_batch=conf[mk.GUID_BATCH])

    return insert_sql


def create_sr_table_select_insert_query(conf, target_table, column_mappings, column_types, op=None):
    '''
    Main function to create query to insert data from mutliple source tables to target table
    The query will be executed on the database where target table exists
    Since the source tables and target tables can be existing on different databases/servers,
    dblink is used here to get data from source database in the select clause
    '''
    key_name = mk.GUID_BATCH
    key_value = conf[mk.GUID_BATCH]
    seq_expression = list(column_mappings[list(column_mappings.keys())[0]].values())[0].replace("'", "''")
    target_keys = []
    source_keys = []
    source_key_assignments = []
    source_values = []
    primary_table = list(column_mappings.keys())[0].lower()
    prev_table = ''
    for source_table in column_mappings.keys():
        if 'nextval' in list(column_mappings[source_table].values())[0]:
            seq_expression = list(column_mappings[source_table].values())[0].replace("'", "''")
            source_keys.extend(list(re.sub('^', source_table.lower() + '.', value).replace("'", "''") for value in list(column_mappings[source_table].values())[1:]))
        else:
            source_keys.extend(list(re.sub('^', source_table.lower() + '.', value).replace("'", "''") for value in list(column_mappings[source_table].values())))
        target_keys.extend(list(column_mappings[source_table].keys()))
        if source_table.lower() == primary_table:
            source_key_assignments.append(combine_schema_and_table(conf[mk.SOURCE_DB_SCHEMA], source_table) + ' ' + source_table.lower())
        else:
            source_key_assignments.append('INNER JOIN ' + combine_schema_and_table(conf[mk.SOURCE_DB_SCHEMA], source_table) + ' ' + source_table.lower() + \
                                          ' ON ' + source_table.lower() + '.' + key_name + ' = ' + prev_table.lower() + '.' + key_name)
        source_values.extend(list(column_types[source_table].values()))
        prev_table = source_table

    # TODO:if guid_batch is changed to uuid, need to add quotes around it
    if op is None:
        insert_sql = ["INSERT INTO {target_schema_and_table}(",
                      ",".join(target_keys),
                      ") SELECT * FROM ",
                      "dblink(\'host={host} port={port} dbname={db_name} user={db_user} password={db_password}\', ",
                      "\'SELECT {seq_expression}, * FROM (SELECT " + ",".join(source_keys),
                      " FROM " + ' '.join(source_key_assignments),
                      " WHERE " + primary_table + ".{key_name}=\'\'{key_value}\'\') as y\') AS t(",
                      ",".join(source_values),
                      ");"]
    else:
        insert_sql = ["INSERT INTO {target_schema_and_table}(",
                      ",".join(target_keys),
                      ") SELECT * FROM ",
                      "dblink(\'host={host} port={port} dbname={db_name} user={db_user} password={db_password}\', ",
                      "\'SELECT {seq_expression}, * FROM (SELECT " + ",".join(source_keys),
                      " FROM " + ' '.join(source_key_assignments),
                      " WHERE op = \'\'{op}\'\' AND " + list(column_mappings.keys())[0].lower() + ".{key_name}=\'\'{key_value}\'\') as y\') AS t(",
                      ",".join(source_values),
                      ");"]
    insert_sql = "".join(insert_sql).format(target_schema_and_table=combine_schema_and_table(conf[mk.TARGET_DB_SCHEMA],
                                                                                             target_table),
                                            host=conf[mk.SOURCE_DB_HOST],
                                            port=conf[mk.SOURCE_DB_PORT],
                                            db_name=conf[mk.SOURCE_DB_NAME],
                                            db_user=conf[mk.SOURCE_DB_USER],
                                            db_password=conf[mk.SOURCE_DB_PASSWORD],
                                            seq_expression=seq_expression,
                                            op=op,
                                            key_name=key_name,
                                            key_value=key_value)

    return insert_sql


def create_delete_query(schema_name, table_name, criteria):
    '''
    Main function to crate a query to delete table
    @param schema_name: db schema name
    @param table_name: db table name
    @param criteria: set of query criteria to apply
                    This is a dictionary of pairs field_name : field_value
    '''
    return "DELETE FROM " + combine_schema_and_table(schema_name, table_name) + \
        " WHERE " + " and ".join(list(key + "='" + value + "'" for key, value in criteria.items()))


def enable_trigger_query(schema_name, table_name, is_enable):
    '''
    Main function to crate a query to disable/enable trigger in table
    @param is_enable: True: enable trigger, False: disbale trigger
    '''
    action = 'ENABLE'
    if not is_enable:
        action = 'DISABLE'
    sql_template = 'ALTER TABLE {schema_name_and_table} {action} TRIGGER ALL'

    return sql_template.format(schema_name_and_table=combine_schema_and_table(schema_name, table_name),
                               action=action)


def update_foreign_rec_id_query(schema, condition_value, info_map):
    '''
    Main function to crate query to update foreign key [foreign]_rec_id in table fact_asmt_outcome
    '''
    update_query = ["UPDATE {schema_and_fact_table} ",
                    "SET {foreign_in_fact}=dim.dim_{foreign_in_dim} FROM (SELECT ",
                    "{foreign_in_dim} AS dim_{foreign_in_dim}, ",
                    ",".join(guid_in_dim + ' AS dim_' + guid_in_dim
                             for guid_in_dim in sorted(list(info_map['guid_column_map'].keys()))),
                    " FROM {schema_and_dim_table}) dim",
                    " WHERE {foreign_in_fact}={fake_value} AND ",
                    " AND ".join(guid_in_fact + '=dim_' + guid_in_dim
                                 for guid_in_dim, guid_in_fact in sorted(info_map['guid_column_map'].items()))
                    ]
    update_query = "".join(update_query).format(schema_and_fact_table=combine_schema_and_table(schema,
                                                                                               info_map['table_map'][1]),
                                                schema_and_dim_table=combine_schema_and_table(schema,
                                                                                              info_map['table_map'][0]),
                                                foreign_in_dim=info_map['rec_id_map'][0],
                                                foreign_in_fact=info_map['rec_id_map'][1],
                                                fake_value=condition_value)
    return update_query


def create_information_query(target_table):
    '''
    Main function to crate query to get column types in a table. 'information_schema.columns' is used.
    '''
    select_template = "SELECT column_name, data_type, character_maximum_length " + \
                      "FROM information_schema.columns " + \
                      "WHERE table_name=\'{target_table}\'"
    return select_template.format(target_table=target_table)


def combine_schema_and_table(schema_name, table_name):
    '''
    Function to create the expression of "schema_name"."table_name"
    '''
    return '\"' + schema_name + '\".\"' + table_name + '\"'


def get_dim_table_mapping_query(schema_name, table_name, phase_number):
    '''
    Function to get target table and source table mapping in a specific udl phase
    '''
    sql_template = "SELECT distinct target_table, source_table " + \
                   "FROM {source_schema_and_table} " + \
                   "WHERE phase={phase_number}"
    return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                               phase_number=phase_number)


def get_column_mapping_query(schema_name, table_name, phase_number, target_table, source_table=None):
    '''
    Function to mapping columns on tables in a specific udl phase
    '''
    if source_table:
        sql_template = "SELECT distinct target_column, source_column " + \
            "FROM {source_schema_and_table} " + \
            "WHERE target_table='{target_table}' and source_table='{source_table}'"
        return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                                   target_table=target_table, source_table=source_table)
    else:
        sql_template = "SELECT distinct target_column, source_column " + \
            "FROM {source_schema_and_table} " + \
            "WHERE target_table='{target_table}'"
        return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                                   target_table=target_table)


def find_unmatched_deleted_fact_asmt_outcome_row(schema_name, table_name, batch_guid, status_code):
    '''
    create a query to search any record that should be deleted/updated but has no record in production database
    '''
    sql_template = "SELECT status FROM {source_schema_and_table} " + \
                   "WHERE status in ({status}) and batch_guid = '{batch_guid}'"
    return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                               status=",".join(["'{i}'".format(i=s[1]) for s in status_code]),
                               batch_guid=batch_guid)


def find_deleted_fact_asmt_outcome_rows(schema_name, table_name, batch_guid, matched_columns, status_code):
    '''
    create a query to find all delete/updated record in current batch
    '''
    cols = [m[0] for m in matched_columns]
    cols.extend(list(set([s[0] for s in status_code])))
    sql_template = "SELECT {cols} " +\
                   "FROM {source_schema_and_table} " + \
                   "WHERE batch_guid = '{batch_guid}' AND status in ({status})"
    return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                               cols=" ,".join(cols),
                               status=", ".join(["'{i}'".format(i=s[1]) for s in status_code]),
                               batch_guid=batch_guid)


def match_delete_fact_asmt_outcome_row_in_prod(schema_name, table_name, matched_columns, matched_status,
                                               matched_preprod_values):
    '''
    create a query to find all delete/updated record in current batch, get the rec_id back
    '''
    pred_to_prod_col_map = dict(matched_columns)
    matched_prod_values = {}
    for k, v in matched_preprod_values.items():
        matched_prod_values[pred_to_prod_col_map[k]] = v
    prod_cols = [c[1] for c in matched_columns]
    prod_cols.extend(list(set([s[0] for s in matched_status])))
    for s in matched_status:
        matched_prod_values[s[0]] = s[1]
    condition_clause = " AND ".join(["{c} = '{v}'".format(c=c, v=matched_prod_values[c]) for c in prod_cols])
    sql_template = "SELECT asmnt_rec_id, {cols} " + \
                   "FROM {source_schema_and_table} " + \
                   "WHERE {condition_clause}"

    return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                               cols=", ".join(prod_cols),
                               condition_clause=condition_clause)


def update_matched_fact_asmt_outcome_row(schema_name, table_name, batch_guid, matched_columns, matched_status,
                                         matched_prod_values):
    '''
    create a query to find all delete/updated record in current batch
    '''
    prod_to_pred_col_map = dict([(s[1], s[0]) for s in matched_columns])
    matched_pred_values = {}
    pred_cols = [c[0] for c in matched_columns]
    pred_cols.extend(list(set([s[0] for s in matched_status])))
    for k, v in matched_prod_values.items():
        try:
            matched_pred_values[prod_to_pred_col_map[k]] = v
        except KeyError as e:
            # ok when prod has more value that pre doesn't have
            pass
    # match deleted record should be 'C' in prod, but in pre-prod. it is the
    for s in matched_status:
        matched_pred_values[s[0]] = s[1]
    condition_clause = " AND ".join(["{c} = '{v}'".format(c=c, v=matched_pred_values[c]) for c in pred_cols])
    prod_rec_id = matched_prod_values['asmnt_rec_id']
    sql_template = "UPDATE {source_schema_and_table} " \
                   "SET asmnt_outcome_rec_id = {prod_rec_id}, status = 'C' || status " +\
                   "WHERE batch_guid = '{batch_guid}' AND {condition_clause}"
    return sql_template.format(source_schema_and_table=combine_schema_and_table(schema_name, table_name),
                               prod_rec_id=prod_rec_id,
                               batch_guid=batch_guid,
                               condition_clause=condition_clause)
