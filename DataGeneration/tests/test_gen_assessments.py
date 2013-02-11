'''
Created on Feb 11, 2013

@author: swimberly
'''
import unittest

import gen_assessments as genasmt
from constants import MIN_ASSMT_SCORE, MAX_ASSMT_SCORE


class Test(unittest.TestCase):

    def test_generate_assessment_types(self):
        expect_asmt_num = 13 * 2 * 4  # 13 grades X 2 subjects X 4 assessments per subject (3 interim, 1 summative)
        result = genasmt.generate_assessment_types()

        self.assertEqual(len(result), expect_asmt_num)
        self.assertEqual(len(genasmt.ASSESSMENT_TYPES_LIST), expect_asmt_num)

    def test_generate_single_asmt(self):
        asmt = genasmt.generate_single_asmt(10, 'INTERIM', 'BOY', 'ELA')

        self.assertIsNotNone(asmt.asmt_id)
        self.assertIsNotNone(asmt.asmt_external_id)
        self.assertEqual(asmt.asmt_grade, 10)
        self.assertEqual(asmt.asmt_period, 'BOY')
        self.assertEqual(asmt.asmt_subject, 'ELA')
        self.assertEqual(asmt.asmt_type, 'INTERIM')
        self.assertIsNotNone(asmt.asmt_period_year)
        self.assertIsNotNone(asmt.asmt_version)
        self.assertLess(asmt.asmt_cut_point_1, MAX_ASSMT_SCORE)
        self.assertGreater(asmt.asmt_cut_point_1, MIN_ASSMT_SCORE)
        self.assertLess(asmt.asmt_cut_point_2, MAX_ASSMT_SCORE)
        self.assertGreater(asmt.asmt_cut_point_2, MIN_ASSMT_SCORE)
        self.assertLess(asmt.asmt_cut_point_3, MAX_ASSMT_SCORE)
        self.assertGreater(asmt.asmt_cut_point_3, MIN_ASSMT_SCORE)

    def test_generate_id(self):
        res = genasmt.generate_id()

        self.assertIsNotNone(res)
        self.assertIsInstance(res, int)

    def test_generate_version(self):
        res = genasmt.generate_version()

        self.assertIsNotNone(res)

    def test_calc_claim_min_max(self):
        res = genasmt.calc_claim_min_max(100, 500, 10)

        self.assertEqual(res[0], 10)
        self.assertEqual(res[1], 50)

        res = genasmt.calc_claim_min_max(100, 500, 40)

        self.assertEqual(res[0], int(100 * .4))
        self.assertEqual(res[1], int(500 * .4))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
