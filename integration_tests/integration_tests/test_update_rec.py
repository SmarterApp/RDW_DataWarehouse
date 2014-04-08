'''
Created on Apr 8, 2014

@author: bpatel
'''
import unittest
from integration_tests.udl_helper import empty_batch_table, empty_stats_table, copy_file_to_tmp, run_udl_pipeline, \
    check_job_completion, migrate_data, validate_edware_stats_table_before_mig, validate_edware_stats_table_after_mig
import os
import shutil
from uuid import uuid4
from edudl2.database.udl2_connector import get_prod_connection
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql import select, and_


@unittest.skip("Disabling the test till update functionality get fix")
class Test(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.archived_file = os.path.join(self.data_dir, 'test_update_record.tar.gz.gpg')
        empty_stats_table(self)
        empty_batch_table(self)
        self.guid_batch_id = str(uuid4())

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def test_update_record(self):
        run_udl_pipeline(self, self.guid_batch_id)
        print("UDL pipeleine completed successfull")
        self.validate_edware_stats_table_before_mig()
        migrate_data(self)
        self.validate_edware_stats_table_after_mig()
        self.validate_edware_prod()

    def validate_edware_stats_table_before_mig(self):
        with StatsDBConnection() as conn:
            print()
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('udl.ingested',)]
            self.assertEquals(result, expected_result)

    # Validate udl_stats table under edware_stats DB for successful migration
    def validate_edware_stats_table_after_mig(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('migrate.ingested',)]
            self.assertEquals(result, expected_result)

    def validate_edware_prod(self):
        with get_prod_connection() as connection:
            fact_table = connection.get_table('fact_asmt_outcome')
            dim_student = connection.get_table('dim_student')
            update_output_data = select([fact_table.c.rec_status], and_(fact_table.c.student_guid == 'e2c4e2c0-2a2d-4572-81fb-529b511c6e8c', fact_table.c.asmt_guid == '8117f196-bf78-4190-a1d0-e7ab004d1e09'))
            update_output_table = connection.execute(update_output_data).fetchall()
            self.assertIn(('D',), update_output_table, "Delete status D is not found in the Update record")
            #self.assertIn(('I',), update_output_table, "Insert status I is not found in the Update record")
            # verify update asmt_score in fact_table

            update_asmt_score = select([fact_table.c.asmt_score], and_(fact_table.c.student_guid == 'e2c4e2c0-2a2d-4572-81fb-529b511c6e8c', fact_table.c.rec_status == 'I', fact_table.c.asmt_guid == '8117f196-bf78-4190-a1d0-e7ab004d1e09'))
            new_asmt_score = connection.execute(update_asmt_score).fetchall()
            expected_asmt_score = [(1400,)]
            #self.assertEquals(new_asmt_score, expected_asmt_score)
            # TODO add verification for dim_student update
            #update_last_name = select([dim_student.c.last_name], and_(dim_student.c.studne_guid))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()