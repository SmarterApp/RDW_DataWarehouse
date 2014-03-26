'''
Created on Mar 24, 2014

@author: dip
'''
from sqlalchemy.sql import select
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.sql.expression import bindparam, text


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


def create_schema(connector, metadata_generator, schema_name, drop_if_exists=True):
    """
    Creates a schema defined by the connector database and metadata

    @param connector: connection to the database
    @param schema_name: name of the schema to be dropped
    """
    engine = connector.get_engine()
    if drop_if_exists and schema_exists(connector, schema_name):
        drop_schema(connector, schema_name)
    connector.execute(CreateSchema(schema_name))
    metadata = metadata_generator(schema_name=schema_name, bind=engine)
    metadata.create_all()


def drop_schema(connector, schema_name):
    """
    Drops the entire schema

    @param connector: connection to the database
    @param schema_name: name of the schema to be dropped
    """
    if schema_exists(connector, schema_name):
        connector.set_metadata_by_reflect(schema_name)
        metadata = connector.get_metadata()
        metadata.drop_all()
        connector.execute(DropSchema(schema_name, cascade=True))
