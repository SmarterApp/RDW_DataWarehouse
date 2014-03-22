'''
Created on May 22, 2013

@author: ejen
'''
import os
import unittest
import logging
import re
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2_util.database_util import connect_db, get_schema_metadata
from edudl2.database.metadata.udl2_metadata import generate_udl2_metadata


logger = logging.getLogger()
logger.level = logging.DEBUG


class TestUdl2Database(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        cls.conf = conf_tup[0]
        (cls.conn, cls.engine) = cls._create_conn_engine(cls.conf)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    @classmethod
    def _create_conn_engine(cls, udl2_conf):
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

    def _compare_columns(self, ddl_metadata, db_metadata, table_name):
        ddl_columns = ddl_metadata.tables[table_name].columns
        db_columns = db_metadata.tables[table_name].columns
        if len(ddl_columns) != len(db_columns):
            return False
        for col1, col2 in zip(ddl_columns, db_columns):
            if col1.name != col2.name:
                return False
            if not self._is_same_type(col1, col2):
                return False
        else:
            return True

    def _is_same_type(self, col1, col2):
        # have to check by isinstance() or type names because reflect metadata contains database(i.e. postgresql) specific types
        return isinstance(col2.type, type(col1.type)) or col1.__class__.__name__.lower() == col2.__class__.__name__.lower()

    def _compare_table_keys(self, ddl_meta, table_meta):
        # check that there are the same number of foreign keys
        self.assertEqual(ddl_meta.foreign_keys, table_meta.foreign_keys, 'foreign keys not equal')
        # check unique keys
        pk1 = [c.name for c in ddl_meta.primary_key.columns]
        pk2 = [c.name for c in table_meta.primary_key.columns]
        self.assertEqual(pk1, pk2, 'primary keys not equal')

        return True

    def _compare_table_defition_in_code_and_database(self, table_name):
        #(conn, engine) = self._create_conn_engine(self.conf)
        db_metadata = get_schema_metadata(TestUdl2Database.engine)
        ddl_metadata = generate_udl2_metadata()
        return self._compare_columns(ddl_metadata, db_metadata, table_name)

    def _compare_table_key_definitions_in_code_and_db(self, table_name):
        #(conn, engine) = self._create_conn_engine(self.conf)
        db_metadata = get_schema_metadata(TestUdl2Database.engine)
        table_metadata = db_metadata.tables[table_name]
        metadata_in_code = generate_udl2_metadata()
        ddl_metadata = metadata_in_code.tables[table_name]

        return self._compare_table_keys(ddl_metadata, table_metadata)

    def test_STG_SBAC_ASMT_OUTCOME(self):
        table_name = 'STG_SBAC_ASMT_OUTCOME'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    def test_STG_SBAC_STU_REG(self):
        table_name = 'STG_SBAC_STU_REG'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    def test_INT_SBAC_ASMT(self):
        table_name = 'INT_SBAC_ASMT'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    def test_INT_SBAC_ASMT_OUTCOME(self):
        table_name = 'INT_SBAC_ASMT_OUTCOME'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    def test_INT_SBAC_STU_REG(self):
        table_name = 'INT_SBAC_STU_REG'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))

    def test_INT_SBAC_STU_REG_META(self):
        table_name = 'INT_SBAC_STU_REG_META'
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

    def test_SR_REF_COLUMN_MAPPING(self):
        table_name = 'SR_REF_COLUMN_MAPPING'
        self.assertTrue(self._compare_table_defition_in_code_and_database(table_name))
        self.assertTrue(self._compare_table_key_definitions_in_code_and_db(table_name))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
