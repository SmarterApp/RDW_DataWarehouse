__author__ = 'sravi'

import unittest
import shutil
import tempfile
import time
import os
from edcore.watch.util import FileUtil
from edcore.tests.watch.common_test_utils import get_file_hash, write_something_to_a_blank_file, create_checksum_file


class TestUtil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.tmp_dir_1 = tempfile.mkdtemp(prefix='tmp_1')
        self.test_file_1 = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir_1, ignore_errors=True)

    def test_get_file_stat_for_non_empty_file(self):
        file_size = FileUtil.get_file_stat(self.test_file_1)[0]
        self.assertEqual(file_size, 5)

    def test_get_file_stat_for_empty_file(self):
        test_file = tempfile.NamedTemporaryFile(dir=self.tmp_dir_1, delete=True)
        self.assertEqual(FileUtil.get_file_stat(test_file.name)[0], 0)

    def test_get_file_stat_for_invalid_file(self):
        self.assertIsNone(FileUtil.get_file_stat('/tmp/xyz.gpg'))

    def test_get_complement_file_name(self):
        self.assertEqual(FileUtil.get_complement_file_name(self.test_file_1), self.test_file_1 + ".done")
        self.assertEqual(FileUtil.get_complement_file_name(self.test_file_1 + ".done"), self.test_file_1)

    def test_file_contains_hash(self):
        hex_digest, digest = get_file_hash(self.test_file_1)
        check_sum_file_path = create_checksum_file(self.test_file_1)
        self.assertTrue(FileUtil.file_contains_hash(check_sum_file_path, hex_digest))

    def test_get_updated_stats(self):
        test_file = tempfile.NamedTemporaryFile(dir=self.tmp_dir_1, delete=True)
        self.assertEqual(FileUtil.get_file_stat(test_file.name)[0], 0)
        test_file.write(b"test\n")
        test_file.flush()
        self.assertEqual(FileUtil.get_file_stat(test_file.name)[0], 5)

    def test_get_file_tenant_and_user_name(self):
        self.assertEqual(FileUtil.get_file_tenant_and_user_name(
            '/opt/edware/home/landing/arrivals/ca/ca_user1/file_drop/xyz.gz.gpg',
            '/opt/edware/home/landing/arrivals'), ('ca', 'ca_user1'))
        self.assertEqual(FileUtil.get_file_tenant_and_user_name(
            '/opt/edware/home/landing/arrivals/ca/ca_user1/file_drop/xyz.gz.gpg',
            '/opt/edware/home/landing/arrivals/ca'), (None, None))
        self.assertEqual(FileUtil.get_file_tenant_and_user_name(
            '/opt/edware/home/landing/arrivals/ca/ca_user1/xyz.gz.gpg',
            '/opt/edware/home/landing/arrivals'), (None, None))
        self.assertEqual(FileUtil.get_file_tenant_and_user_name(
            '/opt/edware/home/landing/arrivals/ca/ca_user1/file_drop/xyz.gz.gpg',
            '/tmp'), (None, None))
        self.assertEqual(FileUtil.get_file_tenant_and_user_name(
            '/opt/edware/home/landing/arrivals/ca/xyz.gz.gpg',
            '/opt/edware/home/landing/arrivals'), (None, None))

    def test_get_file_last_modified_time_for_invalid_file(self):
        self.assertIsNone(FileUtil.get_file_last_modified_time('/tmp/xyz.gpg'))

    def test_get_file_last_modified_time_for_valid_file(self):
        test_file = tempfile.NamedTemporaryFile(dir=self.tmp_dir_1, delete=True)
        file_last_modified_time = FileUtil.get_file_last_modified_time(test_file.name)
        time.sleep(2)
        self.assertTrue(int(time.time() - file_last_modified_time) > 1)

    def test_create_checksum_file(self):
        test_file = tempfile.NamedTemporaryFile(dir=self.tmp_dir_1, delete=True)
        test_file.write(b"test\n")
        test_file.flush()
        FileUtil.create_checksum_file(test_file.name, '715a9aa9257aadb001e1b85c858b0a91')
        self.assertTrue(os.path.exists(test_file.name + '.done'))
        with open(test_file.name + '.done') as f:
            line = f.readline()
            self.assertEqual(line.strip(), '715a9aa9257aadb001e1b85c858b0a91'  + ' ' +  os.path.basename(test_file.name))
