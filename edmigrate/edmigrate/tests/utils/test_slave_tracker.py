'''
Created on Mar 15, 2014

@author: tosako
'''
import unittest
from edmigrate.utils.slave_tracker import SlaveTracker
from edmigrate.exceptions import SlaveAlreadyRegisteredException, \
    SlaveNotRegisteredException, SlaveStatusTimedoutException,\
    SlaveDelayedRegistrationException
from edmigrate.utils.constants import Constants
import time


class Test(unittest.TestCase):

    def setUp(self):
        slavetracker1 = SlaveTracker()
        slavetracker1.reset()
        slavetracker1.set_accept_slave(True)
        slavetracker1.add_slave(123)
        slavetracker1.set_accept_slave(False)

    def test_singletone(self):
        slavetracker1 = SlaveTracker()
        slavetracker2 = SlaveTracker()
        self.assertTrue(slavetracker1 == slavetracker2)

    def test_add_slave(self):
        slavetracker1 = SlaveTracker()
        slavetracker2 = SlaveTracker()
        slaves = slavetracker2.get_slave_ids()
        self.assertEqual(1, len(slaves))
        slavetracker1.set_accept_slave(True)
        self.assertRaises(SlaveAlreadyRegisteredException, slavetracker1.add_slave, 123)
        slavetracker1.add_slave(2)
        slavetracker1.set_accept_slave(False)
        slaves = slavetracker2.get_slave_ids()
        self.assertEqual(2, len(slaves))
        self.assertIn(123, slaves)
        self.assertIn(2, slaves)

    def test_set_pgpool_connected(self):
        slavetracker1 = SlaveTracker()
        self.assertTrue(slavetracker1.is_pgpool_connected(123))
        self.assertFalse(slavetracker1.is_pgpool_disconnected(123))
        slavetracker1.set_pgpool_disconnected(123)
        self.assertFalse(slavetracker1.is_pgpool_connected(123))
        self.assertTrue(slavetracker1.is_pgpool_disconnected(123))

    def test_set_pgpool_disconnected(self):
        slavetracker1 = SlaveTracker()
        slavetracker1.set_pgpool_disconnected(123)
        self.assertFalse(slavetracker1.is_pgpool_connected(123))
        self.assertTrue(slavetracker1.is_pgpool_disconnected(123))
        slavetracker1.set_pgpool_connected(123)
        self.assertTrue(slavetracker1.is_pgpool_connected(123))
        self.assertFalse(slavetracker1.is_pgpool_disconnected(123))

    def test_set_master_connected(self):
        slavetracker1 = SlaveTracker()
        self.assertTrue(slavetracker1.is_replication_started(123))
        self.assertFalse(slavetracker1.is_replication_stopped(123))
        slavetracker1.set_replication_stopped(123)
        self.assertFalse(slavetracker1.is_replication_started(123))
        self.assertTrue(slavetracker1.is_replication_stopped(123))

    def test_set_master_disconnected(self):
        slavetracker1 = SlaveTracker()
        slavetracker1.set_replication_stopped(123)
        self.assertFalse(slavetracker1.is_replication_started(123))
        self.assertTrue(slavetracker1.is_replication_stopped(123))
        slavetracker1.set_replication_started(123)
        self.assertTrue(slavetracker1.is_replication_started(123))
        self.assertFalse(slavetracker1.is_pgpool_disconnected(123))

    def test_set_pgpool_connected_no_slave_exist(self):
        slavetracker1 = SlaveTracker()
        self.assertRaises(SlaveNotRegisteredException, slavetracker1.set_pgpool_disconnected, 1)

    def test_is_pgpool_connected_no_slave_exist(self):
        slavetracker1 = SlaveTracker()
        self.assertRaises(SlaveStatusTimedoutException, slavetracker1.is_pgpool_disconnected, 1, 1)

    def test_get_slave_ids(self):
        slavetracker1 = SlaveTracker()
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(1, len(ids))
        slavetracker1.set_accept_slave(True)
        slavetracker1.add_slave(1)
        slavetracker1.set_accept_slave(False)
        ids = slavetracker1.get_slave_ids('A')
        self.assertEqual(0, len(ids))
        slavetracker1.set_slave_group(123, 'A')
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(2, len(ids))
        ids = slavetracker1.get_slave_ids('A')
        self.assertEqual(1, len(ids))
        ids = slavetracker1.get_slave_ids('B')
        self.assertEqual(0, len(ids))

    def test_reset(self):
        slavetracker1 = SlaveTracker()
        slavetracker2 = SlaveTracker()
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(1, len(ids))
        slavetracker1.reset()
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(0, len(ids))
        ids = slavetracker2.get_slave_ids()
        self.assertEqual(0, len(ids))

    def test__set_slave_status(self):
        slavetracker1 = SlaveTracker()
        slavetracker1._set_slave_status(123, Constants.SLAVE_PGPOOL_CONNECTION_STATUS, Constants.SLAVE_CONNECTION_STATUS_DISCONNECTED)
        self.assertTrue(slavetracker1.is_pgpool_disconnected(123))
        self.assertRaises(SlaveNotRegisteredException, slavetracker1._set_slave_status, 1, Constants.SLAVE_PGPOOL_CONNECTION_STATUS, Constants.SLAVE_CONNECTION_STATUS_DISCONNECTED)

    def test__is_slave_status(self):
        slavetracker1 = SlaveTracker()
        self.assertFalse(slavetracker1._is_slave_status(123, 'test', 'abc'))
        slavetracker1._set_slave_status(123, 'test', 'abc')
        self.assertTrue(slavetracker1._is_slave_status(123, 'test', 'abc'))
        timeout = 3
        start_time = time.time()
        self.assertRaises(SlaveStatusTimedoutException, slavetracker1._is_slave_status, 1, 'test', 'abc', timeout)
        end_time = time.time()
        self.assertTrue(end_time - start_time > timeout)

    def test_set_accept_slave(self):
        slavetracker1 = SlaveTracker()
        slavetracker1.reset()
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(0, len(ids))
        slavetracker1.set_accept_slave(True)
        slavetracker1.add_slave(1)
        slavetracker1.add_slave(2)
        slavetracker1.set_accept_slave(False)
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(2, len(ids))
        self.assertRaises(SlaveDelayedRegistrationException, slavetracker1.add_slave, 3)
        ids = slavetracker1.get_slave_ids()
        self.assertEqual(2, len(ids))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_singletone']
    unittest.main()
