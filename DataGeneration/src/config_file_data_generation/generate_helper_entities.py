from helper_entities_2 import State, District, School, Claim
from idgen import IdGen
from uuid import uuid4
import gennames
import util_2 as util


def generate_state(state_name, state_code):
    return State(state_name, state_code)


def generate_district(name_list_1, name_list_2):
    id_generator = IdGen()
    district_guid = id_generator.get_id()
    district_name = util.generate_district_name(name_list_1, name_list_2)
    return District(district_guid, district_name)


def generate_school(school_type, name_list_1, name_list_2):
    id_generator = IdGen()
    school_guid = id_generator.get_id()
    school_name = util.generate_school_name(school_type, name_list_1, name_list_2)
    return School(school_guid, school_name, school_type)


def generate_claim(claim_name, claim_score_min, claim_score_max, claim_score_weight):
    return Claim(claim_name, claim_score_min, claim_score_max, claim_score_weight)
