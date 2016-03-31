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
