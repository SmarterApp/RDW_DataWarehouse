__author__ = 'sravi'

from sqlalchemy.sql.expression import text, bindparam
from sqlalchemy.sql import select
from sqlalchemy.schema import CreateSchema, DropSchema


def get_filtered_tables(connector, table_name_prefix=None):
    """This function returns list of tables starting with table_name_prefix from schema metadata

    :param connector: The connection to the database
    :returns : A list of table names
             [dim_section, dim_student]
    """
    all_tables = []
    for table in connector.get_metadata().tables.keys():
        if '.' in table:
            all_tables.append(table.split('.')[1])
        else:
            all_tables.append(table)
    if table_name_prefix is not None:
        all_tables = [table for table in all_tables if table.lower().startswith(table_name_prefix.lower())]
    return all_tables


def _get_schema_table_name(schema_name, table_name):
    return '\"' + schema_name + '\".' + '\"' + table_name + '\"' \
           if schema_name is not None else '\"' + table_name + '\"'


def get_delete_table_query(schema_name, table_name, column_name, value, batch_size, row_locator):
    query_template = "DELETE FROM {schema_table_name} WHERE {row_locator} IN " +\
                     "(SELECT {row_locator} FROM {schema_table_name} WHERE {column_name} = :value " +\
                     "ORDER BY {row_locator} LIMIT :batch_size)"
    query = query_template.format(schema_table_name=_get_schema_table_name(schema_name, table_name),
                                  column_name=column_name,
                                  row_locator=row_locator)
    params = [bindparam('value', value), bindparam('batch_size', batch_size)]
    return text(query, bindparams=params)


def _delete_rows_in_batches(connector, schema_name, table_name, column_name, value, row_locator, batch_size=10000):
    rows_deleted = -1
    query_to_delete_rows = get_delete_table_query(schema_name, table_name, column_name, value, batch_size, row_locator)
    while rows_deleted is not 0:
        result = connector.execute(query_to_delete_rows)
        rows_deleted = result.rowcount


def _delete_all_rows(connector, table, column_name, value):
    delete_query = table.delete(table.c[column_name] == value)
    connector.execute(delete_query)


def cleanup_table(connector, schema_name, column_name, value, batch_delete, table_name, row_locator='ctid'):
    """
    cleanup table for the given column and value
    """
    table = connector.get_table(table_name)
    if column_name in table.columns:
        if not batch_delete:
            _delete_all_rows(connector, table, column_name, value)
        else:
            _delete_rows_in_batches(connector, schema_name, table_name, column_name, value, row_locator)


def cleanup_all_tables(connector, schema_name, column_name, value, batch_delete=True, table_name_prefix=None, tables=None):
    """
    cleanup all tables for the given column and matching value

    All rows matching the given guid_batch will be delted from all the tables
    in the given connector schema
    """
    tables_to_cleanup = get_filtered_tables(connector, table_name_prefix) if tables is None else tables
    for table in tables_to_cleanup:
        cleanup_table(connector, schema_name, column_name, value, batch_delete, table)


def _get_schema_check_query(schema_name):
    """
    returns the sql query to look for schema presence
    """
    return select([("schema_name")]).select_from("information_schema.schemata").where("schema_name = '" + schema_name + "'")


def schema_exists(connector, schema_name):
    """
    check if schema with the given name exists in the database defined by given connection
    """
    query = _get_schema_check_query(schema_name)
    result = connector.execute(query).fetchone()
    return True if result is not None else False


def create_schema(connector, metadata_generator, schema_name):
    """
    Creates a schema defined by the connector database and metadata

    @param connector: connection to the database
    @param schema_name: name of the schema to be dropped
    """
    engine = connector.get_engine()
    connector.execute(CreateSchema(schema_name))
    metadata = metadata_generator(schema_name=schema_name, bind=engine)
    metadata.create_all()


def drop_schema(connector, schema_name):
    """
    Drops the entire schema

    @param connector: connection to the database
    @param schema_name: name of the schema to be dropped
    """
    metadata = connector.get_metadata(schema_name=schema_name)
    metadata.drop_all()
    connector.execute(DropSchema(schema_name, cascade=True))
