# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import tempfile
import tarfile
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from pyramid import testing
import os
import shutil
from smarter_score_batcher.trigger.file_monitor import FileEncryption, move_to_staging, prepare_assessment_dir
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite
from smarter_score_batcher.tests.processing.utils import read_data
from smarter_score_batcher.processing.file_processor import process_assessment_data
from smarter_score_batcher.utils.meta import extract_meta_names
from smarter_score_batcher.error.exceptions import TSBSecurityException


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class TestFileMonitor(Unittest_with_tsb_sqlite):

    def setUp(self):
        self.__workspace = tempfile.mkdtemp()
        self.__staging = tempfile.mkdtemp()
        # setup request
        self.__request = DummyRequest()
        self.__request.method = 'POST'
        # setup settings
        # use the one for UDL
        here = os.path.abspath(os.path.dirname(__file__))
        self.gpg_home = os.path.abspath(os.path.join(here, '..', '..', '..', '..', 'config', 'gpg'))
        self.settings = {
            'smarter_score_batcher.gpg.keyserver': None,
            'smarter_score_batcher.gpg.homedir': self.gpg_home,
            'smarter_score_batcher.gpg.public_key.ca': 'sbac_data_provider@sbac.com',
            'smarter_score_batcher.gpg.public_key.cat': 'sbac_data_provider@sbac.com',
            'smarter_score_batcher.gpg.public_key.fish': 'sbac_data_provider@sbac.com',
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
        '''create test file under a temporary directory with structure like /tmp/{tenant}/{asmt_id}/{asmt_id}.{csv, json}'''
        self.test_tenant = 'CA'
        self.asmt_guid = 'SBAC-FT-SomeDescription-ELA-7'
        self.test_asmt = "test_1"
        self.test_files = ['test_1.csv', 'test_1.json']
        self.test_tenants = ['cat', 'fish']
        # prepare path
        for tenant in self.test_tenants:
            self.temp_directory = os.path.join(self.__workspace, tenant, self.test_asmt)
            if not os.path.exists(self.temp_directory):
                os.makedirs(self.temp_directory, 0o700)
            # prepare testing files
            for file in self.test_files:
                with open(os.path.join(self.temp_directory, file), 'a') as f:
                    f.write(file)
        # prepare data in database
        data = read_data("assessment.xml")
        meta = extract_meta_names(data)
        root = ET.fromstring(data)
        try:
            process_assessment_data(root, meta)
        except Exception:
            pass

    def tearDown(self):
        super().tearDown()
        if os.path.exists(self.__workspace):
            shutil.rmtree(self.__workspace)
        if os.path.exists(self.__staging):
            shutil.rmtree(self.__staging)
        testing.tearDown()

    def test_prepare_assessment_dir_path_traversal(self):
        with tempfile.TemporaryDirectory() as base_dir:
            self.assertRaises(TSBSecurityException, prepare_assessment_dir, base_dir, '..', 'CDE')

    def test_prepare_assessment(self):
        with tempfile.TemporaryDirectory() as base_dir:
            directory = prepare_assessment_dir(base_dir, 'state_code', 'asmt_id')
            self.assertEqual(os.path.join(base_dir, 'state_code', 'asmt_id'), directory)

    def test_compress(self):
        with FileEncryption(self.temp_directory, self.test_tenant, self.asmt_guid) as fl:
            data_directory = fl.save_to_tempdir()
            tar = fl.archive_to_tar(data_directory)
            self.assertTrue(os.path.exists(tar), "compress funcion should create a tar file")
            self.assertTrue(tarfile.is_tarfile(tar), "compress funcion should create a tar file")
            self.assertNotEqual(os.path.getsize(tar), 0)

    def test_encrypted_archive_files(self):
        with FileEncryption(self.temp_directory, self.test_tenant, self.asmt_guid) as fl:
            data_directory = fl.save_to_tempdir()
            tar = fl.archive_to_tar(data_directory)
            outputfile = fl.encrypt(tar, self.settings)
            self.assertTrue(os.path.isfile(outputfile))
            self.assertNotEqual(os.path.getsize(outputfile), 0)

    def test_move_to_tempdir(self):
        with FileEncryption(self.temp_directory, self.test_tenant, self.asmt_guid) as fl:
            target_dir = fl.save_to_tempdir()
            self.assertTrue(os.path.exists(target_dir), "should create a temporary directory for JSON and CSV files")
            expected_csv = os.path.join(target_dir, "SBAC-FT-SomeDescription-ELA-7.csv")
            self.assertTrue(os.path.isfile(expected_csv), "CSV file should be moved to temporary directory")

    def test_move_files(self):
        staging_dir = self.__staging
        with FileEncryption(self.temp_directory, self.test_tenant, self.asmt_guid) as fl:
            data_directory = fl.save_to_tempdir()
            tar = fl.archive_to_tar(data_directory)
            outputfile = fl.encrypt(tar, self.settings)
            dest_file = fl.move_files(outputfile, staging_dir)
            self.assertTrue(os.path.isfile(dest_file), "should move gpg file to staging directory")
            self.assertFalse(os.path.exists(dest_file + ".partial"), "should remove transient file after file transfer complete")
            self.assertTrue(os.path.isfile(dest_file + ".done"), "should move checksum file to staging directory")

    def test_context_management(self):
        with FileEncryption(self.temp_directory, self.test_tenant, self.asmt_guid):
            temp_dir = os.path.join(self.temp_directory, "ca", self.asmt_guid)
            self.assertTrue(os.path.exists(temp_dir), "should create a temporary directory for file manipulation")
        self.assertFalse(os.path.exists(temp_dir), "should remove the temporary directory that is created for file manipulation")

    def test_move_to_staging(self):
        move_to_staging(self.settings)
        staging_dir = self.__staging
        working_dir = self.__workspace
        unexpected_dir = os.path.join(working_dir, "test_1")
        self.assertFalse(os.path.exists(unexpected_dir), "working directory should be cleaned up after assessments being moved")

    def test_create_checksum(self):
        # use test_1.csv to test checksum
        csv_file_path = os.path.join(self.temp_directory, "test_1.csv")
        with FileEncryption(self.temp_directory, self.test_tenant, self.asmt_guid) as fl:
            checksum = fl._create_checksum(csv_file_path)
            self.assertIsNotNone(checksum, "should create a checksum file")
            self.assertTrue(os.path.isfile(checksum), "should create a checksum file")
