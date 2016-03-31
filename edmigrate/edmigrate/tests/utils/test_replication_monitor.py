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
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.utils.replication_monitor import replication_monitor
from edmigrate.exceptions import NoReplicationToMonitorException, \
    ReplicationToMonitorOrphanNodeException,\
    ReplicationToMonitorOutOfSyncException
import time


class Test(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def test_replication_monitor_no_ids_exist_at_all(self):
        self.assertRaises(NoReplicationToMonitorException, replication_monitor, [100, 101, 102])
        self.assertRaises(NoReplicationToMonitorException, replication_monitor, [103])

    def test_replication_monitor_timeout(self):
        timeout = 5
        start_time = time.time()
        self.assertRaises(ReplicationToMonitorOutOfSyncException, replication_monitor, [2, 3, 4], timeout=timeout)
        end_time = time.time()
        self.assertTrue(end_time - start_time > timeout)

    def test_replication_monitor_replication_lag_tolerance(self):
        timeout = 1
        self.assertRaises(ReplicationToMonitorOutOfSyncException, replication_monitor, [5], timeout=timeout)
        rtn = replication_monitor([5], replication_lag_tolerance=1050)
        self.assertTrue(rtn)

    def test_replication_monitor_apply_lag(self):
        timeout = 1
        self.assertRaises(ReplicationToMonitorOutOfSyncException, replication_monitor, [6], timeout=timeout)
        rtn = replication_monitor([6], apply_lag_tolerance=1050)
        self.assertTrue(rtn)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
