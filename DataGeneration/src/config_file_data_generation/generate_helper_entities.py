from helper_entities_2 import State, District, School
from idgen import IdGen
from uuid import uuid4
import gennames
import util_2 as util

def generate_state(state_name, state_code, districts=None):
    return State(state_name, state_code, districts)

def generate_district():
    id_generator = IdGen()
    district_guid = id_generator.get_id()
    # TODO: Implement generate_name_from_lists(list_1, list_2)
    district_name = util.generate_name_from_lists(None, None)
    return District(district_guid, district_name)

def generate_school(school_category):
    id_generator = IdGen()
    school_guid = id_generator.get_id()
    # TODO: Implement generate_name_from_lists(list_1, list_2)
    school_name = util.generate_name_from_lists(None, None)
    return School(school_guid, school_name, school_category)