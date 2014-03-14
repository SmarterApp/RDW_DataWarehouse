'''
Created on Jan 29, 2014

@author: sravi
'''
from database.connector import DBConnection

config_namespace = 'edware_rep.db'


class RepMgrDBConnection(DBConnection):
    '''
    DBConnector for Connecting to RepMgr Schema
    This is used for database connection for replication monitoring
    '''

    def __init__(self, tenant):
        super().__init__(name=self.get_datasource_name(tenant))

    def get_metadata(self, schema_name=None):
        return super(RepMgrDBConnection, self).get_metadata(schema_name=schema_name)

    @staticmethod
    def get_namespace():
        '''
        Returns the namespace of RepMgr database connection
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
        return RepMgrDBConnection.get_namespace() + tenant

    @staticmethod
    def get_db_config_prefix(tenant=None):
        '''
        Returns database config prefix based on tenant name
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return RepMgrDBConnection.get_namespace() + tenant + '.'

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Generates metadata for repmgr
        '''
        return None
