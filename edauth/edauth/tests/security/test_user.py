'''
Created on Mar 14, 2013

@author: dip
'''
import unittest
from edauth.security.user import User


class TestUser(unittest.TestCase):

    def test_empty_user(self):
        user = User()
        data = {'name': {'fullName': None, 'firstName': None, 'lastName': None}, 'uid': None, 'roles': [], 'tenant': None, 'guid': None}

        name = user.get_name()
        self.assertEqual(name, {'name': data['name']})

        uid = user.get_uid()
        self.assertEqual(uid, data['uid'])

        context = user.get_user_context()
        self.assertEqual(context, data)

        roles = user.get_roles()
        self.assertEqual(roles, data['roles'])

        tenant = user.get_tenant()
        self.assertIsNone(tenant)

        guid = user.get_guid()
        self.assertIsNone(guid)

    def test_non_empty_user(self):
        user = User()
        data = {'name': {'fullName': 'Joe Doe', 'firstName': 'Joe', 'lastName': 'Doe'}, 'uid': 'joe.doe', 'roles': ['TEACHER'], 'stateCode': None, 'tenant': 'dog', 'guid': '123'}
        user.set_name(data['name'])
        user.set_uid(data['uid'])
        user.set_roles(data['roles'])
        user.set_guid(data['guid'])
        user.set_tenant(data['tenant'])

        name = user.get_name()
        self.assertEqual(name, {'name': data['name']})

        uid = user.get_uid()
        self.assertEqual(uid, data['uid'])

        context = user.get_user_context()
        self.assertEqual(context, data)

        roles = user.get_roles()
        self.assertEqual(roles, data['roles'])

        tenant = user.get_tenant()
        self.assertEqual(tenant, data['tenant'])

        guid = user.get_guid()
        self.assertEqual(guid, data['guid'])

    def test_set_individual_names(self):
        user = User()
        data = {'name': {'fullName': 'Joe MDoe', 'firstName': 'Joe', 'lastName': 'Doe'}, 'uid': 'joe.doe', 'roles': ['TEACHER'], 'tenant': 'dog', 'guid': '123'}
        user.set_first_name(data['name']['firstName'])
        user.set_last_name(data['name']['lastName'])
        user.set_full_name(data['name']['fullName'])

        name = user.get_name()
        self.assertEqual(name, {'name': data['name']})

    def test_get_user_context(self):
        user = User()
        data = {'name': {'fullName': 'Joe Doe', 'firstName': 'Joe', 'lastName': 'Doe'}, 'uid': 'joe.doe', 'roles': ['TEACHER'], 'tenant': 'dog', 'guid': '123'}
        user.set_name(data['name'])
        user.set_uid(data['uid'])
        user.set_roles(data['roles'])
        user.set_guid(data['guid'])
        user.set_tenant(data['tenant'])

        context = user.get_user_context()
        self.assertEqual(context['uid'], data['uid'])
        self.assertEqual(context['name'], data['name'])
        self.assertEqual(context['roles'], data['roles'])
        self.assertEqual(context['guid'], data['guid'])
        self.assertEqual(context['tenant'], data['tenant'])

    def test_set_user_info(self):
        user = User()
        data = {'name': {'fullName': 'Joe Doe', 'firstName': 'Joe', 'lastName': 'Doe'}, 'uid': 'joe.doe', 'junk': 'junk', 'roles': ['TEACHER'], 'tenant': 'dog', 'guid': '123'}

        user.set_user_info(data)
        context = user.get_user_context()
        self.assertEqual(len(context), 5)
        self.assertEqual(context['name'], data['name'])
        self.assertEqual(context['uid'], data['uid'])
        self.assertEqual(context['roles'], data['roles'])
        self.assertEqual(context['guid'], data['guid'])
        self.assertEqual(context['tenant'], data['tenant'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
