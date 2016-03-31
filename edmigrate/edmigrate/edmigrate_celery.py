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

__author__ = 'sravi'
from edcore.database.stats_connector import StatsDBConnection
from edworker.celery import setup_celery as setup_for_worker, configure_celeryd, get_config_file
from edmigrate.settings.config import setup_settings
import logging
import logging.config
from edcore.database import initialize_db
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.utils.constants import Constants


logger = logging.getLogger(Constants.WORKER_NAME)
PREFIX = 'migrate.celery'


def setup_celery(settings, prefix=PREFIX):
    '''
    Setup celery based on parameters defined in setting (ini file).
    This calls by client application when dictionary of settings is given

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    setup_for_worker(celery, settings, prefix)
    setup_settings(settings)


# Create an instance of celery, check if it's for prod celeryd mode and configure it for prod mode if so
celery, conf = configure_celeryd(PREFIX, prefix=PREFIX)
prod_config = get_config_file()
if prod_config:
    # We should only need to setup db connection in prod mode
    # setup_db_connection(conf)
    initialize_db(RepMgrDBConnection, conf)
    initialize_db(StatsDBConnection, conf)
    setup_settings(conf)
    logging.config.fileConfig(prod_config)
