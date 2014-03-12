from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edcore.utils.cleanup import drop_schema
from edmigrate.utils.constants import Constants
from edmigrate.celery import conf


def cleanup_batch(schema_name, tenant):
    """
    cleanup this batch
    """
    # clearing up the targetDB/pre-prod database for the batch and tenant
    with EdMigrateSourceConnection(tenant) as source_connector:
        # drop schema
        drop_schema(source_connector, schema_name)


def cleanup_tenant_batches(tenant):
    # TODO: to be implemented
    pass

if __name__ == '__main__':
    # TODO: remove this. temp entry point for testing cleanup as a script
    import edmigrate.celery as c
    cleanup_batch('f3a50333-af8c-459e-9d8c-1a3cd4fdb83d', 'ca')
