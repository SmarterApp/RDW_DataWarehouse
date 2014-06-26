'''
Created on Nov 7, 2013

@author: dip
'''

import unittest
from unittest.mock import patch

import glob
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
from edextract.celery import setup_celery
from edextract.status.constants import Constants
from sqlalchemy.sql.expression import and_, select
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from celery.canvas import group
from edextract.exceptions import ExtractionError
from edextract.settings.config import setup_settings
from edextract.tasks.constants import ExtractionDataType
from edextract.tasks.extract import (generate_extract_file_tasks, generate_extract_file, archive, archive_with_stream,
                                     remote_copy, prepare_path, generate_item_or_raw_extract_file)
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
                    'extract.retry_delay': '3',
                    'hpz.file_upload_base_url': 'http://somehost:82/files',
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

    def test_archive_with_stream(self):
        open(self.__tmp_zip, 'wb').write(archive_with_stream('req_id', self.__tmp_dir))

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
        self.assertEqual("tasks.extract.generate_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'StudentAssessmentCompletionReportCSV'), ('file_name', 'abc'), ('task_queries', OrderedDict([('query', 'q1')])), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_generate_extract_file_tasks_for_item_level_extract_request(self):
        # Have to use OrderedDict here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.QUERY_ITEMS_CSV),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, OrderedDict([(QueryType.QUERY, 'q1')])),
                              (TaskConstants.TASK_TASK_ID, 'abc')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_item_or_raw_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'QueryItemsCSVExtract'), ('file_name', 'abc'), ('task_queries', OrderedDict([('query', 'q1')])), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_generate_extract_file_tasks_for_raw_data_extract_request(self):
        # Have to use OrderedDict here to ensure order in results.
        tasks = [OrderedDict([(TaskConstants.EXTRACTION_DATA_TYPE, ExtractionDataType.QUERY_RAW_XML),
                              (TaskConstants.TASK_FILE_NAME, 'abc'),
                              (TaskConstants.TASK_QUERIES, OrderedDict([(QueryType.QUERY, 'q1')])),
                              (TaskConstants.TASK_TASK_ID, 'abc')])]

        tasks_group = generate_extract_file_tasks(self._tenant, 'request', tasks)

        self.assertIsInstance(tasks_group, group)
        self.assertEqual("tasks.extract.generate_item_or_raw_extract_file('tomcat', 'request', OrderedDict([('extraction_data_type', 'QueryRawXML'), ('file_name', 'abc'), ('task_queries', OrderedDict([('query', 'q1')])), ('task_id', 'abc')]))", str(tasks_group.kwargs['tasks'][0]))

    def test_generate_raw_extract_with_missing_output_dir(self):
        output_dir = '/tmp/xyz'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_RAW_XML,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: '/tmp/abc',
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: 'query'}
        }

        result = generate_item_or_raw_extract_file.apply(args=[self._tenant, 'request_id', task])

        self.assertRaises(ExtractionError, result.get,)

    def test_generate_raw_extract_file_valid_case(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2015',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3'}
        query = self.__create_item_raw_extract_query(params)
        root_dir = tempfile.mkdtemp()
        output_dir = tempfile.mkdtemp(dir=root_dir)
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_RAW_XML,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: '',
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query},
            TaskConstants.ROOT_DIRECTORY: root_dir
        }

        result = generate_item_or_raw_extract_file.apply(args=[self._tenant, 'request_id', task])
        result.get()

        self.assertTrue(os.path.exists(output_dir))
        all_extracted_files = glob.glob(os.path.join(output_dir, '*.xml'))
        self.assertEqual(len(all_extracted_files), 0)

    def test_generate_item_extract_file_valid_case(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2015',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3'}
        query = self.__create_item_raw_extract_query(params)
        root_dir = tempfile.mkdtemp()
        output_dir = tempfile.mkdtemp(dir=root_dir)
        output_file = os.path.join(output_dir, 'items_output.csv')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_ITEMS_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: output_file,
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query},
            TaskConstants.ROOT_DIRECTORY: root_dir,
            TaskConstants.ITEM_IDS: None
        }

        result = generate_item_or_raw_extract_file.apply(args=[self._tenant, 'request_id', task])
        result.get()
        self.assertTrue(os.path.exists(output_file))
        with open(output_file) as f:
            line = f.readline()
            header = line.split(',')
            self.assertEqual(len(header), 18)
            self.assertTrue('key' in header)

    def test_generate_item_extract_with_missing_output_file(self):
        output_dir = '/tmp/xyz'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_ITEMS_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: '/tmp/items_xyz.csv',
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: 'query'}
        }

        result = generate_item_or_raw_extract_file.apply(args=[self._tenant, 'request_id', task])

        self.assertRaises(ExtractionError, result.get,)

    @patch('edextract.tasks.extract.insert_extract_stats')
    @patch('edextract.tasks.extract.http_file_upload')
    def test_remote_copy_success(self, file_upload_patch, insert_stats_patch):
        file_upload_patch.side_effect = None
        insert_stats_patch.side_effect = None
        insert_stats_patch.return_value = None
        request_id = 'test_request_id'
        file_name = 'test_file_name'
        reg_id = 'a1-b2-c3-d4-e5'

        results = remote_copy.apply(args=[request_id, file_name, reg_id])
        results.get()

        file_upload_patch.assert_called_once_with('test_file_name', 'a1-b2-c3-d4-e5')
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(2, insert_stats_patch.call_count)

    @patch('edextract.tasks.extract.insert_extract_stats')
    @patch('edextract.tasks.extract.http_file_upload')
    def test_remote_copy_connection_error(self, file_upload_patch, insert_stats_patch):
        file_upload_patch.side_effect = RemoteCopyError('ooops!')
        insert_stats_patch.side_effect = None
        insert_stats_patch.return_value = None
        request_id = 'test_request_id'
        file_name = 'test_file_name'
        reg_id = 'a1-b2-c3-d4-e5'

        results = remote_copy.apply(args=[request_id, file_name, reg_id])

        file_upload_patch.assert_called_with('test_file_name', 'a1-b2-c3-d4-e5')
        self.assertEqual(2, file_upload_patch.call_count)
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(4, insert_stats_patch.call_count)

        self.assertRaises(ExtractionError, results.get)

    @patch('edextract.tasks.extract.archive_files')
    @patch('edextract.tasks.extract.insert_extract_stats')
    def test_archive_task(self, insert_stats_patch, archive_patch):
        request_id = '1'
        zip_file = 'output.zip'
        csv_dir = 'csv/file/dir'

        result = archive.apply(args=[request_id, zip_file, csv_dir])
        result.get()

        archive_patch.assert_called_once_with(csv_dir, zip_file)
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(2, insert_stats_patch.call_count)

    def test_prepare_path(self):
        tmp_dir = tempfile.mkdtemp()
        shutil.rmtree(tmp_dir, ignore_errors=True)
        self.assertFalse(os.path.exists(tmp_dir))

        prepare_path.apply(args=["id", [tmp_dir]]).get()

        self.assertTrue(os.path.exists(tmp_dir))

    def __create_item_raw_extract_query(self, params):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            fact_asmt_outcome_vw = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact_asmt_outcome_vw.c.state_code,
                            fact_asmt_outcome_vw.c.asmt_year,
                            fact_asmt_outcome_vw.c.asmt_type,
                            dim_asmt.c.effective_date,
                            fact_asmt_outcome_vw.c.asmt_subject,
                            fact_asmt_outcome_vw.c.asmt_grade,
                            fact_asmt_outcome_vw.c.district_guid,
                            fact_asmt_outcome_vw.c.student_guid],
                           from_obj=[fact_asmt_outcome_vw
                                     .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id))])

            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_year == params['asmtYear']))
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_type == params['asmtType']))
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_subject == params['asmtSubject']))
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == params['asmtGrade']))
            query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == 'C'))
            return query


if __name__ == "__main__":
    unittest.main()
