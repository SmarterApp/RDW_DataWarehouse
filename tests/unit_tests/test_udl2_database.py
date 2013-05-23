'''
Created on May 22, 2013

@author: ejen
'''
import sys
import os
import unittest
import logging
from udl2.database import UDL_METADATA
from udl2_util.database_util import connect_db, execute_queries, get_table_columns_info
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import re


logger = logging.getLogger()
logger.level = logging.DEBUG
        

class TestUdl2Database(unittest.TestCase):
    
    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
    
    def tearDown(self):
        pass
    
    def _create_conn_engine(self, udl2_conf):
        (conn, engine) = connect_db(udl2_conf['udl2_db']['db_driver'],
                                udl2_conf['udl2_db']['db_user'],
                                udl2_conf['udl2_db']['db_pass'],
                                udl2_conf['udl2_db']['db_host'],
                                udl2_conf['udl2_db']['db_port'],
                                udl2_conf['udl2_db']['db_name'])
        return (conn, engine)

    
    
    def _compare_column_names(self,  ddl_in_code, ddl_in_db):
        ddl_code_column_names = [c[0] for c in ddl_in_code]
        ddl_db_column_names = [c[0] for c in ddl_in_db]
        return ddl_code_column_names == ddl_db_column_names
        
        
    def _compare_column_types(self, ddl_in_code, ddl_in_db):
        ddl_code_column_types = []
        for c in ddl_in_code:
            column_type = re.sub('\(.+\)', '', c[2])
            if column_type == 'bigserial':
                column_type = 'bigint'
            if column_type == 'json':
                column_type = 'text' # sql alchmey generated it as text
            ddl_code_column_types.append(column_type)
        ddl_db_column_types = []
        for c in ddl_in_db:
            column_type = c[1]
            if c[1] == 'bigserial':
                column_type = 'bigint'
            elif c[1] == 'character varying':
                column_type = 'varchar'
            elif c[1] == 'timestamp without time zone':
                column_type = 'timestamp'
            elif c[1] == 'double precision':
                column_type = 'double'
            ddl_db_column_types.append(column_type)
        
        return ddl_code_column_types == ddl_db_column_types
    
    def _compare_column_sizes(self, ddl_in_code, ddl_in_db):
        ddl_code_column_sizes = []
        for c in ddl_in_code:
            found = re.findall('\(.+\)', c[2])
            if len(found) > 0:
                ddl_code_column_sizes.append(found[0].replace('(', '').replace(')', ''))
            else:
                ddl_code_column_sizes.append('None')
        ddl_db_column_sizes = [str(c[2]) for c in ddl_in_db]
        return ddl_code_column_sizes == ddl_db_column_sizes
    
    
    def _compare_columns(self, ddl_in_code, ddl_in_db):
        if len(ddl_in_code) != len(ddl_in_db):
            return False
        elif not self._compare_column_names(ddl_in_code, ddl_in_db):
            return False
        elif not self._compare_column_types(ddl_in_code, ddl_in_db):
            return False
        elif not self._compare_column_sizes(ddl_in_code, ddl_in_db):
            return False
        else:
            return True
        
    
    def _compare_table_defition_in_code_and_database(self, table_name):
        (conn, engine) = self._create_conn_engine(self.conf)
        ddl_in_code = UDL_METADATA['TABLES'][table_name]['columns']
        ddl_in_db = get_table_columns_info(conn, table_name)
        return self._compare_columns(ddl_in_code, ddl_in_db)


    def test_STG_SBAC_ASMT(self):
        table_name = 'STG_SBAC_ASMT'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))
        

    def test_STG_SBAC_ASMT_OUTCOME(self):
        table_name = 'STG_SBAC_ASMT_OUTCOME'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))
    

    def test_INT_SBAC_ASMT(self):
        table_name = 'INT_SBAC_ASMT'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    
    def test_INT_SBAC_ASMT_OUTCOME(self):
        table_name = 'INT_SBAC_ASMT_OUTCOME'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    
    def test_ERR_LIST(self):
        table_name = 'ERR_LIST'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    
    def test_UDL_BATCH(self):
        table_name = 'UDL_BATCH'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
