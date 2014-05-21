'''
Created on Nov 7, 2013

@author: dip
'''
import unittest
from unittest.mock import patch

import tempfile
import os
import shutil
import json
import csv
from zipfile import ZipFile
from collections import OrderedDict

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, UnittestEdcoreDBConnection,
                                                            get_unittest_tenant_name)
from sqlalchemy.sql.expression import select
from edextract.celery import setup_celery
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from celery.canvas import group
from edextract.exceptions import ExtractionError
from edextract.settings.config import setup_settings
from edextract.tasks.constants import ExtractionDataType
from edextract.tasks.extract import (generate_extract_file_tasks, generate_extract_file, archive, archive_with_encryption,
                                     remote_copy, prepare_path)
from edcore.exceptions import RemoteCopyError


class TestExtractTask(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        settings = {'extract.celery.BROKER_URL': 'memory',
                    'extract.gpg.keyserver': None,
                    'extract.gpg.homedir': gpg_home,
                    'extract.gpg.public_key.cat': 'kswimberly@amplify.com',
                    'extract.celery.CELERY_ALWAYS_EAGER': 'True',
                    'extract.retries_allowed': '1',
                    'extract.retry_delay': '3'
                    }
        setup_celery(settings)
        setup_settings(settings)
        self._tenant = get_unittest_tenant_name()
        self.__files = ['a.txt', 'b.txt', 'c.txt']
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self.__tmp_zip = os.path.join(tempfile.mkdtemp('zip'), 'test.zip')
        for file in self.__files:
            with open(os.path.join(self.__tmp_dir, file), "w") as f:
                f.write('hello ' + file)
        self.maxDiff = None

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)
        shutil.rmtree(os.path.dirname(self.__tmp_zip))

    def test_generate(self):
        pass

    def test_archive(self):
        open(self.__tmp_zip, 'wb').write(archive('req_id', self.__tmp_dir))

        zipfile = ZipFile(self.__tmp_zip, "r")
        namelist = zipfile.namelist()
        self.assertEqual(3, len(namelist))
        self.assertIn('a.txt', namelist)
        self.assertIn('b.txt', namelist)
        self.assertIn('c.txt', namelist)

        file_a = zipfile.read('a.txt')
        self.assertEqual(b'hello a.txt', file_a)
        file_b = zipfile.read('b.txt')
        self.assertEqual(b'hello b.txt', file_b)
        file_c = zipfile.read('c.txt')
        self.assertEqual(b'hello c.txt', file_c)
        zipfile.close()

    def test_generate_csv_no_tenant(self):
        output = '/tmp/unittest.csv.gz.pgp'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: None
        }

        result = generate_extract_file.apply(args=[None, '0', task])    # @UndefinedVariable
        result.get()

        self.assertFalse(os.path.exists(output))

    def test_generate_csv(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid, dim_asmt.c.asmt_period], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '7d10d26b-b013-4cdd-a916-5d577e895cff')
        output = os.path.join(self.__tmp_dir, 'asmt.csv')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query}
        }

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])    # @UndefinedVariable
        result.get()

        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 2)
        self.assertEqual(csv_data[0], ['asmt_guid', 'asmt_period'])
        self.assertEqual(csv_data[1], ['7d10d26b-b013-4cdd-a916-5d577e895cff', 'Spring 2016'])

    def test_generate_csv_with_bad_file(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '2123122')
        output = 'C:'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query}
        }

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])    # @UndefinedVariable

        self.assertRaises(ExtractionError, result.get,)

    def test_generate_json(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '7d10d26b-b013-4cdd-a916-5d577e895cff')
            output = os.path.join(self.__tmp_dir, 'asmt.json')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_JSON,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query}
        }

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])    # @UndefinedVariable
        results.get()

        self.assertTrue(os.path.exists(output))
        with open(output) as out:
            data = json.load(out)
        self.assertEqual(data['asmt_guid'], '7d10d26b-b013-4cdd-a916-5d577e895cff')

    def test_generate_json_not_writable(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '7d10d26b-b013-4cdd-a916-5d577e895cff')
        output = os.path.join('', 'asmt.json')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_JSON,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query}
        }

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])    # @UndefinedVariable

        self.assertRaises(ExtractionError, results.get)

    def test_generate_json_with_no_results(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '2123122')
        output = os.path.join(self.__tmp_dir, 'asmt.json')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_JSON,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query}
        }

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])    # @UndefinedVariable
        results.get()

        self.assertTrue(os.path.exists(output))
        statinfo = os.stat(output)
        self.assertEqual(0, statinfo.st_size)

    def test_generate_json_with_bad_file(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '2123122')
        output = 'C:'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_JSON,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query}
        }

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])    # @UndefinedVariable

        self.assertRaises(ExtractionError, results.get)

    @patch('edextract.tasks.extract.generate_statistics_report')
    def test_generate_sr_statistics_csv_success(self, mock_generate_statistics_report):
        mock_generate_statistics_report.return_value = None
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        queries = {QueryType.QUERY: 'academic_year_query', QueryType.MATCH_ID_QUERY: 'match_id_query'}
        task = {TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_STATISTICS, TaskConstants.TASK_TASK_ID: 'task_id',
                TaskConstants.ACADEMIC_YEAR: 2016, TaskConstants.TASK_FILE_NAME: output, TaskConstants.TASK_QUERIES: queries,
                TaskConstants.CSV_HEADERS: 'statistics_csv_headers'}

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])
        result.get()

        task_info = {Constants.TASK_ID: task[TaskConstants.TASK_TASK_ID],
                     Constants.CELERY_TASK_ID: result.id,
                     Constants.REQUEST_GUID: 'request_id'}

        mock_generate_statistics_report.assert_called_with(self._tenant, output, task_info, task)

    def test_generate_sr_statistics_csv_no_tenant(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_STATISTICS,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.ACADEMIC_YEAR: 2014
        }

        result = generate_extract_file.apply(args=[None, 'request_id', task])
        result.get()

        self.assertFalse(os.path.exists(output))

    def test_generate_sr_statistics_csv_bad_file(self):
        output = 'C:'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_STATISTICS,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.TASK_FILE_NAME: output,
            TaskConstants.ACADEMIC_YEAR: 2014
        }

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])

        self.assertRaises(ExtractionError, result.get,)

    @patch('edextract.tasks.extract.generate_completion_report')
    def test_generate_sr_completion_csv_success(self, mock_generate_completion_report):
        mock_generate_completion_report.return_value = None
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        queries = {QueryType.QUERY: 'q1'}
        task = {TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_COMPLETION, TaskConstants.TASK_TASK_ID: 'task_id',
                TaskConstants.ACADEMIC_YEAR: 2016, TaskConstants.TASK_FILE_NAME: output, TaskConstants.TASK_QUERIES: queries,
                TaskConstants.CSV_HEADERS: 'completion_csv_headers'}

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])
        result.get()

        task_info = {Constants.TASK_ID: task[TaskConstants.TASK_TASK_ID],
                     Constants.CELERY_TASK_ID: result.id,
                     Constants.REQUEST_GUID: 'request_id'}

        mock_generate_completion_report.assert_called_with(self._tenant, output, task_info, task)

    def test_generate_extract_file_tasks_asmt_json_request(self):
        # Have to use OrderedDict here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.QUERY_JSON),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, {QueryType.QUERY: 'abc'}),
                              (TaskConstants.TASK_TASK_ID, 'abc')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'QueryJSONExtract'), ('file_name', 'abc'), ('task_queries', {'query': 'abc'}), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_generate_extract_file_tasks_asmt_csv_request(self):
        # Have to use OrderedDict here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.QUERY_CSV),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, {QueryType.QUERY: 'abc'}),
                              (TaskConstants.TASK_TASK_ID, 'abc')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'QueryCSVExtract'), ('file_name', 'abc'), ('task_queries', {'query': 'abc'}), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_generate_extract_file_tasks_json_request_asmt_multi_requests(self):
        # Have to use OrderedDicts here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.QUERY_JSON),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, {QueryType.QUERY: 'abc'}),
                              (TaskConstants.TASK_TASK_ID, 'abc')]),
                 OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.QUERY_CSV),
                              (TaskConstants.TASK_FILE_NAME, 'def'),
                              (TaskConstants.TASK_QUERIES, {QueryType.QUERY: 'def'}),
                              (TaskConstants.TASK_TASK_ID, 'def')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'QueryJSONExtract'), ('file_name', 'abc'), ('task_queries', {'query': 'abc'}), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'QueryCSVExtract'), ('file_name', 'def'), ('task_queries', {'query': 'def'}), ('task_id', 'def')]))", str(tasks_group.kwargs['tasks'][1]))

    def test_generate_extract_file_tasks_sr_statistics_request(self):
        # Have to use OrderedDict here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.SR_STATISTICS),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, OrderedDict([(QueryType.QUERY, 'ayq1'), (QueryType.MATCH_ID_QUERY, 'miq1')])),
                              (TaskConstants.TASK_TASK_ID, 'abc')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'StudentRegistrationStatisticsReportCSV'), ('file_name', 'abc'), ('task_queries', OrderedDict([('query', 'ayq1'), ('match_id_query', 'miq1')])), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_generate_extract_file_tasks_sr_completion_request(self):
        # Have to use OrderedDict here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.SR_COMPLETION),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, OrderedDict([(QueryType.QUERY, 'q1')])),
                              (TaskConstants.TASK_TASK_ID, 'abc')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'StudentRegistrationCompletionReportCSV'), ('file_name', 'abc'), ('task_queries', OrderedDict([('query', 'q1')])), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_archive_with_encryption(self):
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as _dir:
            csv_dir = os.path.join(_dir, 'csv')
            os.mkdir(csv_dir)
            gpg_file = os.path.join(_dir, 'gpg', 'output.gpg')
            os.mkdir(os.path.dirname(gpg_file))
            for file in files:
                with open(os.path.join(csv_dir, file), 'a') as f:
                    f.write(file)

            request_id = '1'
            recipients = 'kswimberly@amplify.com'

            result = archive_with_encryption.apply(args=[request_id, recipients, gpg_file, csv_dir])
            result.get()

            self.assertTrue(os.path.exists(gpg_file))

    def test_archive_with_encryption_no_recipients(self):
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as _dir:
            csv_dir = os.path.join(_dir, 'csv')
            os.mkdir(csv_dir)
            gpg_file = os.path.join(_dir, 'gpg', 'output.gpg')
            os.mkdir(os.path.dirname(gpg_file))
            for file in files:
                with open(os.path.join(csv_dir, file), 'a') as f:
                    f.write(file)

            request_id = '1'
            recipients = 'nobody@amplify.com'

            result = archive_with_encryption.apply(args=[request_id, recipients, gpg_file, csv_dir])

            self.assertRaises(ExtractionError, result.get)

    @patch('edextract.tasks.extract.copy')
    def test_remote_copy_success(self, mock_copy):
        mock_copy.return_value = None
        request_id = '1'
        tenant = 'es'
        gatekeeper = 'foo'
        sftp_info = ['128.0.0.2', 'nobody', '/dev/null']
        with tempfile.TemporaryDirectory() as _dir:
            src_file_name = os.path.join(_dir, 'src.txt')
            open(src_file_name, 'w').close()

            remote_copy.apply(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info], kwargs={'timeout': 3})

            mock_copy.assert_called_with(src_file_name, '128.0.0.2', 'es', 'foo', 'nobody', '/dev/null', timeout=3)

    @patch('edextract.tasks.extract.copy')
    def test_remote_copy_failure(self, mock_copy):
        mock_copy.side_effect = RemoteCopyError
        request_id = '1'
        tenant = 'es'
        gatekeeper = 'foo'
        sftp_info = ['128.0.0.2', 'nobody', '/dev/null']
        with tempfile.TemporaryDirectory() as _dir:
            src_file_name = os.path.join(_dir, 'src.txt')
            open(src_file_name, 'w').close()

            result = remote_copy.apply(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info], kwargs={'timeout': 3})

            self.assertRaises(ExtractionError, result.get)

    def test_prepare_path(self):
        tmp_dir = tempfile.mkdtemp()
        shutil.rmtree(tmp_dir, ignore_errors=True)
        self.assertFalse(os.path.exists(tmp_dir))

        prepare_path.apply(args=["id", [tmp_dir]]).get()

        self.assertTrue(os.path.exists(tmp_dir))


if __name__ == "__main__":
    unittest.main()
