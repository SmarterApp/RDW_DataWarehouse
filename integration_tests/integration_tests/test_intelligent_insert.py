'''
Created on Mar 7, 2014

@author: bpatel
This test will validate intelligent insert to dim tables and forign key validation.
Test Scenario: 1) Test file contains one record that is not exist in production.
               2) This test also verify that foregn keys into fact_asmt table is match to dim_tables 
               2) In second udl run, it will verify that duplicate records in fact_table is inactive. also in preprod dim tables status of duplicate record is S
'''
from sqlalchemy.schema import DropSchema
import unittest
import os
import shutil
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf
import time
from time import sleep
import subprocess
from uuid import uuid4
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection, get_prod_connection
from integration_tests.migrate_helper import start_migrate,\
    get_stats_table_has_migrated_ingested_status
from edcore.database.stats_connector import StatsDBConnection
from integration_tests.udl_helper import empty_batch_table, empty_stats_table, copy_file_to_tmp, run_udl_pipeline, \
    check_job_completion, migrate_data, validate_edware_stats_table_after_mig, validate_udl_stats_before_mig, validate_udl_stats_after_mig


#@unittest.skip("skipping this test till till ready for jenkins")
class Test_Intelligent_Insert(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.archived_file = os.path.join(self.data_dir, 'test_intelligent_insert.tar.gz.gpg')
        empty_batch_table(self)
        empty_stats_table(self)

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    # This method will call first, it will run the UDL and migrate data to production
    def test_intelligent_insert_validation(self):
        '''
        This test will run the udl pipeline twice with same file and with different batch_guid.
        '''
        self.guid_batch_id = str(uuid4())
        run_udl_pipeline(self, self.guid_batch_id)
        # Take the btach guid of first run in parameter for later verification
        self.guid = self.guid_batch_id

        # This method will verify that forien keys : asmt_rec_id, inst_hier.rec_id and student_rec_id is match with \
        # dim tables primary keys.
        self.validate_edware_database(schema_name=self.guid)
        validate_udl_stats_before_mig(self)
        migrate_data(self)

        # This method will verify that after the migration data got loaded successfully into production
        validate_udl_stats_after_mig(self)
        self.validate_prod(self.guid)

        # Run the udl pipeline againe with same file
        empty_stats_table(self)
        empty_batch_table(self)
        self.guid_batch_id = str(uuid4())
        run_udl_pipeline(self, self.guid_batch_id)
        time.sleep(5)
        self.validate_edware_database(schema_name=self.guid_batch_id)

        #this method will verify that for duplicate record ,status change to S in dim tables
        self.validate_prepod_tables(schema_name=self.guid_batch_id)
        validate_udl_stats_before_mig(self)
        migrate_data(self)
        validate_udl_stats_after_mig(self)

        # This method will verify that duplicate records status change to incative
        self.validate_prod_after_sec_migration()

    # Validate preprod edware schema for foriegn key validation
    def validate_edware_database(self, schema_name):
        with get_target_connection() as ed_connector:
            ed_connector.set_metadata_by_reflect(schema_name)
            fact_table = ed_connector.get_table('fact_asmt_outcome')
            pre_prod_data = select([fact_table.c.student_rec_id, fact_table.c.inst_hier_rec_id, fact_table.c.asmt_rec_id])
            pre_prod_table = ed_connector.execute(pre_prod_data).fetchall()
            self.expected_pk_val_for_student = pre_prod_table[0][0]
            self.expected_pk_val_for_inst = pre_prod_table[0][1]
            self.expected_pk_val_for_asmt = pre_prod_table[0][2]

            lean_table = ed_connector.get_table('fact_asmt_outcome_primary')
            pre_prod_data = select([lean_table.c.student_rec_id, fact_table.c.inst_hier_rec_id, fact_table.c.asmt_rec_id])
            pre_prod_table = ed_connector.execute(pre_prod_data).fetchall()
            self.lean_pk_val_for_student = pre_prod_table[0][0]
            self.lean_pk_val_for_inst = pre_prod_table[0][1]
            self.lean_pk_val_for_asmt = pre_prod_table[0][2]

            dim_student = ed_connector.get_table('dim_student')
            dim_student_data = select([dim_student.c.student_rec_id])
            result_student_id = ed_connector.execute(dim_student_data).fetchall()
            self.expected_student_id = result_student_id[0][0]

            dim_inst_hier = ed_connector.get_table('dim_inst_hier')
            dim_inst_hier_data = select([dim_inst_hier.c.inst_hier_rec_id])
            dim_inst_hier_result = ed_connector.execute(dim_inst_hier_data).fetchall()
            self.expected_inst_hier_rec_id = dim_inst_hier_result[0][0]

            dim_asmt = ed_connector.get_table('dim_asmt')
            dim_asmt_data = select([dim_asmt.c.asmt_rec_id])
            dim_asmt_result = ed_connector.execute(dim_asmt_data).fetchall()
            self.expected_asmt_rec_id = dim_asmt_result[0][0]

            self.assertEqual(self.expected_student_id, self.expected_pk_val_for_student, "Error:student_rec_id of dim table not maching to fact table")
            self.assertEqual(self.expected_inst_hier_rec_id, self.expected_pk_val_for_inst, "Error:student_rec_id of dim table not maching to fact table")
            self.assertEqual(self.expected_asmt_rec_id, self.expected_pk_val_for_asmt, "Error:student_rec_id of dim table not maching to fact table")

            self.assertEqual(self.expected_student_id, self.lean_pk_val_for_student, "Error:student_rec_id of dim table not maching to fact table")
            self.assertEqual(self.expected_inst_hier_rec_id, self.lean_pk_val_for_inst, "Error:student_rec_id of dim table not maching to fact table")
            self.assertEqual(self.expected_asmt_rec_id, self.lean_pk_val_for_asmt, "Error:student_rec_id of dim table not maching to fact table")

    # Validate preprod tables after second run of udl pipeline.
    # For duplicate data into dim tables status change to S
    def validate_prepod_tables(self, schema_name):
        with get_target_connection() as connection:
            connection.set_metadata_by_reflect(schema_name)
            fact_table = connection.get_table('fact_asmt_outcome')
            dim_inst_hier = connection.get_table('dim_inst_hier')
            dim_student = connection.get_table('dim_student')
            dim_asmt = connection.get_table('dim_asmt')
            dim_tables = [dim_asmt, dim_student, dim_inst_hier]
            for table in dim_tables:
                    query = select([table.c.rec_status])
                    result = connection.execute(query).fetchall()
                    expected_status = [('S',)]
                    self.assertEqual(result, expected_status, "Error: In Dim_tables rec_status have not change to S")
            fact_table_data = select([fact_table.c.rec_status])
            fact_table_rows = connection.execute(fact_table_data).fetchall()
            expected_status = [('C',)]
            self.assertEquals(fact_table_rows, expected_status, "Error")

    # Validate prod after the first udl run for data has been migrated to production successfully.
    def validate_prod(self, guid_batch_id):
        with get_prod_connection() as conn:
            fact_table = conn.get_table('fact_asmt_outcome')
            dim_asmt = conn.get_table('dim_asmt')
            dim_inst_hier = conn.get_table('dim_inst_hier')
            dim_student = conn.get_table('dim_student')
            dim_tables = [fact_table, dim_inst_hier, dim_asmt, dim_student]
            for table in dim_tables:
                query = select([table.c.rec_status]).where(table.c.batch_guid == guid_batch_id)
                result = conn.execute(query).fetchall()
                rec_status = result
                actual_status = [('C',)]
                actual_rows = len(result)
                expected_no_rows = 1
                self.assertEquals(rec_status, actual_status, "Error: Status is not C")
                self.assertEquals(actual_rows, expected_no_rows, "Data has not been loaded to prod  after edmigrate")

    # Validate prod dim tables and fact tables after second run of udl pipeleine.
    # This will verify that for duplicate records status changes to I (inactive)
    def validate_prod_after_sec_migration(self):
        with get_prod_connection() as conn:
            fact_table = conn.get_table('fact_asmt_outcome')
            query = select([fact_table.c.rec_status]).where(fact_table.c.batch_guid == self.guid_batch_id)
            result = conn.execute(query).fetchall()
            expected_status = [('C',)]
            self.assertEquals(result, expected_status, "Error: Error in Status of newly added record")
            # for new record , status change to C
            new_query = select([fact_table.c.rec_status]).where(fact_table.c.batch_guid == self.guid)
            new_result = conn.execute(new_query).fetchall()
            expected_old_status = [('I',)]
            self.assertEquals(new_result, expected_old_status, "Error:Error in status of inactive record ")
            dim_asmt = conn.get_table('dim_asmt')
            dim_inst_hier = conn.get_table('dim_inst_hier')
            dim_student = conn.get_table('dim_student')
            dim_tables = [dim_inst_hier, dim_asmt, dim_student]
            for table in dim_tables:
                rows_in_dim_tables = select([table]).where(table.c.batch_guid == self.guid_batch_id)
                actual_dim_table_rows = conn.execute(rows_in_dim_tables).fetchall()
                expected_rows_in_dim_tables = 0
                self.assertEquals(len(actual_dim_table_rows), expected_rows_in_dim_tables, "Error: Data has been loaded to dim_tables")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
