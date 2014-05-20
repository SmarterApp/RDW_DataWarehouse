"""
Created on Oct 18, 2013

Unit test for initialize_sftp_zone.py
"""
from edsftp.src import configure_sftp_zone
from edsftp.src.util import create_path

__author__ = 'sravi'

import unittest
import os
import shutil


class TestInitializeSFTPZone(unittest.TestCase):

    def setUp(self):
        self.test_sftp_conf = {
            'home': '/tmp',
            'base_dir': 'sftp',
            'arrivals_dir': 'arrivals',
            'sftp_departures_dir': 'departures'
        }
        self.sftp_zone_path = os.path.join(self.test_sftp_conf['home'], self.test_sftp_conf['base_dir'])
        self.sftp_arrivals_path = os.path.join(self.sftp_zone_path, self.test_sftp_conf['arrivals_dir'])
        self.sftp_departures_path = os.path.join(self.sftp_zone_path, self.test_sftp_conf['sftp_departures_dir'])

    def tearDown(self):
        pass

    def test__create_non_existing_path_as_root(self):
        test_path = "/tmp/sftp"
        create_path(test_path)
        self.assertTrue(os.path.exists(test_path))

        # cleanup
        if os.path.exists(test_path):
            shutil.rmtree(test_path, True)
        self.assertFalse(os.path.exists(test_path))

    def test__create_existing_path_as_root(self):
        test_path = "/tmp/sftp"
        create_path(test_path)
        self.assertTrue(os.path.exists(test_path))

        # try creating again
        create_path(test_path)
        self.assertTrue(os.path.exists(test_path))

        # cleanup
        if os.path.exists(test_path):
            shutil.rmtree(test_path, True)
        self.assertFalse(os.path.exists(test_path))

    def test__initialize_sftp_zone(self):
        configure_sftp_zone.initialize(self.test_sftp_conf)
        self.assertTrue(os.path.exists(self.sftp_zone_path))
        self.assertTrue(os.path.exists(self.sftp_arrivals_path))
        self.assertTrue(os.path.exists(self.sftp_departures_path))

    def test__cleanup(self):
        configure_sftp_zone.cleanup(self.test_sftp_conf)
        self.assertFalse(os.path.exists(self.sftp_zone_path))
        self.assertFalse(os.path.exists(self.sftp_arrivals_path))
        self.assertFalse(os.path.exists(self.sftp_departures_path))
