'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.security.roles.teacher import Teacher
from smarter.security.roles.default import DefaultRole
from smarter.security.context_role_map import ContextRoleMap


class TestContextFactory(unittest.TestCase):

    def test_get_context_with_no_role(self):
        context = ContextRoleMap.get_context("invalid")
        self.assertEqual(context, DefaultRole)

    def test_get_context_with_valid_role(self):
        context = ContextRoleMap.get_context('TEACHER')
        self.assertEqual(context, Teacher)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
