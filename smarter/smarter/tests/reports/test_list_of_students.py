'''
Created on Feb 4, 2013

@author: tosako
'''
import unittest

from pyramid.testing import DummyRequest
from pyramid import testing
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pyramid.security import Allow
from pyramid.httpexceptions import HTTPForbidden

from smarter.reports.list_of_students_report import get_list_of_students_report,\
    get_group_filters
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport


class TestLOS(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }

        CacheManager(**parse_cache_config_options(cache_opts))

        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_invalid_params(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'AA'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)
        self.assertIsInstance(results, HTTPForbidden)

    def test_assessments(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('cutpoints' in results['metadata'], "returning JSON must have metadata")
        self.assertTrue('assessments' in results, "returning JSON must have assessments")

        cutpoints = results['metadata']['cutpoints']
        self.assertEqual(2, len(cutpoints), "cutpoints are ELA and MATH")
        self.assertTrue('subject2' in cutpoints, 'subject2')
        self.assertTrue('subject1' in cutpoints, 'subject1')

        claims = results['metadata']['claims']
        self.assertEqual(2, len(claims), "cutpoints are ELA and MATH")
        self.assertTrue('subject2' in claims)
        self.assertTrue('subject1' in claims)

        assessments = results['assessments']
        self.assertEqual(3, len(assessments), "3 assessments")
        student1 = assessments['20160106']['Interim Comprehensive']['f9da4c5d-dc65-42d0-a36f-5d13ba930c50']
        student2 = assessments['20160106']['Interim Comprehensive']['e2f3c6a5-e28b-43e8-817b-fc7afed02b9b']
        student3 = assessments['20160106']['Interim Comprehensive']['dae1acf4-afb0-4013-90ba-9dcde4b25621']
        self.assertEqual("Verda", student1['student_first_name'], "first_name")
        self.assertEqual("Mi-Ha", student2['student_first_name'], "first_name")
        self.assertEqual("Lettie", student3['student_first_name'], "first_name")

    def test_breadcrumbs(self):
        testParam = {}
        testParam['stateCode'] = 'NC'
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('context' in results, "returning JSON must have context")

    def test_asmt_administration(self):
        testParam = {}
        testParam['stateCode'] = 'NC'
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)
        self.assertTrue('asmt_administration' in results, "asmt_administration is missing")
        self.assertEquals(len(results['asmt_administration']), 3, "should have 3 different test")

    def test_ELA_only(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['ELA']
        results = get_list_of_students_report(testParam)

        self.assertTrue('metadata' in results, "returning JSON must have metadata")
        self.assertTrue('assessments' in results, "returning JSON must have assessments")

        cutpoints = results['metadata']['cutpoints']
        self.assertEqual(1, len(cutpoints), "cutpoints are ELA and MATH")
        self.assertTrue('subject1' in cutpoints, 'subject1')

        claims = results['metadata']['claims']
        self.assertEqual(1, len(claims), "claims are ELA")
        self.assertTrue('subject1' in claims, 'subject1')

    def test_Math_only(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('metadata' in results, "returning JSON must have cutpoints")

        cutpoints = results['metadata']['cutpoints']
        self.assertEqual(1, len(cutpoints))
        self.assertTrue('subject1' in cutpoints, 'subject1')

        claims = results['metadata']['claims']
        self.assertEqual(1, len(claims), "claims are ELA")
        self.assertTrue('subject1' in claims, 'subject1')

    def test_invalid_asmt_subject(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = 3
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['Dummy']
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 0, "should return no results")

    def test_LOS_with_filters(self):
        testParam = {'asmtGrade': '3', 'gender': ['male'], 'stateCode': 'NC', 'districtId': '228', 'schoolId': '242'}
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 3)

        testParam['gender'] = ['not_stated']
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 3)

    def test_asmt_type(self):
        testParam = {'asmtGrade': '3', 'stateCode': 'NC', 'districtId': '228', 'schoolId': '242', 'asmtYear': '2015'}
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 3)
        self.assertIsNotNone(results['assessments']['20150106']['Interim Comprehensive']['cad811ad-9b08-4dd1-aa10-52360b80ff7f']['subject2'])

    def test_get_group_filters(self):
        groups = [{'group_1_id': 'id1', 'group_1_text': 'something', 'group_2_id': None, 'group_3_id': None, 'group_4_id': None, 'group_5_id': None, 'group_6_id': None, 'group_7_id': None,
                   'group_8_id': None, 'group_9_id': None, 'group_10_id': None}, {'group_1_id': 'id1', 'group_1_text': 'something', 'group_2_id': 'id2', 'group_2_text': 'something', 'group_3_id': None,
                                                                                  'group_4_id': None, 'group_5_id': None, 'group_6_id': None, 'group_7_id': None, 'group_8_id': None, 'group_9_id': None,
                                                                                  'group_10_id': None}]
        results = get_group_filters(groups)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['label'], 'something')

    def test_get_group_filters_group_1_only(self):
        groups = [{'group_1_id': 'id1', 'group_1_text': 'something', 'group_2_id': None, 'group_3_id': None, 'group_4_id': None, 'group_5_id': None, 'group_6_id': None, 'group_7_id': None,
                   'group_8_id': None, 'group_9_id': None, 'group_10_id': None}, {'group_1_id': 'id2', 'group_1_text': 'foo', 'group_2_id': None, 'group_3_id': None, 'group_4_id': None,
                                                                                  'group_5_id': None, 'group_6_id': None, 'group_7_id': None, 'group_8_id': None, 'group_9_id': None, 'group_10_id': None}]
        results = get_group_filters(groups)
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]), 2)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
