from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edcore.utils.cleanup import drop_schema, schema_exists
from edmigrate.utils.constants import Constants
from edmigrate.celery import conf


def cleanup_batch(schema_name, tenant):
    """
    Drops the entire schema given by the schema_name from the given tenants pre-prod database
    """
    # clearing up the targetDB/pre-prod database for the batch and tenant
    with EdMigrateSourceConnection(tenant) as source_connector:
        # drop schema
        if schema_exists(source_connector, schema_name):
            drop_schema(source_connector, schema_name)

if __name__ == '__main__':
    import edmigrate.celery as c
    cleanup_batch('test-xxx-yyy-zzz', 'cat')
