import logging

from edmigrate.exceptions import EdMigrateUdl_statException
from sqlalchemy.sql.expression import select, and_
from edmigrate.migrate.migrate_by_batch import migrate_snapshot
from edmigrate.migrate.migrate_by_row import migrate_by_row
from edmigrate.utils.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edcore.database.utils.constants import UdlStatsConstants, LoadType
from edcore.database.utils.utils import drop_schema
from edschema.metadata.ed_metadata import generate_ed_metadata

__author__ = 'sravi'
TABLES_NOT_CONNECTED_WITH_BATCH = [Constants.DIM_SECTION]
logger = logging.getLogger('edmigrate')
admin_logger = logging.getLogger(Constants.EDMIGRATE_ADMIN_LOGGER)


def start_migrate_daily_delta(tenant=None):
    """migration starting point for a tenant

    :param tenant: Tenant name of the tenant to perform the migration

    :returns Nothing
    """
    migrate_ok_count = 0
    batches_to_migrate = get_batches_to_migrate(tenant=tenant)
    if batches_to_migrate:
        for batch in batches_to_migrate:
            batch_guid = batch[UdlStatsConstants.BATCH_GUID]
            batch[UdlStatsConstants.SCHEMA_NAME] = batch_guid
            logger.debug('processing batch_guid: ' + batch_guid)
            if migrate_batch(batch=batch):
                migrate_ok_count += 1
                admin_logger.info('Migrating batch[' + batch_guid + '] is processed')
            else:
                admin_logger.info('Migrating batch[' + batch_guid + '] failed')
            cleanup_batch(batch=batch)
    else:
        logger.debug('no batch found for migration')
        admin_logger.info('no batch found for migration')
    return migrate_ok_count, len(batches_to_migrate)


def get_batches_to_migrate(tenant=None):
    """ This function returns daily batches to be migrated for a given tenant

    :param tenant: The tenant to be migrated
    :type tenant: str
    :returns: A list mapping batch_guid to the row in udl_stats table
            An empty list if no batches found to be migrated
    """
    logger.info('Master: Getting daily delta batches to migrate' + ('with tenant: ' + tenant) if tenant else '')

    with StatsDBConnection() as connector:
        udl_status_table = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = \
            select([udl_status_table.c.rec_id,
                    udl_status_table.c.batch_guid,
                    udl_status_table.c.tenant,
                    udl_status_table.c.load_type,
                    udl_status_table.c.load_status,
                    udl_status_table.c.batch_operation,
                    udl_status_table.c.snapshot_criteria],
                   from_obj=[udl_status_table]).\
            where(udl_status_table.c.load_status == UdlStatsConstants.UDL_STATUS_INGESTED).\
            order_by(udl_status_table.c.file_arrived)
        if tenant:
            query = query.where(and_(udl_status_table.c.tenant == tenant))
        batches = connector.get_result(query)
    return batches


def migrate_batch(batch):
    """Migrates data for the given batch and given tenant

    :param batch_guid: Batch Guid of the batch under migration

    :returns true: sucess, false: fail (for UT purpose)
    """
    rtn = False
    rec_id = batch[UdlStatsConstants.REC_ID]
    batch_guid = batch[UdlStatsConstants.BATCH_GUID]
    tenant = batch[UdlStatsConstants.TENANT]
    schema_name = batch[UdlStatsConstants.SCHEMA_NAME]
    load_type = batch[UdlStatsConstants.LOAD_TYPE]
    batch_op = batch[UdlStatsConstants.BATCH_OPERATION]
    batch_criteria = batch[UdlStatsConstants.SNAPSHOT_CRITERIA]
    # this flag will be set to false from unit test, if this is not set its always True
    deactivate = batch[Constants.DEACTIVATE] if Constants.DEACTIVATE in batch else True
    logger.info('Migrating batch: ' + batch_guid + ',for tenant: ' + tenant)

    with EdMigrateDestConnection(tenant) as dest_connector, \
            EdMigrateSourceConnection(tenant) as source_connector:
        try:
            # start transaction for this batch
            trans = dest_connector.get_transaction()
            source_connector.set_metadata_by_generate(schema_name=schema_name, metadata_func=generate_ed_metadata)
            report_udl_stats_batch_status(rec_id, UdlStatsConstants.MIGRATE_IN_PROCESS)
            tables_to_migrate = get_ordered_tables_to_migrate(dest_connector, load_type)
            # migrate all tables
            migrate_all_tables(batch_guid, schema_name, source_connector,
                               dest_connector, tables_to_migrate, deactivate=deactivate, batch_op=batch_op, batch_criteria=batch_criteria)
            # report udl stats with the new batch migrated
            report_udl_stats_batch_status(rec_id, UdlStatsConstants.MIGRATE_INGESTED)
            # commit transaction
            trans.commit()
            logger.info('Master: Migration successful for batch: ' + batch_guid)
            rtn = True
        except Exception as e:
            logger.info('Exception happened while migrating batch: ' + batch_guid + ' - Rollback initiated')
            logger.info(e)
            print(e)
            logger.exception('migrate rollback')
            trans.rollback()
            try:
                report_udl_stats_batch_status(rec_id, UdlStatsConstants.MIGRATE_FAILED)
            except Exception as e:
                pass
    return rtn


def report_udl_stats_batch_status(rec_id, migrate_load_status):
    """This method populates udl_stats for batches that had successful migration

    :param batch_guid: The batch that was successfully migrated
    :returns : Nothing
    """
    logger.info('Master: Reporting batch status to udl_stats')
    with StatsDBConnection() as connector:
        udl_stats_table = connector.get_table(UdlStatsConstants.UDL_STATS)
        update_query = udl_stats_table.update().values(load_status=migrate_load_status).\
            where(udl_stats_table.c.rec_id == rec_id)
        rtn = connector.execute(update_query)
        rowcount = rtn.rowcount
        if rowcount == 0:
            raise EdMigrateUdl_statException('Failed to update record for rec_id=' + rec_id)
    return rowcount


def get_ordered_tables_to_migrate(connector, load_type):
    """This function returns an ordered list of tables to be migrated based on schema metadata.

    :param connector: The connection to the database
    @param load_type: The load type for the current table

    @return: A list of table names ordered by dependencies
             e.g., [dim_section, dim_student, fact_asmt_outcome]
    """

    return [table.name for table in connector.get_metadata().sorted_tables if _include_table(table.name, load_type)]


def migrate_all_tables(batch_guid, schema_name, source_connector, dest_connector, tables, deactivate, batch_op, batch_criteria):
    """Migrate all tables for the given batch from source to destination

    :param batch_guid: Batch Guid of the batch under migration
    :param schema_name: Schema name for this batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param tables: list of Tables to be migrated

    :returns Nothing
    """
    logger.info('Migrating all tables for batch: ' + batch_guid)
    for table in tables:
        migrate_table(batch_guid, schema_name, source_connector, dest_connector, table, deactivate, batch_op=batch_op, batch_criteria=batch_criteria)


def migrate_table(batch_guid, schema_name, source_connector, dest_connector, table_name, deactivate, batch_op=None, batch_criteria=None, batch_size=100):
    """Load prod fact table with delta from pre-prod

    :param batch_guid: Batch Guid of the batch under migration
    :param schema_name: Schema name for this batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param batch_size: batch size for migration

    :returns number of record updated
    """
    if schema_name:
        logger.debug('migrating schema[' + schema_name + ']')
    logger.debug('migrating table[' + table_name + ']')

    if batch_op and batch_op == UdlStatsConstants.SNAPSHOT:
        delete_count, insert_count = migrate_snapshot(dest_connector, source_connector, table_name, batch_criteria, batch_size)
    else:
        delete_count, insert_count = migrate_by_row(batch_guid, batch_size, deactivate, dest_connector, source_connector, table_name)

    return delete_count, insert_count


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
            drop_schema(source_connector, schema_name)
            logger.info('Master: Cleanup successful for batch: ' + batch_guid)
            rtn = True
        except Exception as e:
            logger.info('Exception happened while cleaning up batch: ' + batch_guid)
            logger.info(e)
    return rtn


def _include_table(table_name, load_type):
    """
    Determine if table name should be included in tables to migrate.

    @param table_name: Name of table candidate
    @param load_type: Load type of table candidate

    @return: Whether or not table name should be included in migration.
    """

    table_select_criteria = {
        LoadType.ASSESSMENT: table_name.startswith('dim_') or table_name.startswith('fact_'),
        LoadType.STUDENT_REGISTRATION: table_name == Constants.STUDENT_REG
    }

    return table_name not in TABLES_NOT_CONNECTED_WITH_BATCH and table_select_criteria.get(load_type, False)
