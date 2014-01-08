'''
Created on May 24, 2013

@author: ejen
'''
import os
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
from fileloader.file_loader import load_file
from udl2 import message_keys as mk
from tests.functional_tests.util import UDLTestHelper
import rule_maker.rules.code_generator_special_rules as sr
from udl2_util.database_util import execute_queries
from move_to_target import move_to_target, move_to_target_setup
from tests.functional_tests.util import UDLTestHelper
from udl2.udl2_connector import UDL2DBConnection,TargetDBConnection, initialize_db
from conf.udl2_conf import udl2_conf


class FuncTestLoadToIntegrationTable(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(FuncTestLoadToIntegrationTable, cls).setUpClass()
        initialize_db(UDL2DBConnection, udl2_conf)
        initialize_db(TargetDBConnection, udl2_conf)

    def load_file_to_stage(self,):
        # file contain 30 rows
        conf = {
            mk.FILE_TO_LOAD: os.path.join(self.udl2_conf['zones']['datafiles'], 'test_file_realdata.csv'),
            mk.HEADERS: os.path.join(self.udl2_conf['zones']['datafiles'], 'test_file_headers.csv'),
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

        derived_count = int_demo_dict.pop('dmg_eth_derived', None)
        assert derived_count
        assert stg_demo_dict == int_demo_dict

    def test_derive_eth_function(self):
        function_name = sr.special_rules['deriveEthnicity'][0]
        # dmg_eth_blk, dmg_eth_asn, dmg_eth_hsp, dmg_eth_ami, dmg_eth_pcf, dmg_eth_wht
        prepare_data = {'exception': {'src_column': "'sda', 'dg', 'a', 'q', 't', 'fff'", 'expected_code': -1},
                        'not stated 1': {'src_column': "NULL, NULL, NULL, NULL, NULL, NULL", 'expected_code': 0},
                        'not stated 2': {'src_column': "'f', NULL, NULL, 'f', NULL, 'f'", 'expected_code': 0},
                        'african american': {'src_column': "'y', 'n', 'n', 'n', 'n', 'n'", 'expected_code': 1},
                        'asian': {'src_column': "'n', 'y', 'n', 'n', 'n', 'n'", 'expected_code': 2},
                        'hispanic 1': {'src_column': "'n', 'n', 'y', 'n', 'n', 'n'", 'expected_code': 3},
                        'hispanic 2': {'src_column': "'n', 'n', 'y', 'y', 'n', 'y'", 'expected_code': 3},
                        'native american': {'src_column': "'n', 'n', 'n', 'y', 'n', 'n'", 'expected_code': 4},
                        'pacific islander': {'src_column': "'n', 'n', 'n', 'n', 'y', 'n'", 'expected_code': 5},
                        'white': {'src_column': "'n', 'n', 'n', 'n', 'n', 'y'", 'expected_code': 6},
                        'two or more races 1': {'src_column': "'y', 'n', 'n', 'n', 'n', 'y'", 'expected_code': 7},
                        'two or more races 2': {'src_column': "'n', 'y', 'n', 'n', NULL, 'y'", 'expected_code': 7},
                        'two or more races 3': {'src_column': "'y', 'y', 'n', 'y', 'y', 'y'", 'expected_code': 7}
                        }
        sql_template = 'SELECT %s;' % function_name
        for _key, value in prepare_data.items():
            sql = sql_template.format(src_column=value['src_column'])
            result = self.udl2_conn.execute(sql)
            actual_value = ''
            for r in result:
                actual_value = r[0]
                break
            self.assertEqual(actual_value, value['expected_code'])
