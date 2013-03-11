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
        testParam[Constants.DISTRICTID] = 'd1'
        testParam[Constants.SCHOOLID] = 'sc1'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.COLORS in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check grade-level results
        records = results[Constants.RECORDS]
        self.assertEqual(1, len(records), "1 grade in the list")
        self.assertEqual('1', records[0][Constants.ID])
        self.assertEqual('1', records[0][Constants.NAME])
        asmt_results = records[0][Constants.RESULTS]
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results[Constants.SUBJECT1]
        self.assertEqual(3, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(0, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(0, intervals[0][Constants.COUNT])
        subject2 = asmt_results[Constants.SUBJECT2]
        self.assertEqual(3, subject2[Constants.TOTAL])
        self.assertEqual(Constants.ELA, subject2[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject2[Constants.INTERVALS]))
        intervals = subject2[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(67, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(3, len(context_items))
        self.assertEqual('NY', context_items[0][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[1][Constants.NAME])
        self.assertEqual('Sunset Central High', context_items[2][Constants.NAME])

        # check summary results
        summ_results = results[Constants.SUMMARY][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(3, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject1[Constants.INTERVALS]))
        subject2 = summ_results[Constants.SUBJECT2]
        self.assertEqual(3, subject2[Constants.TOTAL])
        self.assertEqual(Constants.ELA, subject2[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject2[Constants.INTERVALS]))
        intervals = subject2[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(67, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check colors
        self.assertTrue('text_color' in results[Constants.COLORS][Constants.SUBJECT1])
        self.assertTrue('bg_color' in results[Constants.COLORS][Constants.SUBJECT1])

    def test_district_view(self):
        testParam = {}
        testParam[Constants.STATEID] = 'NY'
        testParam[Constants.DISTRICTID] = 'd1'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.COLORS in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check grade-level results
        records = results[Constants.RECORDS]
        self.assertEqual(1, len(records), "1 school in the list")
        self.assertEqual('sc1', records[0][Constants.ID])
        self.assertEqual('Sunset Central High', records[0][Constants.NAME])
        asmt_results = records[0][Constants.RESULTS]
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results[Constants.SUBJECT1]
        self.assertEqual(3, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(0, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(0, intervals[0][Constants.COUNT])
        subject2 = asmt_results[Constants.SUBJECT2]
        self.assertEqual(3, subject2[Constants.TOTAL])
        self.assertEqual(Constants.ELA, subject2[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject2[Constants.INTERVALS]))
        intervals = subject2[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(67, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(2, len(context_items))
        self.assertEqual('NY', context_items[0][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[1][Constants.NAME])

        # check summary results
        summ_results = results[Constants.SUMMARY][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(3, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject1[Constants.INTERVALS]))
        subject2 = summ_results[Constants.SUBJECT2]
        self.assertEqual(3, subject2[Constants.TOTAL])
        self.assertEqual(Constants.ELA, subject2[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject2[Constants.INTERVALS]))
        intervals = subject2[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(67, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check colors
        self.assertTrue('text_color' in results[Constants.COLORS][Constants.SUBJECT1])
        self.assertTrue('bg_color' in results[Constants.COLORS][Constants.SUBJECT1])

    def test_state_view(self):
        testParam = {}
        testParam[Constants.STATEID] = 'NY'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.COLORS in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check grade-level results
        records = results[Constants.RECORDS]
        self.assertEqual(1, len(records), "1 district in the list")
        self.assertEqual('d1', records[0][Constants.ID])
        self.assertEqual('Sunset School District', records[0][Constants.NAME])
        asmt_results = records[0][Constants.RESULTS]
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results[Constants.SUBJECT1]
        self.assertEqual(3, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(0, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(0, intervals[0][Constants.COUNT])
        subject2 = asmt_results[Constants.SUBJECT2]
        self.assertEqual(3, subject2[Constants.TOTAL])
        self.assertEqual(Constants.ELA, subject2[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject2[Constants.INTERVALS]))
        intervals = subject2[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(67, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(1, len(context_items))
        self.assertEqual('NY', context_items[0][Constants.NAME])

        # check summary results
        summ_results = results[Constants.SUMMARY][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(3, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject1[Constants.INTERVALS]))
        subject2 = summ_results[Constants.SUBJECT2]
        self.assertEqual(3, subject2[Constants.TOTAL])
        self.assertEqual(Constants.ELA, subject2[Constants.ASMT_SUBJECT])
        self.assertEqual(5, len(subject2[Constants.INTERVALS]))
        intervals = subject2[Constants.INTERVALS]
        self.assertEqual(5, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(67, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check colors
        self.assertTrue('text_color' in results[Constants.COLORS][Constants.SUBJECT1])
        self.assertTrue('bg_color' in results[Constants.COLORS][Constants.SUBJECT1])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
