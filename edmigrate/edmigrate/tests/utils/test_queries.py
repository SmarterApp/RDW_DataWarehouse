from edmigrate.utils.queries import _get_host_name_from_node_conn_info,\
    get_slaves_status
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
        self.assertEqual(_get_host_name_from_node_conn_info(conn_info), 'slave1.dummy.net')
        conn_info = 'host=slave1.dummy.net'
        self.assertEqual(_get_host_name_from_node_conn_info(conn_info), 'slave1.dummy.net')
        conn_info = ''
        self.assertIsNone(_get_host_name_from_node_conn_info(conn_info))
        conn_info = 'slave1.dummy.net'
        self.assertIsNone(_get_host_name_from_node_conn_info(conn_info))

    def test_get_slave_nodes_info_dict(self):
        nodes_info = get_slaves_status('testtenant', ['2', '3'])
        self.assertEqual(len(nodes_info), 2)

    def test_get_daily_delta_batches_to_migrate(self):
        pass


if __name__ == "__main__":
    unittest.main()
