'''
Created on Jan 29, 2014

@author: sravi
'''
from database.connector import DBConnection
from sqlalchemy import schema

config_namespace = 'edware_rep.db'


class RepMgrDBConnection(DBConnection):
    '''
    DBConnector for Connecting to RepMgr Schema
    This is used for database connection for replication monitoring
    '''

    def __init__(self, tenant=''):
        super().__init__(name=self.get_datasource_name(tenant))

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
        return RepMgrDBConnection.get_namespace() + tenant if tenant else RepMgrDBConnection.get_namespace()

    @staticmethod
    def get_db_config_prefix(tenant=None):
        '''
        Returns database config prefix based on tenant name
        '''
        return RepMgrDBConnection.get_namespace() + tenant + '.' if tenant else RepMgrDBConnection.get_namespace()

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Generates metadata for repmgr
        '''
        metadata = schema.MetaData(bind=bind, schema=schema_name)
        metadata.reflect(views=True)
        return metadata
