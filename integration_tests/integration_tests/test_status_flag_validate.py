'''
Created on Mar 28, 2014

@author: bpatel
'''
import unittest
from integration_tests.udl_helper import empty_batch_table, empty_stats_table, run_udl_pipeline, \
    migrate_data, validate_edware_stats_table_before_mig, validate_edware_stats_table_after_mig
import os
import shutil
from uuid import uuid4
from edudl2.database.udl2_connector import get_prod_connection
from sqlalchemy.sql import select
from integration_tests import IntegrationTestCase


class Test_Validate_Status_Flag(IntegrationTestCase):

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.archived_file = self.require_gpg_file('test_status_flag')
        empty_stats_table(self)
        self.status_validation()
        self.first_guid = self.guid
        self.tenant = 'cat'

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
        with get_prod_connection(self.tenant) as connection:
            fact_asmt_outcome_vw = connection.get_table('fact_asmt_outcome_vw')
            connection.get_table('dim_inst_hier')
            dim_student = connection.get_table('dim_student')
            tables = [fact_asmt_outcome_vw, dim_student]
            for table in tables:
                inactive_rec = select([table.c.rec_status]).where(table.c.batch_guid == self.first_guid)
                inactive_rec_result = connection.execute(inactive_rec).fetchall()
                expected_inactive_rec_result = [('I',), ('I',), ('I',)]
                self.assertEqual(inactive_rec_result, expected_inactive_rec_result, "Duplicate record inserted into dim tables")
                active_rec = select([table.c.rec_status]).where(table.c.batch_guid == second_guid)
                active_rec_result = connection.execute(active_rec).fetchall()
                expected_active_rec_result = [('C',), ('C',), ('C',)]
                self.assertEqual(active_rec_result, expected_active_rec_result, "Duplicate record inserted into dim tables")

if __name__ == "__main__":
    unittest.main()
