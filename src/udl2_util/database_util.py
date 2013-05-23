'''
Created on May 22, 2013

@author: ejen
'''

from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import func, text

def connect_db(db_driver, db_user, db_password, db_host, db_port, db_name):
    '''
    Connect to database via sqlalchemy
    '''

    # TODO:define conf_args content
    db_string = '{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'.format(db_driver=db_driver,
                                                                                            db_user=db_user,
                                                                                            db_password=db_password,
                                                                                            db_host=db_host,
                                                                                            db_port=db_port,
                                                                                            db_name=db_name) 
    # print(db_string)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    return db_connection, engine


def execute_queries(conn, list_of_queries, except_msg):
    trans = conn.begin()
    # execute queries
    try:
        for query in list_of_queries:
            conn.execute(query)
        trans.commit()
    except Exception as e:
        print(except_msg, e)
        trans.rollback()
        
        
def get_table_columns_info(conn, table_name, is_conn_a_dblink=False):
    if is_conn_a_dblink:
        sql_query = text("")
    else: # table is in the local database server
        sql_query = text("SELECT column_name, data_type, character_maximum_length " +
                         "FROM information_schema.columns "
                         "WHERE table_name = \'%s\' " 
                        % (table_name))
    result = conn.execute(sql_query)
    columns = []
    for row in result:
        columns.append((row[0], row[1], row[2]))
    return columns
    


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
