'''
Created on Mar 21, 2014ß

@author: ejen
'''
import unittest
from unittest.mock import patch, MagicMock
from unittest import skip
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.tasks.player import Player
from edmigrate.settings.config import Config, get_setting
import edmigrate.settings.config
from edmigrate.utils.constants import Constants
from kombu import Connection
from kombu.entity import Exchange
from edmigrate.utils.utils import get_broker_url
import socket
import subprocess

connection = Connection(get_broker_url())
exchange = Exchange(Constants.CONDUCTOR_EXCHANGE)


class MockLogger(object):

    def __init__(self):
        self.out = []
        self.err = []

    def info(self, msg):
        self.out.append(msg)

    def error(self, msg):
        self.err.append(msg)

    def __repr__(self):
        return "stdout: " + str(self.out) + " stderr: " + str(self.err)


class PlayerTaskTest(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        super(PlayerTaskTest, cls).setUpClass()

    def setUp(self):
        # clean up singleton durign testing
        Player._instances = {}
        self.hostname = 'localhost'
        self.node_id = 1
        self.cluster = 'test_cluster'
        self.pgpool = 'edwdbsrv4.poc.dum.edwdc.net'
        self.master = 'edwdbsrv1.poc.dum.edwdc.net'
        self.routing_key = Constants.CONDUCTOR_ROUTING_KEY
        self.connection = Connection(get_broker_url())
        self.exchange = Exchange(Constants.CONDUCTOR_EXCHANGE)
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.insert().values({Constants.ID: self.node_id,
                                                     Constants.REPL_NODE_CLUSTER: self.cluster,
                                                     Constants.REPL_NODE_CONN_INFO: 'host=localhost user=repmgr dbname=test'}))
        self.noblock_firewall_output = 'Chain PGSQL (1 references)\n'\
            'target     prot opt source               destination         \n'\
            'ACCEPT     all  --  anywhere             anywhere            \n'

        self.block_once_output = 'Chain PGSQL (1 references)\n'\
            'target     prot opt source               destination         \n'\
            'REJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \n'\
            'ACCEPT     all  --  anywhere             anywhere            \n'
        self.block_twice_output = 'Chain PGSQL (1 references)\n'\
            'target     prot opt source               destination         \n'\
            'REJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \n'\
            'REJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \n'\
            'ACCEPT     all  --  anywhere             anywhere            \n'
        self.block_master_once_output = 'Chain PGSQL (1 references)\n'\
            'target     prot opt source               destination         \n'\
            'REJECT     all  --  edwdbsrv1.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \n'\
            'ACCEPT     all  --  anywhere             anywhere            \n'
        self.block_both_once_output = 'Chain PGSQL (1 references)\n'\
            'target     prot opt source               destination         \n'\
            'REJECT     all  --  edwdbsrv1.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \n'\
            'REJECT     all  --  edwdbsrv4.poc.dum.edwdc.net  anywhere            reject-with icmp-port-unreachable \n'\
            'ACCEPT     all  --  anywhere             anywhere            \n'
        # turn on mocket
        Mocket.enable()

    def tearDown(self):
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.delete())
        # since Player is a singleton object. we need to destroy it
        Player._instances = {}
        # turn off mocket when test is over
        Mocket.disable()

    def test_set_node_id_from_hostname(self):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        node_id = player.set_node_id_from_hostname()
        self.assertEqual(node_id, self.node_id)

    def test_search_blocked_hostname_0(self):
        logger = MockLogger()
        MockLogger.info.return_value = lambda: None
        MockLogger.error.return_value = lambda: None
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        not_found = player.search_blocked_hostname(self.noblock_firewall_output, self.pgpool)
        self.assertFalse(not_found)

    def test_search_blocked_hostname_1(self):
        logger = MockLogger()
        MockLogger.info.return_value = lambda: None
        MockLogger.error.return_value = lambda: None
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        found = player.search_blocked_hostname(self.block_once_output, self.pgpool)
        self.assertTrue(found)

    def test_search_blocked_hostname_2(self):
        logger = MockLogger()
        MockLogger.info.return_value = lambda: None
        MockLogger.error.return_value = lambda: None
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        found = player.search_blocked_hostname(self.block_twice_output, self.pgpool)
        self.assertTrue(found)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('subprocess.check_output')
    def test_check_iptable_has_blocked_pgpool_0(self, MockSubprocess):
        logger = MockLogger()
        MockLogger.info.return_value = lambda: None
        MockLogger.error.return_value = lambda: None
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        MockSubprocess.return_value = self.noblock_firewall_output
        result = player.check_iptable_has_blocked_machine(self.pgpool)
        MockSubprocess.assert_called_once_with(['sudo', 'iptables', '-L', 'PGSQL'], universal_newlines=True)
        self.assertFalse(result)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('subprocess.check_output')
    def test_check_iptable_has_blocked_pgpool_1(self, MockSubprocess):
        logger = MockLogger()
        MockLogger.info.return_value = lambda: None
        MockLogger.error.return_value = lambda: None
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        MockSubprocess.return_value = self.block_once_output
        result = player.check_iptable_has_blocked_machine(self.pgpool)
        MockSubprocess.assert_called_once_with(['sudo', 'iptables', '-L', 'PGSQL'], universal_newlines=True)
        self.assertTrue(result)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('subprocess.check_output')
    def test_check_iptable_has_blocked_pgpool_2(self, MockSubprocess):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        MockSubprocess.return_value = self.block_twice_output
        result = player.check_iptable_has_blocked_machine(self.pgpool)
        MockSubprocess.assert_called_once_with(['sudo', 'iptables', '-L', 'PGSQL'], universal_newlines=True)
        self.assertTrue(result)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_register_player_with_node_id(self, MockConductor):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        MockConductor.return_value = lambda: None
        player.register_player()
        self.assertEqual(len(logger.err), 0)
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_register_player_with_no_node_id(self, MockConductor):
        logger = MockLogger()
        Mocket.disable()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        MockConductor.return_value = lambda: None
        player.register_player()
        self.assertEqual(len(player.logger.err), 1)
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_succeed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)
        self.assertEqual(0, len(player.logger.err))
        Mocket.disable()

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_pgpool_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        Mocket.enable()
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        Mocket.disable()
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_master_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_master_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        Mocket.enable()
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        Mocket.disable()
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_both_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_both_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        Mocket.enable()
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        Mocket.disable()
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool_succeed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_pgpool()
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)
        self.assertEqual(0, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_pgpool()
        self.assertEqual(1, len(player.logger.err))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool_succeed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_pgpool()
        self.assertEqual(0, len(player.logger.err))
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_pgpool()
        self.assertEqual(1, len(player.logger.err))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('subprocess.check_output')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master_succeed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_master()
        self.assertEqual(0, len(player.logger.err))
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch('subprocess.check_output')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_master_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_master()
        self.assertEqual(1, len(player.logger.err))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master_succeed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.block_master_once_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_master()
        self.assertEqual(0, len(player.logger.err))
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master_failed(self, MockConductor, MockSubprocess):
        logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockSubprocess.return_value = self.noblock_firewall_output
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_master()
        self.assertEqual(1, len(player.logger.err))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    def test_check_iptable_has_blocked_machine_with_exception(self, MockSubprocess):
        MockSubprocess.side_effect = subprocess.CalledProcessError(1, ['sudo', '-L', 'iptables', 'PGSQL'])
        MockSubprocess.return_value = self.noblock_firewall_output
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.check_iptable_has_blocked_machine(self.hostname)
        MockSubprocess.assert_called_once_with(['sudo', 'iptables', '-L', 'PGSQL'], universal_newlines=True)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    def test_remove_iptable_rules_with_exception(self, MockSubprocess):
        MockSubprocess.side_effect = subprocess.CalledProcessError(1, ['sudo', 'iptables', '-L', 'PGSQL'])
        MockSubprocess.return_value = self.block_once_output
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.remove_iptable_rules(self.pgpool, Constants.REPLICATION_MAX_RETRIES)
        MockSubprocess.assert_called_with(['sudo', 'iptables', '-L', 'PGSQL'], universal_newlines=True)
        self.assertEqual(2, MockSubprocess.call_count)
        self.assertEqual(2, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    def test_add_iptable_rules_with_exception(self, MockSubprocess):
        MockSubprocess.side_effect = subprocess.CalledProcessError(1, ['sudo', 'iptables', '-L', 'PGSQL'])
        MockSubprocess.return_value = self.block_once_output
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.add_iptable_rules(self.pgpool)
        MockSubprocess.assert_called_with(['sudo', 'iptables', '-L', 'PGSQL'], universal_newlines=True)
        self.assertEqual(2, MockSubprocess.call_count)
        self.assertEqual(2, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_run_command_start_replication_with_node_id_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.add_iptable_rules(self.pgpool)
        player.run_command(Constants.COMMAND_START_REPLICATION, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_run_command_start_replication_with_node_id_not_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.add_iptable_rules(self.pgpool)
        player.run_command(Constants.COMMAND_START_REPLICATION, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_run_command_start_replication_without_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.add_iptable_rules(self.pgpool)
        player.run_command(Constants.COMMAND_START_REPLICATION, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_with_node_id_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_master_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.add_iptable_rules(self.pgpool)
        player.run_command(Constants.COMMAND_STOP_REPLICATION, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_with_node_id_not_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_STOP_REPLICATION, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_witout_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_STOP_REPLICATION, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_with_node_id_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_with_node_id_not_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_without_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_with_node_id_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_master_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_CONNECT_PGPOOL, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_with_node_id_not_in_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_CONNECT_PGPOOL, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_without_nodes(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_CONNECT_PGPOOL, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_run_command_register_player(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_REGISTER_PLAYER, None)
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_run_command_register_player_with_node_id(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_REGISTER_PLAYER, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_RESET_PLAYERS, None)
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players_with_node_id(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_RESET_PLAYERS, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players_failed(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_RESET_PLAYERS, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players_with_node_id_failed(self, MockConductor, MockSubprocess):
        MockSubprocess.return_value = self.block_both_once_output
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_RESET_PLAYERS, [self.node_id])
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    def test_run_command_not_implemented(self, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command('Fake Command', None)
        self.assertEqual(1, len(player.logger.err))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: 'PGSQL'})
    @patch("subprocess.check_output")
    def test_run_command_not_implemented_with_node_id(self, MockSubprocess):
        MockSubprocess.return_value = self.noblock_firewall_output
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command('Fake Command', [self.node_id])
        self.assertEqual(1, len(player.logger.err))
