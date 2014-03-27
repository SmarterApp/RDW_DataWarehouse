import unittest
from sqlalchemy.sql.expression import select, delete
from uuid import uuid4
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.preetl.pre_etl import pre_etl_job
from edudl2.database.udl2_connector import initialize_db_udl, get_udl_connection
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.exceptions.errorcodes import ErrorCode


class PreEtlTest(unittest.TestCase):

    def setUp(self):
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path_file)
        self.udl2_conf = conf_tup[0]
        initialize_db_udl(self.udl2_conf)
        self.batch_table_name = self.udl2_conf['udl2_db']['batch_table']

    def tearDown(self):
        pass

    def _verify_pre_etl_step_created_batch_record(self, conn, batch_guid):
        batch_table = conn.get_table(self.batch_table_name)
        query = select([batch_table], batch_table.c.guid_batch == batch_guid)
        result = conn.execute(query)
        records_inserted = result.rowcount
        self.assertEqual(records_inserted, 1)
        batch_record = result.fetchone()
        self.assertEqual(batch_record['udl_phase'], 'PRE ETL')
        self.assertEqual(batch_record['guid_batch'], batch_guid)
        self.assertEqual(batch_record['load_type'], 'Unknown')
        self.assertEqual(batch_record['udl_leaf'], False)
        self.assertEqual(batch_record['udl_phase_step_status'], mk.SUCCESS)

    def _cleanup_pre_etl_created_record_and_verify(self, conn, batch_guid):
        batch_table = conn.get_table(self.batch_table_name)
        delete_query = delete(batch_table, batch_table.c.guid_batch == batch_guid)
        records_deleted = conn.execute(delete_query).rowcount
        self.assertEqual(records_deleted, 1)

    def test_pre_etl_job_forced_batch_guid(self):
        batch_guid_forced = str(uuid4())
        batch_guid = pre_etl_job(self.udl2_conf, batch_guid_forced=batch_guid_forced)

        # make sure that the forced batch guid passed is same as the one pre_etl_job returns
        self.assertEqual(batch_guid_forced, batch_guid)

        # check one row is inserted in batch table
        with get_udl_connection() as conn:
            self._verify_pre_etl_step_created_batch_record(conn, batch_guid)
            self._cleanup_pre_etl_created_record_and_verify(conn, batch_guid)

    def test_pre_etl_job(self):
        batch_guid = pre_etl_job(self.udl2_conf)

        # check one row is inserted in batch table
        with get_udl_connection() as conn:
            self._verify_pre_etl_step_created_batch_record(conn, batch_guid)
            self._cleanup_pre_etl_created_record_and_verify(conn, batch_guid)
