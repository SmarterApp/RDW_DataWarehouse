import unittest
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.database_util import connect_db, execute_query_with_result, execute_queries
from uuid import uuid4
import os
from edudl2.preetl.pre_etl import pre_etl_job
from edudl2.udl2.udl2_connector import initialize_db, TargetDBConnection, UDL2DBConnection
from edudl2.udl2_util.config_reader import read_ini_file
import tempfile
import shutil
from edudl2.exceptions.errorcodes import ErrorCode


class PreEtlTest(unittest.TestCase):

    def setUp(self):
        # get conf file
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path_file)
        self.udl2_conf = conf_tup[0]
        initialize_db(UDL2DBConnection, self.udl2_conf)

        # create test error log file
        self.temp_dir = tempfile.mkdtemp()
        self.test_error_log_file = os.sep.join([self.temp_dir, 'test_error_log.log'])
        open(self.test_error_log_file, 'w').close()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_pre_etl_job(self):
        # read log file, should be empty
        self._check_log_file(is_empty=True)
        batch_guid_forced = str(uuid4())
        batch_guid = pre_etl_job(self.udl2_conf, log_file=self.test_error_log_file, batch_guid_forced=batch_guid_forced)
        self._check_log_file(is_empty=True)

        # make sure that the forced batch guid passed is same as the one pre_etc_job returns
        self.assertEqual(batch_guid_forced, batch_guid)

        # check one row is inserted in batch table
        query = 'SELECT COUNT(*) from "{schema}"."{batch_table}" WHERE guid_batch = \'{batch_guid}\''.format(batch_guid=batch_guid,
                                                                                                             schema=self.udl2_conf['udl2_db']['staging_schema'],
                                                                                                             batch_table=self.udl2_conf['udl2_db']['batch_table'])
        (conn, _engine) = connect_db(self.udl2_conf['udl2_db']['db_driver'],
                                     self.udl2_conf['udl2_db']['db_user'],
                                     self.udl2_conf['udl2_db']['db_pass'],
                                     self.udl2_conf['udl2_db']['db_host'],
                                     self.udl2_conf['udl2_db']['db_port'],
                                     self.udl2_conf['udl2_db']['db_database'])
        result = execute_query_with_result(conn, query, 'Exception in test_pre_etl_job 1', caller_module='PreEtlTest', caller_func='test_pre_etl_job')
        num_of_row = 0
        for row in result:
            num_of_row = row[0]
            break
        self.assertEqual(str(num_of_row), '1')

        # delete this row
        delete_query = 'DELETE FROM "{schema}"."{batch_table}" WHERE guid_batch = \'{batch_guid}\''.format(batch_guid=batch_guid,
                                                                                                           schema=self.udl2_conf['udl2_db']['staging_schema'],
                                                                                                           batch_table=self.udl2_conf['udl2_db']['batch_table'])
        execute_queries(conn, [delete_query], 'Exception in test_pre_etl_job 2', caller_module='PreEtlTest', caller_func='test_pre_etl_job')
        conn.close()

    def test_pre_etl_job_forced_guid(self):
        # read log file, should be empty
        self._check_log_file(is_empty=True)
        batch_guid = pre_etl_job(self.udl2_conf, log_file=self.test_error_log_file)
        self._check_log_file(is_empty=True)

        # check one row is inserted in batch table
        query = 'SELECT COUNT(*) from "{schema}"."{batch_table}" WHERE guid_batch = \'{batch_guid}\''.format(batch_guid=batch_guid,
                                                                                                             schema=self.udl2_conf['udl2_db']['staging_schema'],
                                                                                                             batch_table=self.udl2_conf['udl2_db']['batch_table'])
        (conn, _engine) = connect_db(self.udl2_conf['udl2_db']['db_driver'],
                                     self.udl2_conf['udl2_db']['db_user'],
                                     self.udl2_conf['udl2_db']['db_pass'],
                                     self.udl2_conf['udl2_db']['db_host'],
                                     self.udl2_conf['udl2_db']['db_port'],
                                     self.udl2_conf['udl2_db']['db_database'])
        result = execute_query_with_result(conn, query, 'Exception in test_pre_etl_job 1', caller_module='PreEtlTest', caller_func='test_pre_etl_job')
        num_of_row = 0
        for row in result:
            num_of_row = row[0]
            break
        self.assertEqual(str(num_of_row), '1')

        # delete this row
        delete_query = 'DELETE FROM "{schema}"."{batch_table}" WHERE guid_batch = \'{batch_guid}\''.format(batch_guid=batch_guid,
                                                                                                           schema=self.udl2_conf['udl2_db']['staging_schema'],
                                                                                                           batch_table=self.udl2_conf['udl2_db']['batch_table'])
        execute_queries(conn, [delete_query], 'Exception in test_pre_etl_job 2', caller_module='PreEtlTest', caller_func='test_pre_etl_job')
        conn.close()

    def _check_log_file(self, is_empty):
        with open(self.test_error_log_file) as f:
            content = f.readlines()
        if is_empty is True:
            self.assertEqual(len(content), 0)
        else:
            self.assertTrue(len(content) > 0)
            expected_error_code = ErrorCode.BATCH_REC_FAILED

            # get error code in log message
            actual_error_code = content[0].split(']')[1].split(':')[0].strip()
            self.assertEqual(expected_error_code, actual_error_code)
