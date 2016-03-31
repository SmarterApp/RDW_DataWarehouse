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
Created on Mar 16, 2014

@author: tosako
'''
import unittest
from kombu import Connection
from edmigrate.utils.consumer import ConsumerThread
from edmigrate.utils.player_tracker import PlayerTracker
from edmigrate.utils import reply_to_conductor
import time
import threading
from edmigrate.queues import conductor
from edmigrate.utils.constants import Constants


class Test(unittest.TestCase):

    lock = threading.Lock()

    def setUp(self):
        self.lock.acquire()
        self.__connection = Connection("memory://")
        self.__thread = ConsumerThread(self.__connection)
        self.__thread.start()
        time.sleep(1)
        PlayerTracker().clear()
        PlayerTracker().set_accept_player(True)

    def tearDown(self):
        self.__thread.stop()
        self.lock.release()

    def test_ACK_COMMAND_FIND_PLAYER(self):
        reply_to_conductor.register_player(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.register_player(115, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        player_tracker = PlayerTracker()
        ids = player_tracker.get_player_ids(timeout=5)
        self.assertEqual(2, len(ids))
        self.assertIn(112, ids)
        self.assertIn(115, ids)

    def test_ACK_COMMAND_DISCONNECT_MASTER(self):
        reply_to_conductor.register_player(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.register_player(115, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.acknowledgement_master_disconnected(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        player_tracker = PlayerTracker()
        self.assertTrue(player_tracker.is_replication_stopped(112))
        self.assertFalse(player_tracker.is_replication_stopped(115))

    def test_ACK_COMMAND_CONNECT_MASTER(self):
        reply_to_conductor.register_player(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.register_player(115, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        player_tracker = PlayerTracker()
        self.assertFalse(player_tracker.is_replication_started(112))
        self.assertFalse(player_tracker.is_replication_started(115))
        reply_to_conductor.acknowledgement_master_disconnected(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        self.assertTrue(player_tracker.is_replication_stopped(112))
        self.assertFalse(player_tracker.is_replication_started(115))
        reply_to_conductor.acknowledgement_master_connected(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        self.assertTrue(player_tracker.is_replication_started(112))
        self.assertFalse(player_tracker.is_replication_started(115))

    def test_ACK_COMMAND_DISCONNECT_PGPOOL(self):
        reply_to_conductor.register_player(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.register_player(115, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.acknowledgement_pgpool_disconnected(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        player_tracker = PlayerTracker()
        self.assertTrue(player_tracker.is_pgpool_disconnected(112))
        self.assertFalse(player_tracker.is_pgpool_disconnected(115))

    def test_ACK_COMMAND_CONNECT_PGPOOL(self):
        reply_to_conductor.register_player(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        reply_to_conductor.register_player(115, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        player_tracker = PlayerTracker()
        self.assertFalse(player_tracker.is_pgpool_connected(112))
        self.assertFalse(player_tracker.is_pgpool_connected(115))
        reply_to_conductor.acknowledgement_pgpool_disconnected(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        self.assertTrue(player_tracker.is_pgpool_disconnected(112))
        self.assertFalse(player_tracker.is_pgpool_connected(115))
        reply_to_conductor.acknowledgement_pgpool_connected(112, self.__connection, conductor.exchange, Constants.CONDUCTOR_ROUTING_KEY)
        time.sleep(2)
        self.assertTrue(player_tracker.is_pgpool_connected(112))
        self.assertFalse(player_tracker.is_pgpool_connected(115))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_ACK_COMMAND_FIND_PLAYER']
    unittest.main()
