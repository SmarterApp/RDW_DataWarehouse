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


#@unittest.skip("skipping this test till till ready for jenkins")
class Test_Error_In_Migration(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.archived_file = os.path.join(self.data_dir, 'test_delete_record.tar.gz.gpg')

    def test_error_validation(self):
        '''
        This is the first test : Empty udl_batch table, empty udl_stats table, run UDL with an unique batch guid
        '''
        self.empty_udl_batch_table()
        self.empty_stat_table()
        self.run_validate_udl()

    # This test method will call secondly: This will empty batch table, run pipeline and validate udl and prepod schema
    # trigger migration and validate prod.Migration will migrate data of two udl batches.
    def test_validation(self):
        self.empty_udl_batch_table()
        self.run_validate_udl()
        self.migrate_data()
        self.validate_udl_stats()
        self.validate_prod()

    def empty_udl_batch_table(self):
        '''
        Deletes entire data from UDL batch_table
        '''
        with get_udl_connection() as connector:
            batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            self.assertEqual(len(result1), 0)
            print("udl_batch table is empty. ", len(result1), "rows found")

    #Delete all data from udl_stats table in edware_stats
    def empty_stat_table(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            conn.execute(table.delete())
            query = select([table])
            query_tab = conn.execute(query).fetchall()
            no_rows = len(query_tab)
            print(no_rows)

    #Run UDL pipeline with file in tenant dir
    def run_udl_pipeline(self, guid_batch_id):
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    #Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            print("copying")
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            self.assertEqual(len(result), 1, "1 guids not found.")
            print('Waited for', timer, 'second(s) for job to complete.')

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

    # Validate udl_stats table
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
        #TODO validate that pre prod schema has been deleted

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
