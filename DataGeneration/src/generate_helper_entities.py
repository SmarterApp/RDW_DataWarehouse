from helper_entities_2 import State, District, School, Claim, ClaimScore, AssessmentScore
from uuid import uuid4
import util_2 as util


def generate_state(state_name, state_code):
    return State(state_name, state_code)


def generate_district(name_list_1, name_list_2):
    district_guid = uuid4()
    district_name = util.generate_district_name(name_list_1, name_list_2)
    return District(district_guid, district_name)


def generate_school(school_type, name_list_1, name_list_2):
    school_guid = uuid4()
    school_name = util.generate_school_name(school_type, name_list_1, name_list_2)
    return School(school_guid, school_name, school_type)


def generate_claim(claim_name, claim_score_min, claim_score_max, claim_score_weight):
    return Claim(claim_name, claim_score_min, claim_score_max, claim_score_weight)


def generate_assessment_score(overall_score, perf_lvl, interval_min, interval_max, claim_scores, asmt_create_date):
    return AssessmentScore(overall_score, perf_lvl, interval_min, interval_max, claim_scores, asmt_create_date)


def generate_claim_score(claim_score, claim_score_interval_minimum, claim_score_interval_maximum):
    return ClaimScore(claim_score, claim_score_interval_minimum, claim_score_interval_maximum)
