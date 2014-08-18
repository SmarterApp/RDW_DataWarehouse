'''
Created on Aug 15, 2014

@author: bpatel
'''
import unittest
import os
import shutil
from sqlalchemy.sql import select
import time
from time import sleep
from edudl2.database.udl2_connector import get_udl_connection
from uuid import uuid4
import subprocess
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql import select, and_
from edudl2.database.udl2_connector import get_target_connection, get_prod_connection,\
    initialize_all_db
from integration_tests.udl_helper import empty_batch_table, empty_stats_table, migrate_data, validate_edware_stats_table_before_mig, validate_edware_stats_table_after_mig
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf
from edudl2.udl2.constants import Constants


class TestMultiUdlBatch(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data", "test_multi_udl_batch")
        self.tenant = 'cat'
        initialize_all_db(udl2_conf, udl2_flat_conf)
        empty_batch_table(self)
        empty_stats_table(self)
        self.expected_unique_batch_guids = 2

    def tearDown(self):
            if os.path.exists(self.tenant_dir):
                shutil.rmtree(self.tenant_dir)

    def test_multi_udl_batch(self):
        self.guid_batch_id = str(uuid4())
        self.guid = self.guid_batch_id
        self.archived_file = os.path.join(self.data_dir, 'test_data.tar.gz.gpg')
        self.run_udl_pipeline(self.guid_batch_id, self.archived_file)
        self.run_udl_with_second_file()
        validate_edware_stats_table_before_mig(self)
        migrate_data(self)
        time.sleep(15)
        validate_edware_stats_table_after_mig(self)
        self.validate_after_migration(self.guid_batch_id, self.guid)

    def run_udl_with_second_file(self):
        self.guid_batch_id = str(uuid4())
        self.archived_file = os.path.join(self.data_dir, 'ASMT_ID_76a9ab517e76402793d3f2339391f5.tar.gz.gpg')
        self.run_udl_pipeline(self.guid_batch_id, self.archived_file)
        self.check_job_completion()

    def run_udl_pipeline(self, guid_batch_id, file_to_load):
        arch_file = self.copy_file_to_tmp(file_to_load)
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=self.guid_batch_id)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    def validate_after_migration(self, guid_batch_id, guid):
        with get_prod_connection(self.tenant) as conn:
            fact_table = conn.get_table('fact_asmt_outcome_vw')
            query = select([fact_table.c.rec_status], and_(fact_table.c.batch_guid == guid_batch_id, fact_table.c.student_id == '72947dea9aef496089d39fa47556ae'))
            result = conn.execute(query).fetchall()
            query_new = select([fact_table.c.rec_status], and_(fact_table.c.batch_guid == guid, fact_table.c.student_id == '72947dea9aef496089d39fa47556ae'))
            result_new = conn.execute(query_new).fetchall()
            self.assertEquals(result, [('C',)])
            self.assertEquals(result_new, [('I',)])

    #Copy file to tenant folder
    def copy_file_to_tmp(self, file_to_copy):
        if not os.path.exists(self.tenant_dir):
            os.makedirs(self.tenant_dir)
        return shutil.copy2(file_to_copy, self.tenant_dir)

    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS', batch_table.c.guid_batch == self.guid_batch_id))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            self.assertEqual(len(result), 1, "UDL pipeline fils")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()