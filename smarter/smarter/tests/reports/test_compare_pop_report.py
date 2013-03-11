'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.compare_pop_report import get_comparing_populations_report
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite


class TestComparingPopulations(Unittest_with_smarter_sqlite):

    def test_school_view(self):
        testParam = {}
        testParam['stateId'] = 'NY'
        testParam['districtId'] = 'd1'
        testParam['schoolId'] = 'sc1'
        results = get_comparing_populations_report(testParam)

        self.assertTrue('records' in results, "returning JSON must have records")
        self.assertTrue('colors' in results, "returning JSON must have colors")
        self.assertTrue('subjects' in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue('summary' in results, "returning JSON must have summary")

        records = results['records']
        self.assertEqual(1, len(records), "1 school in the list")
        asmt_results = records[0]['results']
        self.assertEqual(2, len(asmt_results))
        self.assertTrue('subject1' in asmt_results)
        self.assertTrue('subject2' in asmt_results)
        self.assertTrue('subject3' not in asmt_results)
        subject1 = asmt_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        self.assertEqual(5, len(subject1['intervals']))
        subject2 = asmt_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))

        self.assertTrue('subject1' in results['subjects'])
        self.assertTrue('subject2' in results['subjects'])

        #self.assertEquals(2, len(results['context']['items']))

        records = results['records']
        self.assertEqual(1, len(records), "1 school in the list")
        summ_results = records[0]['results']
        self.assertEqual(2, len(summ_results))
        self.assertTrue('subject1' in summ_results)
        self.assertTrue('subject2' in summ_results)
        self.assertTrue('subject3' not in summ_results)
        subject1 = summ_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        self.assertEqual(5, len(subject1['intervals']))
        subject2 = summ_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
