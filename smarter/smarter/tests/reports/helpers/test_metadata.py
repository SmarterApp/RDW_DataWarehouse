'''
Created on Aug 5, 2013

@author: dawu
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite,\
    UnittestSmarterDBConnection, get_unittest_tenant_name
from edapi.tests.dummy import DummyRequest
from pyramid import testing
from edauth.security.session import Session
from smarter.reports.helpers.metadata import get_custom_metadata,\
    get_subjects_map
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from smarter.reports.helpers.constants import Constants


class TestCustomMetaData(Unittest_with_smarter_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        with UnittestSmarterDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
        dummy_session = Session()
        dummy_session.set_session_id('123')
        dummy_session.set_roles(['TEACHER'])
        dummy_session.set_uid('272')
        dummy_session.set_tenant(get_unittest_tenant_name())
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestSmarterDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_get_custom_metadata(self):
        tenant = get_unittest_tenant_name()
        results = get_custom_metadata('NY', tenant)
        # check non-empty results
        self.assertEqual(set(['subject1', 'subject2']), results.keys(), "result map should contain two subjects' id")
        text = results.get('subject1')
        self.assertIsNotNone(text, "subject1 should not be empty")
        self.assertEqual(4, len(text), "subject 1 should contain 4 colors")
        self.assertIsInstance(text[0], dict, "subject 1 value should be a json object")

    def test_get_empty_custom_metadata(self):
        tenant = get_unittest_tenant_name()
        results = get_custom_metadata('blablabla', tenant)
        # check empty results
        self.assertEqual(set(['subject1', 'subject2']), results.keys(), "result map should contain two subjects' id")
        text = results.get('subject1')
        self.assertIsNone(text, "subject1 should be empty")

    def test_get_subjects_map(self):
        # test empty subject
        result = get_subjects_map(asmtSubject=None)
        self.assertEqual(result, {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2})
        # test math
        result = get_subjects_map(asmtSubject=(Constants.MATH))
        self.assertEqual(result, {Constants.MATH: Constants.SUBJECT1})
        # test ela
        result = get_subjects_map(asmtSubject=(Constants.ELA))
        self.assertEqual(result, {Constants.ELA: Constants.SUBJECT1})
        # test math and ela
        result = get_subjects_map(asmtSubject=(Constants.ELA, Constants.MATH))
        self.assertEqual(result, {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2})


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()