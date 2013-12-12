"""
Created on Oct 21, 2013

Unit test for configure_sftp_groups.py
"""
from sftp.src import configure_sftp_groups

__author__ = 'sravi'

import unittest


class TestConfigureSFTPGroups(unittest.TestCase):

    def setUp(self):
        self.test_sftp_conf = {
            'sftp_home': '/tmp',
            'sftp_base_dir': 'sftp',
            'sftp_arrivals_dir': 'arrivals',
            'sftp_departures_dir': 'departures',
            'group': 'edwaredataadmin',
            'roles': ['testgrp1', 'testgrp2']
        }

        self.test_invalid_sftp_conf = {
            'sftp_home': '/tmp',
            'sftp_base_dir': 'sftp',
            'sftp_arrivals_dir': 'arrivals',
            'group': 'edwaredataadmin',
            'sftp_departures_dir': 'departures',
            'roles': [None, '']
        }

    def tearDown(self):
        pass

    def test__initialize_valid_sftp_groups(self):
        configure_sftp_groups.initialize(self.test_sftp_conf)
        # the initialize groups only works on linux based machines
        group = self.test_sftp_conf['group']
        self.assertFalse(configure_sftp_groups._group_exists(group))

    def test__initialize_invalid_sftp_groups(self):

        configure_sftp_groups.initialize(self.test_invalid_sftp_conf)
        # the initialize groups only works on linux based machines
        group = self.test_sftp_conf['group']
        self.assertFalse(configure_sftp_groups._group_exists(group))

    def test__cleanup_sftp_groups(self):
        configure_sftp_groups.cleanup(self.test_sftp_conf)
        # the cleanup groups only works on linux based machines
        group = self.test_sftp_conf['group']
        self.assertFalse(configure_sftp_groups._group_exists(group))
