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
        pass

    def test_load_sbac_csv(self, ):
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
        move_data_from_staging_to_integration(conf)


if __name__ == '__main__':
    unittest.main()
