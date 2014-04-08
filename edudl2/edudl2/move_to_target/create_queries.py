import re
from edudl2.udl2 import message_keys as mk
from sqlalchemy.sql.expression import text, bindparam, select, and_
from edudl2.database.udl2_connector import get_udl_connection, \
    get_target_connection, get_prod_connection
from psycopg2.extensions import QuotedString
from edudl2.udl2_util.database_util import create_filtered_sql_string
import edschema.metadata.util as edschema_util


def create_insert_query(conf, source_table, target_table, column_mapping, column_types, need_distinct, op=None):
    '''
    Main function to create query to insert data from source table to target table
    The query will be executed on the database where target table exists
    Since the source tables and target tables can be existing on different databases/servers,
    dblink is used here to get data from source database in the select clause
    '''
    distinct_expression = 'DISTINCT ' if need_distinct else ''
    seq_expression = list(column_mapping.values())[0].replace("'", "''")
    target_columns = ",".join(list(column_mapping.keys()))
    lst = list(column_mapping.values())
    quoted_source_columns = ",".join(value.replace("'", "''") for value in lst[1:])
    record_mapping = ",".join(list(column_types.values()))
    params = []
    # TODO:if guid_batch is changed to uuid, need to add quotes around it
    if op is None:
        query = "INSERT INTO {target_schema_and_table} ({target_columns}) " + \
                "SELECT * FROM " + \
                "dblink({dblink_url}, " + \
                "'SELECT {seq_expression}, * FROM (SELECT {distinct_expression}" + \
                "{quoted_source_columns} " + \
                "FROM {source_schema_and_table} " + \
                "WHERE guid_batch=':guid_batch') as y') AS t({record_mapping});"
        params = [bindparam('guid_batch', conf[mk.GUID_BATCH])]
    else:
        query = "INSERT INTO {target_schema_and_table} ({target_columns}) " + \
                "SELECT * FROM " + \
                "dblink({dblink_url}, " + \
                "'SELECT {seq_expression}, * FROM (SELECT {distinct_expression}" + \
                "{quoted_source_columns} " + \
                "FROM {source_schema_and_table} " + \
                "WHERE op = ':op' AND guid_batch=':guid_batch') as y') AS t({record_mapping});"
        params = [bindparam('guid_batch', conf[mk.GUID_BATCH]), bindparam('op', op)]
    query = query.format(target_schema_and_table=combine_schema_and_table(conf[mk.TARGET_DB_SCHEMA],
                                                                          target_table),
                         dblink_url=dblink_url_composer(host=conf[mk.SOURCE_DB_HOST],
                                                        port=conf[mk.SOURCE_DB_PORT],
                                                        db_name=conf[mk.SOURCE_DB_NAME],
                                                        db_user=conf[mk.SOURCE_DB_USER],
                                                        db_password=conf[mk.SOURCE_DB_PASSWORD]),
                         seq_expression=seq_expression,
                         distinct_expression=distinct_expression,
                         source_schema_and_table=combine_schema_and_table(conf[mk.SOURCE_DB_SCHEMA], source_table),
                         quoted_source_columns=quoted_source_columns,
                         record_mapping=record_mapping,
                         target_columns=target_columns)

    return text(query, bindparams=params)


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
                    "dblink({dblink_url}, ",
                    "\'SELECT {seq_expression}, * FROM (SELECT " + ",".join(source_keys),
                    " FROM " + ' '.join(source_key_assignments) + " {where_statement} AS t(" + ",".join(types) + ");"]
    insert_query = "".join(insert_query).format(target_schema_and_table=combine_schema_and_table(conf[mk.TARGET_DB_SCHEMA], target_table),
                                                dblink_url=dblink_url_composer(host=conf[mk.SOURCE_DB_HOST],
                                                                               port=conf[mk.SOURCE_DB_PORT],
                                                                               db_name=conf[mk.SOURCE_DB_NAME],
                                                                               db_user=conf[mk.SOURCE_DB_USER],
                                                                               db_password=conf[mk.SOURCE_DB_PASSWORD]),
                                                seq_expression=seq_expression, where_statement=where_statement)

    return insert_query


def create_delete_query(tenant, schema_name, table_name, criteria=None):
    '''
    Create a query to delete a db table.

    @param schema_name: DB schema name
    @param table_name: DB table name
    @param criteria: (optional) Delete criteria to apply
                    This is a dictionary of pairs of field_name : field_value

    @return Delete query
    '''
    with get_target_connection(tenant, schema_name) as conn:
        table = conn.get_table(table_name)
        query = table.delete()
        if criteria:
            expr = [k == v for k, v in criteria.items()]
            query = query.where(and_(*expr))

    return query


def enable_trigger_query(schema_name, table_name, is_enable):
    '''
    Main function to crate a query to disable/enable trigger in table
    @param is_enable: True: enable trigger, False: disbale trigger
    '''
    action = 'ENABLE'
    if not is_enable:
        action = 'DISABLE'
    sql_template = 'ALTER TABLE {schema_name_and_table} {action} TRIGGER ALL'

    return text(sql_template.format(schema_name_and_table=combine_schema_and_table(schema_name, table_name),
                                    action=action))


def update_foreign_rec_id_query(fk_constraint):
    '''
    Create query to update foreign key in table
    @param fk_constraint: Foreign key constraint object to build query for
    '''
    # Store the target table
    target = fk_constraint.table
    target_col_names = [column.name for column in target.columns]

    # Process each key
    queries = []
    for fk in fk_constraint.foreign_keys:
        # Get source table
        source = fk.column.table

        # Get natural key from source table
        source_nk = edschema_util.get_natural_key(source)

        if source_nk is None:
            continue

        # Validate the existence of each column in the target table
        for column in source_nk:
            if column.name not in target_col_names:
                raise Exception('Missing required natural key column (%s) in target table (%s)' % (column.name,
                                                                                                   str(target)))

        # Build the query
        where_clauses = []
        for column in source_nk:
            where_clauses.append(target.c[column.name] == source.c[column.name])

        update_query = target.update().values({target.c[fk.parent.name]: source.c[fk.column.name]})
        update_query = update_query.where(and_(*where_clauses))

        # Put the query into the list
        queries.append(update_query)

    return queries


def create_information_query(target_table):
    '''
    Main function to crate query to get column types in a table. 'information_schema.columns' is used.
    '''
    # TODO: Investigate what this is used for
    query = text("SELECT column_name, data_type, character_maximum_length "
                 "FROM information_schema.columns "
                 "WHERE table_name = :target_table",
                 bindparams=[bindparam('target_table', target_table)])

    return query


def combine_schema_and_table(schema_name, table_name):
    '''
    Function to create the expression of "schema_name"."table_name"
    '''
    if schema_name:
        return create_filtered_sql_string('"{schema}"."{table}"', schema=schema_name, table=table_name)
    else:
        return create_filtered_sql_string('"{table}"', table=table_name)


def get_dim_table_mapping_query(schema_name, table_name, phase_number):
    '''
    Function to get target table and source table mapping in a specific udl phase
    '''
    with get_udl_connection() as conn:
        table = conn.get_table(table_name)
        query = select([table.c.target_table,
                        table.c.source_table],
                       from_obj=table).where(table.c.phase == phase_number).group_by(table.c.target_table, table.c.source_table)
        return query


def get_column_mapping_query(schema_name, ref_table, target_table, source_table=None):
    '''
    Get column mapping to target table.

    @param schema_name: DB schema name
    @param ref_table: DB reference mapping table name
    @target_table: Table into which to insert data
    @param source_table: (optional) Only include columns from this table

    @return Mapping query
    '''
    with get_udl_connection() as conn:
        table = conn.get_table(ref_table)
        query = select([table.c.target_column,
                        table.c.source_column],
                       from_obj=table)
        query = query.where(table.c.target_table == target_table)
        if source_table:
            query = query.where(and_(table.c.source_table == source_table))
    return query


def get_delete_candidates(tenant, schema_name, table_name, batch_guid, matching_conf):
    '''
    create a query to find all delete/updated record in current batch
    '''
    with get_target_connection(tenant, schema_name) as conn:
        fact_asmt = conn.get_table(table_name)
        columns = [fact_asmt.c[column_name] for column_name in matching_conf['columns']]
        criterias = [fact_asmt.c[criteria] == matching_conf[criteria] for criteria in matching_conf['condition']]
        query = select(columns, from_obj=fact_asmt).where(and_(fact_asmt.c.batch_guid == batch_guid))
        query = query.where(and_(*criterias))
        return conn.get_result(query)


def match_delete_record_against_prod(tenant_name, schema_name, table_name, matching_conf, matched_preprod_values):
    '''
    create a query to find all delete/updated record in current batch, get the rec_id back
    '''
    matched_prod_values = matched_preprod_values.copy()
    matched_prod_values['rec_status'] = matching_conf['rec_status']
    with get_prod_connection(tenant_name) as conn:
        fact_asmt = conn.get_table(table_name)
        columns = [fact_asmt.c[column_name] for column_name in matching_conf['columns']]
        criterias = [fact_asmt.c[criteria] == matched_prod_values[criteria] for criteria in matching_conf['condition']]
        query = select(columns, from_obj=fact_asmt)
        query = query.where(and_(*criterias))
        return conn.get_result(query)


def update_matched_fact_asmt_outcome_row(tenant_name, schema_name, table_name, batch_guid, matching_conf,
                                         matched_prod_values):
    '''
    create a query to find all delete/updated record in current batch
    UPDATE edware.fact_asmt_outcome
    SET inst_hier_rec_id=tmp_dim_info.inst_hier_rec_id
    FROM edware.dim_inst_hier,
    (SELECT edware.dim_inst_hier.inst_hier_rec_id AS inst_hier_rec_id,
    edware.dim_inst_hier.district_guid AS district_guid,
    edware.dim_inst_hier.school_guid AS school_guid,
    edware.dim_inst_hier.state_code AS state_code
    FROM edware.dim_inst_hier) AS tmp_dim_info
    WHERE edware.fact_asmt_outcome.inst_hier_rec_id =  -1
    AND edware.dim_inst_hier.district_guid = tmp_dim_info.district_guid
    AND edware.dim_inst_hier.school_guid = tmp_dim_info.school_guid
    AND edware.dim_inst_hier.state_code = tmp_dim_info.state_code
    '''
    values = {}
    matched_prod_values['rec_status'] = matching_conf['new_status']

    matched_preprod_values = matched_prod_values.copy()
    matched_preprod_values['rec_status'] = matching_conf['rec_status']
    del matched_preprod_values['asmnt_outcome_rec_id']
    # TODO: Query simplication
    for k in matching_conf['columns'].keys():
        values[k] = matched_prod_values[k]
    with get_target_connection(tenant_name, schema_name) as conn:
        fact_asmt = conn.get_table('fact_asmt_outcome')
        criterias = [fact_asmt.c[k] == v for k, v in matched_preprod_values.items()]
        query = fact_asmt.update().values(values).where(fact_asmt.c.batch_guid == batch_guid)
        query = query.where(and_(*criterias))

    return query


def dblink_url_composer(host, port, db_name, db_user, db_password):
    return QuotedString('host={host} port={port} dbname={db_name} user={db_user} password={db_password}'
                        .format(host=host, port=port, db_name=db_name, db_user=db_user, db_password=db_password))
