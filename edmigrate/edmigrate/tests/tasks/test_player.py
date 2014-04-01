'''
Created on Mar 21, 2014ß

@author: ejen
'''
from unittest.mock import patch
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from edmigrate.tasks.player import Player
from edmigrate.settings.config import Config
import edmigrate.settings.config
from edmigrate.utils.constants import Constants
from kombu import Connection
from kombu.entity import Exchange
from edmigrate.utils.utils import get_broker_url
import socket
from edmigrate.utils.iptables import Iptables


connection = Connection(get_broker_url())
exchange = Exchange(Constants.CONDUCTOR_EXCHANGE)


class MockLogger(object):

    def __init__(self):
        self.debug_log = []
        self.error_log = []
        self.warn_log = []
        self.critical_log = []
        self.info_log = []

    def debug(self, msg):
        self.debug_log.append(msg)

    def info(self, msg):
        self.info_log.append(msg)

    def error(self, msg):
        self.error_log.append(msg)

    def warning(self, msg):
        self.warn_log.append(msg)

    def critical(self, msg):
        self.critical_log.append(msg)

    def __repr__(self):
        return "debug: " + str(self.debug_log) + \
               " info: " + str(self.info_log) + \
               " warning: " + str(self.warn_log) + \
               " error: " + str(self.error_log) + \
               " critical: " + str(self.critical_log)


class PlayerTaskTest(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        super(PlayerTaskTest, cls).setUpClass()

    def setUp(self):
        # clean up singleton durign testing
        Player.cleanup()
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
        # turn on mocket
        Mocket.enable()

    def tearDown(self):
        with RepMgrDBConnection() as conn:
            repl_nodes = conn.get_table(Constants.REPL_NODES)
            conn.execute(repl_nodes.delete())
        # since Player is a singleton object. we need to destroy it
        Player.cleanup()
        # turn off mocket when test is over
        Mocket.disable()

    def test_cleanup(self):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        self.assertEquals(len(Player._instances.items()), 1)
        Player.cleanup()
        self.assertEqual(len(Player._instances.items()), 0)

    def test__node_id(self):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        self.assertEqual("1", player._node_id())
        Mocket.disable()
        Player.cleanup()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        self.assertEqual("", player._node_id())

    def test__hostname(self):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        self.assertEqual("localhost", player._hostname())
        player.set_hostname("")
        player.set_node_id_from_hostname()
        self.assertEqual("", player._hostname())

    def test_set_node_id_from_hostname(self):
        logger = MockLogger()
        player = Player(logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        node_id = player.set_node_id_from_hostname()
        self.assertEqual(node_id, self.node_id)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_register_player_with_node_id(self, MockConductor):
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        MockConductor.return_value = lambda: None
        player.register_player()
        self.assertEqual(len(logger.error_log), 0)
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_register_player_with_no_node_id(self, MockConductor):
        logger = MockLogger()
        sys_logger = MockLogger()
        Mocket.disable()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        MockConductor.return_value = lambda: None
        player.register_player()
        self.assertEqual(len(player.logger.error_log), 1)
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, '_check_rules')
    @patch.object(edmigrate.utils.iptables.Iptables, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.Iptables, 'check_block_output')
    @patch.object(edmigrate.utils.iptables.Iptables, 'check_block_input')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_succeed(self, MockConductor, MockBlockInput, MockBlockOutput, MockModifyRule,
                                   MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockBlockInput.return_value = True
        MockBlockOutput.return_value = True
        MockCheckRule.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)
        self.assertEqual(0, len(player.logger.error_log))
        Mocket.disable()

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, '_check_rules')
    @patch.object(edmigrate.utils.iptables.Iptables, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.Iptables, 'check_block_input')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_pgpool_failed(self, MockConductor, MockCheckBlockInput, MockModifyRule,
                                              MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockCheckBlockInput.return_value = False
        MockModifyRule.return_value = None
        MockCheckRule.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        Mocket.enable()
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        Mocket.disable()
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.error_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, '_check_rules')
    @patch.object(edmigrate.utils.iptables.Iptables, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.Iptables, 'check_block_output')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_master_failed(self, MockConductor, MockCheckBlockOutput, MockModifyRule,
                                              MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckBlockOutput.return_value = False
        MockCheckRule.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        Mocket.enable()
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        Mocket.disable()
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.error_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, '_check_rules')
    @patch.object(edmigrate.utils.iptables.Iptables, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.Iptables, 'check_block_output')
    @patch.object(edmigrate.utils.iptables.Iptables, 'check_block_input')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_both_failed(self, MockConductor, MockCheckBlockInput,
                                            MockCheckBlockOutput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = False
        MockCheckBlockOutput.return_value = False
        MockCheckRule.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        Mocket.enable()
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.reset_players()
        Mocket.disable()
        self.assertFalse(MockConductor.called)
        self.assertEqual(1, len(player.logger.error_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool_succeed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_pgpool()
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)
        self.assertEqual(0, len(player.logger.error_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool_failed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = False
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_pgpool()
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool_succeed(self, MockConductor, MockCheckBlockInput, MockModifyRule,
                                       MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = False
        MockCheckRule.return_value = False
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_pgpool()
        self.assertEqual(0, len(player.logger.error_log))
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool_failed(self, MockConductor, MockCheckBlockInput, MockModifyRule,
                                      ModifyCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = True
        ModifyCheckRule.return_value = False
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_pgpool()
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master_succeed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockCheckRule.return_value = True
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_master()
        self.assertEqual(0, len(player.logger.error_log))
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master_failed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockCheckRule.return_value = True
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = False
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.connect_master()
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master_succeed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockCheckRule.return_value = False
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = False
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_master()
        self.assertEqual(0, len(player.logger.error_log))
        MockConductor.assert_called_once_with(player.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master_failed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        logger = MockLogger()
        sys_logger = MockLogger()
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = False
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.disconnect_master()
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))
        self.assertFalse(MockConductor.called)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_with_node_id_not_in_nodes(self, MockConductor, MockBlockOutput, MockModifyRule):
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_STOP_REPLICATION, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_witout_nodes(self, MockConductor, MockBlockOutput, MockModifyRule):
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_STOP_REPLICATION, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_with_node_id_not_in_nodes(self, MockConductor, MockBlockInput, MockModifyRule):
        MockBlockInput.return_value = True
        MockModifyRule.return_value = None
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_without_nodes(self, MockConductor, MockBlockInput, MockModifyRule):
        MockBlockInput.return_value = True
        MockModifyRule.return_value = None
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_with_node_id_in_nodes(self, MockConductor, MockBlockInput,
                                                              MockModifyRule, MockCheckRule):
        MockBlockInput.return_value = True
        MockModifyRule.return_value = None
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_CONNECT_PGPOOL, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_with_node_id_not_in_nodes(self, MockConductor, MockBlockInput, MockModifyRule):
        MockBlockInput.return_value = False
        MockModifyRule.return_value = None
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_CONNECT_PGPOOL, [])
        self.assertFalse(MockConductor.called)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_without_nodes(self, MockConductor, MockBlockInput, MockModifyRule):
        MockBlockInput.return_value = False
        MockModifyRule.return_value = None
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_CONNECT_PGPOOL, None)
        self.assertFalse(MockConductor.called)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_run_command_register_player(self, MockConductor, MockBlockInput, MockBlockOutput, MockModifyRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_REGISTER_PLAYER, None)
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_run_command_register_player_with_node_id(self, MockConductor, MockBlockInput, MockBlockOutput, MockModifyRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        MockConductor.return_value = lambda: None
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_REGISTER_PLAYER, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players(self, MockConductor, MockBlockInput, MockBlockOutput, MockModifyRule,
                                       MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = True
        MockBlockOutput.return_value = True
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_RESET_PLAYERS, None)
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_check_rules")
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players_with_node_id(self, MockConductor, MockBlockInput, MockBlockOutput,
                                                    MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = True
        MockBlockOutput.return_value = True
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command(Constants.COMMAND_RESET_PLAYERS, [self.node_id])
        MockConductor.assert_called_once_with(self.node_id, self.connection, self.exchange, self.routing_key)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    def test_run_command_not_implemented(self, MockBlockInput, MockBlockOutput, MockModifyRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command('Fake Command', None)
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.MASTER_HOSTNAME: 'edwdbsrv1.poc.dum.edwdc.net',
                        Config.PGPOOL_HOSTNAME: 'edwdbsrv4.poc.dum.edwdc.net',
                        Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.Iptables, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_output")
    @patch.object(edmigrate.utils.iptables.Iptables, "check_block_input")
    def test_run_command_not_implemented_with_node_id(self, MockBlockInput, MockBlockOutput, MockModifyRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        logger = MockLogger()
        sys_logger = MockLogger()
        player = Player(logger, sys_logger, self.connection, self.exchange, self.routing_key)
        player.set_hostname(socket.gethostname())
        player.set_node_id_from_hostname()
        player.run_command('Fake Command', [self.node_id])
        self.assertEqual(0, len(player.logger.error_log))
        self.assertEqual(1, len(player.logger.warn_log))
