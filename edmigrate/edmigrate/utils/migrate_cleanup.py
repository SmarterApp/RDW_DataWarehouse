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

def testfor_guid_schemas(batch_guid, schema_name, tenant):
    with EdMigrateSourceConnection(tenant) as source_connector:
        
        # the schema name is based on the batch_guid being migrated
        source_tab = source_connector.get_table('fact_asmt_outcome', schema_name=schema_name)
        print(source_tab)
        query = source_tab.select().where(source_tab.c.batch_guid == batch_guid)
        print(query)
        rtn = source_connector.execute(query)
        print(rtn.rowcount)


def cleanup_tenant_batches(tenant):
    # TODO: to be implemented
    pass

if __name__ == '__main__':
    # TODO: remove this. temp entry point for testing cleanup as a script
    import edmigrate.celery as c
    #initialize_db(EdMigrateSourceConnection, c.conf, )
    cleanup_batch('f3a50333-af8c-459e-9d8c-1a3cd4fdb83d', 'dog', tables=None)
    testfor_guid_schemas('f3a50333-af8c-459e-9d8c-1a3cd4fdb83d', 'f3a50333-af8c-459e-9d8c-1a3cd4fdb83d', 'dog')
    testfor_guid_schemas('820568d0-ddaa-11e2-a63d-68a86d3c2f82', None, 'dog')
