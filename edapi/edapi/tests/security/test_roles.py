'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edapi.security.roles import has_undefined_roles, Roles


class TestRoles(unittest.TestCase):

    def test_one_bad_role(self):
        self.assertTrue(has_undefined_roles(['I do not exist']))

    def test_no_bad_roles(self):
        self.assertFalse(has_undefined_roles([Roles.SYSTEM_ADMINISTRATOR, Roles.TEACHER, Roles.CONSORTIUM_EDUCATION_ADMINISTRATOR_1, Roles.STUDENT]))

    def test_good_and_bad_roles(self):
        self.assertTrue(has_undefined_roles([Roles.PARENT, Roles.STATE_DATA_EXTRACTOR, "Bad Role", Roles.STATE_EDUCATION_ADMINISTRATOR_1]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
