__author__ = 'swimberly'

import unittest
import os
import shutil

from sftp.src import initialize_sftp_tenant
from sftp.src.util import cleanup_directory


class TestInitializeTenant(unittest.TestCase):

    def setUp(self):
        self.sftp_conf = {
            'sftp_home': '/',
            'sftp_base_dir': 'tmp',
            'sftp_arrivals_dir': 'test_arrivals',
            'sftp_departures_dir': 'test_departures',
            'groups': ['sftparrivals', 'tenantadmin'],
            'group_directories': {
                'sftparrivals': 'arrivals',
                'tenantadmin': 'departures'
            }
        }
        # make sure directories are empty
        shutil.rmtree('/tmp/test_arrivals')
        shutil.rmtree('/tmp/test_departures')

        # Create directories
        os.mkdir('/tmp/test_arrivals')
        os.mkdir('/tmp/test_departures')

    def tearDown(self):
        shutil.rmtree('/tmp/test_arrivals')
        shutil.rmtree('/tmp/test_departures')

    def test_create_tenant_path_string_arrivals(self):
        tenant = 'test_tenant123'
        expected = '/tmp/test_arrivals/test_tenant123'
        result = initialize_sftp_tenant.create_tenant_path_string(tenant, self.sftp_conf, True)

        self.assertEqual(expected, result)

    def test_create_tenant_path_string_departures(self):
        tenant = 'test_tenant123'
        expected = '/tmp/test_departures/test_tenant123'
        result = initialize_sftp_tenant.create_tenant_path_string(tenant, self.sftp_conf, False)

        self.assertEqual(expected, result)

    def test_create_tenant(self):
        tenant = 'test_tenant123'
        expected_path1 = '/tmp/test_arrivals/test_tenant123'
        expected_path2 = '/tmp/test_departures/test_tenant123'
        self.assertFalse(os.path.exists(expected_path1), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path2), 'expected path should not exist')

        initialize_sftp_tenant.create_tenant(tenant, self.sftp_conf)
        self.assertTrue(os.path.exists(expected_path1))
        self.assertTrue(os.path.exists(expected_path2))

    def test_remove_tenant(self):
        tenant = 'test_tenant123'
        expected_path1 = '/tmp/test_arrivals/test_tenant123'
        expected_path2 = '/tmp/test_departures/test_tenant123'
        initialize_sftp_tenant.create_tenant(tenant, self.sftp_conf)
        self.assertTrue(os.path.exists(expected_path1))
        self.assertTrue(os.path.exists(expected_path2))

        initialize_sftp_tenant.remove_tenant(tenant, self.sftp_conf)
        self.assertFalse(os.path.exists(expected_path1), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path2), 'expected path should not exist')


if __name__ == '__main__':
    unittest.main()
