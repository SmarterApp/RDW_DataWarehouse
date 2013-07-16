'''
Created on May 24, 2013

@author: ejen
'''
import sys
import os
import unittest
import logging
from udl2 import database
from udl2.database import UDL_METADATA
from udl2_util.database_util import connect_db, execute_queries, get_table_columns_info
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
from fileloader.file_loader import load_file
import imp
import re
from udl2 import message_keys as mk


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
            WHERE batch_id = '{batch_id}'
            """
        sql_stg = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                  staging_table='STG_SBAC_ASMT_OUTCOME',
                                  batch_id=self.conf['batch_id'])
        sql_int = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                  staging_table='INT_SBAC_ASMT_OUTCOME',
                                  batch_id=self.conf['batch_id'])
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
            mk.BATCH_ID: '00000000-0000-0000-0000-000000000000'
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
            WHERE batch_id = '{batch_id}'
        """
        sql = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                  staging_table='INT_SBAC_ASMT_OUTCOME',
                                  batch_id=self.conf['batch_id'])
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
            WHERE batch_id = '{batch_id}'
        """
        sql = sql_template.format(staging_schema=self.conf['udl2_db']['staging_schema'],
                                  staging_table='INT_SBAC_ASMT_OUTCOME',
                                  batch_id=self.conf['batch_id'])
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
            mk.BATCH_ID: '00000000-0000-0000-0000-000000000000',
            mk.SOURCE_DB_DRIVER: self.conf['udl2_db']['db_driver'],

            # source database setting
            mk.SOURCE_DB_HOST: self.conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: self.conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: self.conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: self.conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: self.conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_SCHEMA: self.conf['udl2_db']['staging_schema'],

            # target database setting
            mk.TARGET_DB_HOST: self.conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.conf['udl2_db']['db_pass'],
            mk.TARGET_DB_SCHEMA: self.conf['udl2_db']['integration_schema'],

            mk.REF_TABLE: self.conf['udl2_db']['ref_table_name'],
            mk.ERROR_DB_SCHEMA: self.conf['udl2_db']['staging_schema'],

            mk.MAP_TYPE: 'staging_to_integration_sbac_asmt_outcome'
        }
        self.conf['batch_id'] = '00000000-0000-0000-0000-000000000000'
        self.load_file_to_stage()
        preloading_total = self.postloading_count()
        print(preloading_total)
        move_data_from_staging_to_integration(conf)
        postloading_total = self.postloading_count()
        print(postloading_total)
        self.assertEqual(preloading_total + 30, postloading_total)

        int_avg_query=""" SELECT avg(score_asmt::int),
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
	        avg(score_claim_4_max) FROM udl2."INT_SBAC_ASMT_OUTCOME" """
        result = self.udl2_conn.execute(int_avg_query)
        for row in result:
            int_asmt_avgs = row

        stg_avg_query=""" select avg(score_asmt::int),
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
	        avg(score_claim_4_max::int) from udl2."STG_SBAC_ASMT_OUTCOME";"""
        result = self.udl2_conn.execute(stg_avg_query)
        for row in result:
            stg_asmt_avgs = row

        assert stg_asmt_avgs == int_asmt_avgs

if __name__ == '__main__':
    unittest.main()
