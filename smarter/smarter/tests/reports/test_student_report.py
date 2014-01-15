'''
Created on Jan 17, 2013

@author: tosako
'''

import unittest
from smarter.reports.student_report import get_student_report
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from edapi.exceptions import NotFoundException
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.session import Session
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


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
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
        dummy_session = Session()
        dummy_session.set_roles(['TEACHER'])
        dummy_session.set_uid('272')
        dummy_session.set_tenant(get_unittest_tenant_name())
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_student_report(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', "assessmentGuid": 20}
        result = get_student_report(params)['items']['Summative']
        self.assertEqual(1, len(result), "studentGuid should have 1 report")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject')
        self.assertEqual('2200', result[0]['claims'][0]['score'], 'asmt_claim_1_score 88')
        self.assertEqual('Research & Inquiry', result[0]['claims'][3]['name'], 'asmt_claim_4_name Spelling')

    def test_assessment_header_info(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621'}
        result = get_student_report(params)['items']['Summative']
        student_report = result[0]

        self.assertEqual('Math', student_report['asmt_subject'], 'asmt_subject')
        self.assertEqual(21, student_report['date_taken_day'])
        self.assertEqual(9, student_report['date_taken_month'])
        self.assertEqual(2012, student_report['date_taken_year'])

    def test_custom_metadata(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621', "stateCode": 'NY'}
        result = get_student_report(params)['items']['Summative']
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
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621'}
        result = get_student_report(params)['items']['Summative']
        student_report = result[0]

        self.assertEqual(student_report['asmt_score'], student_report['asmt_score_range_min'] + student_report['asmt_score_interval'])
        self.assertEqual(student_report['asmt_score'], student_report['asmt_score_range_max'] - student_report['asmt_score_interval'])

    def test_context(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621'}
        result = get_student_report(params)['context']['items']
        self.assertEqual('New York', result[0]['name'])
        self.assertEqual('Sunset School District', result[1]['name'])
        self.assertEqual("3", result[3]['name'])
        self.assertEqual("Sunset - Eastern Elementary", result[2]['name'])
        self.assertEqual("Lettie L. Hose", result[4]['name'])

    def test_claims(self):
        params = {"studentGuid": 'dae1acf4-afb0-4013-90ba-9dcde4b25621'}
        items = get_student_report(params)['items']['Summative']
        result = items[0]
        self.assertEqual(3, len(result['claims']))
        self.assertEqual('Concepts & Procedures', result['claims'][0]['name'])
        self.assertEqual('Problem Solving and Modeling & Data Analysis', result['claims'][1]['name'])
        self.assertEqual('Communicating Reasoning', result['claims'][2]['name'])
        result = items[1]
        self.assertEqual(4, len(result['claims']))
        self.assertEqual('Reading', result['claims'][0]['name'])
        self.assertEqual('Writing', result['claims'][1]['name'])
        self.assertEqual('Listening', result['claims'][2]['name'])
        self.assertEqual('Research & Inquiry', result['claims'][3]['name'])

    def test_invalid_student_id(self):
        params = {'studentGuid': 'invalid'}
        self.assertRaises(NotFoundException, get_student_report, params)

if __name__ == '__main__':
    unittest.main()
