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
from move_to_integration.move_to_integration import move_data_from_staging_to_integration, create_migration_query
from move_to_integration.column_mapping import get_column_mapping
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import re
from collections import OrderedDict
from udl2 import message_keys as mk

class TestLoadToIntegrationTable(unittest.TestCase):

    def setUp(self, ):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf 

    def tearDown(self, ):
        pass

    def test_get_column_mapping(self, ):
        # test unit test table exists with the fixture data
        self.assertEqual(get_column_mapping('unit_test'),
                        {'source': 'STG_MOCK_LOAD',
                         'target': 'INT_MOCK_LOAD',
                         'error': 'ERR_LIST',
                         'mapping': OrderedDict([
                            ('batch_id', ("{src_field}", "batch_id")),
                            ('substr_test', ("SUBSTR({src_field}, 1, 10)", "substr_test")),
                            ('number_test', ("TO_NUMBER({src_field}, '99999')", "number_test")),
                            ])
                        })
    
    def test_create_migration_query(self, ):
        # get unit test column mapping
        self.maxDiff = None
        query_result = """
        INSERT INTO "udl2"."INT_MOCK_LOAD"
            (batch_id, substr_test, number_test)
        SELECT A.batch_id, SUBSTR(A.substr_test, 1, 10), TO_NUMBER(A.number_test, '99999')
            FROM "udl2"."STG_MOCK_LOAD" AS A LEFT JOIN
            "udl2"."ERR_LIST" AS B ON (A.record_sid = B.record_sid )
             WHERE B.record_sid IS NULL AND A.batch_id = '00000000-0000-0000-0000-000000000000'
        """
        unit_test_column_mapping = get_column_mapping('unit_test')
        query = create_migration_query('udl2', unit_test_column_mapping['source'],
                                       'udl2', unit_test_column_mapping['target'],
                                       'udl2', unit_test_column_mapping['error'],
                                       unit_test_column_mapping['mapping'],
                                       '00000000-0000-0000-0000-000000000000')
        # remove new lines, tab and multiple space. then the query should always be the same
        # because it should be the same query
        # whenever template changes, we should change the tests to make it correct.
        
        self.assertEqual(re.sub('\s+', ' ', query_result.replace('\n', ' ').replace('\t', ' ')),
                         re.sub('\s+', ' ', query.replace('\n', ' ').replace('\t', ' ')))
        
        
    def test_move_data_from_staging_to_integration(self, ):
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

            mk.ERROR_DB_SCHEMA: self.conf['udl2_db']['staging_schema'],

            mk.MAP_TYPE: 'unit_test'
        }
       
        move_data_from_staging_to_integration(conf)

    

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
