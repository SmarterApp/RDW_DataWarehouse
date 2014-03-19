import unittest
from unittest.mock import patch, MagicMock
from unittest import skip
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.tasks.slave import get_hostname, get_slave_node_id_from_hostname, check_iptable_has_blocked_machine, \
    connect_pgpool, disconnect_pgpool, connect_master, disconnect_master, find_slave, slave_task,\
    parse_iptable_output, reset_slaves
from edmigrate.settings.config import Config, get_setting
import edmigrate.settings.config
from edmigrate.utils.constants import Constants


class SlaveTaskTest(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        super(SlaveTaskTest, cls).setUpClass()

    def setUp(self):
        self.hostname = 'localhost'
        self.node_id = 1
        self.cluster = 'test_cluster'
        self.pgpool = 'edwdbsrv4.poc.dum.edwdc.net'
        self.master = 'edwdbsrv1.poc.dum.edwdc.net'
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.insert().values({Constants.ID: self.node_id,
                                                     Constants.REPL_NODE_CLUSTER: self.cluster,
                                                     Constants.REPL_NODE_CONN_INFO: 'host=localhost user=repmgr dbname=test'}))
        self.noblock_firewall_output = 'Chain INPUT (policy ACCEPT)\ntarget     prot opt source               destination         \nACCEPT     all  --  anywhere             anywhere            state RELATED,ESTABLISHED \nACCEPT     icmp --  anywhere             anywhere            \nACCEPT     all  --  anywhere             anywhere            \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:http \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:webcache \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:ssh \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:distinct \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:solve \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:pcsync-https \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:amqp \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:personal-agent \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:15672 \nPGSQL      tcp  --  anywhere             anywhere            state NEW tcp dpt:postgres flags:FIN,SYN,RST,ACK/SYN \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain FORWARD (policy ACCEPT)\ntarget     prot opt source               destination         \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain OUTPUT (policy ACCEPT)\ntarget     prot opt source               destination         \n\nChain PGSQL (1 references)\ntarget     prot opt source               destination         \nACCEPT     all  --  anywhere             anywhere            \n'

        self.block_once_output = 'Chain INPUT (policy ACCEPT)\ntarget     prot opt source               destination         \nACCEPT     all  --  anywhere             anywhere            state RELATED,ESTABLISHED \nACCEPT     icmp --  anywhere             anywhere            \nACCEPT     all  --  anywhere             anywhere            \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:http \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:webcache \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:ssh \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:distinct \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:solve \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:pcsync-https \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:amqp \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:personal-agent \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:15672 \nPGSQL      tcp  --  anywhere             anywhere            state NEW tcp dpt:postgres flags:FIN,SYN,RST,ACK/SYN \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain FORWARD (policy ACCEPT)\ntarget     prot opt source               destination         \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain OUTPUT (policy ACCEPT)\ntarget     prot opt source               destination         \n\nChain PGSQL (1 references)\ntarget     prot opt source               destination         \nREJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \nACCEPT     all  --  anywhere             anywhere            \n'
        self.block_twice_output = 'Chain INPUT (policy ACCEPT)\ntarget     prot opt source               destination         \nACCEPT     all  --  anywhere             anywhere            state RELATED,ESTABLISHED \nACCEPT     icmp --  anywhere             anywhere            \nACCEPT     all  --  anywhere             anywhere            \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:http \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:webcache \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:ssh \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:distinct \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:solve \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:pcsync-https \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:amqp \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:personal-agent \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:15672 \nPGSQL      tcp  --  anywhere             anywhere            state NEW tcp dpt:postgres flags:FIN,SYN,RST,ACK/SYN \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain FORWARD (policy ACCEPT)\ntarget     prot opt source               destination         \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain OUTPUT (policy ACCEPT)\ntarget     prot opt source               destination         \n\nChain PGSQL (1 references)\ntarget     prot opt source               destination         \nREJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \nREJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \nACCEPT     all  --  anywhere             anywhere            \n'
        self.block_master_once_output = 'Chain INPUT (policy ACCEPT)\ntarget     prot opt source               destination         \nACCEPT     all  --  anywhere             anywhere            state RELATED,ESTABLISHED \nACCEPT     icmp --  anywhere             anywhere            \nACCEPT     all  --  anywhere             anywhere            \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:http \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:webcache \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:ssh \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:distinct \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:solve \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:pcsync-https \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:amqp \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:personal-agent \nACCEPT     tcp  --  anywhere             anywhere            state NEW tcp dpt:15672 \nPGSQL      tcp  --  anywhere             anywhere            state NEW tcp dpt:postgres flags:FIN,SYN,RST,ACK/SYN \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain FORWARD (policy ACCEPT)\ntarget     prot opt source               destination         \nREJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited \n\nChain OUTPUT (policy ACCEPT)\ntarget     prot opt source               destination         \n\nChain PGSQL (1 references)\ntarget     prot opt source               destination         \nREJECT     all  --  edwdbsrv1.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \nACCEPT     all  --  anywhere             anywhere            \n'

    def tearDown(self):
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.delete())

    def test_get_hostname(self):
        Mocket.enable()
        hostname = get_hostname()
        self.assertEqual(hostname, self.hostname)

    def test_get_slave_node_id_from_hostname(self):
        node_id = get_slave_node_id_from_hostname(self.hostname)
        self.assertEqual(node_id, self.node_id)

    def test_parse_iptable_output_0(self):
        not_found = parse_iptable_output(self.noblock_firewall_output, self.pgpool)
        self.assertFalse(not_found)

    def test_parse_iptable_output_1(self):
        found = parse_iptable_output(self.block_once_output, self.pgpool)
        self.assertTrue(found)

    def test_parse_iptable_output_2(self):
        found = parse_iptable_output(self.block_twice_output, self.pgpool)
        self.assertTrue(found)

    @patch('subprocess.check_output')
    def test_check_iptable_has_blocked_pgpool_0(self, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        result = check_iptable_has_blocked_machine(self.pgpool)
        self.assertFalse(result)

    @patch('subprocess.check_output')
    def test_check_iptable_has_blocked_pgpool_1(self, MockSubprocess):
        MockSubprocess.return_value = self.block_once_output
        result = check_iptable_has_blocked_machine(self.pgpool)
        self.assertTrue(result)

    @patch('subprocess.check_output')
    def test_check_iptable_has_blocked_pgpool_2(self, MockSubprocess):
        MockSubprocess.return_value = self.block_twice_output
        result = check_iptable_has_blocked_machine(self.pgpool)
        self.assertTrue(result)

    @patch('edmigrate.utils.reply_to_conductor.register_slave')
    def test_find_slave_0(self, MockConductor):
        MockConductor.return_value = lambda: None
        node_id, routing_key, exchange, conn = 1, None, None, None
        find_slave('localhost', node_id, conn, exchange, routing_key)
        MockConductor.assert_called_once_with(node_id, conn, exchange, routing_key)

    @patch('logging.Logger.info')
    def test_find_slave_1(self, MockLogger):
        MockLogger.return_value = lambda: None
        node_id, routing_key, exchange, conn = None, None, None, None
        find_slave(self.hostname, node_id, conn, exchange, routing_key)
        MockLogger.assert_called_once_with("{hostname} has no node_id".format(hostname=self.hostname))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_slaves')
    def test_reset_slaves_0(self, MockConductor, MockSubprocess):
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        node_id, routing_key, exchange, conn = 1, None, None, None
        reset_slaves(self.hostname, node_id, conn, exchange, routing_key)
        MockConductor.assert_called_once_with(node_id, conn, exchange, routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool(self, MockConductor, MockSubprocess):
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        node_id, routing_key, exchange, conn = 1, None, None, None
        connect_pgpool(self.hostname, node_id, conn, exchange, routing_key)
        MockConductor.assert_called_once_with(node_id, conn, exchange, routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool(self, MockConductor, MockSubprocess):
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_once_output
        node_id, routing_key, exchange, conn = 1, None, None, None
        disconnect_pgpool(self.hostname, node_id, conn, exchange, routing_key)
        MockConductor.assert_called_once_with(node_id, conn, exchange, routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master(self, MockConductor, MockSubprocess):
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        node_id, routing_key, exchange, conn = 1, None, None, None
        connect_master(self.hostname, node_id, conn, exchange, routing_key)
        MockConductor.assert_called_once_with(node_id, conn, exchange, routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master(self, MockConductor, MockSubprocess):
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_master_once_output
        node_id, routing_key, exchange, conn = 1, None, None, None
        disconnect_master(self.hostname, node_id, conn, exchange, routing_key)
        MockConductor.assert_called_once_with(node_id, conn, exchange, routing_key)
