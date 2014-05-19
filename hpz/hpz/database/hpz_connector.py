from edschema.database.generic_connector import setup_db_connection_from_ini
from edschema.database.connector import DBConnection
from hpz.database.metadata import generate_metadata

__author__ = 'npandey'

HPZ_NAMESPACE = 'hpz_db_conn'


class HPZDBConnection(DBConnection):
    """
    DBConnector for the UDL Database
    """
    def __init__(self, namespace=HPZ_NAMESPACE):
        self.datasource_name = namespace
        super().__init__(name=self.datasource_name)

    def get_namespace(self):
        return self.namespace

    def get_datasource_name(self):
        '''
        Returns datasource name for UDL Stats
        '''
        return self.datasource_name


def get_hpz_connection():
    '''
    Get HPZ connection
    '''
    return HPZDBConnection(namespace=HPZ_NAMESPACE)


def initialize_db(settings):
    create_sqlalchemy(HPZ_NAMESPACE, settings, False, generate_metadata)


def create_sqlalchemy(namespace, settings, allow_schema_create, metadata_generator):

    datasource_name = namespace

    settings = {
        'url': settings['hpz.db.url'],
        'schema_name': settings['hpz.db.schema_name']
    }
    setup_db_connection_from_ini(settings, '', metadata_generator, datasource_name, allow_schema_create)
