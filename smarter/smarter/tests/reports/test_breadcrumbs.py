'''
Created on Mar 8, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context


class TestContext(Unittest_with_smarter_sqlite):

    def testStateContext(self):
        results = get_breadcrumbs_context()
        self.assertEqual(len(results['items']), 1)
        self.assertEqual(results['items'][0]['name'], 'New York')
        self.assertEqual(results['items'][0]['id'], 'NY')
        self.assertEqual(results['items'][0]['type'], 'state')

    def testExplicitStateContext(self):
        results = get_breadcrumbs_context(state_guid='NY')
        self.assertEqual(len(results['items']), 1)
        self.assertEqual(results['items'][0]['name'], 'New York')
        self.assertEqual(results['items'][0]['id'], 'NY')
        self.assertEqual(results['items'][0]['type'], 'state')

    def testDistrictContext(self):
        results = get_breadcrumbs_context(district_guid='228')
        self.assertEqual(len(results['items']), 2)
        self.assertEqual(results['items'][0]['name'], 'New York')
        self.assertEqual(results['items'][0]['type'], 'state')
        self.assertEqual(results['items'][1]['name'], 'Sunset School District')
        self.assertEqual(results['items'][1]['type'], 'district')
        self.assertEqual(results['items'][1]['id'], '228')

    def testSchoolContext(self):
        results = get_breadcrumbs_context(district_guid='228', school_guid='242')
        self.assertEqual(len(results['items']), 3)
        self.assertEqual(results['items'][0]['name'], 'New York')
        self.assertEqual(results['items'][1]['name'], 'Sunset School District')
        self.assertEqual(results['items'][2]['name'], 'Sunset - Eastern Elementary')
        self.assertEqual(results['items'][2]['id'], '242')
        self.assertEqual(results['items'][2]['type'], 'school')

    def testGradeContext(self):
        results = get_breadcrumbs_context(district_guid='228', school_guid='242', asmt_grade='3')
        self.assertEqual(len(results['items']), 4)
        self.assertEqual(results['items'][3]['name'], '3')
        self.assertEqual(results['items'][3]['id'], '3')
        self.assertEqual(results['items'][3]['type'], 'grade')

    def testStudentContext(self):
        results = get_breadcrumbs_context(district_guid='228', school_guid='242', asmt_grade='3', student_name='StudentName')
        self.assertEqual(len(results['items']), 5)
        self.assertEqual(results['items'][4]['name'], 'StudentName')
        self.assertEqual(results['items'][4]['type'], 'student')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
