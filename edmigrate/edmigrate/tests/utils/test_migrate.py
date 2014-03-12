from edmigrate.utils.migrate import get_batches_to_migrate, migrate_fact_asmt_outcome, migrate_batch, \
    report_udl_stats_batch_status
from edmigrate.tests.utils.unittest_with_preprod_sqlite import Unittest_with_preprod_sqlite, \
    get_unittest_tenant_name as get_unittest_preprod_tenant_name
from edmigrate.exceptions import EdMigrateRecordAlreadyDeletedException, \
    EdMigrateUdl_statException
from sqlalchemy.sql.expression import select, func
from edmigrate.utils.constants import Constants
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edmigrate.database.migrate_dest_connector import EdMigrateDestConnection
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection
from edcore.database.utils.constants import UdlStatsConstants
__author__ = 'sravi'

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    get_unittest_tenant_name as get_unittest_prod_tenant_name


class TestMigrate(Unittest_with_edcore_sqlite, Unittest_with_preprod_sqlite, Unittest_with_stats_sqlite):

    test_tenant = 'tomcat'

    def setUp(self):
        self.__tenant = TestExtractTask.test_tenant

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass(EdMigrateDestConnection.get_datasource_name(TestExtractTask.test_tenant))
        Unittest_with_preprod_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        pass

    def test_migrate_fact_asmt_outcome(self):
        preprod_conn = EdMigrateSourceConnection(tenant=get_unittest_preprod_tenant_name())
        prod_conn = EdMigrateDestConnection(tenant=get_unittest_prod_tenant_name())
        batch_guid = "288220EB-3876-41EB-B3A7-F0E6C8BD013B"
        fact_asmt_outcome_table = prod_conn.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select([func.count().label('asmt_outcome_rec_ids')], fact_asmt_outcome_table.c.asmnt_outcome_rec_id.in_([1011691, 1011681, 1011671]))
        query_c = query.where(fact_asmt_outcome_table.c.status == 'C')
        query_d = query.where(fact_asmt_outcome_table.c.status == 'D')
        rset = prod_conn.execute(query_c)
        row = rset.fetchone()
        self.assertEqual(3, row['asmt_outcome_rec_ids'])
        rset.close()

        delete_count, insert_count = migrate_fact_asmt_outcome(batch_guid, None, preprod_conn, prod_conn)
        self.assertEqual(3, delete_count)
        self.assertEqual(3, insert_count)
        rset = prod_conn.execute(query_c)
        row = rset.fetchone()
        self.assertEqual(0, row['asmt_outcome_rec_ids'])
        rset.close()
        rset = prod_conn.execute(query_d)
        row = rset.fetchone()
        self.assertEqual(3, row['asmt_outcome_rec_ids'])
        rset.close()

    def test_migrate_fact_asmt_outcome_record_already_deleted1(self):
        preprod_conn = EdMigrateSourceConnection(tenant=get_unittest_preprod_tenant_name())
        prod_conn = EdMigrateDestConnection(tenant=get_unittest_prod_tenant_name())
        batch_guid = "9FCD871F-DE8F-4DDD-936C-E02F00258DD8"
        self.assertRaises(EdMigrateRecordAlreadyDeletedException, migrate_fact_asmt_outcome, batch_guid, None, preprod_conn, prod_conn)

    def test_migrate_fact_asmt_outcome_record_already_deleted2(self):
        preprod_conn = EdMigrateSourceConnection(tenant=get_unittest_preprod_tenant_name())
        prod_conn = EdMigrateDestConnection(tenant=get_unittest_prod_tenant_name())
        batch_guid = "9FCD871F-DE8F-4DDD-936C-E02F00258DD8"
        self.assertRaises(EdMigrateRecordAlreadyDeletedException, migrate_fact_asmt_outcome, batch_guid, None, preprod_conn, prod_conn, batch_size=1)

    def test_get_batches_to_migrate_with_specified_tenant(self):
        batches_to_migrate = get_batches_to_migrate('test')
        self.assertEqual(4, len(batches_to_migrate))

    #def test_migrate_batch(self):
    #    batch = {UdlStatsConstants.BATCH_GUID: '3384654F-9076-45A6-BB13-64E8EE252A49', UdlStatsConstants.TENANT: self.__tenant}
    #    rtn = migrate_batch(batch)
    #    self.assertTrue(rtn)

    def test_migrate_batch_with_roll_back(self):
        batch = {UdlStatsConstants.BATCH_GUID: '13DCC2AB-4FC6-418D-844E-65ED5D9CED38', UdlStatsConstants.TENANT: 'tomcat', UdlStatsConstants.SCHEMA_NAME: None}
        prod_conn = EdMigrateDestConnection(tenant=get_unittest_prod_tenant_name())
        fact_asmt_outcome_table = prod_conn.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select([func.count(fact_asmt_outcome_table.c.status).label('cnt')], fact_asmt_outcome_table.c.asmnt_outcome_rec_id.in_([101306, 101304, 101302]))
        query_c = query.where(fact_asmt_outcome_table.c.status == 'C')
        query_d = query.where(fact_asmt_outcome_table.c.status == 'D')
        rset = prod_conn.execute(query_c)
        row = rset.fetchone()
        self.assertEqual(2, row['cnt'])
        rset.close()
        rset = prod_conn.execute(query_d)
        row = rset.fetchone()
        self.assertEqual(1, row['cnt'])
        rtn = migrate_batch(batch)
        rset.close()
        self.assertFalse(rtn)
        rset = prod_conn.execute(query_c)
        row = rset.fetchone()
        self.assertEqual(2, row['cnt'])
        rset.close()
        rset = prod_conn.execute(query_d)
        row = rset.fetchone()
        self.assertEqual(1, row['cnt'])
        rtn = migrate_batch(batch)
        rset.close()

    def test_report_udl_stats_batch_status(self):
        batches_to_migrate = get_batches_to_migrate('hotdog')
        self.assertEqual(1, len(batches_to_migrate))
        self.assertEqual(UdlStatsConstants.UDL_STATUS_INGESTED, batches_to_migrate[0][UdlStatsConstants.LOAD_STATUS])
        updated_count = report_udl_stats_batch_status(batches_to_migrate[0][UdlStatsConstants.BATCH_GUID], UdlStatsConstants.MIGRATE_INGESTED)
        self.assertEqual(1, updated_count)
        batches_to_migrate = get_batches_to_migrate('hotdog')
        self.assertEqual(0, len(batches_to_migrate))

    def test_report_udl_stats_batch_status_non_exist_batch_id(self):
        self.assertRaises(EdMigrateUdl_statException, report_udl_stats_batch_status, 'non-exist-uuid', UdlStatsConstants.MIGRATE_IN_PROCESS)
