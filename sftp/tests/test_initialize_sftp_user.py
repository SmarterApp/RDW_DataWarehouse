__author__ = 'swimberly'

import unittest
import pwd
import sys
import os

from sftp.src.initialize_sftp_user import _create_user, create_sftp_user, delete_user, _verify_user_tenant_and_role
from sftp.src.configure_sftp_groups import initialize, cleanup
from sftp.src.util import create_path, cleanup_directory
from sftp.src.initialize_sftp_tenant import create_tenant, remove_tenant


class TestInitSFTPUser(unittest.TestCase):

    def setUp(self):
        self.sftp_conf = {
            'sftp_home': '/tmp',
            'sftp_base_dir': 'sftp',
            'sftp_arrivals_dir': 'arrivals',
            'sftp_departures_dir': 'departures',
            'groups': ['testgrp1', 'testgrp2'],
            'group_directories': {
                'testgrp1': 'arrivals',
                'testgrp2': 'departures'
            },
            'file_drop': 'tst_file_drop',
        }

    def test_create_sftp_user(self):
        tenant = 'test_tenant1'
        user = 'test_user1'
        role = 'testgrp1'
        self.check_user_does_not_exist(user)

        if sys.platform == 'linux':
            create_tenant(tenant, self.sftp_conf)
            initialize(self.sftp_conf)
            create_sftp_user(tenant, user, role, self.sftp_conf)
            self.assertIsNotNone(pwd.getpwnam(user))

            # cleanup
            delete_user(user)
            remove_tenant(tenant, self.sftp_conf)
            cleanup(self.sftp_conf)

    def test_create_user_and_delete_user(self):
        user = 'test_user1'
        home_folder = '/tmp/test_sftp_user'
        if sys.platform == 'linux':
            initialize(self.sftp_conf)
            self.check_user_does_not_exist(user)
            _create_user(user, home_folder, 'testgrp1', 'file_drop')
            self.assertIsNotNone(pwd.getpwnam(user))

            file_drop_folder = os.path.join(home_folder, self.sftp_conf['file_drop'])

            # check that directory exists and that owner and permission are correct
            self.assertTrue(os.path.exists(file_drop_folder))
            self.assertEqual(pwd.getpwuid(os.stat(file_drop_folder).st_uid), user)
            self.assertEqual((os.stat(file_drop_folder).st_mode & 0o777), 0o777)
            delete_user(user)
            self.check_user_does_not_exist(user)
            cleanup(self.sftp_conf)

    def test_verify_user_tenant_and_role_tenant_path(self):
        home_folder = '/tmp/does_not_exist'
        expected_result = (False, 'Tenant does not exist!')
        result = _verify_user_tenant_and_role(home_folder, 'test_user', 'some_role')

        self.assertEqual(expected_result, result)

    def test_verify_user_tenant_and_role__role(self):
        tenant_folder = '/tmp/test_does_exist'
        create_path(tenant_folder)
        expected_result = (False, 'Role does not exist as a group in the system')
        result = _verify_user_tenant_and_role(tenant_folder, 'some_user', 'made_up_role')

        self.assertEqual(result, expected_result)
        cleanup_directory(tenant_folder)

    def test_verify_user_tenant_and_role__user(self):
        tenant_folder = '/tmp/test_does_exist'
        create_path(tenant_folder)
        expected_result = (False, 'User already exists!')
        result = _verify_user_tenant_and_role(tenant_folder, 'root', 'wheel')

        self.assertEqual(expected_result, result)
        cleanup_directory(tenant_folder)

    def test_verify_user_tenant_and_role__valid_input(self):
        tenant_folder = '/tmp/test_does_exist'
        create_path(tenant_folder)
        expected_result = True, ""
        result = _verify_user_tenant_and_role(tenant_folder, 'the_roots', 'wheel')

        self.assertEqual(expected_result, result)
        cleanup_directory(tenant_folder)

    def check_user_does_not_exist(self, user):
        with self.assertRaises(KeyError):
            pwd.getpwnam(user)

if __name__ == '__main__':
    unittest.main()
