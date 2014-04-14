'''
Created on Mar 7, 2014
@author: bpatel
Description: Deleting the same record in two different batches will lead to a successful first migration batch and failed second migration batch.
'''
from sqlalchemy.schema import DropSchema
import unittest
import os
import shutil
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf
from time import sleep
import subprocess
from uuid import uuid4
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection, get_prod_connection
from integration_tests.migrate_helper import start_migrate,\
    get_stats_table_has_migrated_ingested_status
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql.expression import bindparam, text
from integration_tests.udl_helper import empty_batch_table, empty_stats_table, copy_file_to_tmp, run_udl_pipeline, \
    check_job_completion, migrate_data, validate_edware_stats_table_after_mig, validate_udl_stats_before_mig, validate_udl_stats_after_mig, validate_edware_stats_table_before_mig


#@unittest.skip("skipping this test till till ready for jenkins")
class Test_Error_In_Migration(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.archived_file = os.path.join(self.data_dir, 'test_delete_record.tar.gz.gpg')

    def test_migration_error_validation(self):
        '''
        This test will run the udl twice with same delete record.first migration branch will be successful and second migration will be
        failure as it is trying to delete same record twice
        '''
        # ---- RUN 1 ----
        # Empty udl batch table and udl_stats table under edware_stats
        empty_batch_table(self)
        empty_stats_table(self)
        # Get unique batch guid and run the udl pipeline
        self.guid_batch_id = str(uuid4())
        run_udl_pipeline(self, self.guid_batch_id)
        # validate that record has been deleted in preprod
        self.validate_edware_database(schema_name=self.guid_batch_id)

        # ----- RUN 2 -----
        # Empty udl batch table,get unique batch guid and run the udl pipeline
        empty_batch_table(self)
        self.guid_batch_id = str(uuid4())
        run_udl_pipeline(self, self.guid_batch_id)
        # validate the stats table and start migration
        validate_edware_stats_table_before_mig
        self.migrate_data()
        # validate that one migration batch is success and second batch is failure.
        # This will also validate that schema clean up is successful in the case of miration success or migration failure.
        self.validate_udl_stats()
        # validate production database for delete record
        self.validate_prod()

    # Validate edware database : value in status column chnage to D from C.
    def validate_edware_database(self, schema_name):
        with get_target_connection() as ed_connector:
            ed_connector.set_metadata_by_reflect(schema_name)
            fact_table = ed_connector.get_table('fact_asmt_outcome')
            prod_output_data = select([fact_table.c.rec_status]).where(fact_table.c.student_guid == '115f7b10-9e18-11e2-9e96-0800200c9a66', )
            prod_output_table = ed_connector.execute(prod_output_data).fetchall()
            expected_status_val_D = [('D',)]
            self.assertEquals(prod_output_table, expected_status_val_D, 'Status is wrong in fact table for delete record')

    def run_validate_udl(self):
        self.guid_batch_id = str(uuid4())
        self.run_udl_pipeline(self.guid_batch_id)
        self.validate_edware_database(schema_name=self.guid_batch_id)

    # Call migration
    def migrate_data(self):
        start_migrate()
        tenant = 'cat'
        results = get_stats_table_has_migrated_ingested_status(tenant)

    # Validate udl_stats table for migration success and failure
    # Validate that pre prod schema is delted in both the cases : migration success or migration failure
    def validate_udl_stats(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('migrate.ingested',), ('migrate.failed',)]
            #Validate that one migration batch is failed and one is successful.
            self.assertEquals(result, expected_result)
            #Validate that schema clean up is successful for both the scenario: Migration.ingested and migration.failed
            schema_name = select([table.c.batch_guid])
            schema_name_result = conn.execute(schema_name).fetchall()
            tpl_schema_name_1 = schema_name_result[0]
            tpl_schema_name_2 = schema_name_result[1]
            schema_name_1 = tpl_schema_name_1[0]
            schema_name_2 = tpl_schema_name_2[0]
            with get_target_connection() as connector:
                    query = select(['schema_name'], from_obj=['information_schema.schemata']).where('schema_name in :a')
                    params = [bindparam('a', (schema_name_1, schema_name_2))]
                    new_query = text(str(query), bindparams=params)
                    result = connector.execute(new_query).fetchall()
                    self.assertEqual(len(result), 0, "Schema clean up after migration is unsuccessful")

    #Validate edware_prod table for given student status has change to D for first batch.
    def validate_prod(self):
        with get_prod_connection() as conn:
            fact_table = conn.get_table('fact_asmt_outcome')
            query = select([fact_table], and_(fact_table.c.student_guid == '115f7b10-9e18-11e2-9e96-0800200c9a66', fact_table.c.rec_status == 'D'))
            result = conn.execute(query).fetchall()
            expected_no_rows = 1
            self.assertEquals(len(result), expected_no_rows, "Data has not been loaded to prod_fact_table after edmigrate")

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
