'''
Entry point for migrating data from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
import configparser
import sys
from edmigrate.utils.migrate import start_migrate_daily_delta
import os
from edcore.database import initialize_db
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edmigrate.database.repmgr_connector import RepMgrDBConnection


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


def main(file=None, tenant='cat'):
    if file is None:
        file = get_ini_file()
    settings = read_ini(file)
    initialize_db(RepMgrDBConnection, settings)
    initialize_db(StatsDBConnection, settings)
    initialize_db(EdMigrateSourceConnection, settings)
    initialize_db(EdMigrateDestConnection, settings)
    start_migrate_daily_delta(tenant)


if __name__ == '__main__':
    # Entry point for testing migration
    # python main.py [tenant]
    tenant = 'cat'
    if len(sys.argv) > 1:
        tenant = sys.argv[1]
    main(tenant=tenant)
