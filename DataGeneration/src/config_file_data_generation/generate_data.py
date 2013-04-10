import argparse
import datetime
import os
from write_to_csv import create_csv
from importlib import import_module
from generate_entities import generate_institution_hierarchy
from generate_helper_entities import generate_state, generate_district, generate_school
from datetime import date


DATAFILE_PATH = str(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

INSTITUTION_HIERARCHY_PATH =  DATAFILE_PATH + '/datafiles/csv/dim_inst_hier.csv'
SECTION_PATH = DATAFILE_PATH + '/datafiles/csv/dim_section.csv'
ASSESSMENT_PATH = DATAFILE_PATH + '/datafiles/csv/dim_asmt.csv'
ASSESSMENT_OUTCOME_PATH = DATAFILE_PATH + '/datafiles/csv/fact_asmt_outcome.csv'
STAFF_PATH = DATAFILE_PATH + '/datafiles/csv/dim_staff.csv'
EXTERNAL_USER_STUDENT_PATH = DATAFILE_PATH + '/datafiles/csv/external_user_student_rel.csv'
STUDENT_PATH = DATAFILE_PATH + '/datafiles/csv/dim_student.csv'

def generate_data_from_config_file(config_module):
    # Get information from the config module
    school_types = config_module.get_school_types()
    district_types = config_module.get_district_types()
    state_types = config_module.get_state_types()
    states = config_module.get_states()

    # Iterate over all the states we're supposed to create and add them to 'states_in_consortium'
    states_in_consortium = []
    for state in states:
        # Pull out basic state information
        state_name = state[config_module.NAME]
        state_code = state[config_module.STATE_CODE]

        # Create state object from gathered info
        current_state = generate_state(state_name, state_code)

        # Pull out information on districts within this state
        state_type_name = state[config_module.STATE_TYPE]
        state_type = state_types[state_type_name]
        district_types_and_counts = state_type[config_module.DISTRICT_TYPES_AND_COUNTS]

        # Create all the districts for the given state.
        # We don't have a state, district, or school table, but we have an institution_hierarchy table.
        # Each row of this table contains all state, district, and school information.

        # districts_by_type is a dictionary such that:
        # key: <string> The type of district
        # value: <list> A list of district objects
        districts_by_type = generate_district_dictionary(district_types_and_counts)
        districts_in_state = []

        for district_type_name in districts_by_type.keys():
            districts = districts_by_type[district_type_name]
            district_type = district_types[district_type_name]

            # Pull out school information for this type of district
            # Here we get info on the types of schools to create
            school_types_and_ratios = district_type[config_module.SCHOOL_TYPES_AND_RATIOS]

            # Here we get info on the number of schools to create
            school_counts = district_type[config_module.SCHOOL_COUNTS]

            schools_by_type = create_school_dictionary(school_counts, school_types_and_ratios)

            #for school_type_name in schools_by_type.keys():
                #schools = schools_by_type[school_type_name]
                #school_type = school_types[school_type_name]
                #students = generate_students_for_school(school_type)

            districts_in_state.append(districts)

        current_state.add_districts(districts_in_state)
        states_in_consortium.append(current_state)
    institution_hierarchies = transform_states_into_institution_hierarchies(states_in_consortium)
    create_csv(institution_hierarchies, INSTITUTION_HIERARCHY_PATH)

def generate_district_dictionary(district_types_and_counts):
    district_dictionary = {}
    for district_type in district_types_and_counts:
        district_count = district_types_and_counts[district_type]
        district_list = []
        for i in range(district_count):
            district = generate_district()
            district_list.append(district)
        district_dictionary[district_type] = district_list
    return district_dictionary

def create_school_dictionary(school_counts, school_types_and_ratios):
    num_schools_min = school_counts[config_module.MIN]
    num_schools_avg = school_counts[config_module.AVG]
    num_schools_max = school_counts[config_module.MAX]
    # TODO: Can we assume number of schools is a normal distribution?
    number_of_schools_in_district = calculate_number_of_schools(num_schools_min, num_schools_avg, num_schools_max)

    ratio_sum = sum(school_types_and_ratios.values())
    ratio_unit = max((number_of_schools_in_district // ratio_sum), 1)

    school_dictionary = {}
    for school_type_name in school_types_and_ratios:
        # Get the ratio so we can calculate the number of school types to create for each district
        school_type_ratio = school_types_and_ratios[school_type_name]
        number_of_schools_for_type = school_type_ratio * ratio_unit
        school_list = []
        for i in range(number_of_schools_for_type):
            school = generate_school(school_type_name)
            school_list.append(school)
        school_dictionary[school_type_name] = school_list
    return school_dictionary

def transform_states_into_institution_hierarchies(states_in_consortium):
    institution_hierarchies = []
    for state in states_in_consortium:
        state_name = state.state_name
        state_code = state.state_code
        districts = state.get_districts()
        for district in districts:
            district_name = district.district_name
            district_guid = district.district_guid
            schools = district.get_schools()
            for school in schools:
                school_name = school.school_name
                school_category = school.school_category
                school_guid = school.school_guid
                from_date = date.today
                most_recent = True
                institution_hierarchy = generate_institution_hierarchy(state_name, state_code,
                                                                       district_guid, district_name,
                                                                       school_guid, school_name,
                                                                       school_category, from_date, most_recent)
                institution_hierarchies.append(institution_hierarchy)
    return institution_hierarchies




if __name__ == '__main__':

    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate fixture data from a configuration file.')
    parser.add_argument('--config', dest='config_module', action='store', default='dg_types',
                        help='Specify the configuration module that informs that data creation process.', required=False)
    args = parser.parse_args()

    t1 = datetime.datetime.now()
    config_module = import_module(args.config_module)
    generate_data_from_config_file(config_module)
    t2 = datetime.datetime.now()

    print("data_generation starts ", t1)
    print("data_generation ends   ", t2)


