__author__ = 'sravi'

import unittest
import shutil
import tempfile
import time
import os
from edsftp.scripts.watcher import FileSync


class TestWatcher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.pattern = '*.gpg'
        self.sftp_base_dir = tempfile.mkdtemp(prefix='sftp_base')
        self.arrivals_dir = tempfile.mkdtemp(prefix='arrivals', dir=self.sftp_base_dir)
        self.arrivals_rsync_dir = tempfile.mkdtemp(prefix='arrivals_rsync', dir=self.sftp_base_dir)
        self.source_dir = os.path.join(self.sftp_base_dir, self.arrivals_dir)
        self.dest_dir = os.path.join(self.sftp_base_dir, self.arrivals_rsync_dir)
        conf = {
            'sftp_base_dir': self.sftp_base_dir,
            'sftp_arrivals_dir': self.arrivals_dir,
            'sftp_arrivals_rsync_dir': self.arrivals_rsync_dir,
            'file_pattern_to_watch': self.pattern,
            'file_stat_watch_internal_in_seconds': 1,
            'file_stat_watch_period_in_seconds': 5,
            'file_system_scan_delay_in_seconds': 3
        }
        self.test_sync = FileSync(conf)
        FileSync.set_conf(conf)
        self.test_sync.clear_file_stats()
        self.tmp_dir_1 = tempfile.mkdtemp(prefix='tmp_1', dir=self.source_dir)
        self.tmp_dir_2 = tempfile.mkdtemp(prefix='tmp_2', dir=self.source_dir)
        self.test_file_1 = tempfile.NamedTemporaryFile(delete=False, suffix=self.pattern,
                                                       prefix='test_file_1', dir=self.tmp_dir_1)
        self.test_file_2 = tempfile.NamedTemporaryFile(delete=False, suffix=self.pattern,
                                                       prefix='test_file_2', dir=self.tmp_dir_2)

    def tearDown(self):
        shutil.rmtree(self.sftp_base_dir, ignore_errors=True)

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
        time.sleep(5)
        stop.set()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0})

    def test_move_files(self):
        self.test_sync.find_all_files()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_1.name: 0, self.test_file_2.name: 0})
        stop = self.test_sync.watch_and_filter_files_by_stats_changes()
        time.sleep(2)
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        time.sleep(5)
        stop.set()
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0})
        files_moved = self.test_sync.move_files()
        self.assertEqual(files_moved, 1)
        self.assertEqual(len(os.listdir(self.dest_dir)), 1)

    def test_find_and_move_files(self):
        files_moved = self.test_sync.find_and_move_files()
        self.assertEqual(files_moved, 2)
        self.assertEqual(len(os.listdir(self.dest_dir)), 2)
