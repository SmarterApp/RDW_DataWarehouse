# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Mar 5, 2013

@author: tosako
'''
from edschema.database.connector import DBConnection
from edschema.metadata.stats_metadata import generate_stats_metadata

config_namespace = 'edware_stats.db'


class StatsDBConnection(DBConnection):
    '''
    DBConnector for UDL Stats

    Stats Database is NOT tenant specific, there is only one config per install

    '''

    def __init__(self, **kwargs):
        super().__init__(name=self.get_datasource_name(**kwargs))

    @staticmethod
    def get_namespace():
        return config_namespace + "."

    @staticmethod
    def get_datasource_name(**kwargs):
        '''
        Returns datasource name for UDL Stats
        '''
        return config_namespace

    @staticmethod
    def get_db_config_prefix(**kwargs):
        '''
        Returns db configuration prefix for UDL Stats
        '''
        return StatsDBConnection.get_namespace()

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Returns the generated metadata for UDL Stats
        '''
        return generate_stats_metadata(schema_name=schema_name, bind=bind)
