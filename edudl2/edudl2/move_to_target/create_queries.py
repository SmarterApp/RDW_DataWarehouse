import re
from edudl2.udl2 import message_keys as mk
from sqlalchemy.sql.expression import text, bindparam
from edcore.utils.utils import compile_query_to_sql_text


def select_distinct_asmt_guid_query(schema_name, table_name, column_name, guid_batch):
    '''
    Create query to find distict asmt_guid for a given batch in source table
    @schema_name:
    @table_name:
    @column_name:
    @guid_batch
    '''
    query = text("SELECT DISTINCT " + column_name + " " +
                 "FROM " + combine_schema_and_table(schema_name, table_name) + " " +
                 "WHERE guid_batch=:guid_batch",
                 bindparams=[bindparam('guid_batch', guid_batch)])

    return query


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
    '''
    Create a query to select specified columns in a table, with optional select criteria.

    @schema_name: Name of schema in which database resides
    @table_name: Name of table from which to select columns
    @column_names: List of columns to include in select
    @criteria: (optional) Query select criteria
            This is a dictionary of pairs of field_name : field_value

    @return Select query
    '''

    select_query = "SELECT DISTINCT " + ",".join(column_names) + " FROM " + combine_schema_and_table(schema_name, table_name)
    if (criteria):
        select_query += " WHERE " + " AND ".join(list(key + "='" + value + "'" for key, value in criteria.items()))

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


def create_sr_table_select_insert_query(conf, target_table, column_and_type_mapping, op=None):
    '''
    Create a query to insert data from multiple source tables to target table.
    The query will be executed on the database where target table exists.
    Since the source tables and target tables can be existing on different databases/servers,
    dblink is used here to get data from source database in the select clause.

    Query is of format:
    INSERT INTO "{target_schema}"."{target_table}"(target_col_1,target_col_2,...,target_col_n)
    SELECT FROM dblink('host={host} port={port} dbname={db_name} user={db_user} password={db_password}',
    SELECT nextval(''"GLOBAL_REC_SEQ"''), * FROM (SELECT src_table1.src_col_1,...,src_table_1.src_col_j,
    src_table_2.src_col_1,...,src_table_2.src_col_k,...,src_table_m.src_col_1,...,src_table_m.src_col_l
    FROM "{source_schema}"."{source_table_1}" source_table_1_lowercase INNER JOIN
    "{source_schema}"."{source_table_2}" source_table_2_lowercase
    ON source_table_2_lowercase.{key_name} = source_table_1_lowercase.{key_name},... INNER JOIN
    "{source_schema}"."{source_table_m}" source_table_m_lowercase
    ON source_table_m_lowercase.{key_name} = source_table_m-1_lowercase.{key_name}
    WHERE source_table_1_lowercase.{key_name}={key_value}) AS y') AS t(target_col_1 target_col_1_type,
    target_col_2 target_col_2_type,...,target_col_n target_col_n_type);

    Where j + k + ... + l = n

    @conf: Configuration for particular load type (assessment or studentregistration)
    @target_table: Table into which to insert data
    @column_and_type_mapping: Mapping of source table columns and their types to target table columns
    @op: (optional) Value of "op" column upon which to select

    @return Insert query
    '''

    key_name = mk.GUID_BATCH
    key_value = conf[mk.GUID_BATCH]
    primary_table = list(column_and_type_mapping.keys())[0]
    seq_expression = list(column_and_type_mapping[primary_table].values())[0].src_col.replace("'", "''")
    target_keys = []
    source_keys = []
    source_key_assignments = []
    types = []
    prev_table = ''
    primary_table_lower = primary_table.lower()

    # TODO: If guid_batch (key_name) is changed to uuid, need to add quotes around it.
    if op:
        where_statement = "WHERE op = \'\'{op}\'\' AND " + primary_table_lower + ".{key_name}=\'\'{key_value}\'\') AS y\')"
    else:
        where_statement = "WHERE " + primary_table_lower + ".{key_name}=\'\'{key_value}\'\') AS y\')"
    where_statement = where_statement.format(key_name=key_name, key_value=key_value, op=op)

    for source_table in column_and_type_mapping.keys():
        source_table_lower = source_table.lower()

        if 'nextval' in list(column_and_type_mapping[source_table].values())[0].src_col:
            source_keys.extend(list(re.sub('^', source_table.lower() + '.', value.src_col).replace("'", "''") for value in list(column_and_type_mapping[source_table].values())[1:]))
        else:
            source_keys.extend(list(re.sub('^', source_table.lower() + '.', value.src_col).replace("'", "''") for value in list(column_and_type_mapping[source_table].values())))

        target_keys.extend(list(column_and_type_mapping[source_table].keys()))

        if source_table_lower == primary_table_lower:
            source_key_assignments.append(combine_schema_and_table(conf[mk.SOURCE_DB_SCHEMA], source_table) + ' ' + source_table_lower)
        else:
            source_key_assignments.append('INNER JOIN ' + combine_schema_and_table(conf[mk.SOURCE_DB_SCHEMA], source_table) + ' ' + source_table_lower +
                                          ' ON ' + source_table_lower + '.' + key_name + ' = ' + prev_table.lower() + '.' + key_name)

        types.extend(list(value.type for value in column_and_type_mapping[source_table].values()))

        prev_table = source_table

    insert_query = ["INSERT INTO {target_schema_and_table}(" + ",".join(target_keys),
                    ") SELECT * FROM ",
                    "dblink(\'host={host} port={port} dbname={db_name} user={db_user} password={db_password}\', ",
                    "\'SELECT {seq_expression}, * FROM (SELECT " + ",".join(source_keys),
                    " FROM " + ' '.join(source_key_assignments) + " {where_statement} AS t(" + ",".join(types) + ");"]
    insert_query = "".join(insert_query).format(target_schema_and_table=combine_schema_and_table(conf[mk.TARGET_DB_SCHEMA], target_table),
                                                host=conf[mk.SOURCE_DB_HOST], port=conf[mk.SOURCE_DB_PORT], db_name=conf[mk.SOURCE_DB_NAME],
                                                db_user=conf[mk.SOURCE_DB_USER], db_password=conf[mk.SOURCE_DB_PASSWORD],
                                                seq_expression=seq_expression, where_statement=where_statement)

    return insert_query


def create_delete_query(schema_name, table_name, criteria=None):
    '''
    Create a query to delete a db table.

    @param schema_name: DB schema name
    @param table_name: DB table name
    @param criteria: (optional) Delete criteria to apply
                    This is a dictionary of pairs of field_name : field_value

    @return Delete query
    '''

    delete_query = "DELETE FROM " + combine_schema_and_table(schema_name, table_name) + \
        " WHERE " + " AND ".join(list(key + "='" + value + "'" for key, value in criteria.items()))

    return delete_query


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


def get_column_mapping_query(schema_name, ref_table, target_table, source_table=None):
    '''
    Get column mapping to target table.

    @param schema_name: DB schema name
    @param ref_table: DB reference mapping table name
    @target_table: Table into which to insert data
    @param source_table: (optional) Only include columns from this table

    @return Mapping query
    '''

    if source_table:
        where_statement = " WHERE target_table='{target_table}' and source_table='{source_table}'"
    else:
        where_statement = " WHERE target_table='{target_table}'"
    where_statement = where_statement.format(target_table=target_table, source_table=source_table)

    mapping_query = "SELECT distinct target_column, source_column " + "FROM {source_schema_and_ref_table} {where_statement}"
    mapping_query = mapping_query.format(source_schema_and_ref_table=combine_schema_and_table(schema_name, ref_table),
                                         where_statement=where_statement)

    return mapping_query


def find_deleted_fact_asmt_outcome_rows(schema_name, table_name, batch_guid, matching_conf):
    '''
    create a query to find all delete/updated record in current batch
    '''
    params = [bindparam('batch_guid', batch_guid),
              bindparam('status', matching_conf['status'])]
    query = text("SELECT {cols} "
                 "FROM {source_schema_and_table} "
                 "WHERE batch_guid = :batch_guid "
                 "AND status = :status".format(cols=", ".join(matching_conf['columns']),
                                               source_schema_and_table=combine_schema_and_table(schema_name,
                                                                                                table_name)
                                               ),
                 bindparams=params)
    return query


def match_delete_fact_asmt_outcome_row_in_prod(schema_name, table_name, matching_conf, matched_preprod_values):
    '''
    create a query to find all delete/updated record in current batch, get the rec_id back
    '''
    matched_prod_values = matched_preprod_values.copy()
    matched_prod_values['status'] = matching_conf['status']
    condition_clause = " AND ".join(["{c} = :{c}".format(c=c) for c in sorted(matched_prod_values.keys())])
    params = [bindparam(c, matched_prod_values[c]) for c in sorted(matched_prod_values.keys())]
    query = text("SELECT {columns} "
                 "FROM {source_schema_and_table} "
                 "WHERE {condition_clause}".format(source_schema_and_table=combine_schema_and_table(schema_name,
                                                                                                    table_name),
                                                   columns=", ".join(matching_conf['columns']),
                                                   condition_clause=condition_clause),
                 bindparams=params)
    return query


def update_matched_fact_asmt_outcome_row(schema_name, table_name, batch_guid, matching_conf,
                                         matched_prod_values):
    '''
    create a query to find all delete/updated record in current batch
    '''
    set_clause = ", ".join(["{k} = :{v}".format(k=kc, v=kv) for kc, kv in sorted(matching_conf['columns'].items())])
    matched_preprod_values = matched_prod_values.copy()
    matched_preprod_values['status'] = matching_conf['status']
    del matched_preprod_values['asmnt_outcome_rec_id']
    condition_clause = " AND ".join(["{c} = :{c}".format(c=c) for c in sorted(matched_preprod_values.keys())])
    params = [bindparam(c, matched_preprod_values[c]) for c in matched_preprod_values.keys()]
    matched_prod_values['new_status'] = matching_conf['new_status']
    params.extend([bindparam(v, matched_prod_values[v]) for v in matching_conf['columns'].values()])
    params.append(bindparam('batch_guid', batch_guid))
    query = text("UPDATE {target_schema_and_table} "
                 "SET {set_clause} "
                 "WHERE batch_guid = :batch_guid "
                 "AND {condition_clause}".format(condition_clause=condition_clause,
                                                 set_clause=set_clause,
                                                 target_schema_and_table=combine_schema_and_table(schema_name,
                                                                                                  table_name)),

                 bindparams=params)
    return query
