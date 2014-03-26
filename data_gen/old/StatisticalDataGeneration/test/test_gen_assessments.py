'''
Created on Feb 11, 2013

@author: swimberly

Test for gen_assessments.py
'''

import unittest

import gen_assessments as genasmt
from constants import MINIMUM_ASSESSMENT_SCORE, MAXIMUM_ASSESSMENT_SCORE, ASSMT_SCORE_YEARS


class Test(unittest.TestCase):

    def test_generate_assessment_types(self):
        # 13 grades X 2 subjects X 4 assessments per subject (3 interim, 1 summative) * number of years
        expect_asmt_num = 13 * 2 * 4 * len(ASSMT_SCORE_YEARS)
        result = genasmt.generate_dim_assessment()

        self.assertEqual(len(result), expect_asmt_num)

    def test_generate_single_asmt(self):
        asmt = genasmt.generate_single_asmt(10, 'INTERIM', 'BOY', 'ELA', 2012, True)

        self.assertIsNotNone(asmt.asmt_id)
        self.assertIsNotNone(asmt.asmt_rec_id)
        self.assertEqual(asmt.asmt_grade, 10)
        self.assertEqual(asmt.asmt_period, 'BOY')
        self.assertEqual(asmt.asmt_subject, 'ELA')
        self.assertEqual(asmt.asmt_type, 'INTERIM')
        self.assertEqual(asmt.asmt_period_year, 2012)
        self.assertIsNotNone(asmt.asmt_period_year)
        self.assertIsNotNone(asmt.asmt_version)
        self.assertLess(asmt.asmt_cut_point_1, MAXIMUM_ASSESSMENT_SCORE)
        self.assertGreater(asmt.asmt_cut_point_1, MINIMUM_ASSESSMENT_SCORE)
        self.assertLess(asmt.asmt_cut_point_2, MAXIMUM_ASSESSMENT_SCORE)
        self.assertGreater(asmt.asmt_cut_point_2, MINIMUM_ASSESSMENT_SCORE)
        self.assertLess(asmt.asmt_cut_point_3, MAXIMUM_ASSESSMENT_SCORE)
        self.assertGreater(asmt.asmt_cut_point_3, MINIMUM_ASSESSMENT_SCORE)

    def test_generate_id(self):
        res = genasmt.generate_id()

        self.assertIsNotNone(res)
        self.assertIsInstance(res, int)

    def test_generate_version(self):
        res = genasmt.generate_version()

        self.assertIsNotNone(res)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
