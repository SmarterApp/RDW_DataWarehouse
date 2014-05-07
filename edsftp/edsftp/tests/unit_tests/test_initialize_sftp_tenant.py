__author__ = 'swimberly'

import unittest
import os
import shutil
import tempfile
from edsftp.src import initialize_sftp_tenant


class TestInitializeTenant(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.mkdtemp()
        self.sftp_conf = {
            'home': self.__temp_dir,
            'base_dir': 'tenant_test_dir',
            'arrivals_dir': 'test_arrivals_1',
            'sftp_departures_dir': 'test_departures_1',
            'user_home_base_dir': self.__temp_dir,
            'group': 'edwaredataadmin',
            'roles': ['sftparrivals', 'sftpdepartures'],
        }

        # Create directories
        os.makedirs(os.path.join(self.__temp_dir, 'tenant_test_dir/test_arrivals_1'))
        os.makedirs(os.path.join(self.__temp_dir, 'tenant_test_dir/test_departures_1'))
        os.mkdir(os.path.join(self.__temp_dir, 'test_arrivals_1'))
        os.mkdir(os.path.join(self.__temp_dir, 'test_departures_1'))

    def tearDown(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)

    def test_create_tenant_path_string_arrivals(self):
        tenant = 'test_tenant123'
        expected = os.path.join(self.sftp_conf['home'], self.sftp_conf['base_dir'],
                                self.sftp_conf['arrivals_dir'], tenant)
        result = initialize_sftp_tenant.create_tenant_path_string(tenant, self.sftp_conf, True)

        self.assertEqual(expected, result)

    def test_create_tenant_path_string_departures(self):
        tenant = 'test_tenant123'
        expected = os.path.join(self.sftp_conf['home'], self.sftp_conf['base_dir'],
                                self.sftp_conf['sftp_departures_dir'], tenant)
        result = initialize_sftp_tenant.create_tenant_path_string(tenant, self.sftp_conf, False)

        self.assertEqual(expected, result)

    def test_create_tenant_home_folder_string_arrivals(self):
        tenant = "test_tenant1234"
        expected = os.path.join(self.sftp_conf['user_home_base_dir'], self.sftp_conf['arrivals_dir'], tenant)
        result = initialize_sftp_tenant.create_tenant_home_folder_string(tenant, self.sftp_conf, True)

        self.assertEqual(result, expected)

    def test_create_tenant_home_folder_string_departures(self):
        tenant = "test_tenant1234"
        expected = os.path.join(self.sftp_conf['user_home_base_dir'], self.sftp_conf['sftp_departures_dir'], tenant)
        result = initialize_sftp_tenant.create_tenant_home_folder_string(tenant, self.sftp_conf, False)

        self.assertEqual(result, expected)

    def test_create_tenant(self):
        tenant = 'test_tenant123'
        expected_path1 = os.path.join(self.sftp_conf['home'], self.sftp_conf['base_dir'],
                                      self.sftp_conf['arrivals_dir'], tenant)
        expected_path2 = os.path.join(self.sftp_conf['home'], self.sftp_conf['base_dir'],
                                      self.sftp_conf['sftp_departures_dir'], tenant)
        expected_path3 = os.path.join(self.sftp_conf['user_home_base_dir'], self.sftp_conf['arrivals_dir'], tenant)
        expected_path4 = os.path.join(self.sftp_conf['user_home_base_dir'], self.sftp_conf['sftp_departures_dir'], tenant)

        self.assertFalse(os.path.exists(expected_path1), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path2), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path3), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path4), 'expected path should not exist')

        initialize_sftp_tenant.create_tenant(tenant, self.sftp_conf)
        self.assertTrue(os.path.exists(expected_path1))
        self.assertTrue(os.path.exists(expected_path2))
        self.assertTrue(os.path.exists(expected_path3))
        self.assertTrue(os.path.exists(expected_path4))

    def test_remove_tenant(self):
        tenant = 'test_tenant123'
        expected_path1 = os.path.join(self.sftp_conf['home'], self.sftp_conf['base_dir'],
                                      self.sftp_conf['arrivals_dir'], tenant)
        expected_path2 = os.path.join(self.sftp_conf['home'], self.sftp_conf['base_dir'],
                                      self.sftp_conf['sftp_departures_dir'], tenant)
        expected_path3 = os.path.join(self.sftp_conf['user_home_base_dir'], self.sftp_conf['arrivals_dir'], tenant)
        expected_path4 = os.path.join(self.sftp_conf['user_home_base_dir'], self.sftp_conf['sftp_departures_dir'], tenant)

        initialize_sftp_tenant.create_tenant(tenant, self.sftp_conf)
        self.assertTrue(os.path.exists(expected_path1))
        self.assertTrue(os.path.exists(expected_path2))
        self.assertTrue(os.path.exists(expected_path3))
        self.assertTrue(os.path.exists(expected_path4))

        initialize_sftp_tenant.remove_tenant(tenant, self.sftp_conf)
        self.assertFalse(os.path.exists(expected_path1), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path2), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path3), 'expected path should not exist')
        self.assertFalse(os.path.exists(expected_path4), 'expected path should not exist')


if __name__ == '__main__':
    unittest.main()
