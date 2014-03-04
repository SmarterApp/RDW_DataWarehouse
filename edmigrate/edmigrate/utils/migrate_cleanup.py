from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
import edcore.utils.cleanup as cleanup
from edmigrate.utils.constants import Constants

def cleanup_tables(connector, batch_guid, table_name_prefix, tables):
    """
    """
    cleanup.cleanup_all_tables(connector=connector, column_name='batch_guid', value=batch_guid, table_name_prefix=table_name_prefix, tables=tables)


def cleanup_batch(batch_guid, tenant, tables):
    """
    """
    # clearing up the targetDB/pre-prod database for the batch and tenant
    with EdMigrateSourceConnection(tenant) as source_connector:
        # clean up fact
        cleanup_tables(source_connector, batch_guid, 'fact_', tables)
        # clean up dims
        cleanup_tables(source_connector, batch_guid, 'dim_', tables)


def cleanup_tenant_batches(tenant):
    pass

if __name__ == '__main__':
    # TODO: remove this. temp entry point for testing cleanup as a script
    import edmigrate.celery
    #cleanup_batch('14132978-2d94-4f14-9674-3e6db840b580', 'cat', tables=['dim_asmt', 'dim_inst_hier'])
    cleanup_batch('14132978-2d94-4f14-9674-3e6db840b580', 'cat', tables=None)
