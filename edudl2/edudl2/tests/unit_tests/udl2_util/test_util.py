__author__ = 'sravi'

import unittest
import os
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2_util.util import get_tenant_name
from edudl2.udl2_util.util import get_assessment_type


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

    def test_get_assessment_type(self):
        valid_json_dir = '../tests/unit_tests/data/valid_assessment_json'
        absolute_path = os.path.abspath(valid_json_dir)
        result = get_assessment_type(absolute_path)
        expected = 'SUMMATIVE'
        self.assertEqual(result, expected)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
