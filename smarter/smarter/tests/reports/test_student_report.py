'''
Created on Jan 17, 2013

@author: tosako
'''

import unittest
from smarter.reports.student_report import get_student_report, \
    get_student_assessment
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
import json


class TestStudentReport(Unittest_with_sqlite):

    def test_student_report(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567', "assessmentId": 1}
        result = get_student_report(params)['items']
        self.assertEqual(1, len(result), "studentId should have 1 report")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject')
        self.assertEqual(88, result[0]['asmt_claim_1_score'], 'asmt_claim_1_score 88')
        self.assertEqual('Research', result[0]['asmt_claim_4_name'], 'asmt_claim_4_name Spelling')

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
        self.assertEqual('Lili', student_report['teacher_first_name'], 'teacher first name should be Lili')
        self.assertEqual('M', student_report['teacher_middle_name'], 'teacher middle name should be M')
        self.assertEqual('Chen', student_report['teacher_last_name'], 'teacher last name should be Chen')
        self.assertEqual(1, student_report['date_taken_day'])
        self.assertEqual(1, student_report['date_taken_month'])
        self.assertEqual(2013, student_report['date_taken_year'])

    def test_custom_metadata(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_report(params)['items']
        student_report = result[0]

        cut_points_list = student_report['cut_points']
        self.assertEqual(4, len(cut_points_list), "we should have 4 cut points")

        for cut_point in cut_points_list:
            self.assertIsInstance(cut_point, dict, "each cut point should be a dictionary")

            keys = cut_point.keys()
            self.assertIn("name", keys, "should contain the name of the cut point")
            self.assertIn("cut_point", keys, "should contain the value of the cut point")
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


if __name__ == '__main__':
    unittest.main()
