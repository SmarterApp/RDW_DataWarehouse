'''
Entry point for migrating data from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
import configparser
import sys
from edmigrate.celery import setup_db_connection
from edmigrate.utils.migrate import start_migrate_daily_delta


def read_ini(file):
    # Entry point for testing migration
    # python migrate.py dev.ini cat
    config = configparser.ConfigParser()
    config.read(file)
    return config['app:main']


def main(file, tenant):
    # Entry point for testing migration
    # python migrate.py dev.ini cat
    settings = read_ini(file)
    setup_db_connection(settings)
    start_migrate_daily_delta(tenant)


if __name__ == '__main__':
    # Entry point for testing migration
    # python migrate.py dev.ini cat
    main(sys.argv[1], sys.argv[2])
