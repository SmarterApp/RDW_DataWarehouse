'''
Created on Mar 28, 2014

@author: bpatel
'''
from edudl2.udl2.celery import udl2_conf
from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql import select, and_
from edcore.database.stats_connector import StatsDBConnection
import os
import shutil
import subprocess
from time import sleep
from integration_tests.migrate_helper import start_migrate,\
    get_stats_table_has_migrated_ingested_status
from edudl2.udl2.constants import Constants


def empty_batch_table(self):
        #Delete all data from batch_table
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)


def empty_stats_table(self):
        #Delete all data from udl_stats table inside edware_stats DB
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            conn.execute(table.delete())
            query = select([table])
            query_tab = conn.execute(query).fetchall()
            no_rows = len(query_tab)
            self.assertEqual(no_rows, 0)


#Copy file to tenant folder
def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            print("copying")
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)


#Run UDL pipeline with file in tenant dir
def run_udl_pipeline(self, guid_batch_id):
        self.conf = udl2_conf
        arch_file = copy_file_to_tmp(self)
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        check_job_completion(self)


#Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
def check_job_completion(self, max_wait=60):
        with get_udl_connection() as connector:
            print("UDL Pipeline is running...")
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            self.assertEqual(len(result), 1, "1 guids not found.")
            print('Waited for', timer, 'second(s) for job to complete.')


# Trigger migration
def migrate_data(self):
        start_migrate()
        tenant = 'cat'
        results = get_stats_table_has_migrated_ingested_status(tenant)
        for result in results:
            self.assertEqual(result['load_status'], 'migrate.ingested')


def validate_edware_stats_table_before_mig(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('udl.ingested',), ('udl.ingested',)]
            self.assertEquals(result, expected_result)


# Validate udl_stats table under edware_stats DB for successful migration
def validate_edware_stats_table_after_mig(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('migrate.ingested',), ('migrate.ingested',)]
            self.assertEquals(result, expected_result)


# Validate udl_stars table with single batch(file) in migration
def validate_udl_stats_before_mig(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('udl.ingested',)]
            self.assertEquals(result, expected_result)
            print("Ready for migration")


#validate udl_stats after single udl pipeline and before migration start.
def validate_udl_stats_after_mig(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('migrate.ingested',)]
            self.assertEquals(result, expected_result)
            print("Migration is complete")
