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
            'sftp_arrivals_dir': 'test_arrivals_1',
            'sftp_departures_dir': 'test_departures_1',
            'groups': ['sftparrivals', 'tenantadmin'],
            'group_directories': {
                'sftparrivals': 'arrivals',
                'tenantadmin': 'departures'
            }
        }

        # Create directories
        os.mkdir('/tmp/test_arrivals_1')
        os.mkdir('/tmp/test_departures_1')

    def tearDown(self):
        shutil.rmtree('/tmp/test_arrivals_1')
        shutil.rmtree('/tmp/test_departures_1')

    def test_create_tenant_path_string_arrivals(self):
        tenant = 'test_tenant123'
        expected = '/tmp/test_arrivals_1/test_tenant123'
        result = initialize_sftp_tenant.create_tenant_path_string(tenant, self.sftp_conf, True)

        self.assertEqual(expected, result)

    def test_create_tenant_path_string_departures(self):
        tenant = 'test_tenant123'
        expected = '/tmp/test_departures_1/test_tenant123'
        result = initialize_sftp_tenant.create_tenant_path_string(tenant, self.sftp_conf, False)

        self.assertEqual(expected, result)

    def test_create_tenant(self):
        tenant = 'test_tenant123'
        expected_path1 = '/tmp/test_arrivals_1/test_tenant123'
        expected_path2 = '/tmp/test_departures_1/test_tenant123'
        self.assertFalse(os.path.exists(expected_path1), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path2), 'expected path should not exist')

        initialize_sftp_tenant.create_tenant(tenant, self.sftp_conf)
        self.assertTrue(os.path.exists(expected_path1))
        self.assertTrue(os.path.exists(expected_path2))

    def test_remove_tenant(self):
        tenant = 'test_tenant123'
        expected_path1 = '/tmp/test_arrivals_1/test_tenant123'
        expected_path2 = '/tmp/test_departures_1/test_tenant123'
        initialize_sftp_tenant.create_tenant(tenant, self.sftp_conf)
        self.assertTrue(os.path.exists(expected_path1))
        self.assertTrue(os.path.exists(expected_path2))

        initialize_sftp_tenant.remove_tenant(tenant, self.sftp_conf)
        self.assertFalse(os.path.exists(expected_path1), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path2), 'expected path should not exist')


if __name__ == '__main__':
    unittest.main()
