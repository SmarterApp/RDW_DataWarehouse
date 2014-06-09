__author__ = 'sravi'

import unittest
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2_util.util import get_tenant_name


class TestUtil(unittest.TestCase):

    def test_get_tenant_name_regular_directory(self):
        udl2_conf['zones']['arrivals'] = '/opt/edware/zones/landing/arrivals'
        dir_name = '/opt/edware/zones/landing/arrivals/ri/some_user/file_drop/some_file.tgz'
        expected = 'ri'
        result = get_tenant_name(dir_name)
        self.assertEqual(result, expected)

    def test_get_tenant_name_invalid_directory(self):
        udl2_conf['zones']['arrivals'] = '/opt/edware/zones/landing/arrivals'
        dir_name = '/ri/some_user/file_drop/some_file.tgz'
        result = get_tenant_name(dir_name)
        self.assertIsNone(result)
