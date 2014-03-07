'''
Created on Aug 5, 2013

@author: dawu
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from edapi.tests.dummy import DummyRequest
from pyramid import testing
from smarter.reports.helpers.metadata import get_custom_metadata,\
    get_subjects_map
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from smarter.reports.helpers.constants import Constants
from edauth.tests.test_helper.create_session import create_test_session


class TestCustomMetaData(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        dummy_session = create_test_session(['TEACHER'], uid='272')
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_get_custom_metadata(self):
        tenant = get_unittest_tenant_name()
        results = get_custom_metadata('NC', tenant)
        # check non-empty results
        self.assertEqual(set(['subject1', 'subject2']), results.keys(), "result map should contain two subjects' id")
        subject1 = results.get('subject1')
        self.assertIsNotNone(subject1, "subject1 should not be empty")
        self.assertEqual(4, len(subject1[Constants.COLORS]), "subject 1 should contain 4 colors")
        self.assertIsInstance(subject1[Constants.COLORS][0], dict, "subject 1 value should be a json object")
        self.assertEqual(2, subject1[Constants.MIN_CELL_SIZE])
        subject2 = results.get('subject2')
        self.assertEqual(2, subject2[Constants.MIN_CELL_SIZE])

    def test_get_empty_custom_metadata(self):
        tenant = get_unittest_tenant_name()
        results = get_custom_metadata('blablabla', tenant)
        # check empty results
        self.assertEqual(set(['subject1', 'subject2']), results.keys(), "result map should contain two subjects' id")
        text = results.get('subject1').get(Constants.COLORS)
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
