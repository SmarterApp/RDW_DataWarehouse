'''
Created on Oct 21, 2013

@author: bpatel
'''

import unittest
import os
import shutil
from edsftp.src import configure_sftp_zone
from edsftp.src import configure_sftp_groups
from edsftp.src import sftp_config
import sys
from edsftp.src import initialize_sftp_tenant
from edsftp.src.util import cleanup_directory
from edsftp.src import initialize_sftp_user


class sftpvalidation(unittest.TestCase):
    def setUp(self):
        shutil.rmtree('/tmp/sftp_functional_test/sftp')
        if not os.path.exists("/tmp/sftp_functional_test"):
            os.mkdir("/tmp/sftp_functional_test", 0o755)
        self.test_sftp_conf = {
            'sftp_home': '/tmp/sftp_functional_test',
            'sftp_base_dir': 'sftp',
            'sftp_arrivals_dir': 'arrivals',
            'sftp_departures_dir': 'departures',
            'groups': ['sftparrivals', 'tenantadmin'],
            'group_directories': {'sftparrivals': 'arrivals',
                                  'tenantadmin': 'departures'}
        }
        self.sftp_zone_path = os.path.join(self.test_sftp_conf['sftp_home'], self.test_sftp_conf['sftp_base_dir'])
        self.sftp_arrivals_path = os.path.join(self.sftp_zone_path, self.test_sftp_conf['sftp_arrivals_dir'])
        self.sftp_departures_path = os.path.join(self.sftp_zone_path, self.test_sftp_conf['sftp_departures_dir'])
        self.sftp_arrivals_tenant_path = os.path.join(self.sftp_arrivals_path, 'tenant_dir')
        self.sftp_departures_tenant_path = os.path.join(self.sftp_departures_path, 'tenant_dir')
        self.sftp_arrivals_users = os.path.join(self.sftp_arrivals_tenant_path, 'arrival_user')
        self.sftp_departures_users = os.path.join(self.sftp_departures_tenant_path, 'departure_user')

    def test_sftp(self):
        self.sftp_zones()
        self.sftp_groups()
        self.sftp_tenant()
        self.sftp_users()
        self.sftp_cleanup()

    def sftp_zones(self):

        configure_sftp_zone.initialize(self.test_sftp_conf)
        self.assertTrue(os.path.exists(self.sftp_zone_path))
        self.assertTrue(os.path.exists(self.sftp_arrivals_path))
        self.assertTrue(os.path.exists(self.sftp_departures_path))

    def sftp_groups(self):

        configure_sftp_groups.initialize(self.test_sftp_conf)
        for name in self.test_sftp_conf['groups']:
                    if sys.platform == 'linux':
                        self.assertTrue(configure_sftp_groups._group_exists(name))
                    else:
                        self.assertFalse(configure_sftp_groups._group_exists(name))

    def sftp_tenant(self):
        initialize_sftp_tenant.create_tenant('tenant_dir', self.test_sftp_conf)
        self.assertTrue(os.path.exists(self.sftp_arrivals_tenant_path))
        self.assertTrue(os.path.exists(self.sftp_departures_tenant_path))

    def sftp_users(self):
            initialize_sftp_user.create_sftp_user('tenant_dir', 'arrival_user', 'sftparrivals', self.test_sftp_conf)
            initialize_sftp_user.create_sftp_user('tenant_dir', 'departure_user', 'tenantadmin', self.test_sftp_conf)
            if sys.platform == 'linux':
                    self.assertTrue(os.path.exists(self.sftp_arrivals_users))
                    self.assertTrue(os.path.exists(self.sftp_departures_users))

    def sftp_cleanup(self):

        #For clean up zones and base directories
        configure_sftp_zone.cleanup(self.test_sftp_conf)
        self.assertFalse(os.path.exists(self.sftp_zone_path))
        self.assertFalse(os.path.exists(self.sftp_arrivals_path))
        self.assertFalse(os.path.exists(self.sftp_departures_path))

        #for clean up users
        initialize_sftp_user. delete_user('arrival_user')
        initialize_sftp_user. delete_user('departure_user')

        #for clean up tenant
        initialize_sftp_tenant.remove_tenant('tenant_dir', self.test_sftp_conf)

        #  clean up the groups
        configure_sftp_groups.cleanup(self.test_sftp_conf)
        for name in self.test_sftp_conf['groups']:
            if sys.platform == 'linux':
                self.assertFalse(configure_sftp_groups._group_exists(name))
            else:
                self.assertFalse(configure_sftp_groups._group_exists(name))
