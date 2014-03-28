'''
Created on Mar 15, 2014

@author: tosako
'''
import unittest
from edmigrate.utils.player_tracker import PlayerTracker
from edmigrate.exceptions import PlayerStatusLockingTimedoutException
from edmigrate.utils.utils import Singleton


class Test(unittest.TestCase):

    def test_PlayerStatusLockingTimedoutException(self):
        Singleton._instances.clear()
        PlayerTracker._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, PlayerTracker, timeout=1)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)
        playertracker1 = PlayerTracker(timeout=1)

        PlayerTracker._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.set_migration_in_process, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.set_migration_in_process, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.set_timeout, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.set_accept_player, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1.set_accept_player(True)
        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.add_player, 1)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)
        playertracker1.set_accept_player(False)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.get_player_ids, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1.clear)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1._set_player_status, None, None, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)

        playertracker1._lock.acquire()
        self.assertRaises(PlayerStatusLockingTimedoutException, playertracker1._is_player_status, None, None, None)
        self.assertRaises(RuntimeError, PlayerTracker._lock.release)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_singletone']
    unittest.main()
