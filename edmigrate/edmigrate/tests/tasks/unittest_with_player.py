'''
Created on Mar 27, 2014

@author: tosako
'''
from edmigrate.utils.utils import Singleton, get_broker_url
from edmigrate.tasks.player import Player
from kombu import Connection
from edmigrate.queues import conductor
from edmigrate.utils.constants import Constants
from edmigrate.utils import reply_to_conductor
import unittest
from kombu.entity import Exchange, Queue


exchange = Exchange('test', type='direct')
queue = Queue('test', exchange=exchange, routing_key='test.test', durable=False)


class Unittest_with_player(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mock = MockPlayer()
        Player._instances[Player] = mock

    @classmethod
    def tearDownClass(cls):
        Player._instances.clear()


class MockPlayer(Player):
    def __init__(self):
        self.logger = None
        self.admin_logger = self.logger
        self.connection = Connection(get_broker_url())
        self.exchange = exchange
        self.routing_key = 'test.test'
        self.hostname = 'localhost'
        self.node_id = 222
        self.COMMAND_HANDLERS = {
            Constants.COMMAND_REGISTER_PLAYER: self.register_player,
            Constants.COMMAND_START_REPLICATION: self.connect_master,
            Constants.COMMAND_STOP_REPLICATION: self.disconnect_master,
            Constants.COMMAND_CONNECT_PGPOOL: self.connect_pgpool,
            Constants.COMMAND_DISCONNECT_PGPOOL: self.disconnect_pgpool,
            Constants.COMMAND_RESET_PLAYERS: self.reset_players
        }

    def __enter__(self):
        return self

    def register_player(self):
        reply_to_conductor.register_player(self.node_id, self.connection, self.exchange, self.routing_key)

    def connect_master(self):
        reply_to_conductor.acknowledgement_master_connected(self.node_id, self.connection, self.exchange, self.routing_key)

    def disconnect_master(self):
        reply_to_conductor.acknowledgement_master_disconnected(self.node_id, self.connection, self.exchange, self.routing_key)

    def connect_pgpool(self):
        reply_to_conductor.acknowledgement_pgpool_connected(self.node_id, self.connection, self.exchange, self.routing_key)

    def disconnect_pgpool(self):
        reply_to_conductor.acknowledgement_pgpool_disconnected(self.node_id, self.connection, self.exchange, self.routing_key)

    def reset_players(self):
        reply_to_conductor.acknowledgement_reset_players(self.node_id, self.connection, self.exchange, self.routing_key)
