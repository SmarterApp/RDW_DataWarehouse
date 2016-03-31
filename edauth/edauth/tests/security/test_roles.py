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

'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edauth.security.roles import Roles


class TestRoles(unittest.TestCase):

    def test_one_bad_role(self):
        self.assertTrue(Roles.has_undefined_roles(['I do not exist']))

    def test_no_bad_roles(self):
        mappings = {('Allow', 'DEPLOYMENT_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'DATA_LOADER', ('view', 'logout'))}
        Roles.set_roles(mappings)
        self.assertFalse(Roles.has_undefined_roles(['DEPLOYMENT_ADMINISTRATOR', 'SYSTEM_ADMINISTRATOR', 'DATA_LOADER']))

    def test_good_and_bad_roles(self):
        mappings = {('Allow', 'DEPLOYMENT_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'DATA_LOADER', ('view', 'logout'))}
        Roles.set_roles(mappings)
        self.assertTrue(Roles.has_undefined_roles(['DEPLOYMENT_ADMINISTRATOR', 'DEPLOYMENT_ADMINISTRATOR', 'Bad Role', 'DATA_LOADER']))

    def test_default_permission(self):
        mappings = {('Allow', 'DEPLOYMENT_ADMINISTRATOR', ('view', 'logout', 'default')),
                    ('Allow', 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'DATA_LOADER', ('view', 'logout'))}
        Roles.set_roles(mappings)
        default = Roles.get_default_permission()
        self.assertEqual('DEPLOYMENT_ADMINISTRATOR', default)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
