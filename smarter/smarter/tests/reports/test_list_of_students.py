'''
Created on Feb 4, 2013

@author: tosako
'''
import unittest
from smarter.reports.list_of_students_report import get_list_of_students_report
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite


class TestLOS(Unittest_with_smarter_sqlite):

    def test_assessments(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = 3
        testParam['stateId'] = 'NY'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('cutpoints' in results, "returning JSON must have cutpoints")
        self.assertTrue('assessments' in results, "returning JSON must have assessments")

        cutpoints = results['cutpoints']
        self.assertEqual(2, len(cutpoints), "cutpoints are ELA and MATH")
        self.assertTrue('ELA' in cutpoints, 'ELA')
        self.assertTrue('Math' in cutpoints, 'Math')

        assessments = results['assessments']
        self.assertEqual(35, len(assessments), "35 assessments")
        self.assertEqual("Verda", assessments[9]['student_first_name'], "student_first_name")
        self.assertEqual("Lettie", assessments[10]['student_first_name'], "student_first_name")
        self.assertEqual("Mi-Ha", assessments[29]['student_first_name'], "student_first_name")

    def test_breadcrumbs(self):
        testParam = {}
        testParam['stateId'] = 'NY'
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = 3
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('context' in results, "returning JSON must have context")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
