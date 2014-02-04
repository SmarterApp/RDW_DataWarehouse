__author__ = 'sravi'

import unittest
import edmigrate.utils.queries as queries
from edcore.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite, \
    Unittest_with_repmgr_sqlite_no_data_load, UnittestRepMgrDBConnection


class TestQueries(Unittest_with_repmgr_sqlite):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def tearDown(self):
        pass

    def test_get_host_name_from_node_conn_info(self):
        conn_info = 'host=dbpgdw0.qa.dum.edwdc.net user=repmgr dbname=edware'
        self.assertEqual(queries.get_host_name_from_node_conn_info(conn_info), 'dbpgdw0.qa.dum.edwdc.net')
        conn_info = 'host=dbpgdw0.qa.dum.edwdc.net'
        self.assertEqual(queries.get_host_name_from_node_conn_info(conn_info), 'dbpgdw0.qa.dum.edwdc.net')
        conn_info = ''
        self.assertIsNone(queries.get_host_name_from_node_conn_info(conn_info))
        conn_info = 'dbpgdw0.qa.dum.edwdc.net'
        self.assertIsNone(queries.get_host_name_from_node_conn_info(conn_info))

    def test_is_sync_satus_acceptable(self):
        self.assertTrue(queries.is_sync_satus_acceptable('0 Bytes', '0'))
        self.assertFalse(queries.is_sync_satus_acceptable('10 Bytes', '0'))
        self.assertTrue(queries.is_sync_satus_acceptable('10 Bytes', '10'))
        self.assertFalse(queries.is_sync_satus_acceptable('11 Bytes', '10'))
        self.assertFalse(queries.is_sync_satus_acceptable('11', '10'))
        self.assertFalse(queries.is_sync_satus_acceptable(' ', '10'))
        self.assertFalse(queries.is_sync_satus_acceptable('X Bytes', '10'))

if __name__ == "__main__":
    unittest.main()
