'''
Used for tests to migrate from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
from edmigrate.main import main, read_ini
import os
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import select, and_
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from edmigrate.celery import setup_db_connection


def setUpMigrationConnection():
    setting = get_config()
    setup_db_connection(setting)


def start_migrate(tenant='cat'):
    '''
    Migrate from pre-prod to prod
    '''
    ini_file = get_ini_file()
    main(ini_file, tenant)


def get_config():
    return read_ini(get_ini_file())


def get_ini_file():
    jenkins_ini = '/opt/edware/conf/smarter.ini'
    if os.path.exists(jenkins_ini):
        ini_file = jenkins_ini
    else:
        here = os.path.abspath(os.path.dirname(__file__))
        ini_file = os.path.join(here, '../../config/development.ini')
    return ini_file


def get_prod_table_count(tenant, table_name):
    '''
    Check count numbers in prod tables
    '''
    with EdMigrateDestConnection(tenant) as conn:
        table = conn.get_table(table_name)
        query = select([count().label('total')],
                       from_obj=[table])
        results = conn.get_result(query)
    return results[0]['total']


def get_stats_table_has_migrated_ingested_status(tenant):
    '''
    Check udl_stats that there is tenant of cat is migrate.ingested
    '''
    with StatsDBConnection() as conn:
        udl_stats = conn.get_table(UdlStatsConstants.UDL_STATS)
        query = select([udl_stats.c.load_status],
                       from_obj=([udl_stats]))
        query = query.where(and_(udl_stats.c.tenant == tenant))
        return conn.get_result(query)
