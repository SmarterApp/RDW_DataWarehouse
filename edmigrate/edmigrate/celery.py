__author__ = 'sravi'

from edworker.celery import setup_celery as setup, configure_celeryd,\
    get_config_file
from edmigrate.settings.config import setup_settings
from edcore.database import initialize_db
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
import logging

logger = logging.getLogger('edmigrate')
PREFIX = 'migrate.celery'


def setup_celery(settings, prefix=PREFIX):
    '''
    Setup celery based on parameters defined in setting (ini file).
    This calls by client application when dictionary of settings is given

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    setup(celery, settings, prefix)
    setup_settings(settings)


def setup_db_connection(settings):
    initialize_db(RepMgrDBConnection, settings)
    initialize_db(StatsDBConnection, settings)
    initialize_db(EdMigrateSourceConnection, settings)
    initialize_db(EdMigrateDestConnection, settings)


# Create an instance of celery, check if it's for prod celeryd mode and configure it for prod mode if so
celery, conf = configure_celeryd(PREFIX, prefix=PREFIX)
prod_config = get_config_file()
if prod_config:
    # We should only need to setup db connection in prod mode
    setup_db_connection(conf)
    setup_settings(conf)
