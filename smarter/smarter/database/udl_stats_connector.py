'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection
from edschema.metadata.stats_metadata import generate_stats_metadata

config_namespace = 'edware_stats.db'


class StatsDBConnection(DBConnection):
    '''
    DBConnector for Stats
    '''

    def __init__(self, tenant=None):
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
        return generate_stats_metadata(schema_name=schema_name, bind=bind)
