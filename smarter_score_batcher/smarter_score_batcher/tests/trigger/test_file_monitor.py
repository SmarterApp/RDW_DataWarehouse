import os
import unittest
import tempfile
import shutil
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.trigger.file_monitor import *


class TestFileMonitor(unittest.TestCase):

    def setUp(self):
        self.__tempfolder = tempfile.TemporaryDirectory()
        # setup request
        self.__request = DummyRequest()
        self.__request.method = 'POST'
        # setup settings
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        self.settings = {
            # TODO: gpg key definitions?
            'extract.gpg.keyserver': None,
            'extract.gpg.homedir': gpg_home,
            'extract.gpg.public_key.cat': 'kswimberly@amplify.com',
            'extract.gpg.path': 'gpg',
            'smarter_score_batcher.base_dir': self.__tempfolder.name
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
        self.temp_dir_root = tempfile.mkdtemp()
        # prepare path
        temp_directory = os.path.join(self.temp_dir_root, assessment_id)
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory, 0o700)
        # prepare testing files
        for file in files:
            with open(os.path.join(temp_directory, file), 'a') as f:
                f.write(file)

    def tearDown(self):
        # clean up temporary directory
        shutil.rmtree(self.temp_dir_root)
        testing.tearDown()

    def test_list_assessment_files(self):
        base_dir = self.temp_dir_root
        filenames = list_assessment_files(base_dir)
        expected = {'test_1'}
        self.assertEqual(filenames, expected, "list_assessment_files() should return a list of csv files")

    def test_copy_files(self):
        # TODO:
        copy_files(self.settings)
        pass

    def test_compress(self):
        fixture_len = 241
        assessment_id = 'test_1'
        with FileEncryption(self.temp_dir_root, assessment_id) as fl:
            tar = fl.compress()
            self.assertEqual(os.path.getsize(tar), fixture_len)

    def test_encrypted_archive_files(self):
        fixture_len = 695
        assessment_id = 'test_1'
        with FileEncryption(self.temp_dir_root, assessment_id) as fl:
            outputfile = fl.encrypt(self.settings)
            self.assertTrue(os.path.isfile(outputfile))
            self.assertEqual(os.path.getsize(outputfile), fixture_len)
