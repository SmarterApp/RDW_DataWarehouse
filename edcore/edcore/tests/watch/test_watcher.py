__author__ = 'sravi'

import unittest
import shutil
import tempfile
import time
import os
import hashlib
from edcore.watch.watcher import Watcher


class TestWatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.pattern = ['*.gpg', '*.gpg.done']
        self.base_dir = tempfile.mkdtemp(prefix='base')
        self.source_dir = tempfile.mkdtemp(prefix='arrivals', dir=self.base_dir)
        self.dest_dir = tempfile.mkdtemp(prefix='arrivals_sync', dir=self.base_dir)
        self.source_path = os.path.join(self.base_dir, self.source_dir)
        self.dest_path = os.path.join(self.base_dir, self.dest_dir)
        self.conf = {
            'base_dir': self.base_dir,
            'source_dir': self.source_dir,
            'dest_dir': self.dest_dir,
            'file_patterns_to_watch': self.pattern,
            'file_stat_watch_internal_in_seconds': 1,
            'file_stat_watch_period_in_seconds': 3,
            'file_system_scan_delay_in_seconds': 2
        }
        self.test_sync = Watcher()
        self.test_sync.set_conf(self.conf)
        self.tmp_dir_1 = tempfile.mkdtemp(prefix='tmp_1', dir=self.source_path)
        self.tmp_dir_2 = tempfile.mkdtemp(prefix='tmp_2', dir=self.source_path)
        self.test_file_1 = tempfile.NamedTemporaryFile(delete=False, suffix=self.pattern[0],
                                                       prefix='test_file_1', dir=self.tmp_dir_1)
        self.test_file_2 = tempfile.NamedTemporaryFile(delete=False, suffix=self.pattern[0],
                                                       prefix='test_file_2', dir=self.tmp_dir_2)

    def tearDown(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)

    def test_clear_file_stats(self):
        self.test_sync.clear_file_stats()
        self.assertEqual(self.test_sync.get_file_stats(), {})

    def test_get_file_stat(self):
        test_file = tempfile.NamedTemporaryFile(delete=True)
        self.assertEqual(self.test_sync.get_file_stat(test_file.name), 0)

    def test_get_updated_stats(self):
        test_file = tempfile.NamedTemporaryFile(delete=True)
        self.assertEqual(self.test_sync.get_file_stat(test_file.name), 0)
        test_file.write(b"test\n")
        test_file.flush()
        self.assertEqual(self.test_sync.get_file_stat(test_file.name), 5)

    def test_find_all_files(self):
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0})

    def test_get_updated_file_stats(self):
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0})
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        self.assertEqual(self.test_sync.get_updated_file_stats(), {self.test_file_1.name: 5, self.test_file_2.name: 0})

    def test_watch_files(self):
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0})
        stop = self.test_sync.watch_and_filter_files_by_stats_changes()
        time.sleep(2)
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        time.sleep(self.conf['file_stat_watch_period_in_seconds'])
        stop.set()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0})

    def test_move_files(self):
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0})
        stop = self.test_sync.watch_and_filter_files_by_stats_changes()
        time.sleep(2)
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        time.sleep(self.conf['file_stat_watch_period_in_seconds'])
        stop.set()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0})
        files_moved = self.test_sync.move_files()
        self.assertEqual(files_moved, 1)
        self.assertEqual(len(os.listdir(self.dest_path)), 1)

    def test_watch_and_move_files(self):
        files_moved = self.test_sync.watch_and_move_files()
        self.assertEqual(files_moved, 2)
        self.assertEqual(len(os.listdir(self.dest_path)), 2)

    def _get_file_hash(self, test_file_path):
        with open(test_file_path, 'rb') as f:
            md5 = hashlib.md5()
            for buf in iter(lambda: f.read(md5.block_size), b''):
                md5.update(buf)
            return md5.hexdigest(), md5.digest()

    def _write_something_to_a_blank_file(self):
        with tempfile.NamedTemporaryFile(delete=False, dir=self.tmp_dir_1, prefix='source', suffix=self.pattern[0]) as test_file:
            self.assertEqual(self.test_sync.get_file_stat(test_file.name), 0)
            test_file.write(b"test\n")
            test_file.flush()
            return test_file.name

    def _create_checksum_file(self, source_file_path, valid_check_sum=True):
        with open(source_file_path + '.done', 'wb') as checksum_file:
            self.assertEqual(self.test_sync.get_file_stat(checksum_file.name), 0)
            hex_digest, _ = self._get_file_hash(source_file_path)
            if not valid_check_sum:
                checksum_file.write(bytes("MD5 =" + 'aaavfi385etegdg83kdgd', 'UTF-8'))
            else:
                checksum_file.write(bytes("MD5 =" + hex_digest, 'UTF-8'))
            checksum_file.flush()
            return checksum_file.name

    def test_md5_for_file(self):
        test_file_path = self._write_something_to_a_blank_file()
        hex_digest, digest = self._get_file_hash(test_file_path)
        self.assertEqual(self.test_sync.md5_for_file(test_file_path), hex_digest)
        self.assertEqual(self.test_sync.md5_for_file(test_file_path, block_size=64, hex_digest=True), hex_digest)
        self.assertEqual(self.test_sync.md5_for_file(test_file_path, hex_digest=False), digest)
        self.assertEqual(self.test_sync.get_file_hash(test_file_path), hex_digest)

    def test_file_contains_hash(self):
        test_file_path = self._write_something_to_a_blank_file()
        hex_digest, digest = self._get_file_hash(test_file_path)
        check_sum_file_path = self._create_checksum_file(test_file_path)
        self.assertTrue(self.test_sync.file_contains_hash(check_sum_file_path, hex_digest))

    def test_valid_check_sum_with_no_checksum_file(self):
        test_file_path = self._write_something_to_a_blank_file()
        self.assertFalse(self.test_sync.valid_check_sum(test_file_path))

    def test_valid_check_sum_with_valid_checksum_file(self):
        test_file_path = self._write_something_to_a_blank_file()
        _ = self._create_checksum_file(test_file_path)
        self.assertTrue(self.test_sync.valid_check_sum(test_file_path))

    def test_valid_check_sum_with_invalid_checksum_file(self):
        test_file_path = self._write_something_to_a_blank_file()
        _ = self._create_checksum_file(test_file_path, valid_check_sum=False)
        self.assertFalse(self.test_sync.valid_check_sum(test_file_path))

    def test_get_complement_file_name(self):
        self.assertEqual(self.test_sync.get_complement_file_name(self.test_file_1.name), self.test_file_1.name + ".done")
        self.assertEqual(self.test_sync.get_complement_file_name(self.test_file_1.name + ".done"), self.test_file_1.name)

    def test_remove_files_from_dict(self):
        test_file_path = self._write_something_to_a_blank_file()
        checksum_file_path = self._create_checksum_file(test_file_path)
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0,
                                                           test_file_path: 5, checksum_file_path: 37})
        self.test_sync.remove_file_from_dict(self.test_file_1.name)
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0, test_file_path: 5,
                                                           checksum_file_path: 37})
        self.test_sync.remove_file_pair_from_dict(test_file_path)
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0})
        self.test_sync.remove_file_pair_from_dict(self.test_file_2.name)
        self.assertEqual(self.test_sync.get_file_stats(), {})

    def test_filter_files_for_digest_mismatch(self):
        test_file_3_path = self._write_something_to_a_blank_file()
        checksum_file_3_path = self._create_checksum_file(test_file_3_path)
        test_file_4_path = self._write_something_to_a_blank_file()
        checksum_file_4_path = self._create_checksum_file(test_file_4_path)
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0,
                                                           test_file_3_path: 5, checksum_file_3_path: 37,
                                                           test_file_4_path: 5, checksum_file_4_path: 37})
        self.test_sync.filter_files_for_digest_mismatch()
        self.assertEqual(self.test_sync.get_file_stats(), {test_file_3_path: 5, checksum_file_3_path: 37,
                                                           test_file_4_path: 5, checksum_file_4_path: 37})
        test_file_5_path = self._write_something_to_a_blank_file()
        checksum_file_5_path = self._create_checksum_file(test_file_5_path, valid_check_sum=False)
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0,
                                                           test_file_3_path: 5, checksum_file_3_path: 37,
                                                           test_file_4_path: 5, checksum_file_4_path: 37,
                                                           test_file_5_path: 5, checksum_file_5_path: 26})
        self.test_sync.filter_files_for_digest_mismatch()
        self.assertEqual(self.test_sync.get_file_stats(), {test_file_3_path: 5, checksum_file_3_path: 37,
                                                           test_file_4_path: 5, checksum_file_4_path: 37})

    def test_filter_files_for_digest_mismatch(self):
        test_file_3_path = self._write_something_to_a_blank_file()
        checksum_file_3_path = self._create_checksum_file(test_file_3_path)
        test_file_4_path = self._write_something_to_a_blank_file()
        checksum_file_4_path = self._create_checksum_file(test_file_4_path)
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0,
                                                           test_file_3_path: 5, checksum_file_3_path: 37,
                                                           test_file_4_path: 5, checksum_file_4_path: 37})
        self.test_sync.filter_checksum_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0,
                                                           test_file_3_path: 5, test_file_4_path: 5})
