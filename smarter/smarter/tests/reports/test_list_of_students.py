'''
Created on Feb 4, 2013

@author: tosako
'''
import unittest
from smarter.reports.list_of_students_report import get_list_of_students_report
from database.tests.unittest_with_sqlite import Unittest_with_sqlite


class Test(Unittest_with_sqlite):

    def testReport(self):
        testParam = {}
        testParam['districtId'] = 1
        testParam['schoolId'] = 1
        testParam['asmtGrade'] = 1
        testParam['asmtSubject'] = ['ELA', 'MATH']
        results = get_list_of_students_report(testParam)

        self.assertTrue('cutpoints' in results, "returning JSON must have cutpoints")
        self.assertTrue('assessments' in results, "returning JSON must have assessments")

        cutpoints = results['cutpoints']
        self.assertEqual(2, len(cutpoints), "cutpoints are ELA and MATH")
        self.assertTrue('ELA' in cutpoints, 'ELA')
        self.assertTrue('MATH' in cutpoints, 'MATH')

        assessments = results['assessments']
        self.assertEqual(3, len(assessments), "3 assessments")
        self.assertEqual("Adam", assessments[0]['student_first_name'], "student_first_name")
        self.assertEqual("Doris", assessments[1]['student_first_name'], "student_first_name")
        self.assertEqual("Takashi", assessments[2]['student_first_name'], "student_first_name")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
