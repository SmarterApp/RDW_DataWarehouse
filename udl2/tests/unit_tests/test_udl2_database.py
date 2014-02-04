'''
Created on May 22, 2013

@author: ejen
'''
import os
import unittest
import logging
from udl2.database import UDL_METADATA
from udl2_util.database_util import connect_db, get_table_columns_info, get_schema_metadata
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import re
from udl2_util.config_reader import read_ini_file


logger = logging.getLogger()
logger.level = logging.DEBUG


class TestUdl2Database(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        self.conf = read_ini_file(config_path)

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

    def _compare_column_names(self, ddl_in_code, ddl_in_db):
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
                column_type = 'text'  # sql alchmey generated it as text
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
            elif c[1] == 'time without time zone':
                column_type = 'time'
            elif c[1] == 'double precision':
                column_type = 'double'
            elif c[1] == 'boolean':
                column_type = 'bool'
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

    def _compare_table_keys(self, table_keys_in_code, table_meta):
        foreign_k = table_keys_in_code.get('foreign', [])
        # TODO: Deterimine how to check unique keys

        # check that there are the same number of foreign keys
        self.assertEqual(len(table_meta.foreign_keys), len(foreign_k), 'length of foreign keys not equal')

        for col in table_meta.c:
            # Get foreign key definitions
            db_fks = col.foreign_keys

            # if no foreign keys in db for column, continue
            if not db_fks:
                continue

            # get list of foreign keys from code ddl for the current table
            code_fks = [x for x in foreign_k if x[0] == col.key]
            self.assertEquals(len(db_fks), len(code_fks))

            # place foreign keys in sets and compare them
            db_fks_targets = {x.target_fullname for x in db_fks}
            code_fks_targets = {x[1] for x in code_fks}

            # if the symmetric_difference of sets is not empty fail
            if code_fks_targets ^ db_fks_targets:
                return False

        return True

    def _compare_table_defition_in_code_and_database(self, table_name):
        (conn, engine) = self._create_conn_engine(self.conf)
        ddl_in_code = UDL_METADATA['TABLES'][table_name]['columns']
        ddl_in_db = get_table_columns_info(conn, table_name)
        ddl_in_code = sorted(ddl_in_code, key=lambda tup: tup[0])
        ddl_in_db = sorted(ddl_in_db, key=lambda tup: tup[0])
        print('ddl_in_code', ddl_in_code, '\nddl_in_db', ddl_in_db)
        return self._compare_columns(ddl_in_code, ddl_in_db)

    def _compare_table_key_definitions_in_code_and_db(self, table_name):
        (conn, engine) = self._create_conn_engine(self.conf)
        db_metadata = get_schema_metadata(engine)
        table_metadata = db_metadata.tables[table_name]
        table_keys_in_code = UDL_METADATA['TABLES'][table_name]['keys']

        return self._compare_table_keys(table_keys_in_code, table_metadata)

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

    def test_REF_COLUMN_MAPPING(self):
        table_name = 'REF_COLUMN_MAPPING'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))
        self.assertTrue(self._compare_table_key_definitions_in_code_and_db(table_name))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
