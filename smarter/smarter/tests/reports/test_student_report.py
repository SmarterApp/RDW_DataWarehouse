'''
Created on Jan 17, 2013

@author: tosako
'''

import unittest
from smarter.reports.student_report import get_student_report
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edapi.exceptions import NotFoundException
from pyramid.testing import DummyRequest
from pyramid import testing
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from pyramid.httpexceptions import HTTPForbidden
from smarter.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map


class TestStudentReport(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }

        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
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
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', "assessmentGuid": '3b10d26b-b013-4cdd-a916-5d577e895ed4', 'stateCode': 'AA'}
        results = get_student_report(params)
        self.assertIsInstance(results, HTTPForbidden)

    def test_student_report(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', "assessmentGuid": '3b10d26b-b013-4cdd-a916-5d577e895ed4', 'stateCode': 'NC'}
        result = get_student_report(params)['all_results']
        self.assertEqual(1, len(result), "studentGuid should have 1 report")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject')
        self.assertEqual('2200', result[0]['claims'][0]['score'], 'asmt_claim_1_score 88')
        self.assertEqual('Research & Inquiry', result[0]['claims'][3]['name'], 'asmt_claim_4_name Spelling')

    def test_assessment_header_info(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', 'stateCode': 'NC'}
        result = get_student_report(params)
        student_report = result['all_results'][0]

        self.assertEqual('Math', student_report['asmt_subject'], 'asmt_subject')
        self.assertEqual(2016, student_report['date_taken_year'])

    def test_custom_metadata(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', "stateCode": 'NC'}
        result = get_student_report(params)['all_results']
        student_report = result[0]

        cut_points_list = student_report['cut_point_intervals']
        self.assertEqual(4, len(cut_points_list), "we should have 4 cut point intervals")

        expected_cut_point_names = set(['Minimal Understanding', 'Partial Understanding', 'Adequate Understanding', 'Thorough Understanding'])
        for cut_point in cut_points_list:
            self.assertIsInstance(cut_point, dict, "each cut point should be a dictionary")

            keys = cut_point.keys()
            cut_point_name = cut_point['name']
            self.assertIn(cut_point_name.strip(), expected_cut_point_names, "unexpected cut point name")
            self.assertIn("name", keys, "should contain the name of the cut point")
            self.assertIn("interval", keys, "should contain the value of the cut point")
            self.assertIn("text_color", keys, "should contain the text_color of the cut point")
            self.assertIn("end_gradient_bg_color", keys, "should contain the end_gradient_bg_color of the cut point")
            self.assertIn("start_gradient_bg_color", keys, "should contain the start_gradient_bg_color of the cut point")
            self.assertIn("bg_color", keys, "should contain the bg_color of the cut point")

    def test_score_interval(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', 'stateCode': 'NC'}
        result = get_student_report(params)['all_results']
        student_report = result[0]

        self.assertEqual(student_report['asmt_score'], student_report['asmt_score_range_min'] + student_report['asmt_score_interval'])
        self.assertEqual(student_report['asmt_score'], student_report['asmt_score_range_max'] - student_report['asmt_score_interval'])

    def test_context(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', 'stateCode': 'NC'}
        result = get_student_report(params)['context']['items']
        self.assertEqual('North Carolina', result[1]['name'])
        self.assertEqual('Sunset School District', result[2]['name'])
        self.assertEqual("3", result[4]['name'])
        self.assertEqual("Sunset - Eastern Elementary", result[3]['name'])
        self.assertEqual("Lettie L. Hose", result[5]['name'])

    def test_claims(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', 'stateCode': 'NC'}
        items = get_student_report(params)['all_results']
        result = items[0]
        self.assertEqual(3, len(result['claims']))
        self.assertEqual('Concepts & Procedures', result['claims'][0]['name'])
        self.assertEqual('Problem Solving and Modeling & Data Analysis', result['claims'][1]['name'])
        self.assertEqual('Communicating Reasoning', result['claims'][2]['name'])
        result = items[1]
        self.assertEqual(3, len(result['claims']))
        self.assertEqual('Concepts & Procedures', result['claims'][0]['name'])
        self.assertEqual('Problem Solving and Modeling & Data Analysis', result['claims'][1]['name'])
        self.assertEqual('Communicating Reasoning', result['claims'][2]['name'])
        self.assertEqual(7, len(result['accommodations']))
        self.assertEqual(5, len(result['accommodations'][0]))
        self.assertEqual(1, len(result['accommodations'][5]))
        self.assertEqual(1, len(result['accommodations'][6]))
        self.assertEqual(1, len(result['accommodations'][7]))
        self.assertEqual(3, len(result['accommodations'][9]))
        self.assertEqual(1, len(result['accommodations'][10]))

    def test_invalid_student_id(self):
        params = {'studentGuid': 'invalid', 'stateCode': 'NC'}
        self.assertRaises(NotFoundException, get_student_report, params)

if __name__ == '__main__':
    unittest.main()
