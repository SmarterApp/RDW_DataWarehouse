'''
Created on Mar 15, 2014

@author: tosako
'''
import unittest
from edmigrate.utils.player_tracker import PlayerTracker
from edmigrate.exceptions import PlayerAlreadyRegisteredException, \
    PlayerNotRegisteredException, PlayerStatusTimedoutException,\
    PlayerDelayedRegistrationException
from edmigrate.utils.constants import Constants
import time
from edmigrate.utils.conductor import Conductor


class Test(unittest.TestCase):

    def setUp(self):
        playertracker1 = PlayerTracker()
        playertracker1.reset()
        playertracker1.set_accept_player(True)
        playertracker1.add_player(123)
        playertracker1.set_accept_player(False)

    def test_singletone(self):
        playertracker1 = PlayerTracker()
        playertracker2 = PlayerTracker()
        self.assertTrue(playertracker1 == playertracker2)

    def test_add_player(self):
        playertracker1 = PlayerTracker()
        playertracker2 = PlayerTracker()
        players = playertracker2.get_player_ids()
        self.assertEqual(1, len(players))
        playertracker1.set_accept_player(True)
        self.assertRaises(PlayerAlreadyRegisteredException, playertracker1.add_player, 123)
        playertracker1.add_player(2)
        playertracker1.set_accept_player(False)
        players = playertracker2.get_player_ids()
        self.assertEqual(2, len(players))
        self.assertIn(123, players)
        self.assertIn(2, players)

    def test_set_pgpool_connected(self):
        playertracker1 = PlayerTracker()
        self.assertTrue(playertracker1.is_pgpool_connected(123))
        self.assertFalse(playertracker1.is_pgpool_disconnected(123))
        playertracker1.set_pgpool_disconnected(123)
        self.assertFalse(playertracker1.is_pgpool_connected(123))
        self.assertTrue(playertracker1.is_pgpool_disconnected(123))

    def test_set_pgpool_disconnected(self):
        playertracker1 = PlayerTracker()
        playertracker1.set_pgpool_disconnected(123)
        self.assertFalse(playertracker1.is_pgpool_connected(123))
        self.assertTrue(playertracker1.is_pgpool_disconnected(123))
        playertracker1.set_pgpool_connected(123)
        self.assertTrue(playertracker1.is_pgpool_connected(123))
        self.assertFalse(playertracker1.is_pgpool_disconnected(123))

    def test_set_master_connected(self):
        playertracker1 = PlayerTracker()
        self.assertTrue(playertracker1.is_replication_started(123))
        self.assertFalse(playertracker1.is_replication_stopped(123))
        playertracker1.set_replication_stopped(123)
        self.assertFalse(playertracker1.is_replication_started(123))
        self.assertTrue(playertracker1.is_replication_stopped(123))

    def test_set_master_disconnected(self):
        playertracker1 = PlayerTracker()
        playertracker1.set_replication_stopped(123)
        self.assertFalse(playertracker1.is_replication_started(123))
        self.assertTrue(playertracker1.is_replication_stopped(123))
        playertracker1.set_replication_started(123)
        self.assertTrue(playertracker1.is_replication_started(123))
        self.assertFalse(playertracker1.is_pgpool_disconnected(123))

    def test_set_pgpool_connected_no_player_exist(self):
        playertracker1 = PlayerTracker()
        self.assertRaises(PlayerNotRegisteredException, playertracker1.set_pgpool_disconnected, 1)

    def test_is_pgpool_connected_no_player_exist(self):
        playertracker1 = PlayerTracker()
        self.assertRaises(PlayerStatusTimedoutException, playertracker1.is_pgpool_disconnected, 1, 1)

    def test_get_player_ids(self):
        playertracker1 = PlayerTracker()
        ids = playertracker1.get_player_ids()
        self.assertEqual(1, len(ids))
        playertracker1.set_accept_player(True)
        playertracker1.add_player(1)
        playertracker1.set_accept_player(False)
        ids = playertracker1.get_player_ids('A')
        self.assertEqual(0, len(ids))
        playertracker1.set_player_group(123, 'A')
        ids = playertracker1.get_player_ids()
        self.assertEqual(2, len(ids))
        ids = playertracker1.get_player_ids('A')
        self.assertEqual(1, len(ids))
        ids = playertracker1.get_player_ids('B')
        self.assertEqual(0, len(ids))

    def test_reset(self):
        playertracker1 = PlayerTracker()
        playertracker2 = PlayerTracker()
        ids = playertracker1.get_player_ids()
        self.assertEqual(1, len(ids))
        playertracker1.reset()
        ids = playertracker1.get_player_ids()
        self.assertEqual(0, len(ids))
        ids = playertracker2.get_player_ids()
        self.assertEqual(0, len(ids))

    def test__set_player_status(self):
        playertracker1 = PlayerTracker()
        playertracker1._set_player_status(123, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_DISCONNECTED)
        self.assertTrue(playertracker1.is_pgpool_disconnected(123))
        self.assertRaises(PlayerNotRegisteredException, playertracker1._set_player_status, 1, Constants.PLAYER_PGPOOL_CONNECTION_STATUS, Constants.PLAYER_CONNECTION_STATUS_DISCONNECTED)

    def test__is_player_status(self):
        playertracker1 = PlayerTracker()
        self.assertFalse(playertracker1._is_player_status(123, 'test', 'abc'))
        playertracker1._set_player_status(123, 'test', 'abc')
        self.assertTrue(playertracker1._is_player_status(123, 'test', 'abc'))
        timeout = 3
        start_time = time.time()
        self.assertRaises(PlayerStatusTimedoutException, playertracker1._is_player_status, 1, 'test', 'abc', timeout)
        end_time = time.time()
        self.assertTrue(end_time - start_time > timeout)

    def test_set_accept_player(self):
        playertracker1 = PlayerTracker()
        playertracker1.reset()
        ids = playertracker1.get_player_ids()
        self.assertEqual(0, len(ids))
        playertracker1.set_accept_player(True)
        playertracker1.add_player(1)
        playertracker1.add_player(2)
        playertracker1.set_accept_player(False)
        ids = playertracker1.get_player_ids()
        self.assertEqual(2, len(ids))
        self.assertRaises(PlayerDelayedRegistrationException, playertracker1.add_player, 3)
        ids = playertracker1.get_player_ids()
        self.assertEqual(2, len(ids))

    def test_is_migration_in_process(self):
        playertracker1 = PlayerTracker()
        self.assertFalse(playertracker1.is_migration_in_process())
        conductor = Conductor()
        self.assertTrue(playertracker1.is_migration_in_process())
        del conductor
        self.assertFalse(playertracker1.is_migration_in_process())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_singletone']
    unittest.main()
