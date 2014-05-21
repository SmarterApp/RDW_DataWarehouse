__author__ = 'sravi'

import unittest
from edcore.watch.constants import WatcherConstants as Const


class TestWatcherConstants(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_watcher_constants(self):
        self.assertEqual(Const.FILE_SYSTEM_SCAN_DELAY, 'file_system_scan_delay')
        self.assertEqual(Const.FILE_STAT_WATCH_INTERVAL, 'file_stat_watch_interval')
        self.assertEqual(Const.FILE_STAT_WATCH_PERIOD, 'file_stat_watch_period')
        self.assertEqual(Const.FILE_PATTERNS_TO_WATCH, 'file_patterns_to_watch')
        self.assertEqual(Const.FILE_CHECKSUM_THRESHOLD_WAIT_PERIOD, 'file_checksum_threshold_wait_period')
        self.assertEqual(Const.CHECKSUM_FILE_EXTENSION, '.done')
        self.assertEqual(Const.SOURCE_DIR, 'source_dir')
        self.assertEqual(Const.DEST_DIR, 'dest_dir')
        self.assertEqual(Const.BASE_DIR, 'base_dir')
