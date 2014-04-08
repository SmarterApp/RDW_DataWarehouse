from unittest.mock import MagicMock
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edmigrate.migrate import migrate_by_batch
from edmigrate.tests.utils.unittest_with_preprod_sqlite import Unittest_with_preprod_sqlite

__author__ = 'ablum'


class TestMigrate(Unittest_with_edcore_sqlite, Unittest_with_preprod_sqlite, Unittest_with_stats_sqlite):

    test_tenant = 'tomcat'

    def setUp(self):
        self.__tenant = TestMigrate.test_tenant

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass(EdMigrateDestConnection.get_datasource_name(TestMigrate.test_tenant),
                                               use_metadata_from_db=False)
        Unittest_with_preprod_sqlite.setUpClass()

    def test_migrate_by_batch_valid_batch_op(self):
        migrate_by_batch._migrate_snapshot = MagicMock(return_value=(1, 1))
        dcount, icount = migrate_by_batch.migrate_by_batch(None, None, None, 's', None, None)

        self.assertEquals(1, dcount)
        self.assertEquals(1, icount)

    def test_migrate_by_batch_invalid_batch_op(self):
        migrate_by_batch._migrate_snapshot = MagicMock(return_value=(0, 0))
        dcount, icount = migrate_by_batch.migrate_by_batch(None, None, None, 'i', None, None)

        self.assertEquals(0, dcount)
        self.assertEquals(0, icount)
