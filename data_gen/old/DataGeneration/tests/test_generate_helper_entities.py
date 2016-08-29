__author__ = 'abrien'

import unittest
from DataGeneration.src.generators.generate_helper_entities import generate_state, generate_school, generate_claim, generate_district, \
    generate_assessment_score, generate_claim_score
from DataGeneration.src.models.helper_entities import ClaimScore
from uuid import UUID
from datetime import date


class TestGenerateHelperEntities(unittest.TestCase):

    def test_generate_state(self):
        state_name = 'North Carolina'
        state_code = 'NC'
        new_york_state = generate_state(state_name, state_code)
        self.assertEquals(new_york_state.state_name, state_name)
        self.assertEquals(new_york_state.state_code, state_code)

    def test_generate_district(self):
        name_list_1 = ['banana', 'apple', 'pear']
        name_list_2 = ['carrot', 'potato', 'celery']
        food_district = generate_district(name_list_1, name_list_2)
        component_words = food_district.district_name.split()
        first_word = component_words[0]
        second_word = component_words[1]
        self.assertIn(first_word, name_list_1)
        self.assertIn(second_word, name_list_2)
        self.assertIsInstance(food_district.district_id, UUID)

    def test_generate_school(self):
        school_type = 'High School'
        name_list_1 = ['honda', 'ford', 'toyota']
        name_list_2 = ['subaru', 'bmw', 'mercedes']
        car_school = generate_school(school_type, name_list_1, name_list_2)
        component_words = car_school.school_name.split()
        first_word = component_words[0]
        second_word = component_words[1]
        self.assertIn(first_word, name_list_1)
        self.assertIn(second_word, name_list_2)
        self.assertIsInstance(car_school.school_id, UUID)

    def test_generate_claim(self):
        claim_name = 'claim_1'
        claim_score_min = 10
        claim_score_max = 55
        claim_score_weight = .5
        test_claim = generate_claim(claim_name, claim_score_min, claim_score_max, claim_score_weight)
        self.assertEquals(test_claim.claim_name, claim_name)
        self.assertEquals(test_claim.claim_score_min, claim_score_min)
        self.assertEquals(test_claim.claim_score_max, claim_score_max)
        self.assertEquals(test_claim.claim_score_weight, claim_score_weight)

    def test_generate_assessment_score(self):
        overall_score = 1800
        perf_lvl = 2
        interval_min = 1700
        interval_max = 1900
        asmt_create_date = date(2013, 4, 24)

        claim_score_val_1 = 1800
        claim_score_1_interval_minimum = 1700
        claim_score_1_interval_maximum = 1900
        perf_lvl_1 = 2
        claim_score_1 = ClaimScore(claim_score_val_1, claim_score_1_interval_minimum,
                                   claim_score_1_interval_maximum, perf_lvl_1)

        claim_score_val_2 = 1900
        claim_score_2_interval_minimum = 1800
        claim_score_2_interval_maximum = 2000
        perf_lvl_2 = 2
        claim_score_2 = ClaimScore(claim_score_val_2, claim_score_2_interval_minimum,
                                   claim_score_2_interval_maximum, perf_lvl_2)

        claim_score_val_3 = 1900
        claim_score_3_interval_minimum = 1800
        claim_score_3_interval_maximum = 2000
        perf_lvl_3 = 2
        claim_score_3 = ClaimScore(claim_score_val_3, claim_score_3_interval_minimum,
                                   claim_score_3_interval_maximum, perf_lvl_3)

        claim_scores = [claim_score_1, claim_score_2, claim_score_3]
        assessment_score = generate_assessment_score(overall_score, perf_lvl, interval_min, interval_max,
                                                     claim_scores, asmt_create_date)

        #self.assertIsInstance(assessment_score, AssessmentScore)
        self.assertEquals(assessment_score.overall_score, overall_score)
        self.assertEquals(assessment_score.perf_lvl, perf_lvl)
        self.assertEquals(assessment_score.interval_min, interval_min)
        self.assertEquals(assessment_score.interval_max, interval_max)
        self.assertEquals(assessment_score.claim_scores, claim_scores)
        self.assertEquals(assessment_score.asmt_create_date, asmt_create_date)

    def test_generate_claim_score(self):
        claim_score_value = 1950
        claim_score_interval_minimum = 1850
        claim_score_interval_maximum = 2050
        perf_lvl = 2
        claim_score = generate_claim_score(claim_score_value, claim_score_interval_minimum, claim_score_interval_maximum, perf_lvl)
