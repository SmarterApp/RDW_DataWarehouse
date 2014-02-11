__author__ = 'sravi'

from sqlalchemy.sql.expression import select

from edmigrate.utils.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.utils.utils import merge_dict

from datetime import datetime

# these tables will be dropped in future
TABLES_NOT_CONNECTED_WITH_BATCH = ['dim_section']


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


def get_daily_delta_batch_record(connector, batch_guid):
    """
    query daily batches for a single batch
    """
    udl_daily_status_table = connector.get_table(Constants.UDL_DAILY_STATS_TABLE)
    query = select([udl_daily_status_table.c.batch_guid,
                    udl_daily_status_table.c.tenant,
                    udl_daily_status_table.c.state_code,
                    udl_daily_status_table.c.record_loaded_count],
                   from_obj=[udl_daily_status_table]).where(udl_daily_status_table.c.batch_guid == batch_guid)
    udl_daily_status_record = connector.execute(query).fetchone()
    return udl_daily_status_record


def get_daily_delta_batches_to_migrate():
    '''
    get list of batches to be migrated to prod
    '''
    print('Master: Getting daily delta batches to migrate')
    with StatsDBConnection() as connector:
        batches_to_be_migrated = query_daily_delta_batches_to_migrate(connector)
    return batches_to_be_migrated


def insert_udl_stats_batch_record(connector, *dict_values):
    """
    insert udl stats for the new batch migrated
    """
    values = {}
    for d in dict_values:
        values = merge_dict(d, values)

    udl_stats_table = connector.get_table(Constants.UDL_STATS_TABLE)
    connector.execute(udl_stats_table.insert(), False, values)


def report_udl_stats_batch_status(batch_guid):
    '''
    update udl_stats for batches that had successful migration
    '''
    print('Master: Reporting batch status to udl_stats')
    with StatsDBConnection() as connector:
        udl_daily_stats_batch_record = get_daily_delta_batch_record(connector, batch_guid)
        udl_stats = {
            'batch_guid': udl_daily_stats_batch_record['batch_guid'],
            'tenant': udl_daily_stats_batch_record['tenant'],
            'state_code': udl_daily_stats_batch_record['state_code'],
            'record_loaded_count': udl_daily_stats_batch_record['record_loaded_count'],
            'load_start': datetime.now(),
            'load_end': datetime.now(),
            'load_status': 'ingested'
        }
        print(udl_stats)
        insert_udl_stats_batch_record(connector, udl_stats)


def get_tables_to_migrate(connector):
    """
    Return all the tables to be migrated based on metadata
    """
    all_tables = [table.split('.')[1] for table in connector.get_metadata().tables.keys()]
    return all_tables


def get_source_key(tenant):
    #TODO: return the actual source prefix key
    return 'cat'


def get_dest_key(tenant):
    #TODO: return the actual dest prefix key
    return 'dog'


def yield_rows(connector, query, batch_size):
    """
    stream the query results in batches of batch_size
    """
    result = connector.execute(query, stream_results=True)
    rows = result.fetchmany(batch_size)
    while len(rows) > 0:
        yield rows
        rows = result.fetchmany(batch_size)


def get_source_query(source_tab, batch_guid, migrate_all=False):
    """
    returns the source query to fetch records from pre-prod
    """
    # hack for now to allow dim_section migration (fake record) with out batch_guid matching
    if migrate_all is True:
        return source_tab.select()
    return source_tab.select().where(source_tab.c.batch_guid == batch_guid)


def migrate_from_preprod_to_prod(batch_guid, source_connector, dest_connector, table_name, batch_size=100):
    """
    Load prod fact table with delta from pre-prod
    """
    source_tab = source_connector.get_table(table_name)
    dest_Tab = dest_connector.get_table(table_name)

    if table_name in TABLES_NOT_CONNECTED_WITH_BATCH:
        query = get_source_query(source_tab, batch_guid, migrate_all=True)
    else:
        query = get_source_query(source_tab, batch_guid)
    # get handle to query result iterator
    rows = yield_rows(source_connector, query, batch_size)
    for batch in rows:
        # execute insert to target schema in batches
        print('Bulk Inserting batch of size: ' + str(len(batch)))
        dest_connector.execute(dest_Tab.insert(), False, batch)


def migrate_fact(batch_guid, pre_prod_connection, prod_connection):
    """
    Migrate fact
    """
    print('Migrating fact for batch: ' + batch_guid)
    migrate_from_preprod_to_prod(batch_guid, pre_prod_connection, prod_connection, 'fact_asmt_outcome')


def migrate_dims(batch_guid, pre_prod_connection, prod_connection, table):
    """
    Migrate all the dimension tables
    """
    print('Migrating dimension for batch: ' + batch_guid + ' table: ' + table)
    migrate_from_preprod_to_prod(batch_guid, pre_prod_connection, prod_connection, table)


def migrate_all_tables(batch_guid, pre_prod_connection, prod_connection, tables):
    """
    migrate all tables
    """
    print('Migrating all tables for batch: ' + batch_guid)
    # migrate dims first
    for table in list(filter(lambda x: x.startswith('dim_'), tables)):
        migrate_dims(batch_guid, pre_prod_connection, prod_connection, table)
    # migrate fact
    migrate_fact(batch_guid, pre_prod_connection, prod_connection)


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
            # start transaction for this batch
            trans = prod_connection.get_transaction()
            tables_to_migrate = get_tables_to_migrate(prod_connection)
            # migrate all tables
            migrate_all_tables(batch_guid, pre_prod_connection, prod_connection, tables_to_migrate)
            # report udl stats with the new batch migrated
            report_udl_stats_batch_status(batch_guid)
            # commit transaction
            trans.commit()
            print('Master: Migration successful for batch: ' + batch_guid)
        except Exception as e:
            print('Exception happened while migrating batch: ' + batch_guid, ' - Rollback initiated')
            print(e)
            trans.rollback()


def start_migrate_daily_delta():
    """
    migration starting point
    """
    batches_to_migrate = get_daily_delta_batches_to_migrate()
    for batch in batches_to_migrate:
        migrate_batch(batch['batch_guid'], batch['tenant'])
        break

if __name__ == '__main__':
    # TODO: remove this. temp thing for testing as script
    import edmigrate.celery
    start_migrate_daily_delta()