__author__ = 'sravi'

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name


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
#        from edmigrate.utils.migrate import get_daily_delta_batches_to_migrate
#        test_batches_to_be_migrated = get_daily_delta_batches_to_migrate(get_unittest_tenant_name())
#        self.assertDictEqual(test_batches_to_be_migrated, {})
        pass
