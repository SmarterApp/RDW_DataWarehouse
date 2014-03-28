'''
Created on Mar 26, 2014

@author: tosako
'''
import unittest
from edmigrate.utils.conductor import Conductor
from edmigrate.exceptions import ConductorTimeoutException, \
    PlayerDelayedRegistrationException
from edmigrate.edmigrate_celery import setup_celery
from edmigrate.tests.tasks.unittest_with_player import Unittest_with_player
from edmigrate.utils.utils import get_broker_url
from edmigrate.utils.player_tracker import PlayerTracker
from kombu.connection import Connection
from edmigrate.utils import conductor
from edmigrate.tests.utils.mock_logger import MockLogger
from edmigrate.tests.tasks import unittest_with_player
from edmigrate.utils.constants import Constants
from queue import Empty


class Test(Unittest_with_player):
    _consumerThread = None
    _connection = None
    _queue = None

    @classmethod
    def setUpClass(cls):
        Unittest_with_player.setUpClass()
        settings = {'migrate.celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)
        Test._connection = Connection(get_broker_url())
        Test._queue = Test._connection.SimpleQueue(unittest_with_player.queue, no_ack=True)
        conductor.logger = MockLogger('test')

    @classmethod
    def tearDownClass(cls):
        Test._queue.close()
        Test._connection.close()

    def setUp(self):
        PlayerTracker().clear()

    def test_conductor_lock(self):
        tested = False
        with Conductor() as conductor1:
            self.assertRaises(ConductorTimeoutException, Conductor, locktimeout=1)
            tested = True
        self.assertTrue(tested)

    def test_accept_players(self):
        with Conductor() as conductor1:
            conductor1.accept_players()
            PlayerTracker().add_player(12345)
            ids = conductor1.get_player_ids()
        self.assertEqual(1, len(ids))
        self.assertEqual(12345, ids[0])

    def test_reject_players(self):
        tested = False
        with Conductor() as conductor1:
            conductor1.reject_players()
            playerTracker = PlayerTracker()
            self.assertRaises(PlayerDelayedRegistrationException, playerTracker.add_player, 123123)
            tested = True
        self.assertTrue(tested)

    def test_find_players(self):
        with Conductor() as conductor1:
            conductor1.find_players()
            message = Test._queue.get(timeout=5)
        self.assertEqual(Constants.ACK_COMMAND_FIND_PLAYER, message.payload[Constants.MESSAGE_ACK_COMMAND])
        self.assertEqual(222, message.payload[Constants.MESSAGE_NODE_ID])

    def test_get_player_ids(self):
        tested = False
        with Conductor() as conductor1:
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(123)
            playerTracker.add_player(222)
            playerTracker.add_player(333)
            playerTracker.add_player(444)
            playerTracker.set_accept_player(False)
            self.assertRaises(PlayerDelayedRegistrationException, playerTracker.add_player, 123123)
            ids = conductor1.get_player_ids()
            self.assertEqual(4, len(ids))
            self.assertIn(123, ids)
            self.assertIn(222, ids)
            self.assertIn(333, ids)
            self.assertIn(444, ids)
            ids = playerTracker.get_player_ids(Constants.PLAYER_GROUP_A)
            self.assertEqual(0, len(ids))
            tested = True
        self.assertTrue(tested)

    def test_grouping_players(self):
        tested = False
        with Conductor() as conductor1:
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(123)
            playerTracker.add_player(222)
            playerTracker.add_player(333)
            playerTracker.add_player(444)
            playerTracker.set_accept_player(False)
            conductor1.grouping_players()
            groupA = playerTracker.get_player_ids(Constants.PLAYER_GROUP_A)
            self.assertEqual(2, len(groupA))
            groupB = playerTracker.get_player_ids(Constants.PLAYER_GROUP_B)
            self.assertEqual(2, len(groupB))
            tested = True
        self.assertTrue(tested)

    def test_send_disconnect_PGPool(self):
        with Conductor() as conductor1:
            conductor1.send_disconnect_PGPool()
            self.assertRaises(Empty, Test._queue.get, timeout=1)
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            conductor1.send_disconnect_PGPool()
            message = Test._queue.get(timeout=5)
        self.assertEqual(Constants.ACK_COMMAND_DISCONNECT_PGPOOL, message.payload[Constants.MESSAGE_ACK_COMMAND])

    def test_send_connect_PGPool(self):
        with Conductor() as conductor1:
            conductor1.send_connect_PGPool()
            self.assertRaises(Empty, Test._queue.get, timeout=1)
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            conductor1.send_connect_PGPool()
            message = Test._queue.get(timeout=5)
        self.assertEqual(Constants.ACK_COMMAND_CONNECT_PGPOOL, message.payload[Constants.MESSAGE_ACK_COMMAND])

    def test_send_stop_replication(self):
        with Conductor() as conductor1:
            conductor1.send_stop_replication()
            self.assertRaises(Empty, Test._queue.get, timeout=1)
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            conductor1.send_stop_replication()
            message = Test._queue.get(timeout=5)
        self.assertEqual(Constants.ACK_COMMAND_STOP_REPLICATION, message.payload[Constants.MESSAGE_ACK_COMMAND])

    def test_send_start_replication(self):
        with Conductor() as conductor1:
            conductor1.send_start_replication()
            self.assertRaises(Empty, Test._queue.get, timeout=1)
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            conductor1.send_start_replication()
            message = Test._queue.get(timeout=5)
        self.assertEqual(Constants.ACK_COMMAND_START_REPLICATION, message.payload[Constants.MESSAGE_ACK_COMMAND])

    def test_wait_PGPool_disconnected(self):
        tested = False
        with Conductor() as conductor1:
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            self.assertRaises(ConductorTimeoutException, conductor1.wait_PGPool_disconnected, timeout=1)
            playerTracker.set_pgpool_disconnected(222)
            conductor1.wait_PGPool_disconnected(timeout=1)
            tested = True
        self.assertTrue(tested)

    def test_wait_PGPool_connected(self):
        tested = False
        with Conductor() as conductor1:
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            self.assertRaises(ConductorTimeoutException, conductor1.wait_PGPool_connected, timeout=1)
            playerTracker.set_pgpool_connected(222)
            conductor1.wait_PGPool_connected(timeout=3)
            tested = True
        self.assertTrue(tested)

    def test_wait_replication_stopped(self):
        tested = False
        with Conductor() as conductor1:
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            self.assertRaises(ConductorTimeoutException, conductor1.wait_replication_stopped, timeout=1)
            playerTracker.set_replication_stopped(222)
            conductor1.wait_replication_stopped(timeout=1)
            tested = True
        self.assertTrue(tested)

    def test_wait_replication_started(self):
        tested = False
        with Conductor() as conductor1:
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            self.assertRaises(ConductorTimeoutException, conductor1.wait_replication_started, timeout=1)
            playerTracker.set_replication_started(222)
            conductor1.wait_replication_started(timeout=1)
            tested = True
        self.assertTrue(tested)

    def test_send_reset_players(self):
        with Conductor() as conductor1:
            conductor1.send_reset_players()
            self.assertRaises(Empty, Test._queue.get, timeout=1)
            playerTracker = PlayerTracker()
            playerTracker.set_accept_player(True)
            playerTracker.add_player(222)
            playerTracker.set_accept_player(False)
            conductor1.send_reset_players()
            message = Test._queue.get(timeout=5)
        self.assertEqual(Constants.ACK_COMMAND_RESET_PLAYERS, message.payload[Constants.MESSAGE_ACK_COMMAND])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_conductor_lock']
    unittest.main()
