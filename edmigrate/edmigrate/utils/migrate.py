__author__ = 'sravi'

from sqlalchemy.sql.expression import select

from edmigrate.utils.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.edcore_connector import EdCoreDBConnection

# This is a hack needed for now for migration.
# These tables will be dropped in future
TABLES_NOT_CONNECTED_WITH_BATCH = [Constants.DIM_SECTION]

# batches to be migrated
batches_to_migrate = {}


def get_daily_delta_batches_to_migrate(tenant):
    """ This function returns daily batches to be migrated for a given tenant

    :param tenant: The tenant to be migrated
    :type tenant: str
    :returns: A dict mapping batch_guid to the row in udl_daily_stats table
            {'f340322f-b0a8-44df-97bb-6a1f53c4ba48': OrderedDict([
                    ('batch_guid','f340322f-b0a8-44df-97bb-6a1f53c4ba48'),
                    ('tenant','ca'),
                    ('state_code','ca'),
                    ('record_loaded_count',100)
                ]),
                'g344322h-p0at-44df-97bb-8a1e53c1ba90': OrderedDict([
                    ('batch_guid','g344322h-p0at-44df-97bb-8a1e53c1ba90'),
                    ('tenant','ca'),
                    ('state_code','ca'),
                    ('record_loaded_count',150)
            ])}
            An empty dict if no batches found to be migrated
    """
    print('Master: Getting daily delta batches to migrate')
    with StatsDBConnection() as connector:
        batches = {}
        udl_daily_status_table = connector.get_table(Constants.UDL_DAILY_STATS_TABLE)
        query = \
            select([udl_daily_status_table.c.batch_guid,
                        udl_daily_status_table.c.tenant,
                        udl_daily_status_table.c.state_code,
                        udl_daily_status_table.c.record_loaded_count,
                        udl_daily_status_table.c.udl_start,
                        udl_daily_status_table.c.udl_end],
                       from_obj=[udl_daily_status_table]).\
            where(udl_daily_status_table.c.tenant == tenant).\
            order_by(udl_daily_status_table.c.file_arrived)
        udl_daily_status_rows = connector.get_result(query)
        for row in udl_daily_status_rows:
            batches[row[Constants.BATCH_GUID]] = row
        return batches


def report_udl_stats_batch_status(batch_guid):
    """This method populates udl_stats for batches that had successful migration

    :param batch_guid: The batch that was successfully migrated
    :returns : Nothing
    """
    print('Master: Reporting batch status to udl_stats')
    with StatsDBConnection() as connector:
        udl_daily_stats_batch_record = batches_to_migrate[batch_guid]
        udl_stats_table = connector.get_table(Constants.UDL_STATS_TABLE)
        udl_stats = {
            Constants.BATCH_GUID: udl_daily_stats_batch_record[Constants.BATCH_GUID],
            Constants.TENANT: udl_daily_stats_batch_record[Constants.TENANT],
            Constants.STATE_CODE: udl_daily_stats_batch_record[Constants.STATE_CODE],
            Constants.RECORD_LOADED_COUNT: udl_daily_stats_batch_record[Constants.RECORD_LOADED_COUNT],
            Constants.LOAD_START: udl_daily_stats_batch_record[Constants.UDL_START],
            Constants.LOAD_END: udl_daily_stats_batch_record[Constants.UDL_END],
            Constants.LOAD_STATUS: Constants.STATUS_INGESTED
        }
        connector.execute(udl_stats_table.insert(), False, udl_stats)


def get_tables_to_migrate(connector):
    """This function returns list of tables to be migrated based on schema metadata

    :param connector: The connection to the database
    :returns : A list of table names
             [dim_section, dim_student, fact_asmt_outcome]
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
    """stream the query results in batches of batch_size

    :param connector: The connection to the database
    :param query: The query to be executed
    :param batch_size: The batch_size for streaming
    :returns : Yields a batch of rows
    """
    result = connector.execute(query, stream_results=True)
    rows = result.fetchmany(batch_size)
    while len(rows) > 0:
        yield rows
        rows = result.fetchmany(batch_size)


def get_source_query(source_tab, batch_guid, migrate_all=False):
    """Returns the source query to fetch records from pre-prod

    :param source_tab: Source table to be queried for
    :param batch_guid: Batch Guid of the batch under migration
    :param migrate_all: Flag to ignore batch_guid if set to true

    :returns Sql alchemy query object
    """
    # hack for now to allow dim_section migration (fake record) with out batch_guid matching
    if migrate_all is True:
        return source_tab.select()
    return source_tab.select().where(source_tab.c.batch_guid == batch_guid)


def migrate_from_preprod_to_prod(batch_guid, source_connector, dest_connector, table_name, batch_size=100):
    """Load prod fact table with delta from pre-prod

    :param batch_guid: Batch Guid of the batch under migration
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param batch_size: batch size for migration

    :returns Nothing
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


def migrate_fact(batch_guid, source_connector, dest_connector):
    """Migrate fact table for the given batch from source to destination

    :param batch_guid: Batch Guid of the batch under migration
    :param source_connector: Source connection
    :param dest_connector: Destination connection

    :returns Nothing
    """
    print('Migrating fact for batch: ' + batch_guid)
    migrate_from_preprod_to_prod(batch_guid, source_connector, dest_connector, Constants.FACT_ASMT_OUTCOME)


def migrate_dims(batch_guid, source_connector, dest_connector, table):
    """Migrate the given table for the given batch from source to destination

    :param batch_guid: Batch Guid of the batch under migration
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table: Table to be migrated

    :returns Nothing
    """
    print('Migrating dimension for batch: ' + batch_guid + ' table: ' + table)
    migrate_from_preprod_to_prod(batch_guid, source_connector, dest_connector, table)


def migrate_all_tables(batch_guid, source_connector, dest_connector, tables):
    """Migrate all tables for the given batch from source to destination

    :param batch_guid: Batch Guid of the batch under migration
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param tables: list of Tables to be migrated

    :returns Nothing
    """
    print('Migrating all tables for batch: ' + batch_guid)
    # migrate dims first
    for table in list(filter(lambda x: x.startswith('dim_'), tables)):
        migrate_dims(batch_guid, source_connector, dest_connector, table)
    # migrate fact
    migrate_fact(batch_guid, source_connector, dest_connector)


def migrate_batch(batch_guid, tenant):
    """Migrates data for the given batch and given tenant

    :param batch_guid: Batch Guid of the batch under migration
    :param tenant: Tenant name of the tenant to which this batch belongs to
                    This is needed to grab the right source and destination connection

    :returns Nothing
    """
    print('Migrating batch: ' + batch_guid + ',for tenant: ' + tenant)

    # get the source and dest key to grab a connection
    source = get_source_key(tenant)
    dest = get_dest_key(tenant)

    # TODO: EdCoreConnection will be replaced with real one later
    with EdCoreDBConnection(dest) as dest_connector, \
            EdCoreDBConnection(source) as source_connector:
        try:
            # start transaction for this batch
            trans = dest_connector.get_transaction()
            tables_to_migrate = get_tables_to_migrate(dest_connector)
            # migrate all tables
            migrate_all_tables(batch_guid, source_connector, dest_connector, tables_to_migrate)
            # report udl stats with the new batch migrated
            report_udl_stats_batch_status(batch_guid)
            # commit transaction
            trans.commit()
            print('Master: Migration successful for batch: ' + batch_guid)
        except Exception as e:
            print('Exception happened while migrating batch: ' + batch_guid, ' - Rollback initiated')
            print(e)
            trans.rollback()


def start_migrate_daily_delta(tenant):
    """migration starting point for a tenant

    :param tenant: Tenant name of the tenant to perform the migration

    :returns Nothing
    """
    global batches_to_migrate
    batches_to_migrate = get_daily_delta_batches_to_migrate(tenant)
    for batch_guid in batches_to_migrate.keys():
        migrate_batch(batch_guid=batch_guid, tenant=tenant)

if __name__ == '__main__':
    # TODO: remove this. temp entry point for testing migration as a script
    import edmigrate.celery
    start_migrate_daily_delta('ca')