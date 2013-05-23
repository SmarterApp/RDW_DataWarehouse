from fileloader.file_loader import connect_db, execute_queries
from collections import OrderedDict
import move_to_target.column_mapping as col_map


DBDRIVER = "postgresql"


def explode_data_to_fact_table(conf, db_user_target, db_password_target, db_host_target, db_name_target, source_table, target_table, column_mapping, column_types):
    asmt_rec_id_info = col_map.get_asmt_rec_id_info()

    # get asmt_rec_id
    asmt_rec_id = get_asmt_rec_id(conf,
                             asmt_rec_id_info['guid_column_name'],
                             asmt_rec_id_info['guid_column_in_source'],
                             asmt_rec_id_info['guid_column_name'],
                             asmt_rec_id_info['target_table'],
                             asmt_rec_id_info['source_table'])

    # get section_rec_id
    section_rec_id, section_rec_id_column_name = get_section_rec_id()

    # get inst_hier_rec_id
    inst_hier_rec_id_map = get_rec_id_map(conf, conf['target_schema'], 'dim_inst_hier', 'inst_hier_rec_id', conf['batch_id'])
    print("asmt_rec_id, section_rec_id, length of inst_hier_rec_id_map are: %s, %s, %d"
          % (asmt_rec_id, section_rec_id, len(inst_hier_rec_id_map)))

    # create the query to insert into fact table via dblink
    # create db connection
    conn, _engine = connect_db(conf['db_user'], conf['db_password'], conf['db_host'], conf['db_name'])
    column_mapping = col_map.get_column_mapping()[target_table]
    column_mapping[asmt_rec_id_info['rec_id']] = "'" + asmt_rec_id + "'"
    column_mapping[section_rec_id_column_name] = section_rec_id
    column_mapping[col_map.get_column_for_inst_hier_map()[1]] = 'TO_BE_DESIGNED'

    column_types = get_table_column_types(conf, target_table, list(column_mapping.keys()))
    # create insertion query
    query = create_insert_query(conf, source_table, target_table, column_mapping, column_types)
    print("*******%s" % query)
    conn.close()


def get_asmt_rec_id(conf, guid_column_name_in_target, guid_column_name_in_source, rec_id_column_name, target_table_name, source_table_name):
    # connect to integration table, to get guid_column_value
    conn_to_source_db, _engine = connect_db(conf['db_user'], conf['db_password'], conf['db_host'], conf['db_name'])
    query_to_get_guid = "SELECT DISTINCT {guid_column_name_in_source} FROM \"{source_schema}\".\"{source_table}\" WHERE batch_id={batch_id}".format(
                                                                                                                                  guid_column_name_in_source=guid_column_name_in_source,
                                                                                                                                  source_schema=conf['source_schema'],
                                                                                                                                  source_table=source_table_name,
                                                                                                                                  batch_id=conf['batch_id']
                                                                                                                                  )
    print(query_to_get_guid)
    guid_column_value = execute_query_get_one_value(conn_to_source_db, query_to_get_guid, guid_column_name_in_source)
    conn_to_source_db.close()

    # connect to target table, to get rec_id_column_value
    conn_to_target_db, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    query_to_get_rec_id = "SELECT DISTINCT {rec_id_column_name} FROM \"{target_schema}\".\"{target_table_name}\" WHERE {guid_column_name_in_target}=\'{guid_column_value_got}\'".format(
                                                                                                                      rec_id_column_name=rec_id_column_name,
                                                                                                                      target_schema=conf['target_schema'],
                                                                                                                      target_table_name=target_table_name,
                                                                                                                      guid_column_name_in_target=guid_column_name_in_target,
                                                                                                                      guid_column_value_got=guid_column_value
                                                                                                                      )
    print(query_to_get_rec_id)
    asmt_rec_id = execute_query_get_one_value(conn_to_target_db, query_to_get_rec_id, rec_id_column_name)
    conn_to_target_db.close()
    return asmt_rec_id


def execute_query_get_one_value(conn, query, column_name):
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
        one_value_result = ['-1']
    return one_value_result[0]


def get_section_rec_id():
    # need to read the fake value from conf file
    return '1', 'section_rec_id'


def get_rec_id_map(conf, target_schema, table_dim_inst_hier, column_inst_hier_rec_id, batch_id):
    # connect to integration table, to get guid_column_value
    conn_to_source_db, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    rec_id_map = {}
    guids_in_hier, inst_hier_rec_id = col_map.get_column_for_inst_hier_map()
    # column_map = col_map.get_column_mapping()[table_dim_inst_hier]
    # guids_in_integration = [column_map[column_name] for column_name in guids_in_hier]
    # create a map which defines the mapping of {(state_code, district_guid, section_guid): inst_hier_rec_id}
    query_to_get_map = ["SELECT DISTINCT ",
                        ",".join(guids_in_hier), ",", inst_hier_rec_id,
                        " FROM \"",
                        target_schema, "\".\"", table_dim_inst_hier, "\""
                        ]
    query_to_get_map = "".join(query_to_get_map)
    print(query_to_get_map)
    try:
        result = conn_to_source_db.execute(query_to_get_map)
        for row in result:
            key = row[0: len(guids_in_hier)]
            value = row[len(guids_in_hier)]
            rec_id_map[tuple(key)] = value
    except Exception as e:
        print(e)
    conn_to_source_db.close()
    return rec_id_map


def explode_data_to_dim_table(conf, db_user, db_password, db_host, db_name, source_table, target_table, column_mapping, column_types):
    '''
    Will use parameters passed in to create query with sqlalchemy
    '''
    # create db connection
    conn, _engine = connect_db(db_user, db_password, db_host, db_name)

    # create insertion query
    query = create_insert_query(conf, source_table, target_table, column_mapping, column_types)
    # print(query)

    # execute the query
    # print("Executing query... %s, %s " % (target_table, query))
    # if target_table in ['dim_asmt']:
    execute_queries(conn, [query], 'Exception -- exploding data from integration to target')
    conn.close()


def create_insert_query(conf, source_table, target_table, column_mapping, column_types):
    seq_expression = list(column_mapping.values())[0].replace("'", "''''")
    insert_sql = ["SELECT dblink_exec(\'dbname={db_name_target} user={db_user_target} password={db_password_target}\',"
             "\'INSERT INTO \"{target_schema}\".\"{target_table}\"(",
             ",".join(list(column_mapping.keys())),
             ")  SELECT * FROM dblink(\''dbname={db_name} user={db_user} password={db_password}\'', \''SELECT {seq_expression}, * FROM (SELECT DISTINCT ",
             ",".join(value.replace("'", "''''") for value in list(column_mapping.values())[1:]),
             " FROM \"{source_schema}\".\"{source_table}\" WHERE batch_id={batch_id}) as y\'') AS t(",
             ",".join(list(column_types.values())),
             ") ;\');"
            ]
    insert_sql = "".join(insert_sql).format(db_name_target=conf['db_name_target'],
                                            db_user_target=conf['db_user_target'],
                                            db_password_target=conf['db_password_target'],
                                            target_schema=conf['target_schema'],
                                            target_table=target_table,
                                            db_name=conf['db_name'],
                                            db_user=conf['db_user'],
                                            db_password=conf['db_password'],
                                            seq_expression=seq_expression,
                                            source_schema=conf['source_schema'],
                                            source_table=source_table,
                                            batch_id=conf['batch_id'])

    return insert_sql


def get_table_column_types(conf, target_table, column_names):
    column_types = OrderedDict([(column_name, '') for column_name in column_names])
    conn, _engine = connect_db(conf['db_user_target'], conf['db_password_target'], conf['db_host_target'], conf['db_name_target'])
    query = create_information_query(conf, target_table)
    # print(query)
    # execute queries
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
    select_query = ["SELECT * FROM dblink(\'dbname={db_name_target} user={db_user_target} password={db_password_target}\',"
                    "\'SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name=\''{target_table}\''')"
                    " AS t1(column_name varchar(256), data_type varchar(256), character_maximum_length integer);"
                    ]
    select_query = "".join(select_query).format(db_name_target=conf['db_name_target'],
                                                db_user_target=conf['db_user_target'],
                                                db_password_target=conf['db_password_target'],
                                                target_table=target_table)
    return select_query
