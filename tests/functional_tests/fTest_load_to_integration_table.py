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
from move_to_integration.move_to_integration import move_data_from_staging_to_integration, create_migration_query
import imp
import re


class FuncTestLoadToIntegrationTable(unittest.TestCase):

    def setUp(self, ):
        pass

    def tearDown(self, ):
        pass

    def load_sbac_csv(self, ):
        pass


if __name__ == '__main__':
    unittest.main()
