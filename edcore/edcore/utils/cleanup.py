from sqlalchemy.sql import select
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.sql.expression import bindparam, text


def get_filtered_tables(connector, table_name_prefix=None):
    """This function returns list of tables starting with table_name_prefix from schema metadata

    :param connector: The connection to the database
    :returns : A list of table names
             [dim_section, dim_student]
    """
    all_tables = []
    for table in connector.get_metadata().tables:
        # when schema is not specified, database name gets prepended
        if '.' in table:
            table = table.split('.')[1]
        if table_name_prefix is None or table.lower().startswith(table_name_prefix.lower()):
            all_tables.append(table)
    return all_tables


def cleanup_all_tables(connector, column_name, value, batch_delete=True, table_name_prefix=None, tables=None):
    """
    cleanup all tables for the given column and matching value

    All rows matching the given guid_batch will be delted from all the tables
    in the given connector schema
    """
    tables_to_cleanup = get_filtered_tables(connector, table_name_prefix) if tables is None else tables
    for table_name in tables_to_cleanup:
        table = connector.get_table(table_name)
        if column_name in table.columns:
            delete_query = table.delete(table.c[column_name] == value)
            connector.execute(delete_query)


def _get_schema_check_query(schema_name):
    """
    returns the sql query to look for schema presence
    """
    query = select(['schema_name'], from_obj=['information_schema.schemata']).where('schema_name = :schema_name')
    params = [bindparam('schema_name', schema_name)]
    return text(str(query), bindparams=params)


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
    connector.set_metadata(schema_name, reflect=True)
    metadata = connector.get_metadata()
    metadata.drop_all()
    connector.execute(DropSchema(schema_name, cascade=True))
