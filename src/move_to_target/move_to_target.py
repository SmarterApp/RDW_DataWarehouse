from fileloader.file_loader import connect_db, execute_queries
from collections import OrderedDict
import move_to_target.column_mapping as col_map
import move_to_target.create_queries as queries
import datetime


DBDRIVER = "postgresql"
FAKE_INST_HIER_REC_ID = -1


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
    query_to_get_guid = queries.select_distinct_asmt_guid_query(conf['source_schema'], source_table_name, guid_column_name_in_source, conf['batch_id'])
    # print(query_to_get_guid)
    guid_column_value = execute_query_get_one_value(conn_to_source_db, query_to_get_guid, guid_column_name_in_source)
    conn_to_source_db.close()

    # connect to target table, to get rec_id_column_value
    conn_to_target_db, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    query_to_get_rec_id = queries.select_distinct_asmt_rec_id_query(conf['target_schema'], target_table_name, rec_id_column_name, guid_column_name_in_target, guid_column_value)
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
    disable_trigger_query = queries.enable_trigger_query(conf['target_schema'], target_table, False)
    # print(disable_trigger_query)

    # create insertion insert_into_fact_table_query
    insert_into_fact_table_query = queries.create_insert_query(conf, source_table, target_table, column_mapping, column_types, False)
    # print(insert_into_fact_table_query)

    # update inst_hier_query back
    update_inst_hier_rec_id_fk_query = queries.update_inst_hier_rec_id_query(conf['target_schema'], FAKE_INST_HIER_REC_ID)
    # print(update_inst_hier_rec_id_fk_query)

    # enable foreign key in fact table
    enable_back_trigger_query = queries.enable_trigger_query(conf['target_schema'], target_table, True)
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
    # TODO: find out if the affected rows, time can be returned, so that the returned info can be put in the log
    query = queries.create_insert_query(conf, source_table, target_table, column_mapping, column_types, True)
    # print(query)

    # execute the query
    execute_queries(conn, [query], 'Exception -- exploding data from integration to target {target_table}'.format(target_table=target_table))
    conn.close()


def get_table_column_types(conf, target_table, column_names):
    '''
    Main function to get column types of a table by querying the table
    @return a dictionary, which has same ordered keys in the input column_names.
    The values are column types with maximum length if it is defined in table.
    The pattern of the value is: <column_name data_type(length)> or <column_name data_type>
    '''
    column_types = OrderedDict([(column_name, '') for column_name in column_names])
    conn, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    query = queries.create_information_query(conf, target_table)
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


def calculate_spend_time_as_second(start_time, finish_time):
    '''
    Main function to calculate period distance as seconds
    '''
    spend_time = finish_time - start_time
    time_as_seconds = float(spend_time.seconds + spend_time.microseconds / 1000000.0)
    return time_as_seconds
