__author__ = 'sravi'

from sqlalchemy.sql.expression import select

from edmigrate.utils.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.edcore_connector import EdCoreDBConnection

# TODO: remove this. temp thing
import edmigrate.celery


def query_daily_delta_batches_to_migrate(connector):
    """
    query daily batches to be migrated
    """
    udl_daily_status_table = connector.get_table(Constants.UDL_DAILY_STATS_TABLE)
    query = select([udl_daily_status_table.c.batch_guid,
                    udl_daily_status_table.c.tenant,
                    udl_daily_status_table.c.file_arrived],
                   from_obj=[udl_daily_status_table]).order_by(udl_daily_status_table.c.file_arrived)
    udl_daily_status_rows = connector.get_result(query)
    return udl_daily_status_rows


def get_daily_delta_batches_to_migrate():
    '''
    get list of batches to be migrated to prod
    '''
    print('Master: Getting daily delta batches to migrate')
    with StatsDBConnection() as connector:
        batches_to_be_migrated = query_daily_delta_batches_to_migrate(connector)
    return batches_to_be_migrated


def get_source_key(tenant):
    #TODO: return the actual source prefix key
    return 'cat'


def get_dest_key(tenant):
    #TODO: return the actual dest prefix key
    return 'dog'


def migrate_fact_from_preprod_to_prod(batch_guid, source_connector, dest_connector, batch_size=100):
    """
    Load prod fact table with delta from pre-prod
    """
    source_tab = source_connector.get_table('fact_asmt_outcome')
    dest_Tab = dest_connector.get_table('fact_asmt_outcome')
    query = source_tab.select().where(source_tab.c.batch_guid == batch_guid).limit(batch_size)
    result_rows = source_connector.execute(query)
    fao_rows = result_rows.fetchall()
    insert_query = dest_Tab.insert()
    dest_connector.execute(insert_query, False, fao_rows)


def migrate_fact(batch_guid, pre_prod_connection, prod_connection):
    """
    Migrate fact
    """
    print('Migrating fact for batch: ' + batch_guid)
    migrate_fact_from_preprod_to_prod(batch_guid, pre_prod_connection, prod_connection)


def migrate_dims(batch_guid, pre_prod_connection, prod_connection):
    """
    Migrate all the dimension tables
    """
    print('Migrating dimensions for batch: ' + batch_guid)
    pass


def migrate_batch(batch_guid, tenant):
    """
    Migrate the entire batch with in a transaction
    """
    print('Migrating batch: ' + batch_guid + ', tenant: ' + tenant)
    source = get_source_key(tenant)
    dest = get_dest_key(tenant)
    # TODO: EdCoreConnection will be replaced with real one later
    with EdCoreDBConnection(dest) as prod_connection, \
            EdCoreDBConnection(source) as pre_prod_connection:
        try:
            trans = prod_connection.get_transaction()
            migrate_fact(batch_guid, pre_prod_connection, prod_connection)
            migrate_dims(batch_guid, pre_prod_connection, prod_connection)
            trans.commit()
        except Exception as e:
            print('Exception happened while migrating batch: ' + batch_guid, e)
            print('Rollback initiated')
            trans.rollback()


def start_migrate_daily_delta():
    """
    migration starting point
    """
    batches_to_migrate = get_daily_delta_batches_to_migrate()
    for batch in batches_to_migrate:
        migrate_batch(batch['batch_guid'], batch['tenant'])


if __name__ == '__main__':
    start_migrate_daily_delta()