import unittest
from DataGeneration.src.demographics.demographic_derived import derive_demographic
from DataGeneration.src.constants.constants import HISPANIC_CODE, TWO_OR_MORE_RACES_CODE


class TestDemographicDerived(unittest.TestCase):

    def test_derive_demographic_only_hispanic(self):
        demo_list = [False, False, True, False, False, False]
        actual_code = derive_demographic(demo_list)
        self.assertEqual(actual_code, HISPANIC_CODE)

    def test_derive_demographic_hispanic(self):
        demo_list = [False, True, True, True, False, False]
        actual_code = derive_demographic(demo_list)
        self.assertEqual(actual_code, HISPANIC_CODE)

    def test_derive_demographic_not_stated_all_false(self):
        demo_list = [False, False, False, False, False, False]
        actual_code = derive_demographic(demo_list)
        self.assertEqual(actual_code, 0)

    def test_derive_demographic_not_stated_false_and_none(self):
        demo_list = [None, False, False, None, False, False]
        actual_code = derive_demographic(demo_list)
        self.assertEqual(actual_code, 0)

    def test_derive_demographic_two_or_more_races(self):
        demo_list = [True, True, False, None, False, True]
        actual_code = derive_demographic(demo_list)
        self.assertEqual(actual_code, TWO_OR_MORE_RACES_CODE)

    def test_derive_demographic_exception(self):
        demo_list = []
        actual_code = derive_demographic(demo_list)
        self.assertEqual(actual_code, -1)
