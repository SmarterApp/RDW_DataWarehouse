'''
Created on Feb 11, 2013

@author: swimberly
'''
import unittest

import gen_assessments as genasmt


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

    def test_generate_id(self):
        res = genasmt.generate_id()

        self.assertIsNotNone(res)
        self.assertIsInstance(res, int)

    def test_generate_version(self):
        res = genasmt.generate_version()

        self.assertIsNotNone(res)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
