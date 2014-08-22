import os
import unittest
import tempfile
import shutil
import tarfile
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from pyramid import testing
from smarter_score_batcher.trigger.file_monitor import *


class TestFileMonitor(unittest.TestCase):

    def setUp(self):
        self.__workspace = tempfile.mkdtemp()
        self.__staging = tempfile.mkdtemp()
        # setup request
        self.__request = DummyRequest()
        self.__request.method = 'POST'
        # setup settings
        here = os.path.abspath(os.path.dirname(__file__))
        self.gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        self.settings = {
            'smarter_score_batcher.gpg.keyserver': None,
            'smarter_score_batcher.gpg.homedir': self.gpg_home,
            'smarter_score_batcher.gpg.public_key.cat': 'kswimberly@amplify.com',
            'smarter_score_batcher.gpg.path': 'gpg',
            'smarter_score_batcher.base_dir.working': self.__workspace,
            'smarter_score_batcher.base_dir.staging': self.__staging
        }
        # setup registr
        reg = Registry()
        reg.settings = self.settings
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self._prepare_testing_files()

    def _prepare_testing_files(self):
        '''create test file under a temporary directory with structure like /tmp/test_1/test_1.{csv, json}'''
        assessment_id = "test_1"
        files = ['test_1.csv', 'test_1.json']
        # prepare path
        self.temp_directory = os.path.join(self.__workspace, assessment_id)
        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory, 0o700)
        # prepare testing files
        for file in files:
            with open(os.path.join(self.temp_directory, file), 'a') as f:
                f.write(file)

    def tearDown(self):
        if path.exists(self.__workspace):
            shutil.rmtree(self.__workspace)
        if path.exists(self.__staging):
            shutil.rmtree(self.__staging)
        testing.tearDown()

    def test_list_assessment_files(self):
        base_dir = self.__workspace
        filenames = list_assessments(base_dir)
        expected = {os.path.join(base_dir, 'test_1')}
        self.assertEqual(filenames, expected, "list_assessment_files() should return a list of csv files")

    def test_compress(self):
        fixture_len = 10240
        with FileEncryption(self.temp_directory) as fl:
            data_directory = fl._move_to_tempdir()
            tar = fl._compress(data_directory)
            self.assertTrue(path.exists(tar), "compress funcion should create a tar file")
            self.assertTrue(tarfile.is_tarfile(tar), "compress funcion should create a tar file")
            self.assertEqual(os.path.getsize(tar), fixture_len)

    def test_encrypted_archive_files(self):
        with FileEncryption(self.temp_directory) as fl:
            outputfile = fl.encrypt(self.settings)
            self.assertTrue(os.path.isfile(outputfile))
            self.assertNotEqual(os.path.getsize(outputfile), 0)

    def test_move_to_tempdir(self):
        with FileEncryption(self.temp_directory) as fl:
            target_dir = fl._move_to_tempdir()
            self.assertTrue(path.exists(target_dir), "should create a temporary directory for JSON and CSV files")
            expected_csv = path.join(target_dir, "test_1.csv")
            self.assertTrue(path.isfile(expected_csv), "CSV file should be moved to temporary directory")
            old_csv = path.join(self.temp_directory, "test_1.csv")
            self.assertFalse(path.exists(old_csv), "Should remove csv file from workspace")

    def test_move_files(self):
        staging_dir = self.__staging
        expected_file = path.join(staging_dir, "test_1.tar.gpg")
        with FileEncryption(self.temp_directory) as fl:
            outputfile = fl.encrypt(self.settings)
            fl.move_files(outputfile, staging_dir)
            self.assertTrue(path.isfile(expected_file), "should move gpg file to staging directory")
            self.assertFalse(path.exists(expected_file + ".partial"), "should remove transient file after file transfer complete")

    def test_context_management(self):
        with FileEncryption(self.temp_directory):
            temp_dir = path.join(self.temp_directory, ".tmp")
            self.assertTrue(path.exists(temp_dir), "should create a temporary directory for file manipulation")
        self.assertFalse(path.exists(temp_dir), "should remove the temporary directory that is created for file manipulation")

    def test_move_to_staging(self):
        move_to_staging(self.settings)
        staging_dir = self.__staging
        expected_file = path.join(staging_dir, "test_1.tar.gpg")
        self.assertTrue(path.exists(expected_file), "should create gpg file under staging directory")
        working_dir = self.__workspace
        unexpected_dir = path.join(working_dir, "test_1")
        self.assertFalse(path.exists(unexpected_dir), "working directory should be cleaned up after assessments being moved")
