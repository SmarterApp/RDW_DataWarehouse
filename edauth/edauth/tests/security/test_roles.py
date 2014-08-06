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
