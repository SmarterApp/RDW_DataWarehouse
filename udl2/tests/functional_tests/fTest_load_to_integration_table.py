'''
Created on May 24, 2013

@author: ejen
'''
import os
import unittest
from udl2 import database
from udl2_util.database_util import connect_db, execute_queries
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
from fileloader.file_loader import load_file
import imp
from udl2 import message_keys as mk
import rule_maker.rules.code_generator_special_rules as sr


class FuncTestLoadToIntegrationTable(unittest.TestCase):

    def setUp(self,):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
        self.udl2_conf = udl2_conf
        self.udl2_conn, self.udl2_engine = database._create_conn_engine(self.udl2_conf['udl2_db'])

    def tearDown(self,):
        (conn, engine) = connect_db(self.conf['udl2_db']['db_driver'],
                                    self.conf['udl2_db']['db_user'],
                                    self.conf['udl2_db']['db_pass'],
                                    self.conf['udl2_db']['db_host'],
                                    self.conf['udl2_db']['db_port'],
                                    self.conf['udl2_db']['db_name'])
        sql_template = """
            DELETE FROM "{staging_schema}"."{staging_table}"
            WHERE guid_batch = '{guid_batch}'
            """
        sql_stg = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                      staging_table='STG_SBAC_ASMT_OUTCOME',
                                      guid_batch=self.conf['guid_batch'])
        sql_int = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                      staging_table='INT_SBAC_ASMT_OUTCOME',
                                      guid_batch=self.conf['guid_batch'])
        except_msg = "Can't not clean up test data from staging table inside functional test FuncTestLoadToIntegrationTable("
        execute_queries(conn, [sql_stg, sql_int], except_msg)

    def load_file_to_stage(self,):
        # file contain 30 rows
        conf = {
            mk.FILE_TO_LOAD: os.getcwd() + '/' + '../data/test_file_realdata.csv',
            mk.HEADERS: os.getcwd() + '/' + '../data/test_file_headers.csv',
            mk.CSV_TABLE: 'csv_table_for_file_loader',
            mk.TARGET_DB_HOST: self.conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.conf['udl2_db']['db_pass'],
            mk.CSV_SCHEMA: self.conf['udl2_db']['staging_schema'],
            mk.REF_TABLE: self.conf['udl2_db']['ref_table_name'],
            mk.CSV_LZ_TABLE: self.conf['udl2_db']['csv_lz_table'],
            mk.FDW_SERVER: 'udl2_fdw_server',
            mk.TARGET_DB_SCHEMA: self.conf['udl2_db']['staging_schema'],
            mk.TARGET_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',
            mk.APPLY_RULES: False,
            mk.ROW_START: 10,
            mk.GUID_BATCH: '00000000-0000-0000-0000-000000000000'
        }
        load_file(conf)

    def preloading_count(self,):
        (conn, engine) = connect_db(self.conf['udl2_db']['db_driver'],
                                    self.conf['udl2_db']['db_user'],
                                    self.conf['udl2_db']['db_pass'],
                                    self.conf['udl2_db']['db_host'],
                                    self.conf['udl2_db']['db_port'],
                                    self.conf['udl2_db']['db_name'])
        sql_template = """
            SELECT COUNT(*) FROM "{staging_schema}"."{staging_table}"
            WHERE guid_batch = '{guid_batch}'
        """
        sql = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                  staging_table='INT_SBAC_ASMT_OUTCOME',
                                  guid_batch=self.conf['guid_batch'])
        result = conn.execute(sql)
        count = 0
        for row in result:
            count = row[0]
        return count

    def postloading_count(self,):
        (conn, engine) = connect_db(self.conf['udl2_db']['db_driver'],
                                    self.conf['udl2_db']['db_user'],
                                    self.conf['udl2_db']['db_pass'],
                                    self.conf['udl2_db']['db_host'],
                                    self.conf['udl2_db']['db_port'],
                                    self.conf['udl2_db']['db_name'])
        sql_template = """
            SELECT COUNT(*) FROM "{staging_schema}"."{staging_table}"
            WHERE guid_batch = '{guid_batch}'
        """
        sql = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                  staging_table='INT_SBAC_ASMT_OUTCOME',
                                  guid_batch=self.conf['guid_batch'])
        result = conn.execute(sql)
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
            mk.SOURCE_DB_DRIVER: self.conf['udl2_db']['db_driver'],

            # source database setting
            mk.SOURCE_DB_HOST: self.conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: self.conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: self.conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: self.conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: self.conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_SCHEMA: self.conf['udl2_db']['staging_schema'],
            mk.SOURCE_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',

            # target database setting
            mk.TARGET_DB_HOST: self.conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.conf['udl2_db']['db_pass'],
            mk.TARGET_DB_SCHEMA: self.conf['udl2_db']['integration_schema'],
            mk.TARGET_DB_TABLE: 'INT_SBAC_ASMT_OUTCOME',

            mk.REF_TABLE: self.conf['udl2_db']['ref_table_name'],
            mk.ERROR_DB_SCHEMA: self.conf['udl2_db']['staging_schema'],

        }
        self.conf['guid_batch'] = '00000000-0000-0000-0000-000000000000'
        self.load_file_to_stage()
        preloading_total = self.postloading_count()
        print(preloading_total)
        move_data_from_staging_to_integration(conf)
        postloading_total = self.postloading_count()
        print(postloading_total)
        self.assertEqual(preloading_total + 30, postloading_total)

        int_avg_query = """ SELECT avg(score_asmt::int),
        avg(score_asmt_min),
        avg(score_asmt_max),
        avg(score_claim_1),
        avg(score_claim_1_min),
        avg(score_claim_1_max),
        avg(score_claim_2),
        avg(score_claim_2_min),
        avg(score_claim_2_max),
        avg(score_claim_3),
        avg(score_claim_3_min),
        avg(score_claim_3_max),
        avg(score_claim_4),
        avg(score_claim_4_min),
        avg(score_claim_4_max) FROM "udl2"."INT_SBAC_ASMT_OUTCOME" WHERE guid_batch='{guid_batch}'""".format(guid_batch=self.conf['guid_batch'])
        result = self.udl2_conn.execute(int_avg_query)
        for row in result:
            int_asmt_avgs = row

        stg_avg_query = """ select avg(score_asmt::int),
        avg(score_asmt_min::int),
        avg(score_asmt_max::int),
        avg(score_claim_1::int),
        avg(score_claim_1_min::int),
        avg(score_claim_1_max::int),
        avg(score_claim_2::int),
        avg(score_claim_2_min::int),
        avg(score_claim_2_max::int),
        avg(score_claim_3::int),
        avg(score_claim_3_min::int),
        avg(score_claim_3_max::int),
        avg(score_claim_4::int),
        avg(score_claim_4_min::int),
        avg(score_claim_4_max::int) from "udl2"."STG_SBAC_ASMT_OUTCOME"  WHERE guid_batch='{guid_batch}';""".format(guid_batch=self.conf['guid_batch'])
        result = self.udl2_conn.execute(stg_avg_query)
        for row in result:
            stg_asmt_avgs = row

        assert stg_asmt_avgs == int_asmt_avgs

        # get staging demographics counts
        demographics = ['dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1']
        stg_demo_dict = {}
        int_demo_dict = {}

        for entry in demographics:
            # get staging
            demo_query = """ select count({demographic}) from "udl2"."STG_SBAC_ASMT_OUTCOME" where guid_batch='{guid_batch}' and ({demographic} = 'Y' or {demographic} = 'y' or {demographic} = 'yes');""".format(demographic=entry, guid_batch=self.conf['guid_batch'])
            result = self.udl2_conn.execute(demo_query)
            for row in result:
                demo_count = row[0]

            stg_demo_dict[entry] = demo_count
            # get integration
            demo_query = """ select count({demographic}) from "udl2"."INT_SBAC_ASMT_OUTCOME" where guid_batch='{guid_batch}' and {demographic} = 'TRUE';""".format(guid_batch=self.conf['guid_batch'], demographic=entry)

            result = self.udl2_conn.execute(demo_query)
            for row in result:
                demo_count = row[0]

            int_demo_dict[entry] = demo_count

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
        self.conf['guid_batch'] = '00000000-0000-0000-0000-000000000000'
        (conn, _engine) = connect_db(self.conf['udl2_db']['db_driver'],
                                     self.conf['udl2_db']['db_user'],
                                     self.conf['udl2_db']['db_pass'],
                                     self.conf['udl2_db']['db_host'],
                                     self.conf['udl2_db']['db_port'],
                                     self.conf['udl2_db']['db_name'])
        sql_template = 'SELECT %s;' % function_name
        for _key, value in prepare_data.items():
            sql = sql_template.format(src_column=value['src_column'])
            result = conn.execute(sql)
            actual_value = ''
            for r in result:
                actual_value = r[0]
                break
            self.assertEqual(actual_value, value['expected_code'])

if __name__ == '__main__':
    unittest.main()
