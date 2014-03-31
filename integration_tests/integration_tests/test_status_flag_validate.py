'''
Created on Mar 28, 2014

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


class Test_Validate_Status_Flag(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.archived_file = os.path.join(self.data_dir, 'test_status_flag.tar.gz.gpg')
        empty_stats_table(self)
        self.status_validation()
        self.first_guid = self.guid

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def status_validation(self):
        empty_batch_table(self)
        guid_batch_id = str(uuid4())
        self.guid = guid_batch_id
        run_udl_pipeline(self, guid_batch_id)
        print("UDL pipeleine completed successfully one time")

    def test_status_flag(self):
        self.status_validation()
        print("UDL pipeline completed second time")
        validate_edware_stats_table_before_mig(self)
        migrate_data(self)
        validate_edware_stats_table_after_mig(self)
        self.validate_edware_prod()

    def validate_edware_prod(self):
        second_guid = self.guid
        with get_prod_connection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            dim_inst_hier = connection.get_table('dim_inst_hier')
            dim_student = connection.get_table('dim_student')
            tables = [fact_asmt_outcome, dim_student]
            for table in tables:
                inactive_rec = select([table.c.rec_status]).where(table.c.batch_guid == self.first_guid)
                inactive_rec_result = connection.execute(inactive_rec).fetchall()
                expected_inactive_rec_result = [('I',), ('I',), ('I',)]
                self.assertEqual(inactive_rec_result, expected_inactive_rec_result, "Duplicate record inserted into dim tables")
                active_rec = select([table.c.rec_status]).where(table.c.batch_guid == second_guid)
                active_rec_result = connection.execute(active_rec).fetchall()
                expected_active_rec_result = [('C',), ('C',), ('C',)]
                self.assertEqual(active_rec_result, expected_active_rec_result, "Duplicate record inserted into dim tables")
            #TODO add verifications for dim_asmt and dim_inst_hier

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
