import unittest
from unittest.mock import MagicMock
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.tasks.slave import get_hostname, get_slave_node_id_from_hostname, check_replication_status,\
    is_replication_paused, is_replication_active, check_iptable_has_blocked_pgpool, connect_pgpool,\
    disconnect_pgpool, connect_master, disconnect_master, find_slave, slave_task


class SlaveTaskTest(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        super(SlaveTaskTest, cls).setUpClass()

    def setUp(self):
        with RepMgrDBConnection() as conn:
            conn.execute("INSERT INTO repl_nodes (id, cluster, conninfo) "
                         "VALUES (1, 'test_cluster', 'host=localhost user=repmgr dbname=test')")

    def tearDown(self):
        pass

    def test_get_hostname(self):
        Mocket.enable()
        hostname = get_hostname()
        self.assertEqual(hostname, 'localhost')

    def test_get_slave_node_id_from_hostname(self):
        hostname = 'localhost'
        node_id = get_slave_node_id_from_hostname(hostname)
        self.assertEqual(node_id, 1)

    def test_check_replication_status(self):
        check_replication_status()
        self.assertEqual(True, False)

    def test_is_replication_paused(self):
        is_replication_paused()
        self.assertEqual(True, False)

    def test_is_replication_active(self):
        is_replication_active()
        self.assertEqual(True, False)

    def test_check_iptable_has_blocked_pgpool(self):
        pgpool = 'localhost'
        check_iptable_has_blocked_pgpool(pgpool)
        self.assertEqual(True, False)

    def test_find_slave(self):
        find_slave()
        self.assertEqual(True, False)

    def test_connect_pgpool(self):
        connect_pgpool()
        self.assertEqual(True, False)

    def test_disconnect_pgpool(self):
        disconnect_pgpool()
        self.assertEqual()

    def test_connect_master(self):
        connect_master()
        self.assertEqual(True, False)

    def test_disconnect_master(self):
        disconnect_master()
        self.assertEqual(True, False)

    def test_slave_task(self):
        slave_task()
        self.assertEqual(True, False)
