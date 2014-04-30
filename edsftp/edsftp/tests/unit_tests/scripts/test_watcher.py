__author__ = 'sravi'

import unittest
import shutil
import tempfile
import os
import time
from edsftp.scripts.watcher import FileSync


class TestWatcher(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        self.pattern = '*.gpg'
        FileSync.source_dir = self.source_dir
        FileSync.dest_dir = self.dest_dir
        FileSync.pattern = self.pattern
        self.test_sync = FileSync()

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.dest_dir)

    def setUp(self):
        self.test_sync.clear_file_stats()
        self.tmp_dir_1 = tempfile.mkdtemp(dir=self.source_dir)
        self.tmp_dir_2 = tempfile.mkdtemp(dir=self.source_dir)
        self.test_file_1 = tempfile.NamedTemporaryFile(delete=False, suffix=self.pattern,
                                                       prefix='test_file_1', dir=self.tmp_dir_1)
        self.test_file_2 = tempfile.NamedTemporaryFile(delete=False, suffix=self.pattern,
                                                       prefix='test_file_2', dir=self.tmp_dir_2)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir_1, ignore_errors=True)
        shutil.rmtree(self.tmp_dir_2, ignore_errors=True)

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
        self.test_sync.watch_and_filter_files_by_stats_changes()
        self.test_file_1.write(b"test\n")
        self.test_file_1.flush()
        time.sleep(10)
        self.assertEqual(self.test_sync.get_file_stats(), {self.test_file_2.name: 0})
