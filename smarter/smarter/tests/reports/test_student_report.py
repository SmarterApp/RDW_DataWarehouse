'''
Created on Jan 17, 2013

@author: tosako
'''

import unittest
from smarter.reports.student_report import get_student_report, \
    get_student_assessment
from database.tests.unittest_with_sqlite import Unittest_with_sqlite


class TestStudentReport(Unittest_with_sqlite):

    def test_student_report(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567', "assessmentId": 1}
        result = get_student_report(params)['items']
        self.assertEqual(1, len(result), "studentId should have 1 report")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject')
        self.assertEqual(447, result[0]['asmt_claim_1_score'], 'asmt_claim_1_score 400')
        self.assertEqual('Spelling', result[0]['asmt_claim_4_name'], 'asmt_claim_4_name Spelling')

    def test_student_assessment_id(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_assessment(params)

        self.assertEqual(2, len(result), "studentId should have 2 assessments")
        self.assertEqual('ELA', result[0]['asmt_subject'], 'asmt_subject ELA')
        self.assertEqual('MATH', result[1]['asmt_subject'], 'asmt_subject MATH')

    def test_assessment_header_info(self):
        params = {"studentId": '286ee893-dad0-4833-ae6c-adef78a11567'}
        result = get_student_report(params)['items']
        student_report = result[0]

        self.assertEqual('MATH', student_report['asmt_subject'], 'asmt_subject')
        self.assertEqual('Lili', student_report['teacher_first_name'], 'teacher first name should be Lili')
        self.assertEqual('M', student_report['teacher_middle_name'], 'teacher middle name should be M')
        self.assertEqual('Chen', student_report['teacher_last_name'], 'teacher last name should be Chen')
        self.assertEqual(1, student_report['date_taken_day'])
        self.assertEqual(1, student_report['date_taken_month'])
        self.assertEqual(2013, student_report['date_taken_year'])

if __name__ == '__main__':
    unittest.main()
