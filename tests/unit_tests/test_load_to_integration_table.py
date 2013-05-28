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
from collections import OrderedDict


class TestLoadToIntegrationTable(unittest.TestCase):

    def setUp(self, ):
        pass

    def tearDown(self, ):
        pass

    def test_move_data_from_staging_to_integration(self, ):
        pass

    def test_create_migration_query(self, ):
        pass
    
    def test_get_column_mapping(self, ):
        # test unit test table exists with the fixture data
        self.assertEqual(get_column_mapping('unit_test'),
                        {'source': 'STG_MOCK_LOAD',
                         'target': 'INT_MOCK_LOAD',
                         'error': 'ERR_LIST',
                         'mapping': OrderedDict([
                            ('batch_id', ("{src_field}", "batch_id")),
                            ('substr_test', ("SUBSTR({src_field}, 0, 10)", "substr_test")),
                            ('number_test', ("TO_NUMBER({src_field}, '99999')", "number_test")),
                            ])
                        })
        
    

if __name__ == '__main__':
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
