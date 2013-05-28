'''
Created on May 24, 2013

@author: ejen
'''
import sys
import os
import unittest
import logging
from udl2.database import UDL_METADATA
from udl2_util.database_util import connect_db, execute_queries, get_table_columns_info
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
from fileloader.file_loader import load_file
import imp
import re


class FuncTestLoadToIntegrationTable(unittest.TestCase):

    def setUp(self, ):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

    def tearDown(self, ):
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
        execute_queries(conn, [sql_stg, sql_int], except_msg )
    
    
    def load_file_to_stage(self, ):
        # file contain 30 rows
        conf = {
            'csv_file':os.getcwd() + '/' + '../data/test_file_realdata.csv',
            'header_file': os.getcwd() + '/' + '../data/test_file_headers.csv',
            'csv_table': 'csv_table_for_file_loader',
            'db_host': self.conf['udl2_db']['db_host'],
            'db_port': self.conf['udl2_db']['db_port'],
            'db_user': self.conf['udl2_db']['db_user'],
            'db_name': self.conf['udl2_db']['db_database'],
            'db_password': self.conf['udl2_db']['db_pass'],
            'csv_schema': self.conf['udl2_db']['staging_schema'],
            'fdw_server': 'udl2_fdw_server',
            'staging_schema': self.conf['udl2_db']['staging_schema'],
            'staging_table': 'STG_SBAC_ASMT_OUTCOME',
            'apply_rules': False,
            'start_seq': 10,
            'batch_id': '00000000-0000-0000-0000-000000000000'
        }
        load_file(conf)
    

    def preloading_count(self, ):
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
    
    
    def postloading_count(self, ):
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
    
    
    def test_load_sbac_csv(self, ):
        '''
        functional tests for testing load from staging to integration as an independent unit tests.
        Use a fixed UUID for the moment. may be dynamic later.
        
        it loads 30 records from test csv file to stagint table then move it to integration. 
        '''
        conf = {
             # add batch_id from msg
            'batch_id': '00000000-0000-0000-0000-000000000000',
            # error schema
            'error_schema': self.conf['udl2_db']['staging_schema'],
            # source schema
            'source_schema': self.conf['udl2_db']['staging_schema'],
            # source database setting
            'db_host_source': self.conf['udl2_db']['db_host'],
            'db_port_source': self.conf['udl2_db']['db_port'],
            'db_user_source': self.conf['udl2_db']['db_user'],
            'db_name_source': self.conf['udl2_db']['db_database'],
            'db_password_source': self.conf['udl2_db']['db_pass'],
            'db_driver_source': self.conf['udl2_db']['db_driver'],

            # target schema
            'target_schema': self.conf['udl2_db']['integration_schema'],
            # target database setting
            'db_host_target': self.conf['udl2_db']['db_host'],
            'db_port_target': self.conf['udl2_db']['db_port'],
            'db_user_target': self.conf['udl2_db']['db_user'],
            'db_name_target': self.conf['udl2_db']['db_database'],
            'db_password_target': self.conf['udl2_db']['db_pass'],
            'map_type': 'staging_to_integration_sbac_asmt_outcome',
        }
        self.conf['batch_id'] = '00000000-0000-0000-0000-000000000000'
        self.load_file_to_stage()
        preloading_total = self.postloading_count()
        print(preloading_total)
        move_data_from_staging_to_integration(conf)
        postloading_total = self.postloading_count()
        print(postloading_total)
        self.assertEqual(preloading_total + 30, postloading_total)

if __name__ == '__main__':
    unittest.main()
