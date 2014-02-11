from edmigrate.utils.queries import get_host_name_from_node_conn_info,\
    is_sync_satus_acceptable, query_slave_nodes_status,\
    query_slave_nodes_info_dict
__author__ = 'sravi'

import unittest
from edcore.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite, \
    UnittestRepMgrDBConnection


class TestQueries(Unittest_with_repmgr_sqlite):

    def setUp(self):
        self.slave_host_names = ['slave1.dummy.net', 'slave2.dummy.net']
        self.slave_nodes_info = {2: 'slave1.dummy.net', 3: 'slave2.dummy.net'}

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def tearDown(self):
        pass

    def test_get_host_name_from_node_conn_info(self):
        conn_info = 'host=slave1.dummy.net user=repmgr dbname=edware'
        self.assertEqual(get_host_name_from_node_conn_info(conn_info), 'slave1.dummy.net')
        conn_info = 'host=slave1.dummy.net'
        self.assertEqual(get_host_name_from_node_conn_info(conn_info), 'slave1.dummy.net')
        conn_info = ''
        self.assertIsNone(get_host_name_from_node_conn_info(conn_info))
        conn_info = 'slave1.dummy.net'
        self.assertIsNone(get_host_name_from_node_conn_info(conn_info))

    def test_is_sync_satus_acceptable(self):
        self.assertTrue(is_sync_satus_acceptable('0 Bytes', '0'))
        self.assertFalse(is_sync_satus_acceptable('10 Bytes', '0'))
        self.assertTrue(is_sync_satus_acceptable('10 Bytes', '10'))
        self.assertFalse(is_sync_satus_acceptable('11 Bytes', '10'))
        self.assertFalse(is_sync_satus_acceptable('11', '10'))
        self.assertFalse(is_sync_satus_acceptable(' ', '10'))
        self.assertFalse(is_sync_satus_acceptable('X Bytes', '10'))

    def test_get_slave_nodes_info_dict(self):
        with UnittestRepMgrDBConnection() as connection:
            nodes_info = query_slave_nodes_info_dict(connection, self.slave_host_names)
        self.assertEqual(sorted(list(nodes_info.values())), self.slave_host_names)

    def test_get_slave_nodes_status(self):
        with UnittestRepMgrDBConnection() as connection:
            nodes_status = query_slave_nodes_status(connection, self.slave_nodes_info)
        self.assertEqual(sorted(nodes_status.keys()), sorted(self.slave_nodes_info.keys()))

    def test_get_daily_delta_batches_to_migrate(self):
        pass


if __name__ == "__main__":
    unittest.main()
