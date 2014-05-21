__author__ = 'sravi'

import unittest
import shutil
import tempfile
import time
import os
from edcore.tests.watch.common_test_utils import write_something_to_a_blank_file, create_checksum_file
from edcore.watch.file_hasher import MD5Hasher
from edcore.watch.watcher import FileWatcher


class TestWatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.pattern = "['*.gpg', '*.gpg.done']"
        self.base_dir = tempfile.mkdtemp(prefix='base')
        self.source_dir = tempfile.mkdtemp(prefix='arrivals', dir=self.base_dir)
        self.source_path = os.path.join(self.base_dir, self.source_dir)
        self.conf = {
            'base_dir': self.base_dir,
            'source_dir': self.source_dir,
            'file_patterns_to_watch': self.pattern,
            'file_stat_watch_interval': 1,
            'file_stat_watch_period': 6,
            'file_checksum_threshold_wait_period': 4,
            'file_system_scan_delay': 2
        }
        self.test_sync = FileWatcher(self.conf)
        self.test_hasher = MD5Hasher()
        self.tmp_dir_1 = tempfile.mkdtemp(prefix='tmp_1', dir=self.source_path)
        self.tmp_dir_2 = tempfile.mkdtemp(prefix='tmp_2', dir=self.source_path)
        self.test_file_1 = tempfile.NamedTemporaryFile(delete=False, suffix='*.gpg',
                                                       prefix='test_file_1', dir=self.tmp_dir_1)
        self.test_file_2 = tempfile.NamedTemporaryFile(delete=False, suffix='*.gpg',
                                                       prefix='test_file_2', dir=self.tmp_dir_2)

    def _without_timestamps(self, file_stats):
        dict_without_timestamps = {}
        for file in file_stats.keys():
            dict_without_timestamps[file] = file_stats[file][0]
        return dict_without_timestamps

    def tearDown(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)

    def test_clear_file_stats(self):
        self.test_sync.clear_file_stats()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {})

    def test_find_all_files(self):
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0})

    def test_add_file_to_snapshot(self):
        self.assertEqual(len(self.test_sync.get_file_stats().keys()), 0)
        self.test_sync.add_file_to_snapshot(self.test_file_1.name)
        self.assertEqual(len(self.test_sync.get_file_stats().keys()), 1)
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {self.test_file_1.name: 0})

    def test_get_updated_file_stats(self):
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0})
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        self.assertEqual(self._without_timestamps(self.test_sync.get_updated_file_stats()), {
            self.test_file_1.name: 5, self.test_file_2.name: 0})

    def test_watch_files_1(self):
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0})
        stop = self.test_sync.watch_and_filter_files_by_stats_changes()
        time.sleep(2)
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        time.sleep(self.conf['file_stat_watch_period'])
        stop.set()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {self.test_file_2.name: 0})

    def test_watch_files_2(self):
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0})
        stop = self.test_sync.watch_and_filter_files_by_stats_changes()
        time.sleep(2)
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        time.sleep(self.conf['file_stat_watch_period'])
        stop.set()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {self.test_file_2.name: 0})

    def test_valid_check_sum_with_no_checksum_file(self):
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        self.assertFalse(self.test_sync.valid_check_sum(test_file_path))

    def test_valid_check_sum_with_no_checksum_file_for_shorter_time(self):
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        time.sleep(2)
        self.assertFalse(self.test_sync.valid_check_sum(test_file_path))

    def test_valid_check_sum_with_no_checksum_file_for_longer_time(self):
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        time.sleep(5)
        self.assertFalse(self.test_sync.valid_check_sum(test_file_path))

    def test_valid_check_sum_with_valid_checksum_file(self):
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        _ = create_checksum_file(test_file_path)
        self.assertTrue(self.test_sync.valid_check_sum(test_file_path))

    def test_valid_check_sum_with_invalid_checksum_file(self):
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        _ = create_checksum_file(test_file_path, valid_check_sum=False)
        self.assertFalse(self.test_sync.valid_check_sum(test_file_path))

    def test_remove_files_from_dict(self):
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_path = create_checksum_file(test_file_path)
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0,
            test_file_path: 5, checksum_file_path: 37})
        self.test_sync.remove_file_from_dict(self.test_file_1.name)
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_2.name: 0, test_file_path: 5, checksum_file_path: 37})
        self.test_sync.remove_file_pair_from_dict(test_file_path)
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {self.test_file_2.name: 0})
        self.test_sync.remove_file_pair_from_dict(self.test_file_2.name)
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {})

    def test_filter_files_for_digest_mismatch_1(self):
        test_file_3_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_3_path = create_checksum_file(test_file_3_path)
        test_file_4_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_4_path = create_checksum_file(test_file_4_path)
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()),
                         {self.test_file_1.name: 0, self.test_file_2.name: 0,
                          test_file_3_path: 5, checksum_file_3_path: 37,
                          test_file_4_path: 5, checksum_file_4_path: 37})
        self.test_sync.filter_files_for_digest_mismatch()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()),
                         {test_file_3_path: 5, checksum_file_3_path: 37,
                          test_file_4_path: 5, checksum_file_4_path: 37})
        test_file_5_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_5_path = create_checksum_file(test_file_5_path, valid_check_sum=False)
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0,
            test_file_3_path: 5, checksum_file_3_path: 37,
            test_file_4_path: 5, checksum_file_4_path: 37,
            test_file_5_path: 5, checksum_file_5_path: 26})
        self.test_sync.filter_files_for_digest_mismatch()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            test_file_3_path: 5, checksum_file_3_path: 37,
            test_file_4_path: 5, checksum_file_4_path: 37})

    def test_filter_files_for_digest_mismatch_2(self):
        test_file_3_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_3_path = create_checksum_file(test_file_3_path)
        test_file_4_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_4_path = create_checksum_file(test_file_4_path)
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0,
            test_file_3_path: 5, checksum_file_3_path: 37,
            test_file_4_path: 5, checksum_file_4_path: 37})
        self.test_sync.filter_checksum_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()), {
            self.test_file_1.name: 0, self.test_file_2.name: 0,
            test_file_3_path: 5, test_file_4_path: 5})

    def test_handle_missing_checksum_files_when_user_forgets_to_drop_checksum_file(self):
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()),
                         {self.test_file_1.name: 0, self.test_file_2.name: 0})
        self.test_sync.handle_missing_checksum_files()
        self.assertEqual(len(self._without_timestamps(self.test_sync.get_file_stats()).keys()), 4)
        self.assertEqual(set(self._without_timestamps(self.test_sync.get_file_stats()).keys()),
                         {self.test_file_1.name, self.test_file_2.name,
                          self.test_file_1.name + '.done', self.test_file_2.name + '.done'})

    def test_handle_missing_checksum_files_with_both_missing_and_avail(self):
        test_file_3_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        checksum_file_3_path = create_checksum_file(test_file_3_path)
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()),
                         {self.test_file_1.name: 0, self.test_file_2.name: 0,
                          test_file_3_path: 5, checksum_file_3_path: 37})
        self.test_sync.handle_missing_checksum_files()
        self.assertEqual(len(self._without_timestamps(self.test_sync.get_file_stats()).keys()), 6)
        self.assertEqual(set(self._without_timestamps(self.test_sync.get_file_stats()).keys()),
                         {self.test_file_1.name, self.test_file_2.name, test_file_3_path,
                          self.test_file_1.name + '.done', self.test_file_2.name + '.done', test_file_3_path + '.done'})

    def test_handle_missing_checksum_files_when_user_drops_checksum_file_during_a_watch_period(self):
        test_file_3_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        self.test_sync.find_all_files()
        self.assertEqual(self._without_timestamps(self.test_sync.get_file_stats()),
                         {self.test_file_1.name: 0, self.test_file_2.name: 0,
                          test_file_3_path: 5})
        # user drops the checksum file after a snapshot is taken
        checksum_file_3_path = create_checksum_file(test_file_3_path)
        self.test_sync.watch_files()
        self.test_sync.handle_missing_checksum_files()
        self.assertEqual(len(self._without_timestamps(self.test_sync.get_file_stats()).keys()), 4)
        self.assertEqual(set(self._without_timestamps(self.test_sync.get_file_stats()).keys()),
                         {self.test_file_1.name, self.test_file_2.name,
                          self.test_file_1.name + '.done', self.test_file_2.name + '.done'})
