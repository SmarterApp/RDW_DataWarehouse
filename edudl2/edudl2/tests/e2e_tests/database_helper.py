'''
Created on Mar 19, 2014

@author: dip
'''
from sqlalchemy.schema import DropSchema
from edudl2.database.udl2_connector import get_target_connection


def drop_target_schema(tenant, schema_name):
    with get_target_connection(tenant) as connector:
        try:
            connector.execute(DropSchema(schema_name, cascade=True))
        except:
            pass
