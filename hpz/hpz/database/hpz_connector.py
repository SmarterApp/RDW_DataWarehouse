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

from edschema.database.generic_connector import setup_db_connection_from_ini
from edschema.database.connector import DBConnection
from hpz.database.metadata import generate_metadata

__author__ = 'npandey'

HPZ_NAMESPACE = 'hpz_db_conn'


class HPZDBConnection(DBConnection):
    """
    DBConnector for the HPZ Database
    """
    def __init__(self, namespace=HPZ_NAMESPACE):
        super().__init__(name=namespace)


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
        'schema_name': settings['hpz.db.schema_name'],
        'pool_size': settings['hpz.db.pool_size']
    }
    setup_db_connection_from_ini(settings, '', metadata_generator, datasource_name, allow_schema_create)
