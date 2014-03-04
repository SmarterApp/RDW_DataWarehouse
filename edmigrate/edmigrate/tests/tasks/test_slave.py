from edmigrate.tasks.slave import slaves_register
__author__ = 'sravi'

import unittest
import os
import shutil
from edcore.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite, \
    Unittest_with_repmgr_sqlite_no_data_load, UnittestRepMgrDBConnection


class TestSlaveWorker(Unittest_with_repmgr_sqlite):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def tearDown(self):
        pass

#    def test_slaves_register(self):
#        slaves_register()


if __name__ == "__main__":
    unittest.main()
