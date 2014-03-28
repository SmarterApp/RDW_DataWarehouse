'''
Created on Mar 27, 2014

@author: tosako
'''
import unittest
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.tests.utils.mock_logger import MockLogger
from edmigrate.utils import replication_admin_monitor


class Test(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def test_replication_admin_monitor(self):
        replication_admin_monitor.logger = MockLogger('test')
        replication_admin_monitor.replication_admin_monitor(interval_check=-1)
        logged = replication_admin_monitor.logger.logged
        self.assertEqual(6, len(logged))
        self.assertEqual('Node ID[2] is out of sync.', logged[2][1])
        self.assertEqual('Node ID[5] is out of sync.', logged[3][1])
        self.assertEqual('Node ID[6] is out of sync.', logged[4][1])

    def test_ReplicationAdminMonitor(self):
        replication_admin_monitor.logger = MockLogger('test')
        monitor = replication_admin_monitor.ReplicationAdminMonitor(interval_check=-1)
        monitor.run()
        logged = replication_admin_monitor.logger.logged
        self.assertEqual(6, len(logged))
        self.assertEqual('Node ID[2] is out of sync.', logged[2][1])
        self.assertEqual('Node ID[5] is out of sync.', logged[3][1])
        self.assertEqual('Node ID[6] is out of sync.', logged[4][1])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
