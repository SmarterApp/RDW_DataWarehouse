__author__ = 'sravi'

import unittest
import os
import shutil
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql.expression import select
from edextract.status.constants import Constants


class TestExtractTask(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        pass

    def test_generate_csv_with_bad_file(self):
        from edmigrate.utils.migrate import get_daily_delta_batches_to_migrate
        #import pdb; pdb.set_trace()
        test_batches_to_be_migrated = get_daily_delta_batches_to_migrate()
        #print(test_batches_to_be_migrated)