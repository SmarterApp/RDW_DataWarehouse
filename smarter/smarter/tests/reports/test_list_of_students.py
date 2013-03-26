'''
Created on Feb 4, 2013

@author: tosako
'''
import unittest
from smarter.reports.list_of_students_report import get_list_of_students_report
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from edapi.exceptions import NotFoundException


class TestLOS(Unittest_with_smarter_sqlite):

    def test_assessments(self):
        testParam = {}
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = 3
        testParam['stateCode'] = 'NY'
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
        self.assertEqual(35, len(assessments), "35 assessments")
        self.assertEqual("Verda", assessments[9]['student_first_name'], "student_first_name")
        self.assertEqual("Lettie", assessments[10]['student_first_name'], "student_first_name")
        self.assertEqual("Mi-Ha", assessments[29]['student_first_name'], "student_first_name")

    def test_breadcrumbs(self):
        testParam = {}
        testParam['stateCode'] = 'NY'
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = 3
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('context' in results, "returning JSON must have context")

    def test_ELA_only(self):
        testParam = {}
        testParam['districtId'] = '228'
        testParam['schoolId'] = '242'
        testParam['asmtGrade'] = 3
        testParam['stateId'] = 'NY'
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
        testParam['asmtGrade'] = 3
        testParam['stateId'] = 'NY'
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
        testParam['stateId'] = 'NY'
        testParam['asmtSubject'] = ['Dummy']
        self.assertRaises(NotFoundException, get_list_of_students_report, testParam)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
