from DataGeneration.src.models.helper_entities import State, District, School, Claim, ClaimScore, AssessmentScore
from uuid import uuid4
import DataGeneration.src.utils.util as util


def generate_state(state_name, state_code, districts=None):
    '''
    Generate a state based on name and code
    @param state_name: The name of the state. (ie. Kansas)
    @param state_code: The code for the state. (ie. KS)
    @return: A State object
    '''
    return State(state_name, state_code, districts)


def generate_district(name_list_1, name_list_2, district_population=None):
    '''
    Generate a district
    @param name_list_1: The list of names to use for naming
    @param name_list_2: The 2nd list of names to use for naming
    @return: A District object
    '''
    district_id = district_population.guid if district_population else uuid4()
    district_name = util.generate_district_name(name_list_1, name_list_2)
    if district_population:
        return District(district_id, district_name, district_population.district_type, district_population.schools)
    return District(district_id, district_name)


def generate_school(school_type, name_list_1, name_list_2, grade_performance_level_counts=None, district_name=None, district_id=None):
    '''
    Generate a school
    @param school_type: The type of school. (ie. Middle)
    @param name_list_1: The list of names to use for naming
    @param name_list_2: The 2nd list of names to use for naming
    @return: A School object
    '''
    school_id = uuid4()
    school_name = util.generate_school_name(school_type, name_list_1, name_list_2)
    return School(school_id, school_name, school_type, grade_performance_level_counts, district_name, district_id)


# TODO: Remove this function and just use constructor directly
def generate_claim(claim_name, claim_score_min, claim_score_max, claim_score_weight):
    ''' Generate a Claim'''
    return Claim(claim_name, claim_score_min, claim_score_max, claim_score_weight)


# TODO: Remove this function and just use constructor directly
def generate_assessment_score(overall_score, perf_lvl, interval_min, interval_max, claim_scores, asmt_create_date):
    ''' Generate an AssessmentScore '''
    return AssessmentScore(overall_score, perf_lvl, interval_min, interval_max, claim_scores, asmt_create_date)


# TODO: Remove this function and just use constructor directly
def generate_claim_score(claim_score, claim_score_interval_minimum, claim_score_interval_maximum, perf_level):
    ''' Generate a ClaimScore '''
    return ClaimScore(claim_score, claim_score_interval_minimum, claim_score_interval_maximum, perf_level)
