from fileloader.file_loader import connect_db, execute_queries
from collections import OrderedDict
import move_to_target.column_mapping as col_map
import datetime


DBDRIVER = "postgresql"


def explode_data_to_fact_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to explode data from integration table INT_SBAC_ASMT_OUTCOME to star schema table fact_asmt_outcome
    The basic steps are:
    0. Get two foreign keys: asmt_rec_id and section_rec_id
    1. Disable trigger of table fact_asmt_outcome
    2. Insert data from INT_SBAC_ASMT_OUTCOME to fact_asmt_outcome. But for column inst_hier_rec_id, put the temporary value as -1
    3. Update foreign key inst_hier_rec_id by comparing district_guid, school_guid and state_code
    4. Enable trigger of table fact_asmt_outcome
    '''
    asmt_rec_id_info = col_map.get_asmt_rec_id_info()

    # get asmt_rec_id, which is one foreign key in fact table
    asmt_rec_id = get_asmt_rec_id(conf, asmt_rec_id_info['guid_column_name'], asmt_rec_id_info['guid_column_in_source'],
                                  asmt_rec_id_info['rec_id'], asmt_rec_id_info['target_table'], asmt_rec_id_info['source_table'])

    # get section_rec_id, which is one foreign key in fact table. We set to a fake value
    section_rec_id, section_rec_id_column_name = get_section_rec_id()

    # update above 2 foreign keys in column mapping
    column_mapping = col_map.get_column_mapping()[target_table]
    column_mapping[asmt_rec_id_info['rec_id']] = str(asmt_rec_id)
    column_mapping[section_rec_id_column_name] = section_rec_id

    # get list of queries to be executed
    queries = create_queries_for_move_to_fact_table(conf, source_table, target_table, column_mapping, column_types)

    # create database connection (connect to target)
    conn, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])

    # execute above four queries in order, 2 parts
    print("I am the exploder, about to copy data into fact table with fake inst_hier_rec_id")
    start_time_p1 = datetime.datetime.now()
    execute_queries(conn, queries[0:2], 'Exception -- exploding data from integration to fact table part 1')
    finish_time_p1 = datetime.datetime.now()
    spend_time_p1 = calculate_spend_time_as_second(start_time_p1, finish_time_p1)
    print("I am the exploder, copied data into fact table with fake inst_hier_rec_id in %.3f seconds" % spend_time_p1)

    print("I am the exploder, about to update inst_hier_rec_id as value in dim_inst_hier")
    execute_queries(conn, queries[2:4], 'Exception -- exploding data from integration to fact table part 2')
    finish_time_p2 = datetime.datetime.now()
    spend_time_p2 = calculate_spend_time_as_second(finish_time_p1, finish_time_p2)
    print("I am the exploder, updated inst_hier_rec_id as value in dim_inst_hier in %.3f seconds" % spend_time_p2)

    conn.close()


def get_asmt_rec_id(conf, guid_column_name_in_target, guid_column_name_in_source, rec_id_column_name, target_table_name, source_table_name):
    '''
    Main function to get asmt_rec_id in dim_asmt table
    Steps:
    1. Get guid_amst from integration table INT_SBAC_ASMT
    2. Select asmt_rec_id from dim_asmt by the same guid_amst got from 1. It should have 1 value
    '''
    # connect to integration table, to get guid_column_value
    conn_to_source_db, _engine = connect_db(conf['db_user'], conf['db_password'], conf['db_host'], conf['db_name'])
    query_to_get_guid = "SELECT DISTINCT {guid_column_name_in_source} FROM {source_schema_and_table} WHERE batch_id={batch_id}".format(
                                                                                                                                  guid_column_name_in_source=guid_column_name_in_source,
                                                                                                                                  source_schema_and_table=combine_schema_and_table(conf['source_schema'], source_table_name),
                                                                                                                                  batch_id=conf['batch_id']
                                                                                                                                  )
    # print(query_to_get_guid)
    guid_column_value = execute_query_get_one_value(conn_to_source_db, query_to_get_guid, guid_column_name_in_source)
    conn_to_source_db.close()

    # connect to target table, to get rec_id_column_value
    conn_to_target_db, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    query_to_get_rec_id = "SELECT DISTINCT {rec_id_column_name} FROM {source_schema_and_table} WHERE {guid_column_name_in_target}=\'{guid_column_value_got}\'".format(
                                                                                                                      rec_id_column_name=rec_id_column_name,
                                                                                                                      source_schema_and_table=combine_schema_and_table(conf['target_schema'], target_table_name),
                                                                                                                      guid_column_name_in_target=guid_column_name_in_target,
                                                                                                                      guid_column_value_got=guid_column_value
                                                                                                                      )
    # print(query_to_get_rec_id)
    asmt_rec_id = execute_query_get_one_value(conn_to_target_db, query_to_get_rec_id, rec_id_column_name)
    conn_to_target_db.close()
    return asmt_rec_id


def execute_query_get_one_value(conn, query, column_name):
    '''
    This is the function to execute one query, and return one correct value returned by the query
    '''
    one_value_result = []
    try:
        result = conn.execute(query)
        for row in result:
            one_value_result.append(row[0])
    except Exception as exception:
        print(exception)
    if len(one_value_result) != 1:
        # raise Exception('Rec id of %s has more/less than 1 record for batch %s' % (column_name, batch_id))
        print('Rec id of %s has more/less than 1 record, length is %d ' % (column_name, len(one_value_result)))
        if len(one_value_result) > 1:
            one_value_result = str(one_value_result[0])
        else:
            one_value_result = ['-1']
    return one_value_result[0]


def get_section_rec_id():
    '''
    This is the function to get section_rec_id from dim_section.
    Currently, we don't have to populate table dim_section, but section_rec_id is a foreign key in fact_asmt_outcome table.
    Thus, we make a fake row in dim_section table with section_rec_id = 1. It should be setup in setup.py afterwards.
    @return: value of section_rec_id which is 1, and column name of section_rec_id
    '''
    # need to read the fake value from conf file
    return '1', 'section_rec_id'


def create_queries_for_move_to_fact_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to create four queries(in order) for moving data from integration table
    INT_SBAC_ASMT_OUTCOME to star schema table fact_asmt_outcome.
    These four queries are corresponding to four steps described in method explode_data_to_fact_table().
    @return: list of four queries
    '''
    # disable foreign key in fact table
    disable_trigger_query = enable_trigger_query(conf['target_schema'], target_table, False)
    # print(disable_trigger_query)

    # create insertion insert_into_fact_table_query
    insert_into_fact_table_query = create_insert_query(conf, source_table, target_table, column_mapping, column_types, False)
    # print(insert_into_fact_table_query)

    # update inst_hier_query back
    update_inst_hier_rec_id_fk_query = update_inst_hier_rec_id_query(conf['target_schema'])
    # print(update_inst_hier_rec_id_fk_query)

    # enable foreign key in fact table
    enable_back_trigger_query = enable_trigger_query(conf['target_schema'], target_table, True)
    # print(enable_back_trigger_query)

    return [disable_trigger_query, insert_into_fact_table_query, update_inst_hier_rec_id_fk_query, enable_back_trigger_query]


def explode_data_to_dim_table(conf, source_table, target_table, column_mapping, column_types):
    '''
    Main function to move data from source table to target tables.
    Source table can be INT_SBAC_ASMT, and INT_SBAC_ASMT_OUTCOME. Target table can be any dim tables in star schema.
    @param conf: one dictionary which has database settings, and batch_id
    @param source_table: name of the source table where the data comes from
    @param target_table: name of the target table where the data should be moved to
    @param column_mapping: one dictionary which defines mapping of:
                           column_name_in_target, column_name_in_source
    @param column_types: data types of all columns in one target table
    '''
    # create database connection to target
    conn, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])

    # create insertion query
    # TODO: find out if the affected rows, time can be returned
    query = create_insert_query(conf, source_table, target_table, column_mapping, column_types, True)
    # print(query)

    # execute the query
    execute_queries(conn, [query], 'Exception -- exploding data from integration to target {target_table}'.format(target_table=target_table))
    conn.close()


def enable_trigger_query(schema_name, table_name, is_enable):
    '''
    Main function to crate a query to disable/enable trigger in table
    @param is_enable: True: enable trigger, False: disbale trigger
    '''
    action = 'ENABLE'
    if not is_enable:
        action = 'DISABLE'
    query = 'ALTER TABLE {schema_name_and_table} {action} TRIGGER ALL'.format(schema_name_and_table=combine_schema_and_table(schema_name, table_name),
                                                                              action=action)
    return query


def create_insert_query(conf, source_table, target_table, column_mapping, column_types, need_distinct):
    '''
    Main function to create query to insert data from source table to target table
    The query will be executed on the database where target table exists
    Since the source tables and target tables can be existing on different databases/servers,
    dblink is used here to get data from source database in the select clause
    '''
    distinct_expression = 'DISTINCT ' if need_distinct else ''
    seq_expression = list(column_mapping.values())[0].replace("'", "''")

    insert_sql = [
             "INSERT INTO {target_shcema_and_table}(",
             ",".join(list(column_mapping.keys())),
             ")  SELECT * FROM dblink(\'dbname={db_name} user={db_user} password={db_password}\', \'SELECT {seq_expression}, * FROM (SELECT {distinct_expression}",
             ",".join(value.replace("'", "''") for value in list(column_mapping.values())[1:]),
             " FROM {source_schema_and_table} WHERE batch_id={batch_id}) as y\') AS t(",
             ",".join(list(column_types.values())),
             ");"
            ]
    insert_sql = "".join(insert_sql).format(target_shcema_and_table=combine_schema_and_table(conf['db_name_target'], target_table),
                                            db_password_target=conf['db_password_target'],
                                            target_schema=conf['target_schema'],
                                            db_name=conf['db_name'],
                                            db_user=conf['db_user'],
                                            db_password=conf['db_password'],
                                            seq_expression=seq_expression,
                                            distinct_expression=distinct_expression,
                                            source_schema_and_table=combine_schema_and_table(conf['source_schema'], source_table),
                                            batch_id=conf['batch_id'])

    return insert_sql


def update_inst_hier_rec_id_query(schema):
    '''
    Main function to crate query to update foreign key inst_hier_rec_id in table fact_asmt_outcome
    '''
    info_map = col_map.get_inst_hier_rec_id_info()
    update_query = ["UPDATE {schema_and_fact_table} ",
             "SET {inst_hier_in_fact}=dim.dim_{inst_hier_in_dim} FROM (SELECT ",
             "{inst_hier_in_dim} AS dim_{inst_hier_in_dim}, ",
             ",".join(guid_in_dim + ' AS dim_' + guid_in_dim for guid_in_dim in list(info_map['guid_column_map'].keys())),
             " FROM {schema_and_dim_table})dim",
             " WHERE {inst_hier_in_fact}=-1 AND ",
             " AND ".join(guid_in_fact + '= dim_' + guid_in_dim for guid_in_dim, guid_in_fact in info_map['guid_column_map'].items())
             ]
    update_query = "".join(update_query).format(schema_and_fact_table=combine_schema_and_table(schema, info_map['table_map'][1]),
                                                schema_and_dim_table=combine_schema_and_table(schema, info_map['table_map'][0]),
                                                inst_hier_in_dim=info_map['rec_id_map'][0],
                                                inst_hier_in_fact=info_map['rec_id_map'][1])
    return update_query


def get_table_column_types(conf, target_table, column_names):
    '''
    Main function to get column types of a table by querying the table
    @return a dictionary, which has same ordered keys in the input column_names.
    The values are column types with maximum length if it is defined in table.
    The pattern of the value is: <column_name data_type(length)> or <column_name data_type>
    '''
    column_types = OrderedDict([(column_name, '') for column_name in column_names])
    conn, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    query = create_information_query(conf, target_table)
    # execute query
    try:
        result = conn.execute(query)
        for row in result:
            column_name = row[0]
            data_type = row[1]
            character_maximum_length = row[2]
            if column_name in column_types.keys():
                return_value = column_name + " " + data_type
                if character_maximum_length:
                    return_value += "(" + str(character_maximum_length) + ")"
                column_types[column_name] = return_value
    except Exception as e:
        print('Exception in getting type', e)

    conn.close()
    return column_types


def create_information_query(conf, target_table):
    '''
    Main function to crate query to get column types in a table. 'information_schema.columns' is used.
    '''
    select_query = "SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name=\'{target_table}\'".format(target_table=target_table)
    return select_query


def calculate_spend_time_as_second(start_time, finish_time):
    '''
    Main function to calculate period distance as seconds
    '''
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)
    return time_as_seconds


def combine_schema_and_table(schema_name, table_name):
    '''
    Function to create the expression of "schema_name"."table_name"
    '''
    return '\"' + schema_name + '\".\"' + table_name + '\"'
