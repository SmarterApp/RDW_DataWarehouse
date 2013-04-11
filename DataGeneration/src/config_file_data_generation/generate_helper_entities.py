from helper_entities_2 import State, District, School
from idgen import IdGen
from uuid import uuid4
import gennames
import util_2 as util

def generate_state(state_name, state_code, districts=None):
    return State(state_name, state_code, districts)

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