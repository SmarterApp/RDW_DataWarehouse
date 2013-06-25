'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from edschema.metadata.ed_metadata import generate_ed_metadata

config_namespace = 'edware.db'


class SmarterDBConnection(DBConnection):
    '''
    DBConnector for Smarter Project
    a name is required for tenancy database connection lookup
    '''

    def __init__(self, tenant=None):

        if tenant is None:
            # Get user's tenant from session
            __user = authenticated_userid(get_current_request())
            if __user:
                tenant = __user.get_tenant()
            else:
                # TODO: have to fix this edge case
                pass
        super().__init__(name=self.get_datasource_name(tenant))

    @staticmethod
    def get_datasource_name(tenant=None):
        if tenant is None:
            return config_namespace
        return config_namespace + '.' + tenant

    @staticmethod
    def get_db_config_prefix(tenant=None):
        if tenant is None:
            return config_namespace + '.'
        return config_namespace + '.' + tenant + '.'

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        return generate_ed_metadata(schema_name=schema_name, bind=bind)
