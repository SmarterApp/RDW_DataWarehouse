'''
Created on Mar 21, 2014ß

@author: ejen
'''
from unittest.mock import patch
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.tasks.player import Player
from edmigrate.settings.config import Config
import edmigrate.settings.config
from edmigrate.utils.constants import Constants
from kombu import Connection
from kombu.entity import Exchange
from edmigrate.utils.utils import get_broker_url
import socket


connection = Connection(get_broker_url())
exchange = Exchange(Constants.CONDUCTOR_EXCHANGE)


class PlayerTaskTest(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        # clean up singleton durign testing
        Player._instances.clear()
        self.hostname = 'localhost'
        self.cluster = 'test_cluster'
        self.routing_key = Constants.CONDUCTOR_ROUTING_KEY
        self.connection = Connection(get_broker_url())
        self.exchange = Exchange(Constants.CONDUCTOR_EXCHANGE)
        # turn on mocket
        Mocket.enable()

    def tearDown(self):
        # since Player is a singleton object. we need to destroy it
        # turn off mocket when test is over
        Mocket.disable()

    def test__node_id(self):
        player = Player(self.connection, self.exchange, self.routing_key)
        self.assertEqual(3, player.node_id)

    def test__hostname(self):
        player = Player(self.connection, self.exchange, self.routing_key)
        self.assertEqual("localhost", player.hostname)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_register_player_with_node_id(self, MockConductor):
        player = Player(self.connection, self.exchange, self.routing_key)
        MockConductor.return_value = lambda: None
        rtn = player.register_player()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_register_player_with_no_node_id(self, MockConductor):
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.register_player()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.IptablesChecker, 'check_block_output')
    @patch.object(edmigrate.utils.iptables.IptablesChecker, 'check_block_input')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_succeed(self, MockConductor, MockBlockInput, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockBlockInput.return_value = True
        MockBlockOutput.return_value = True
        MockCheckRule.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.reset_players()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.IptablesChecker, 'check_block_input')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_pgpool_failed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockCheckBlockInput.return_value = False
        MockCheckRule.return_value = True
        MockModifyRule.return_value = None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.reset_players()
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.IptablesChecker, 'check_block_output')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_master_failed(self, MockConductor, MockCheckBlockOutput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckRule.return_value = True
        MockCheckBlockOutput.return_value = False
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.reset_players()
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, '_modify_rule')
    @patch.object(edmigrate.utils.iptables.IptablesChecker, 'check_block_output')
    @patch.object(edmigrate.utils.iptables.IptablesChecker, 'check_block_input')
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_reset_players_with_both_failed(self, MockConductor, MockCheckBlockInput,
                                            MockCheckBlockOutput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = False
        MockCheckBlockOutput.return_value = False
        MockCheckRule.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.reset_players()
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool_succeed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.connect_pgpool()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_connect_pgpool_failed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        MockModifyRule.return_value = None
        MockCheckBlockInput.return_value = False
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.connect_pgpool()
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool_succeed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckRule.return_value = False
        MockCheckBlockInput.return_value = False
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.disconnect_pgpool()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_disconnect_pgpool_failed(self, MockConductor, MockCheckBlockInput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckRule.return_value = False
        MockCheckBlockInput.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.disconnect_pgpool()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master_succeed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockCheckRule.return_value = True
        MockBlockOutput.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.connect_master()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_connected')
    def test_connect_master_failed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockCheckRule.return_value = True
        MockBlockOutput.return_value = False
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.connect_master()
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master_succeed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = False
        MockCheckRule.return_value = False
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.disconnect_master()
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_disconnect_master_failed(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = False
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.disconnect_master()
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_with_node_id_not_in_nodes(self, MockConductor, MockBlockOutput,
                                                                    MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        MockCheckRule.return_value = False
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_STOP_REPLICATION, [])
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_master_disconnected')
    def test_run_command_stop_replication_without_nodes(self, MockConductor, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockOutput.return_value = True
        MockCheckRule.return_value = False
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_STOP_REPLICATION, None)
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_with_node_id_not_in_nodes(self, MockConductor, MockBlockInput,
                                                                     MockModifyRule, MockCheckRule):
        MockBlockInput.return_value = True
        MockModifyRule.return_value = None
        MockCheckRule.return_value = False
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, [])
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_disconnected')
    def test_run_command_disconnect_pgpool_without_nodes(self, MockConductor, MockBlockInput, MockModifyRule,
                                                         MockCheckRule):
        MockBlockInput.return_value = True
        MockModifyRule.return_value = None
        MockCheckRule.return_value = False
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_DISCONNECT_PGPOOL, None)
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_with_node_id_in_nodes(self, MockConductor, MockBlockInput,
                                                              MockModifyRule, MockCheckRule):
        MockBlockInput.return_value = True
        MockModifyRule.return_value = None
        MockCheckRule.return_value = True
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_CONNECT_PGPOOL, [3])
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_with_node_id_not_in_nodes(self, MockConductor, MockBlockInput, MockModifyRule,
                                                                  MockCheckRule):
        MockBlockInput.return_value = False
        MockModifyRule.return_value = None
        MockCheckRule.return_value = True
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_CONNECT_PGPOOL, [])
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_pgpool_connected')
    def test_run_command_connect_pgpool_without_nodes(self, MockConductor, MockBlockInput, MockModifyRule, MockCheckRule):
        MockBlockInput.return_value = False
        MockModifyRule.return_value = None
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_CONNECT_PGPOOL, None)
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_run_command_register_player(self, MockConductor, MockBlockInput, MockBlockOutput,
                                         MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        MockCheckRule.return_value = True
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_REGISTER_PLAYER, None)
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.register_player')
    def test_run_command_register_player_with_node_id(self, MockConductor, MockBlockInput, MockBlockOutput,
                                                      MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        MockConductor.return_value = lambda: None
        MockCheckRule.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_REGISTER_PLAYER, [3])
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players(self, MockConductor, MockBlockInput, MockBlockOutput, MockModifyRule,
                                       MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = True
        MockBlockOutput.return_value = True
        MockCheckRule.return_value = True
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_RESET_PLAYERS, None)
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    @patch('edmigrate.utils.reply_to_conductor.acknowledgement_reset_players')
    def test_run_command_reset_players_with_node_id(self, MockConductor, MockBlockInput, MockBlockOutput,
                                                    MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = True
        MockBlockOutput.return_value = True
        MockCheckRule.return_value = True
        MockConductor.return_value = lambda: None
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command(Constants.COMMAND_RESET_PLAYERS, [3])
        self.assertTrue(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    def test_run_command_not_implemented(self, MockBlockInput, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        MockCheckRule.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command('Fake Command', None)
        self.assertFalse(rtn)

    @patch.dict(edmigrate.settings.config.settings,
                values={Config.IPTABLES_CHAIN: Constants.IPTABLES_CHAIN})
    @patch.object(edmigrate.utils.iptables.IptablesController, "_check_rules")
    @patch.object(edmigrate.utils.iptables.IptablesController, "_modify_rule")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_output")
    @patch.object(edmigrate.utils.iptables.IptablesChecker, "check_block_input")
    def test_run_command_not_implemented_with_node_id(self, MockBlockInput, MockBlockOutput, MockModifyRule, MockCheckRule):
        MockModifyRule.return_value = None
        MockBlockInput.return_value = False
        MockBlockOutput.return_value = False
        MockCheckRule.return_value = True
        player = Player(self.connection, self.exchange, self.routing_key)
        rtn = player.run_command('Fake Command', [3])
        self.assertFalse(rtn)
