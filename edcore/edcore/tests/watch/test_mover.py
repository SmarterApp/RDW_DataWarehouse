from unittest.mock import patch, call
__author__ = 'sravi'

import unittest
import shutil
import os
import tempfile
from edcore.watch.mover import FileMover
from edcore.tests.watch.common_test_utils import write_something_to_a_blank_file, create_checksum_file
from edcore.watch.constants import MoverConstants as MoverConst, WatcherConstants as WatcherConst


class TestUtil(unittest.TestCase):

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
        conf = {
            'base_dir': self.base_dir,
            'source_dir': self.source_dir,
            'landing_zone_host_name': 'localhost',
            'arrivals_path': 'arrivals',
            'private_key_file': '~/.ssh/id_rsa',
            'sftp_user': 'udl2'
        }
        self.file_mover = FileMover(config=conf)
        self.tmp_dir_1 = tempfile.mkdtemp(prefix='tmp_1')
        self.test_file_1 = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        self.checksum_file_1 = create_checksum_file(self.test_file_1)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir_1, ignore_errors=True)

    def test_move_zero_files(self):
        files_to_move = []
        files_moved = self.file_mover.move_files(files_to_move=files_to_move)
        self.assertEqual(files_moved, 0)

    @patch('edcore.watch.mover.FileMover.move_files_local')
    def test_move_files_with_local(self, mock_move_files_local):
        files_to_move = ['hello']
        self.file_mover.move_files(files_to_move=files_to_move)
        self.assertEqual(1, mock_move_files_local.call_count)
        self.assertEqual(mock_move_files_local.call_args, call(files_to_move))

    @patch('edcore.watch.mover.FileMover.move_files_by_sftp')
    def test_move_files_with_sftp(self, mock_move_files_by_sftp):
        self.file_mover.conf[MoverConst.FILE_MOVE_TYPE] = 'sftp'
        files_to_move = ['hello']
        self.file_mover.move_files(files_to_move=files_to_move)
        self.assertEqual(1, mock_move_files_by_sftp.call_count)
        self.assertEqual(mock_move_files_by_sftp.call_args, call(files_to_move))

    @patch('edcore.watch.mover.FileUtil.get_file_tenant_and_user_name')
    def test_move_files_local(self, mock_get_file_tenant_and_user_name):
        file1 = os.path.join(self.base_dir, '1', '2', '3', 'testfile')
        os.makedirs(os.path.dirname(file1))
        open(file1, 'a').close()
        files_to_move = [file1]
        mock_get_file_tenant_and_user_name.return_value = 'hello', 'world'

        self.file_mover.conf[WatcherConst.STAGING_DIR] = self.base_dir
        moved = self.file_mover.move_files_local(files_to_move)
        self.assertEqual(1, moved)
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, 'hello', 'world', 'testfile')))
