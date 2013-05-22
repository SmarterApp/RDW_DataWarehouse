from fileloader.file_loader import connect_db, execute_queries
from collections import OrderedDict


DBDRIVER = "postgresql"


def explode_data_to_fact_table(conf, db_user_target, db_password_target, db_host_target, db_name_target, source_table, target_table, column_mapping, column_types):
    pass
    # create db connection
    conn, _engine = connect_db(db_user_target, db_password_target, db_host_target, db_name_target)

    # get section_rec_id
    # get asmt_rec_id
    # get inst_hier_rec_id

    conn.close()


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
    # temp:
    if target_table in ['dim_staff', 'dim_inst_hier', 'dim_student']:
        print("Executing query... %s, %s " % (target_table, query))
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
