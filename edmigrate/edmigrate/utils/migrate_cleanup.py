from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edcore.utils.cleanup import cleanup_all_tables
from edmigrate.utils.constants import Constants

def cleanup_tables(connector, batch_guid, table_name_prefix, tables):
    """
    clean up migration tables
    """
    cleanup_all_tables(connector=connector, column_name='batch_guid', value=batch_guid, table_name_prefix=table_name_prefix, tables=tables)


def cleanup_batch(batch_guid, tenant, tables):
    """
    cleanup this batch
    """
    # clearing up the targetDB/pre-prod database for the batch and tenant
    with EdMigrateSourceConnection(tenant) as source_connector:
        # clean up fact
        cleanup_tables(source_connector, batch_guid, 'fact_', tables)
        # clean up dims
        cleanup_tables(source_connector, batch_guid, 'dim_', tables)


def cleanup_tenant_batches(tenant):
    # TODO: to be implemented
    pass
