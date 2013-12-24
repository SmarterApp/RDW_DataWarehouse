'''
Created on Nov 7, 2013

@author: dip
'''
import unittest
from edextract.tasks.extract import archive, generate_csv, generate_json, \
    route_tasks, archive_with_encryption, remote_copy
import tempfile
import os
import shutil
from zipfile import ZipFile
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from sqlalchemy.sql.expression import select
from edextract.celery import setup_celery
from edextract.tasks.constants import Constants as TaskConstants
import json
import csv
from celery.canvas import group
from edextract.exceptions import ExtractionError
import stat
from edextract.settings.config import get_setting


class TestExtractTask(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        settings = {'extract.celery.BROKER_URL': 'memory',
                    'extract.gpg.keyserver': None,
                    'extract.gpg.homedir': gpg_home,
                    'extract.gpg.public_key.cat': 'kswimberly@amplify.com',
                    'extract.celery.CELERY_ALWAYS_EAGER': 'True'
                    }
        setup_celery(settings)
        self._tenant = get_unittest_tenant_name()
        self.__files = ['a.txt', 'b.txt', 'c.txt']
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self.__tmp_zip = os.path.join(tempfile.mkdtemp('zip'), 'test.zip')
        for file in self.__files:
            with open(os.path.join(self.__tmp_dir, file), "w") as f:
                f.write('hello ' + file)

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
        result = generate_csv.apply(args=[None, '0', '1', 'select 0 from dual', output])
        result.get()
        self.assertFalse(os.path.exists(output))

    def test_generate_csv_to_unwritable_file(self):
        output = os.path.join(self.__tmp_dir, 'unwritable.csv')
        open(output, 'w').close()
        mode = os.stat(output)[stat.ST_MODE]
        os.chmod(output, mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid, dim_asmt.c.asmt_period], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '22')
        result = generate_csv.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
        self.assertRaises(ExtractionError, result.get,)

    def test_generate_csv(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid, dim_asmt.c.asmt_period], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '22')
        output = os.path.join(self.__tmp_dir, 'asmt.csv')
        result = generate_csv.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
        result.get()
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 2)
        self.assertEqual(csv_data[0], ['asmt_guid', 'asmt_period'])
        self.assertEqual(csv_data[1], ['22', 'Spring 2012'])

    def test_generate_csv_with_bad_file(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '2123122')
            output = 'C:'
            result = generate_csv.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
            self.assertRaises(ExtractionError, result.get,)

    def test_generate_json(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '22')
            output = os.path.join(self.__tmp_dir, 'asmt.json')
            results = generate_json.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
            results.get()
            self.assertTrue(os.path.exists(output))
            with open(output) as out:
                data = json.load(out)
            self.assertEqual(data['asmt_guid'], '22')

    def test_generate_json_not_writable(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '22')
            output = os.path.join('', 'asmt.json')
            results = generate_json.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
            self.assertRaises(ExtractionError, results.get)

    def test_generate_json_with_no_results(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '2123122')
            output = os.path.join(self.__tmp_dir, 'asmt.json')
            results = generate_json.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
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
            results = generate_json.apply(args=[self._tenant, 'request_id', 'task_id', query, output])
            self.assertRaises(ExtractionError, results.get)

    def test_route_tasks_json_request(self):
        tasks = [{TaskConstants.TASK_IS_JSON_REQUEST: True,
                  TaskConstants.TASK_FILE_NAME: 'abc',
                  TaskConstants.TASK_QUERY: 'abc',
                  TaskConstants.TASK_TASK_ID: 'abc'}]
        tasks_group = route_tasks(self._tenant, 'request', tasks)
        self.assertIsInstance(tasks_group, group)
        self.assertEqual(str(tasks_group.kwargs['tasks'][0]), "tasks.extract.generate_json('testtenant', 'request', 'abc', 'abc', 'abc')")

    def test_route_tasks_csv_request(self):
        tasks = [{TaskConstants.TASK_IS_JSON_REQUEST: False,
                  TaskConstants.TASK_FILE_NAME: 'abc',
                  TaskConstants.TASK_QUERY: 'abc',
                  TaskConstants.TASK_TASK_ID: 'abc'}]
        tasks_group = route_tasks(self._tenant, 'request', tasks)
        self.assertIsInstance(tasks_group, group)
        self.assertEqual(str(tasks_group.kwargs['tasks'][0]), "tasks.extract.generate_csv('testtenant', 'request', 'abc', 'abc', 'abc')")

    def test_route_tasks_json_request_multi_requests(self):
        tasks = [{TaskConstants.TASK_IS_JSON_REQUEST: True,
                  TaskConstants.TASK_FILE_NAME: 'abc',
                  TaskConstants.TASK_QUERY: 'abc',
                  TaskConstants.TASK_TASK_ID: 'abc'},
                 {TaskConstants.TASK_IS_JSON_REQUEST: False,
                  TaskConstants.TASK_FILE_NAME: 'def',
                  TaskConstants.TASK_QUERY: 'def',
                  TaskConstants.TASK_TASK_ID: 'def'}]
        tasks_group = route_tasks(self._tenant, 'request', tasks)
        self.assertIsInstance(tasks_group, group)
        self.assertEqual(str(tasks_group.kwargs['tasks'][0]), "tasks.extract.generate_json('testtenant', 'request', 'abc', 'abc', 'abc')")
        self.assertEqual(str(tasks_group.kwargs['tasks'][1]), "tasks.extract.generate_csv('testtenant', 'request', 'def', 'def', 'def')")

    def test_archive_with_encryption(self):
        files = ['test_0.csv', 'test_1.csv', 'test.json']
        with tempfile.TemporaryDirectory() as dir:
            csv_dir = os.path.join(dir, 'csv')
            os.mkdir(csv_dir)
            gpg_file = os.path.join(dir, 'gpg', 'output.gpg')
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
        with tempfile.TemporaryDirectory() as dir:
            csv_dir = os.path.join(dir, 'csv')
            os.mkdir(csv_dir)
            gpg_file = os.path.join(dir, 'gpg', 'output.gpg')
            os.mkdir(os.path.dirname(gpg_file))
            for file in files:
                with open(os.path.join(csv_dir, file), 'a') as f:
                    f.write(file)

            request_id = '1'
            recipients = 'nobody@amplify.com'
            result = archive_with_encryption.apply(args=[request_id, recipients, gpg_file, csv_dir])
            self.assertRaises(ExtractionError, result.get)

    def test_remote_copy(self):
        request_id = '1'
        tenant = 'es'
        gatekeeper = 'foo'
        sftp_info = '127.0.0.2'
        with tempfile.TemporaryDirectory() as dir:
            src_file_name = os.path.join(dir, 'src.txt')
            open(src_file_name, 'w').close()
            result = remote_copy.apply(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info])
            self.assertRaises(ExtractionError, result.get)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
