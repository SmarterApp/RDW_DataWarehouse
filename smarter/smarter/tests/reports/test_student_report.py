'''
Created on Jan 17, 2013

@author: tosako
'''

import unittest
from smarter.reports.student_report import get_student_report, get_student_assessment
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite


class TestStudentReport(Unittest_with_smarter_sqlite):

    def test_student_report(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567', "assessmentId": 1}
        result = get_student_report(params)['items']
        self.assertEqual(1, len(result), "studentId should have 1 report")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject')
        self.assertEqual(88, result[0]['asmt_claim_1_score'], 'asmt_claim_1_score 88')
        self.assertEqual('Research & Inquiry', result[0]['asmt_claim_4_name'], 'asmt_claim_4_name Spelling')

    def test_student_assessment_id(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_assessment(params)

        self.assertEqual(2, len(result), "studentId should have 2 assessments")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject ELA')
        self.assertEqual('Math', result[1]['asmt_subject'], 'asmt_subject MATH')

    def test_assessment_header_info(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_report(params)['items']
        student_report = result[0]

        self.assertEqual('Math', student_report['asmt_subject'], 'asmt_subject')
        self.assertEqual('Brandon', student_report['teacher_first_name'], 'teacher first name')
        self.assertEqual('Christopher', student_report['teacher_middle_name'], 'teacher middle name')
        self.assertEqual('Suzuki', student_report['teacher_last_name'], 'teacher last name')
        self.assertEqual(1, student_report['date_taken_day'])
        self.assertEqual(1, student_report['date_taken_month'])
        self.assertEqual(2013, student_report['date_taken_year'])

    def test_custom_metadata(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_report(params)['items']
        student_report = result[0]

        cut_points_list = student_report['cut_point_intervals']
        self.assertEqual(4, len(cut_points_list), "we should have 4 cut point intervals")

        expected_cut_point_names = set(['Minimal Command', 'Partial Command', 'Sufficient Command', 'Deep Command'])
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
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_report(params)['items']
        student_report = result[0]

        self.assertEqual(student_report['asmt_score'], student_report['asmt_score_range_min'] + student_report['asmt_score_interval'])
        self.assertEqual(student_report['asmt_score'], student_report['asmt_score_range_max'] - student_report['asmt_score_interval'])

    def test_context(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_report(params)['context']
        self.assertEqual('NY', result['state_name'])
        self.assertEqual('Sunset School District', result['district_name'])
        self.assertEqual("1", result['grade'])
        self.assertEqual("Sunset Central High", result['school_name'])
        self.assertEqual("Verda Herriman", result['student_name'])

    def test_claims(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        items = get_student_report(params)['items']
        result = items[0]
        self.assertEqual('Concepts & Procedures', result['asmt_claim_1_name'])
        self.assertEqual('Problem Solving & Modeling and Data Analysis', result['asmt_claim_2_name'])
        self.assertEqual('Communicating Reasoning', result['asmt_claim_3_name'])
        self.assertEqual('', result['asmt_claim_4_name'])
        result = items[1]
        self.assertEqual('Reading', result['asmt_claim_1_name'])
        self.assertEqual('Writing', result['asmt_claim_2_name'])
        self.assertEqual('Speaking & Listening', result['asmt_claim_3_name'])
        self.assertEqual('Research & Inquiry', result['asmt_claim_4_name'])
if __name__ == '__main__':
    unittest.main()
