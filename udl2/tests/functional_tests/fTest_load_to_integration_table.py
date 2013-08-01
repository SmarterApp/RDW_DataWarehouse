'''
Created on May 24, 2013

@author: ejen
'''
import os
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
from fileloader.file_loader import load_file
from udl2 import message_keys as mk
from tests.functional_tests.util import UDLTestHelper


class FuncTestLoadToIntegrationTable(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(FuncTestLoadToIntegrationTable, cls).setUpClass()

    def load_file_to_stage(self,):
        # file contain 30 rows
        conf = {
            mk.FILE_TO_LOAD: os.getcwd() + '/' + '../data/test_file_realdata.csv',
            mk.HEADERS: os.getcwd() + '/' + '../data/test_file_headers.csv',
            mk.CSV_TABLE: 'csv_table_for_file_loader',
            mk.TARGET_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.CSV_SCHEMA: self.udl2_conf['udl2_db']['staging_schema'],
            mk.REF_TABLE: self.udl2_conf['udl2_db']['ref_table_name'],
            mk.CSV_LZ_TABLE: self.udl2_conf['udl2_db']['csv_lz_table'],
            mk.FDW_SERVER: 'udl2_fdw_server',
            mk.TARGET_DB_SCHEMA: self.udl2_conf['udl2_db']['staging_schema'],
            mk.TARGET_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',
            mk.APPLY_RULES: False,
            mk.ROW_START: 10,
            mk.GUID_BATCH: '00000000-0000-0000-0000-000000000000'
        }
        load_file(conf)

    def postloading_count(self,):
        sql_template = """
            SELECT COUNT(*) FROM "{staging_schema}"."{staging_table}"
            WHERE guid_batch = '{guid_batch}'
        """
        sql = sql_template.format(staging_schema=self.udl2_conf['udl2_db']['staging_schema'],
                                  staging_table='INT_SBAC_ASMT_OUTCOME',
                                  guid_batch=self.udl2_conf['guid_batch'])
        result = self.udl2_conn.execute(sql)
        count = 0
        for row in result:
            count = row[0]
        return count

    def test_load_sbac_csv(self,):
        '''
        functional tests for testing load from staging to integration as an independent unit tests.
        Use a fixed UUID for the moment. may be dynamic later.

        it loads 30 records from test csv file to stagint table then move it to integration.
        '''
        conf = {
            mk.GUID_BATCH: '00000000-0000-0000-0000-000000000000',
            mk.SOURCE_DB_DRIVER: self.udl2_conf['udl2_db']['db_driver'],

            # source database setting
            mk.SOURCE_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_SCHEMA: self.udl2_conf['udl2_db']['staging_schema'],
            mk.SOURCE_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',

            # target database setting
            mk.TARGET_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.TARGET_DB_SCHEMA: self.udl2_conf['udl2_db']['integration_schema'],
            mk.TARGET_DB_TABLE: 'INT_SBAC_ASMT_OUTCOME',

            mk.REF_TABLE: self.udl2_conf['udl2_db']['ref_table_name'],
            mk.ERROR_DB_SCHEMA: self.udl2_conf['udl2_db']['staging_schema'],

        }
        self.udl2_conf['guid_batch'] = '00000000-0000-0000-0000-000000000000'
        self.load_file_to_stage()
        move_data_from_staging_to_integration(conf)
        postloading_total = self.postloading_count()
        print(postloading_total)
        self.assertEqual(30, postloading_total)

        int_asmt_avgs = self.get_integration_asmt_score_avgs()
        stg_asmt_avgs = self.get_staging_asmt_score_avgs()

        assert stg_asmt_avgs == int_asmt_avgs

        stg_demo_dict = self.get_staging_demographic_counts()
        int_demo_dict = self.get_integration_demographic_counts()

        assert stg_demo_dict == int_demo_dict
