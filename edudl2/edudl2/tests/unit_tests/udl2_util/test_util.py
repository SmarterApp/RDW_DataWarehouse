# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
        here = os.path.abspath(os.path.dirname(__file__))
        valid_json_dir = os.path.abspath(os.path.join(os.path.join(here, '..'), 'data', 'valid_assessment_json'))
        result = get_assessment_type(valid_json_dir)
        expected = 'SUMMATIVE'
        self.assertEqual(result, expected)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
