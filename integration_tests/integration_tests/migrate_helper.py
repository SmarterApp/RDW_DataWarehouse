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

'''
Used for tests to migrate from pre-prod to prod

Created on Mar 13, 2014

@author: dip
'''
from edmigrate.main import migrate_only, read_ini, get_ini_file
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import select, and_
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from edcore.database import initialize_db


# def setUpMigrationConnection():
#     setting = get_config()
#     initialize_db(StatsDBConnection, setting)
#     initialize_db(EdMigrateDestConnection, setting)


def start_migrate(tenant='cat'):
    '''
    Migrate from pre-prod to prod
    '''
    ini_file = get_ini_file()
    settings = read_ini(ini_file)
    migrate_only(settings, tenant)


# def get_config():
#     return read_ini(get_ini_file())


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
