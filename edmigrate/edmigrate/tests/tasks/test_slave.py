__author__ = 'sravi'

import unittest
import os
import shutil
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite


class TestSlaveWorker(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        pass

    def test_slaves_get_ready_for_data_migrate(self):
        pass


if __name__ == "__main__":
    unittest.main()