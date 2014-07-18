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
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, UnittestEdcoreDBConnection,
                                                            get_unittest_tenant_name)
from edextract.celery import setup_celery
from edextract.status.constants import Constants
from sqlalchemy.sql.expression import and_, select
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from edextract.exceptions import ExtractionError
from edextract.settings.config import setup_settings
from edextract.tasks.constants import ExtractionDataType
from edextract.tasks.extract import (generate_extract_file, archive, archive_with_stream,
                                     remote_copy, prepare_path, generate_item_or_raw_extract_file, extract_group_separator)
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

        result = generate_extract_file.apply(args=[None, '0', task])  # @UndefinedVariable
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

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])  # @UndefinedVariable
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

        result = generate_extract_file.apply(args=[self._tenant, 'request_id', task])  # @UndefinedVariable

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

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])  # @UndefinedVariable
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

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])  # @UndefinedVariable

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

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])  # @UndefinedVariable
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

        results = generate_extract_file.apply(args=[self._tenant, 'request_id', task])  # @UndefinedVariable

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

    def test_generate_raw_extract_with_missing_output_dir(self):
        output_dir = '/tmp/xyz'
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_RAW_XML,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: '/tmp/abc',
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: 'query'}
        }

        self.assertRaises(ExtractionError, generate_item_or_raw_extract_file, self._tenant, 'request_id', task)

    def test_generate_raw_extract_file_valid_case(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2015',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3'}
        query = self.__create_item_raw_extract_query(params)
        root_dir = tempfile.mkdtemp()
        archive_dir = os.path.join(root_dir, 'archive')
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_RAW_XML,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: archive_dir,
            TaskConstants.TASK_FILE_NAME: '',
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: query},
            TaskConstants.ROOT_DIRECTORY: root_dir
        }
        xml_path1 = os.path.join(root_dir, 'NC', '2015', 'SUMMATIVE', '20150404', 'MATH', '3', '0513ba44-e8ec-4186-9a0e-8481e9c16206')
        xml_path2 = os.path.join(root_dir, 'NC', '2015', 'SUMMATIVE', '20150404', 'MATH', '3', '228')
        xml_path3 = os.path.join(root_dir, 'NC', '2015', 'SUMMATIVE', '20150404', 'MATH', '3', '229')
        xml_path4 = os.path.join(root_dir, 'NC', '2015', 'SUMMATIVE', '20150404', 'MATH', '3', '2ce72d77-1de2-4137-a083-77935831b817')

        def create_files(path, filenames):
            archive_files = []
            for file in filenames:
                f = os.path.join(path, file)
                a = os.path.join(archive_dir, os.path.basename(file))
                open(f, 'w').close()
                archive_files.append(a)
            return archive_files

        files1 = []
        files2 = []
        files3 = []
        files4 = []
        files1.append('f22a52ef-ed1a-4207-9bc8-8d41dd6f8577.xml')
        files1.append('de502030-032c-45b4-af8a-373dafb94400.xml')
        files1.append('aa3e4230-c919-406a-8c33-dfddab59c259.xml')
        files1.append('5791a3ea-e5c8-494f-8798-b4945a40f214.xml')
        files1.append('25f2e010-f8b8-4494-8e60-7ca1c9e3d049.xml')
        files1.append('6f902cb4-e029-4bf4-84ac-4ba3e9e394f1.xml')
        files1.append('6520a1ba-3700-4b6f-b516-6a2caea39e0d.xml')
        files1.append('58162fc8-d10c-476b-95ef-144d231a7ea4.xml')
        files1.append('4f0c7e67-3cf6-42c8-8fac-dbec4401b632.xml')
        files2.append('72d8248d-0e8f-404b-8763-a5b7bcdaf535.xml')
        files2.append('34140997-8949-497e-bbbb-5d72aa7dc9cb.xml')
        files2.append('a84a514b-ee02-4e76-a047-c55b4390087e.xml')
        files2.append('8b890349-1421-439e-99e4-235e13fe28dc.xml')
        files2.append('cad811ad-9b08-4dd1-aa10-52360b80ff7f.xml')
        files2.append('aeed1057-82ad-46c8-bf24-b0dffc171669.xml')
        files2.append('a016a4c1-5aca-4146-a85b-ed1172a01a4d.xml')
        files2.append('b2307755-1752-4f54-a3a1-e2dcd3912d9e.xml')
        files2.append('389c8fd6-228a-4204-bad7-c6a2a3e759cf.xml')
        files2.append('61ec47de-e8b5-4e78-9beb-677c44dd9b50.xml')
        files2.append('a3fcc2a7-16ba-4783-ae58-f225377e8e20.xml')
        files2.append('af68c5f9-b5aa-41e8-b583-e82b7d8ff48b.xml')
        files2.append('3181376a-f3a8-40d3-bbde-e65fdd9f4494.xml')
        files2.append('c72e98d5-ddb6-4cde-90d2-cdb215e67e84.xml')
        files3.append('3efe8485-9c16-4381-ab78-692353104cce.xml')
        files3.append('34b99412-fd5b-48f0-8ce8-f8ca3788634a.xml')
        files4.append('fe3d166a-14b8-4871-b947-b82b6974d15a.xml')
        files4.append('11ddf594-55ab-4e77-b09e-73aa27fb1f04.xml')
        files4.append('c1b43997-f999-4116-94e0-9d76a763e767.xml')
        files4.append('ebf98f09-3522-4a77-87bd-20078883c500.xml')
        files4.append('40d2883d-c7f5-499b-ac75-78047f78af56.xml')
        files4.append('84f57040-e40f-4ace-ba1a-16beeb9d9799.xml')
        files4.append('0d73956c-e7ef-40bd-88b5-57f75e2547d4.xml')
        files4.append('3551ce11-5ee3-4d1a-b65b-cbe92979697b.xml')
        files4.append('8667760a-4f8a-40b1-a53f-08cc7c50d230.xml')
        files4.append('3c5cabec-2425-4266-85e4-dd7271b41071.xml')
        files4.append('8140131b-3e72-418e-a4aa-a2f4c9197543.xml')
        files4.append('f3fbb21c-c602-4bbe-b550-a2be351d3c68.xml')
        files4.append('7a4c0b46-bc9c-4337-af58-dc028e7169d3.xml')
        files4.append('d94160df-2efb-456a-b4b0-f5e98b65c5ac.xml')
        files4.append('a5e1a73d-8866-41e2-8635-9f7cf2b4afb6.xml')
        files4.append('92d59b24-83df-4c29-9e35-46e648bb4578.xml')
        files4.append('f54b5a4a-a677-4f9c-bf46-597848943554.xml')
        os.makedirs(xml_path1)
        os.makedirs(xml_path2)
        os.makedirs(xml_path3)
        os.makedirs(xml_path4)
        os.makedirs(archive_dir)
        a1 = create_files(xml_path1, files1)
        a2 = create_files(xml_path2, files2)
        a3 = create_files(xml_path3, files3)
        a4 = create_files(xml_path4, files4)

        generate_item_or_raw_extract_file(self._tenant, 'request_id', task)

        def assertArchive(archives):
            for archive in archives:
                self.assertTrue(os.path.isfile(archive))
        assertArchive(a1)
        assertArchive(a2)
        assertArchive(a3)
        assertArchive(a4)

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

    @patch('edextract.tasks.extract.insert_extract_stats')
    @patch('edextract.tasks.extract.http_file_upload')
    def test_remote_copy_exception(self, mock_http_file_upload, mock_insert_extract_stats):
        mock_http_file_upload.side_effect = Exception()
        self.assertRaises(ExtractionError, remote_copy, 'request_id', 'src_file_name', 'registration_id')

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

    @patch('edextract.tasks.extract.archive_files')
    @patch('edextract.tasks.extract.insert_extract_stats')
    def test_archive_exception(self, mock_insert_extract_stats, mock_archive_files):
        mock_archive_files.side_effect = Exception()
        self.assertRaises(ExtractionError, archive, 'request_id', 'archive_file_name', 'directory')

    @patch('edextract.tasks.extract.insert_extract_stats')
    @patch('edextract.tasks.extract.file_utils.prepare_path')
    def test_prepare_path_failed(self, mock_prepare_path, mock_insert_extract_stats):
        mock_prepare_path.side_effect = OSError()
        self.assertRaises(ExtractionError, prepare_path, None, ['hello'])

    def test_extract_group_separator(self):
        extract_group_separator()
        self.assertTrue(True)

    @patch('edextract.tasks.extract.get_extract_func')
    @patch('edextract.tasks.extract.insert_extract_stats')
    def test_generate_extract_file(self, mock_insert_extract_stats, mock_get_extract_func):
        f = tempfile.TemporaryDirectory()
        mock_get_extract_func.return_value.side_effect = FileNotFoundError()
        output = os.path.join(f.name, 'hello.out')
        open(output, 'w').close()
        task = {TaskConstants.TASK_FILE_NAME: output, TaskConstants.TASK_TASK_ID: 'a', TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_CSV}
        self.assertRaises(ExtractionError, generate_extract_file, 'tenant', 'request_id', task)
        self.assertFalse(os.path.exists(output))

        mock_get_extract_func.return_value.side_effect = Exception()
        output = os.path.join(f.name, 'hello.out')
        open(output, 'w').close()
        task = {TaskConstants.TASK_FILE_NAME: output, TaskConstants.TASK_TASK_ID: 'a', TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_CSV}
        self.assertRaises(ExtractionError, generate_extract_file, 'tenant', 'request_id', task)
        self.assertFalse(os.path.exists(output))
        f.cleanup()

    @patch('edextract.tasks.extract.insert_extract_stats')
    def test_generate_item_or_raw_extract_file_tenant_is_None(self, mock_insert_extract_stats):
        f = tempfile.TemporaryDirectory()
        output_dir = f.name
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_ITEMS_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: os.path.join(output_dir, 'hello'),
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: 'query'}
        }

        generate_item_or_raw_extract_file(None, 'request_id', task)
        self.assertEqual(2, mock_insert_extract_stats.call_count)
        f.cleanup()

    @patch('edextract.tasks.extract.insert_extract_stats')
    def test_generate_item_or_raw_extract_file_no_outputfile(self, mock_insert_extract_stats):
        f = tempfile.TemporaryDirectory()
        output_dir = f.name
        task = {
            TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.QUERY_ITEMS_CSV,
            TaskConstants.TASK_TASK_ID: 'task_id',
            TaskConstants.DIRECTORY_TO_ARCHIVE: output_dir,
            TaskConstants.TASK_FILE_NAME: os.path.join(output_dir, 'hello', 'world'),
            TaskConstants.TASK_QUERIES: {QueryType.QUERY: 'query'}
        }

        self.assertRaises(ExtractionError, generate_item_or_raw_extract_file, 'hello', 'request_id', task)
        f.cleanup()

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
                            fact_asmt_outcome_vw.c.district_id,
                            fact_asmt_outcome_vw.c.student_id],
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
