'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from edschema.metadata.ed_metadata import generate_ed_metadata

config_namespace = 'edware.db'


class EdCoreDBConnection(DBConnection):
    '''
    DBConnector for Smarter Project
    This is used for database connection for reports
    '''

    def __init__(self, tenant=None):

        if tenant is None:
            # Get user's tenant from session
            __user = authenticated_userid(get_current_request())
            if __user:
                # User object has a list of tenant.  Retrieve the first element
                tenant = __user.get_tenants()[0]
        super().__init__(name=self.get_datasource_name(tenant))

    @staticmethod
    def get_namespace():
        '''
        Returns the namespace of smarter database connection
        '''
        return config_namespace + '.'

    @staticmethod
    def get_datasource_name(tenant=None):
        '''
        Returns datasource name for a tenant
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return EdCoreDBConnection.get_namespace() + tenant

    @staticmethod
    def get_db_config_prefix(tenant=None):
        '''
        Returns database config prefix based on tenant name
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return EdCoreDBConnection.get_namespace() + tenant + '.'

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Generates metadata for edware
        '''
        return generate_ed_metadata(schema_name=schema_name, bind=bind)
