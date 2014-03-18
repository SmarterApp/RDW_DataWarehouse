import unittest
from unittest.mock import MagicMock
from unittest import skip
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.tasks.slave import get_hostname, get_slave_node_id_from_hostname, check_replication_status,\
    is_replication_paused, is_replication_active, check_iptable_has_blocked_pgpool, connect_pgpool,\
    disconnect_pgpool, connect_master, disconnect_master, find_slave, slave_task
from edmigrate.utils.constants import Constants


class SlaveTaskTest(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        super(SlaveTaskTest, cls).setUpClass()

    def setUp(self):
        self.hostname = 'localhost'
        self.node_id = 1
        self.cluster = 'test_cluster'
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.insert().values({Constants.ID: self.node_id,
                                                     Constants.REPL_NODE_CLUSTER: self.cluster,
                                                     Constants.REPL_NODE_CONN_INFO: 'host=localhost user=repmgr dbname=test'}))

    def tearDown(self):
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.delete())

    def test_get_hostname(self):
        Mocket.enable()
        hostname = get_hostname()
        self.assertEqual(hostname, self.hostname)

    def test_get_slave_node_id_from_hostname(self):
        hostname = self.hostname
        node_id = get_slave_node_id_from_hostname(hostname)
        self.assertEqual(node_id, self.node_id)

    @skip("under development")
    def test_check_replication_status(self):
        check_replication_status()
        self.assertEqual(True, False)

    @skip("under development")
    def test_is_replication_paused(self):
        is_replication_paused()
        self.assertEqual(True, False)

    @skip("under development")
    def test_is_replication_active(self):
        is_replication_active()
        self.assertEqual(True, False)

    @skip("under development")
    def test_check_iptable_has_blocked_pgpool(self):
        pgpool = 'localhost'
        check_iptable_has_blocked_pgpool(pgpool)
        self.assertEqual(True, False)

    @skip("under development")
    def test_find_slave(self):
        find_slave()
        self.assertEqual(True, False)

    @skip("under development")
    def test_connect_pgpool(self):
        connect_pgpool()
        self.assertEqual(True, False)

    @skip("under development")
    def test_disconnect_pgpool(self):
        disconnect_pgpool()
        self.assertEqual()

    @skip("under development")
    def test_connect_master(self):
        connect_master()
        self.assertEqual(True, False)

    @skip("under development")
    def test_disconnect_master(self):
        disconnect_master()
        self.assertEqual(True, False)

    @skip("under development")
    def test_slave_task(self):
        slave_task()
        self.assertEqual(True, False)
