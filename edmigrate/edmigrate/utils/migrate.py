from edmigrate.exceptions import EdMigrateRecordAlreadyDeletedException, \
    EdMigrateUdl_statException, EdMigrateRecordInsertionException
from sqlalchemy.sql.expression import select, and_, tuple_
from sqlalchemy import Table, Column, Index
from edmigrate.utils.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
import logging
from edcore.database.utils.constants import UdlStatsConstants
from edcore.utils.cleanup import drop_schema, schema_exists
from edschema.metadata.util import get_natural_key_columns

__author__ = 'sravi'
# This is a hack needed for now for migration.
# These tables will be dropped in future
# CR, remove this line after dim_section is removed from database
TABLES_NOT_CONNECTED_WITH_BATCH = [Constants.DIM_SECTION]
logger = logging.getLogger('edmigrate')


def get_batches_to_migrate(tenant=None):
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
    logger.info('Master: Getting daily delta batches to migrate')

    batches = []
    with StatsDBConnection() as connector:
        udl_status_table = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = \
            select([udl_status_table.c.batch_guid,
                    udl_status_table.c.tenant,
                    udl_status_table.c.state_code,
                    udl_status_table.c.record_loaded_count,
                    udl_status_table.c.load_status,
                    udl_status_table.c.load_start,
                    udl_status_table.c.load_end],
                   from_obj=[udl_status_table]).\
            where(and_(udl_status_table.c.load_type == UdlStatsConstants.LOAD_TYPE_ASSESSMENT, udl_status_table.c.load_status == UdlStatsConstants.UDL_STATUS_INGESTED)).\
            order_by(udl_status_table.c.file_arrived)
        if tenant:
            query = query.where(and_(udl_status_table.c.tenant == tenant))
        batches = connector.get_result(query)
    return batches


def report_udl_stats_batch_status(batch_guid, migrate_load_status):
    """This method populates udl_stats for batches that had successful migration

    :param batch_guid: The batch that was successfully migrated
    :returns : Nothing
    """
    logger.info('Master: Reporting batch status to udl_stats')
    with StatsDBConnection() as connector:
        udl_stats_table = connector.get_table(UdlStatsConstants.UDL_STATS)
        update_query = udl_stats_table.update().values(load_status=migrate_load_status).\
            where(udl_stats_table.c.batch_guid == batch_guid)
        rtn = connector.execute(update_query)
        rowcount = rtn.rowcount
        if rowcount == 0:
            raise EdMigrateUdl_statException('Failed to update record for batch_guid=' + batch_guid)
    return rowcount


def get_tables_to_migrate(connector, batch_guid):
    """This function returns list of tables to be migrated based on schema metadata

    :param connector: The connection to the database
    :returns : A list of table names
             [dim_section, dim_student, fact_asmt_outcome]
    """
    all_tables = []
    for table in connector.get_metadata().tables.keys():
        if '.' in table:
            all_tables.append(table.split('.')[1])
        else:
            all_tables.append(table)
    return all_tables


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


def migrate_table(batch_guid, schema_name, source_connector, dest_connector, table_name, batch_size=100):
    """Load prod fact table with delta from pre-prod

    :param batch_guid: Batch Guid of the batch under migration
    :param schema_name: Schema name for this batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param batch_size: batch size for migration

    :returns number of record updated
    """
    delete_count = 0
    source_connector.set_metadata_by_reflect(schema_name)
    source_table = source_connector.get_table(table_name)
    # TODO: make it possible for composites
    primary_key = source_table.primary_key.columns.keys()[0]
    # if there is a status column, it's a candidate for deletes
    has_status = Constants.STATUS in source_table.columns
    if has_status:
        delete_query = select([primary_key]).where(and_(source_table.c.batch_guid == batch_guid, source_table.c.rec_status == Constants.STATUS_DELETED))
        delete_count = _process_batch(source_connector, dest_connector, preprod_to_prod_delete_records, delete_query, table_name,
                                      primary_key, batch_size)

    # for Insert
    insert_query = select([source_table]).where(source_table.c.batch_guid == batch_guid)
    if has_status:
        insert_query = insert_query.where(and_(source_table.c.rec_status == Constants.STATUS_CREATED))
    insert_count = _process_batch(source_connector, dest_connector, preprod_to_prod_insert_records, insert_query, table_name,
                                  primary_key, batch_size)
    return delete_count, insert_count


def _process_batch(source_connector, dest_connector, handler, query, table_name, primary_key_field_name, batch_size=100):
    '''Process each batch for the given handler and query
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param handler: function that handles the batch for the type (insert/delete)
    :param query: query for the source to select batch
    :param table_name: name of the table to be migrated
    :param primary_key_field_name: primary key for the table_name
    :batch batch of records to be deleted

    :returns number of record updated
    '''
    proxy_rows = yield_rows(source_connector, query, batch_size)
    total_count = 0
    # for rows in a scrollable cursor, preserve primary key
    for rows in proxy_rows:
        total_count += handler(source_connector, dest_connector, table_name, primary_key_field_name, rows)
    return total_count


def preprod_to_prod_delete_records(source_connector, dest_connector, table_name, primary_key_field_name, batch):
    '''Process deletes for the batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param primary_key_field_name: primary key for the table_name
    :batch batch of records to be deleted

    :returns number of record updated
    '''
    # select primary keys to be deleted in destination
    primary_keys = [row[primary_key_field_name] for row in batch]
    batch_size = len(primary_keys)
    dest_table = dest_connector.get_table(table_name)
    dest_primary_key_field = dest_table.columns[primary_key_field_name]
    # set status to D if the status is C for all records in the batch
    update_query = dest_table.update(and_(dest_primary_key_field.in_(primary_keys), dest_table.c.rec_status == Constants.STATUS_CREATED)).values(status=Constants.STATUS_DELETED)
    # if number of updated records doesn't match, that means one of the records was changed from C to D by another batch
    if dest_connector.execute(update_query).rowcount != batch_size:
        raise EdMigrateRecordAlreadyDeletedException
    return batch_size


def preprod_to_prod_insert_records(source_connector, dest_connector, table_name, primary_key_field_name, batch):
    '''Process inserts for the batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param primary_key_field_name: primary key for the table_name
    :batch batch of records to be inserted

    :returns number of record updated
    '''
    import pdb;pdb.set_trace();
    dest_table = dest_connector.get_table(table_name)
    natural_keys = get_natural_key_columns(dest_table)
    key_columns = [dest_table.columns[key] for key in natural_keys]
    key_values = [[row[key] for key in natural_keys] for row in batch]

    batch_size = len(key_values)
    # update prod rec_status to inactive for records matching with the natural keys of the records in the current batch
    update_query = dest_table.update(and_(dest_table.c.rec_status == 'C', tuple_(*key_columns).in_(key_values))).values(rec_status='I')
    dest_connector.execute(update_query)
    # insert the new records to prod with rec_status as current
    insert_query = dest_table.insert()
    records_inserted = dest_connector.execute(insert_query, batch).rowcount
    if records_inserted != batch_size:
        raise EdMigrateRecordInsertionException
    return batch_size


def migrate_all_tables(batch_guid, schema_name, source_connector, dest_connector, tables):
    """Migrate all tables for the given batch from source to destination

    :param batch_guid: Batch Guid of the batch under migration
    :param schema_name: Schema name for this batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param tables: list of Tables to be migrated

    :returns Nothing
    """
    logger.info('Migrating all tables for batch: ' + batch_guid)
    # TODO - we want it to be configurable what to migrate and in which order
    # migrate dims first
    #for table in list(filter(lambda x: (x not in TABLES_NOT_CONNECTED_WITH_BATCH and x.startswith('dim_')), tables)):
    #    migrate_table(batch_guid, schema_name, source_connector, dest_connector, table)
    # migrate facts
    for table in list(filter(lambda x: (x not in TABLES_NOT_CONNECTED_WITH_BATCH and x.startswith('fact_')), tables)):
        migrate_table(batch_guid, schema_name, source_connector, dest_connector, table)


def migrate_batch(batch):
    """Migrates data for the given batch and given tenant

    :param batch_guid: Batch Guid of the batch under migration

    :returns true: sucess, false: fail (for UT purpose)
    """
    rtn = False
    batch_guid = batch[UdlStatsConstants.BATCH_GUID]
    tenant = batch[UdlStatsConstants.TENANT]
    schema_name = batch[UdlStatsConstants.SCHEMA_NAME]
    logger.info('Migrating batch: ' + batch_guid + ',for tenant: ' + tenant)

    with EdMigrateDestConnection(tenant) as dest_connector, \
            EdMigrateSourceConnection(tenant) as source_connector:
        try:
            # start transaction for this batch
            trans = dest_connector.get_transaction()
            report_udl_stats_batch_status(batch_guid, UdlStatsConstants.MIGRATE_IN_PROCESS)
            tables_to_migrate = get_tables_to_migrate(dest_connector, batch_guid)
            # migrate all tables
            migrate_all_tables(batch_guid, schema_name, source_connector, dest_connector, tables_to_migrate)
            # report udl stats with the new batch migrated
            report_udl_stats_batch_status(batch_guid, UdlStatsConstants.MIGRATE_INGESTED)
            # commit transaction
            trans.commit()
            logger.info('Master: Migration successful for batch: ' + batch_guid)
            rtn = True
        except Exception as e:
            logger.info('Exception happened while migrating batch: ' + batch_guid + ' - Rollback initiated')
            logger.info(e)
            print(e)
            trans.rollback()
            try:
                report_udl_stats_batch_status(batch_guid, UdlStatsConstants.MIGRATE_FAILED)
            except Exception as e:
                pass
    return rtn


def cleanup_batch(batch):
    """Cleanup the pre-prod schema for the given batch

    :param batch_guid: Batch Guid of the batch under migration

    :returns true: sucess, false: fail (for UT purpose)
    """
    rtn = False
    batch_guid = batch[UdlStatsConstants.BATCH_GUID]
    tenant = batch[UdlStatsConstants.TENANT]
    schema_name = batch[UdlStatsConstants.SCHEMA_NAME]
    logger.info('Cleaning up batch: ' + batch_guid + ',for tenant: ' + tenant)
    with EdMigrateSourceConnection(tenant) as source_connector:
        try:
            # drop schema if exists
            if schema_exists(source_connector, schema_name):
                drop_schema(source_connector, schema_name)
            logger.info('Master: Cleanup successful for batch: ' + batch_guid)
            rtn = True
        except Exception as e:
            logger.info('Exception happened while cleaning up batch: ' + batch_guid)
            logger.info(e)
    return rtn


def start_migrate_daily_delta(tenant=None):
    """migration starting point for a tenant

    :param tenant: Tenant name of the tenant to perform the migration

    :returns Nothing
    """
    batches_to_migrate = get_batches_to_migrate(tenant=tenant)
    for batch in batches_to_migrate:
        import pdb;pdb.set_trace();
        batch[UdlStatsConstants.SCHEMA_NAME] = batch[UdlStatsConstants.BATCH_GUID]
        logger.debug('processing batch_guid: ' + batch[UdlStatsConstants.BATCH_GUID])
        migrate_batch(batch=batch)
        #cleanup_batch(batch=batch)
