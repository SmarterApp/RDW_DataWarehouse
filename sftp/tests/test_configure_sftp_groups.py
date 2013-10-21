"""
Created on Oct 21, 2013

Unit test for configure_sftp_groups.py
"""

__author__ = 'sravi'

import unittest
import sys

from sftp.src import configure_sftp_groups


class TestConfigureSFTPGroups(unittest.TestCase):

    def setUp(self):
        self.test_sftp_conf = {
            'sftp_home': '/tmp',
            'sftp_base_dir': 'sftp',
            'sftp_arrivals_dir': 'arrivals',
            'sftp_departures_dir': 'departures',
            'groups': ['testgrp1', 'testgrp2']
        }

    def tearDown(self):
        pass

    def test__initialize_sftp_groups(self):
        configure_sftp_groups.initialize(self.test_sftp_conf)
        # the initialize groups only works on linux based machines
        for name in self.test_sftp_conf['groups']:
            if sys.platform == 'linux':
                self.assertTrue(configure_sftp_groups._group_exists(name))
            else:
                self.assertFalse(configure_sftp_groups._group_exists(name))

    def test__cleanup_sftp_groups(self):
        configure_sftp_groups.cleanup(self.test_sftp_conf)
        # the cleanup groups only works on linux based machines
        for name in self.test_sftp_conf['groups']:
            if sys.platform == 'linux':
                self.assertFalse(configure_sftp_groups._group_exists(name))
            else:
                self.assertFalse(configure_sftp_groups._group_exists(name))
