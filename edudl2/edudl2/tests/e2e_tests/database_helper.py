'''
Created on Mar 19, 2014

@author: dip
'''
from edudl2.udl2.udl2_connector import get_target_connection
from sqlalchemy.schema import DropSchema


def drop_target_schema(schema_name):
    pass
#    with get_target_connection() as connector:
#        connector.set_metadata(schema_name, reflect=True)
#        metadata = connector.get_metadata()
#        metadata.drop_all()
#        connector.execute(DropSchema(schema_name, cascade=True))
