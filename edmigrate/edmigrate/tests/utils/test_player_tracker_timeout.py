# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
