from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edcore.utils.cleanup import cleanup_all_tables
from edmigrate.utils.constants import Constants
from edmigrate.celery import conf


def cleanup_tables(connector, schema_name, batch_guid, table_name_prefix, tables):
    """
    clean up migration tables
    """
    cleanup_all_tables(connector=connector, schema_name=schema_name, column_name='batch_guid', 
        value=batch_guid, batch_delete=True, table_name_prefix=table_name_prefix, tables=tables)


def cleanup_batch(batch_guid, tenant, tables):
    """
    cleanup this batch
    """
    # clearing up the targetDB/pre-prod database for the batch and tenant
    with EdMigrateSourceConnection(tenant) as source_connector:
        schema_key = source_connector.get_db_config_prefix(tenant) + 'schema_name'
        schema_name = conf[schema_key]
        # clean up fact
        cleanup_tables(source_connector, schema_name, batch_guid, 'fact_', tables)
        # clean up dims
        # TODO: figure out the issue with deleting dim_student records due to FK issue
        cleanup_tables(source_connector, schema_name, batch_guid, 'dim_', tables)


def cleanup_tenant_batches(tenant):
    # TODO: to be implemented
    pass

if __name__ == '__main__':
    # TODO: remove this. temp entry point for testing cleanup as a script
    import edmigrate.celery
    cleanup_batch('90901b70-ddaa-11e2-a95d-68a86d3c2f82', 'dog', tables=None)
