from edschema.database.connector import DBConnection
from smarter_score_batcher.database.metadata import generate_tsb_metadata

config_namespace = 'smarter_score_batcher.db'


class TSBDBConnection(DBConnection):
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
        return TSBDBConnection.get_namespace()

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Returns the generated metadata for UDL Stats
        '''
        return generate_tsb_metadata(schema_name=schema_name, bind=bind)
