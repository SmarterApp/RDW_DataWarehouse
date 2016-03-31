# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from edschema.database.connector import DBConnection
from smarter_score_batcher.database.metadata import generate_tsb_metadata

config_namespace = 'smarter_score_batcher.db'


class TSBDBConnection(DBConnection):
    '''
    DBConnector for Smarter Score Batcher

    TSB Database is NOT tenant specific, there is only one config per install

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
        return TSBDBConnection.get_namespace()

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Returns the generated metadata for UDL Stats
        '''
        return generate_tsb_metadata(schema_name=schema_name, bind=bind)
