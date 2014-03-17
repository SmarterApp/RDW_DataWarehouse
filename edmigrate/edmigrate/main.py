'''
Entry point for migrating data from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
import configparser
from edmigrate.utils.migrate import start_migrate_daily_delta
import os
from edcore.database import initialize_db
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from kombu import Connection
from edmigrate.conductor_controller import ConductorController
from argparse import ArgumentParser
from edmigrate.utils.utils import get_broker_url
from edmigrate.edmigrate_celery import setup_celery


def get_ini_file():
    '''
    Get ini file path name
    '''
    jenkins_ini = '/opt/edware/conf/smarter.ini'
    if os.path.exists(jenkins_ini):
        ini_file = jenkins_ini
    else:
        here = os.path.abspath(os.path.dirname(__file__))
        ini_file = os.path.join(here, '../../config/development.ini')
    return ini_file


def read_ini(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config['app:main']


def main(file=None, tenant='cat', run_migrate_only=False):
    if file is None:
        file = get_ini_file()
    settings = read_ini(file)
    initialize_db(RepMgrDBConnection, settings)
    initialize_db(StatsDBConnection, settings)
    initialize_db(EdMigrateSourceConnection, settings)
    initialize_db(EdMigrateDestConnection, settings)
    if run_migrate_only:
        start_migrate_daily_delta(tenant)
    else:
        setup_celery(settings)
        url = get_broker_url(settings)
        with Connection(url) as connect:
            controller = ConductorController(connect)
            controller.start()


if __name__ == '__main__':
    # Entry point for testing migration
    # python main.py -t dog --migrateOnly
    parser = ArgumentParser(description='EdMigrate entry point')
    parser.add_argument('--migrateOnly', action='store_true', dest='migrate_only', default=False, help="migrate only mode")
    parser.add_argument('-t', dest='tenant', default='cat', help="tenant name")
    args = parser.parse_args()
    main(tenant=args.tenant, run_migrate_only=args.migrate_only)
