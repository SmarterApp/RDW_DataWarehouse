'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.compare_pop_report import get_comparing_populations_report
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.reports.helpers.constants import Constants


class TestComparingPopulations(Unittest_with_smarter_sqlite):

    def test_school_view(self):
        testParam = {}
        testParam[Constants.STATEID] = 'NY'
        testParam[Constants.DISTRICTID] = '228'
        testParam[Constants.SCHOOLID] = '242'
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
        self.assertEqual('3', records[0][Constants.ID])
        self.assertEqual('Grade 3', records[0][Constants.NAME])
        asmt_results = records[0][Constants.RESULTS]
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results[Constants.SUBJECT1]
        self.assertEqual(35, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(11, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(4, intervals[0][Constants.COUNT])

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(35, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(11, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(4, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(3, len(context_items))
        self.assertEqual('New York', context_items[0][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[1][Constants.NAME])
        self.assertEqual('Sunset - Eastern Elementary', context_items[2][Constants.NAME])

        # check colors
        self.assertTrue('text_color' in results[Constants.COLORS][Constants.SUBJECT1])
        self.assertTrue('bg_color' in results[Constants.COLORS][Constants.SUBJECT1])

    def test_district_view(self):
        testParam = {}
        testParam[Constants.STATEID] = 'NY'
        testParam[Constants.DISTRICTID] = '228'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.COLORS in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check school-level results
        records = results[Constants.RECORDS]
        self.assertEqual(3, len(records), "3 schools in the list")
        found_school = False
        for record in records:
            if record[Constants.ID] == '242':
                found_school = True
                self.assertEqual('Sunset - Eastern Elementary', record[Constants.NAME])
                asmt_results = record[Constants.RESULTS]
                self.assertEqual(2, len(asmt_results))
                subject1 = asmt_results[Constants.SUBJECT1]
                self.assertEqual(35, subject1[Constants.TOTAL])
                self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
                intervals = subject1[Constants.INTERVALS]
                self.assertEqual(4, len(intervals))
                self.assertEqual(1, intervals[0][Constants.LEVEL])
                self.assertEqual(11, intervals[0][Constants.PERCENTAGE])
                self.assertEqual(4, intervals[0][Constants.COUNT])
                break
        self.assertTrue(found_school, 'Did not find school in list')

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(51, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(16, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(8, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(2, len(context_items))
        self.assertEqual('New York', context_items[0][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[1][Constants.NAME])

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

        # check district-level results
        records = results[Constants.RECORDS]
        self.assertEqual(2, len(records), "2 districts in the list")
        found_district = False
        for record in records:
            if record[Constants.ID] == '228':
                found_district = True
                self.assertEqual('Sunset School District', record[Constants.NAME])
                asmt_results = record[Constants.RESULTS]
                self.assertEqual(2, len(asmt_results))
                subject1 = asmt_results[Constants.SUBJECT1]
                self.assertEqual(51, subject1[Constants.TOTAL])
                self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
                intervals = subject1[Constants.INTERVALS]
                self.assertEqual(4, len(intervals))
                self.assertEqual(1, intervals[0][Constants.LEVEL])
                self.assertEqual(16, intervals[0][Constants.PERCENTAGE])
                self.assertEqual(8, intervals[0][Constants.COUNT])
                break
        self.assertTrue(found_district, 'Did not find district in list')

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(79, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(15, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(12, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(1, len(context_items))
        self.assertEqual('New York', context_items[0][Constants.NAME])

        # check colors
        self.assertTrue('text_color' in results[Constants.COLORS][Constants.SUBJECT1])
        self.assertTrue('bg_color' in results[Constants.COLORS][Constants.SUBJECT1])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
