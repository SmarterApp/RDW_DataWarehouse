"""
Created on Oct 21, 2013

Unit test for configure_sftp_groups.py
"""

__author__ = 'sravi'

import unittest
import os
import shutil

from sftp.src import configure_sftp_groups


class TestConfigureSFTPGroups(unittest.TestCase):

    def setUp(self):
        self.test_sftp_conf = {
            'sftp_home': '/tmp',
            'sftp_base_dir': 'sftp',
            'sftp_arrivals_dir': 'arrivals',
            'sftp_departures_dir': 'departures',
            'groups': ['sftparrivals', 'tenantadmin']
        }

    def tearDown(self):
        pass

    def test__create_non_existing_sftp_groups(self):
        configure_sftp_groups.initialize(self.test_sftp_conf)
        self.assertTrue(True)
