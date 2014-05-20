__author__ = 'sravi'

import unittest
import shutil
import os
import tempfile
from edcore.watch.mover import FileMover
from edcore.tests.watch.common_test_utils import write_something_to_a_blank_file, create_checksum_file


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
