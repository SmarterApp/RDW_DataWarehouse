"""This is the general PostgreSQL writer.

:author: gkathuria
:date: March 31, 2014
"""

import psycopg2

import data_generation.writers.filters as writers_filters
import data_generation.writers.util as writers_util


available_filters = writers_filters.FILTERS


def register_filters(filters):
    """Add custom filters to the CSV writer filtering register.

    :param filters: A dictionary of filters to register
    """
    global available_filters
    available_filters = dict(list(available_filters.items()) + list(filters.items()))


def create_dbcon(host, port, dbname, user, password):
    conn_string = "host=%s port=%s dbname=%s user=%s password=%s" %(host,port,dbname,user,password)
    print("connecting to database %s" %conn_string)
    conn = psycopg2.connect(conn_string)
    return conn


def create_table(conn, tblname, columns=None):
    """Create the table with columns and types provided in Postgres database

    :param conn: Connection to PostgresSQL database created using create_dbconn
    :param table: Name of the table
    :param columns: The columns that define the structure of the table
    """
    cursor = conn.cursor()

    stmt=''
    for c in columns:
        colnametype = c['name']+' '+c['type']
        stmt = stmt+colnametype+','

    print("drop table if exists %s" % tblname[:-4])
    print("create table %s (%s)" % (tblname[:-4], stmt[:-1]))

    cursor.execute("drop table if exists %s" % tblname[:-4])
    cursor.execute("create table %s (%s)" % (tblname[:-4], stmt[:-1]))

    conn.commit()


def write_records_to_table(conn, tbl_name, columns, entities, entity_filter=None):
    """For a list of entity objects, write a record to an output path. This requires that the objects in the entities
    parameter have a 'get_object_set' method that returns a dictionary of objects whose attributes are available.

    :param conn: Connection to PostgresSQL database created using create_dbconn
    :param tbl_name: Name of table this row is being generated for (optional). This is used to generate unique record
                     ID values that are unique within a given table.
    :param columns: The dictionary of columns for data values to write for each entity
    :param entities: A list of entity objects to write out to the table
    :param entity_filter: An (attribute, value) tuple that will be evaluated against each object in entities to see if
                          that object should be written to the table. If not provided, all entities are written to file.
                          The attribute is expected to be directly on the entity and is not checked (will raise an
                          exception if not present).
    """
    cursor = conn.cursor()

    num_col = len([i['name'] for i in columns])
    tbl_ins = "insert into %s (%s) values" % (tbl_name, ', '.join(column['name'] for column in columns))

    lst = ['%s' for _ in range(num_col)]
    col_list = ','.join(lst)

    stmt = tbl_ins + '('+col_list+')'

    # Get each row of data
    params = []
    for entity in entities:
        if entity_filter is None or getattr(entity, entity_filter[0]) == entity_filter[1]:
            params.append(writers_util.build_csv_row_values(entity.get_object_set(), columns, available_filters,
                                                            tbl_name))

    # Write all rows
    try:
        cursor.executemany(stmt, params)

    except psycopg2.DataError as e:
        print("NAME: ", tbl_name)
        print("#COLS:", num_col)
        print("STMT: ", stmt)
        print("PARAMS: ", tuple(zip((column['name'] for column in columns), params[0])))
        raise

    except psycopg2.IntegrityError as e:
        print("NAME: ", tbl_name)
        print("#COLS:", num_col)
        print("STMT: ", stmt)
        print("PARAMS: ", tuple(zip((column['name'] for column in columns), params[0])))
        raise

    # Cleanup
    cursor.close()
    conn.commit()
