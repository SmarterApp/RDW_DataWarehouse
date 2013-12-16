'''
Created on May 22, 2013

@author: ejen
'''

from collections import OrderedDict

from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import text
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker


def print_get_affected_rows(result, action, module, function):
    '''
    get affected rows of a query execution and return the info
    '''
    return {'amount': result.rowcount, 'action': action, 'unit': 'rows', 'module': module, 'function': function}


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


def execute_udl_queries(conn, list_of_queries, except_msg, caller_module=None, caller_func=None):
    """
    This should be used when celery is running and db engines have been registered with zope
    :param conn: instance of DBConnection or one of its sub-classes (see udl2/udl2_connector.py)
    :param query: Query to execute
    :param except_msg: Exception string
    :return: row_affected_list
    """
    trans = conn.get_transaction()
    # execute queries
    try:
        row_affected_list = []
        for query in list_of_queries:
            result = conn.execute(query)
            count = result.rowcount
            row_affected_list.append(count)
        trans.commit()
        return row_affected_list
    except Exception as e:
        print(except_msg, e)
        trans.rollback()


def execute_udl_query_with_result(conn, query, except_msg, caller_module=None, caller_func=None):
    """
    This should be used when celery is running and db engines have been registered with zope
    :param conn: instance of DBConnection or one of its sub-classes (see udl2/udl2_connector.py)
    :param query: Query to execute
    :param except_msg: Exception string
    :return: result
    """
    trans = conn.get_transaction()
    # execute queries
    try:
        result = conn.execute(query)
        trans.commit()
        return result
    except Exception as e:
        print(except_msg, e)
        trans.rollback()


def execute_queries(conn, list_of_queries, except_msg, caller_module=None, caller_func=None):
    """
    This should be used when celery is NOT running
    :param conn: instance of DBConnection or one of its sub-classes (see udl2/udl2_connector.py)
    :param query: Query to execute
    :param except_msg: Exception string
    :return: row_affected_list
    """
    trans = conn.begin()
    # execute queries
    try:
        row_affected_list = []
        for query in list_of_queries:
            result = conn.execute(query)
            count = result.rowcount
            row_affected_list.append(count)
        trans.commit()
        return row_affected_list
    except Exception as e:
        print(except_msg, e)
        trans.rollback()


def execute_query_with_result(conn, query, except_msg, caller_module=None, caller_func=None):
    """
    This should be used when celery is running and db engines have been registered with zope
    :param conn: instance of DBConnection or one of its sub-classes (see udl2/udl2_connector.py)
    :param query: Query to execute
    :param except_msg: Exception string
    :return: result
    """
    trans = conn.begin()
    # execute queries
    try:
        result = conn.execute(query)
        trans.commit()
        return result
    except Exception as e:
        print(except_msg, e)
        trans.rollback()


def get_table_columns_info(conn, table_name, is_conn_a_dblink=False):
    if is_conn_a_dblink:
        sql_query = text("")
    else:  # table is in the local database server
        sql_query = text("SELECT DISTINCT column_name, data_type, character_maximum_length " +
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


def get_schema_metadata(db_engine, schema_name=None):
    '''
    Get the SQLAlchemy MetaData object
    @param db_engine: a SQLAlchemy engine object returned connect_db method
    @type db_engine: sqlalchemy.engine
    @param schema_name: the name of the schema to use in getting the MetaData
    @type schema_name: str
    @return: A MetaData object corresponding to the given schema and engine
    @rtype: sqlalchemy.schema.MetaData
    '''

    metadata = MetaData()
    metadata.reflect(db_engine, schema_name)
    return metadata


def get_sqlalch_table_object(db_engine, schema_name, table_name):
    '''
    Get a SQLAlchemy table object for the given table and schema name
    @param db_engine: a SQLAlchemy engine object returned connect_db method
    @type db_engine: sqlalchemy.engine
    @param schema_name: the name of the schema to use in getting the MetaData
    @type schema_name: str
    @param table_name: the name of the table to get
    @type table_name: str
    @return: A table object from SQLAlchemy
    @rtype: sqlalchemy.schema.Table
    '''

    metadata = get_schema_metadata(db_engine, schema_name)
    table = metadata.tables[schema_name + '.' + table_name]
    return table


def create_sqlalch_session(db_engine):
    '''
    Create and return a sqlalchemy session for the given engine
    @param db_engine: a SQLAlchemy engine object returned connect_db method
    @type db_engine: qlalchemy.engine.base.Engine
    @return: A sqlqlchemy session
    @rtype: sqlalchemy.orm.session.Session
    '''

    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session
