"""
Created on Oct 18, 2013

Unit test for initialize_sftp_zone.py
"""

__author__ = 'sravi'

import unittest
import os
import subprocess

from sftp.src import initialize_sftp_zone
from sftp.src.sftp_config import sftp_conf


class TestInitializeSFTPZone(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__create_non_existing_path_as_root(self):
        test_path = "/tmp/sftp"
        initialize_sftp_zone._create_path_as_root(test_path)
        self.assertTrue(os.path.exists(test_path))

        #cleanup
        command_opts = ['sudo', 'rmdir', test_path]
        subprocess.call(command_opts)
        self.assertFalse(os.path.exists(test_path))

    def test__create_existing_path_as_root1(self):
        test_path = "/tmp/sftp"
        initialize_sftp_zone._create_path_as_root(test_path)
        self.assertTrue(os.path.exists(test_path))

        # try creating again
        initialize_sftp_zone._create_path_as_root(test_path)
        self.assertTrue(os.path.exists(test_path))
        #cleanup
        command_opts = ['sudo', 'rmdir', test_path]
        subprocess.call(command_opts)
        self.assertFalse(os.path.exists(test_path))
