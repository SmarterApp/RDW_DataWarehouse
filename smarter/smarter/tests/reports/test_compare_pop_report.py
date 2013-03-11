'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.compare_pop_report import get_comparing_populations_report, Constants
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite


class TestComparingPopulations(Unittest_with_smarter_sqlite):

    def test_school_view(self):
        testParam = {}
        testParam[Constants.STATEID] = 'NY'
        testParam['districtId'] = 'd1'
        testParam['schoolId'] = 'sc1'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue('records' in results, "returning JSON must have records")
        self.assertTrue('colors' in results, "returning JSON must have colors")
        self.assertTrue('subjects' in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue('summary' in results, "returning JSON must have summary")

        # check grade-level results
        records = results['records']
        self.assertEqual(1, len(records), "1 grade in the list")
        self.assertEqual('1', records[0]['id'])
        self.assertEqual('1', records[0]['name'])
        asmt_results = records[0]['results']
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        intervals = subject1['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(0, intervals[0]['percentage'])
        self.assertEqual(0, intervals[0]['count'])
        subject2 = asmt_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))
        intervals = subject2['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(67, intervals[0]['percentage'])
        self.assertEqual(2, intervals[0]['count'])

        # check subjects
        self.assertEqual('Math', results['subjects']['subject1'])
        self.assertEqual('ELA', results['subjects']['subject2'])

        # check context
        context_items = results['context']['items']
        self.assertEqual(3, len(context_items))
        self.assertEqual('NY', context_items[0]['name'])
        self.assertEqual('Sunset School District', context_items[1]['name'])
        self.assertEqual('Sunset Central High', context_items[2]['name'])

        # check summary results
        summ_results = results['summary']['results']
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        self.assertEqual(5, len(subject1['intervals']))
        subject2 = summ_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))
        intervals = subject2['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(67, intervals[0]['percentage'])
        self.assertEqual(2, intervals[0]['count'])

        # check colors
        self.assertTrue('text_color' in results['colors']['subject1'])
        self.assertTrue('bg_color' in results['colors']['subject1'])

    def test_district_view(self):
        testParam = {}
        testParam['stateId'] = 'NY'
        testParam['districtId'] = 'd1'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue('records' in results, "returning JSON must have records")
        self.assertTrue('colors' in results, "returning JSON must have colors")
        self.assertTrue('subjects' in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue('summary' in results, "returning JSON must have summary")

        # check grade-level results
        records = results['records']
        self.assertEqual(1, len(records), "1 school in the list")
        self.assertEqual('sc1', records[0]['id'])
        self.assertEqual('Sunset Central High', records[0]['name'])
        asmt_results = records[0]['results']
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        intervals = subject1['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(0, intervals[0]['percentage'])
        self.assertEqual(0, intervals[0]['count'])
        subject2 = asmt_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))
        intervals = subject2['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(67, intervals[0]['percentage'])
        self.assertEqual(2, intervals[0]['count'])

        # check subjects
        self.assertEqual('Math', results['subjects']['subject1'])
        self.assertEqual('ELA', results['subjects']['subject2'])

        # check context
        context_items = results['context']['items']
        self.assertEqual(2, len(context_items))
        self.assertEqual('NY', context_items[0]['name'])
        self.assertEqual('Sunset School District', context_items[1]['name'])

        # check summary results
        summ_results = results['summary']['results']
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        self.assertEqual(5, len(subject1['intervals']))
        subject2 = summ_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))
        intervals = subject2['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(67, intervals[0]['percentage'])
        self.assertEqual(2, intervals[0]['count'])

        # check colors
        self.assertTrue('text_color' in results['colors']['subject1'])
        self.assertTrue('bg_color' in results['colors']['subject1'])

    def test_state_view(self):
        testParam = {}
        testParam['stateId'] = 'NY'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue('records' in results, "returning JSON must have records")
        self.assertTrue('colors' in results, "returning JSON must have colors")
        self.assertTrue('subjects' in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue('summary' in results, "returning JSON must have summary")

        # check grade-level results
        records = results['records']
        self.assertEqual(1, len(records), "1 district in the list")
        self.assertEqual('d1', records[0]['id'])
        self.assertEqual('Sunset School District', records[0]['name'])
        asmt_results = records[0]['results']
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        intervals = subject1['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(0, intervals[0]['percentage'])
        self.assertEqual(0, intervals[0]['count'])
        subject2 = asmt_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))
        intervals = subject2['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(67, intervals[0]['percentage'])
        self.assertEqual(2, intervals[0]['count'])

        # check subjects
        self.assertEqual('Math', results['subjects']['subject1'])
        self.assertEqual('ELA', results['subjects']['subject2'])

        # check context
        context_items = results['context']['items']
        self.assertEqual(1, len(context_items))
        self.assertEqual('NY', context_items[0]['name'])

        # check summary results
        summ_results = results['summary']['results']
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results['subject1']
        self.assertEqual(3, subject1['total'])
        self.assertEqual('Math', subject1['asmt_subject'])
        self.assertEqual(5, len(subject1['intervals']))
        subject2 = summ_results['subject2']
        self.assertEqual(3, subject2['total'])
        self.assertEqual('ELA', subject2['asmt_subject'])
        self.assertEqual(5, len(subject2['intervals']))
        intervals = subject2['intervals']
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0]['level'])
        self.assertEqual(67, intervals[0]['percentage'])
        self.assertEqual(2, intervals[0]['count'])

        # check colors
        self.assertTrue('text_color' in results['colors']['subject1'])
        self.assertTrue('bg_color' in results['colors']['subject1'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
