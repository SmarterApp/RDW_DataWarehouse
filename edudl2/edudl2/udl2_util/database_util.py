'''
Created on May 22, 2013

@author: ejen
'''
from sqlalchemy.sql.expression import text
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
import re
from edudl2.udl2_util.exceptions import UDL2SQLFilteredSQLStringException


def connect_db(db_driver, db_user, db_password, db_host, db_port, db_name):
    '''
    DO NOT USE THIS!!!!
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


def print_get_affected_rows(result, action, module, function):
    '''
    get affected rows of a query execution and return the info
    '''
    return {'amount': result.rowcount, 'action': action, 'unit': 'rows', 'module': module, 'function': function}


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
        raise


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
        raise


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


def create_filtered_sql_string(query, **kwargs):
    '''
    create string for SQL statement
    '''
    return _create_filtered_string(query, '-_', **kwargs)


def create_filtered_filename_string(query, **kwargs):
    return _create_filtered_string(query, '-_./', **kwargs)


def _create_filtered_string(query, allow_special_chars, **kwargs):
    '''
    create filtered string
    '''
    for value in kwargs.values():
        if type(value) is str:
            if not re.sub('[' + allow_special_chars + ']', '', value).isalnum():
                raise UDL2SQLFilteredSQLStringException('Name contained invalid characters[' + value + ']')
        elif type(value) is int:
            pass
        else:
            raise UDL2SQLFilteredSQLStringException('Type of Name was not string or integer')
    return query.format(**kwargs)
