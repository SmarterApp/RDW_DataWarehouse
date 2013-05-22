from sqlalchemy.engine import create_engine

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