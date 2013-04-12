import argparse
import datetime
import os
import csv
import util_2
import constants_2 as constants
from write_to_csv import create_csv
from importlib import import_module
from generate_entities import generate_institution_hierarchy, generate_sections, generate_students, generate_multiple_staff
from generate_helper_entities import generate_state, generate_district, generate_school
from entities_2 import InstitutionHierarchy, Section, Assessment, AssessmentOutcome, \
    Staff, ExternalUserStudent, Student


DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
components = DATAFILE_PATH.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])

ENTITY_TO_PATH_DICT = {InstitutionHierarchy: DATAFILE_PATH + '/datafiles/csv/dim_inst_hier.csv',
                       Section: DATAFILE_PATH + '/datafiles/csv/dim_section.csv',
                       Assessment: DATAFILE_PATH + '/datafiles/csv/dim_asmt.csv',
                       AssessmentOutcome: DATAFILE_PATH + '/datafiles/csv/fact_asmt_outcome.csv',
                       Staff: DATAFILE_PATH + '/datafiles/csv/dim_staff.csv',
                       ExternalUserStudent: DATAFILE_PATH + '/datafiles/csv/external_user_student_rel.csv',
                       Student: DATAFILE_PATH + '/datafiles/csv/dim_student.csv'}

LAST_NAMES = 'last_names'
FEMALE_FIRST_NAMES = 'female_first_names'
MALE_FIRST_NAMES = 'male_first_names'
BIRDS = 'birds'
FISH = 'fish'
MAMMALS = 'mammals'

NAMES_TO_PATH_DICT = {BIRDS: DATAFILE_PATH + '/datafiles/name_lists/birds.txt',
                      FISH: DATAFILE_PATH + '/datafiles/name_lists/fish.txt',
                      MAMMALS: DATAFILE_PATH + '/datafiles/name_lists/mammals.txt'
                     }

def generate_data_from_config_file(config_module):
    # First thing: prep the csv files by deleting their contents and adding appropriate headers
    """

    :param config_module:
    """
    prepare_csv_files(ENTITY_TO_PATH_DICT)

    # Next, prepare lists that are used to name various entities
    name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)

    # We're going to use the birds and fish list to name our districts
    district_names_1 = name_list_dictionary[BIRDS]
    district_names_2 = name_list_dictionary[FISH]

    # We're going to use mammals and birds to names our schools
    school_names_1 = name_list_dictionary[MAMMALS]
    school_names_2 = name_list_dictionary[BIRDS]

    # Get information from the config module
    school_types = config_module.get_school_types()
    district_types = config_module.get_district_types()
    state_types = config_module.get_state_types()
    states = config_module.get_states()

    # Iterate over all the states we're supposed to create
    # When we get down to the school level, we'll be able to generate an InstitutionHierarchy object
    # And then we'll add it to institution_hierarchies
    institution_hierarchies = []
    for state in states:
        # Pull out basic state information
        state_name = state[config_module.NAME]
        state_code = state[config_module.STATE_CODE]

        # Create state object from gathered info
        current_state = generate_state(state_name, state_code)

        # TODO: should we add some randomness here? What are acceptable numbers? 5-10? 10-20?
        number_of_state_level_staff = 10
        # Add the state-level staff
        state_level_staff = generate_non_teaching_staff(number_of_state_level_staff, state_code=current_state.state_code)

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
        districts_by_type = generate_district_dictionary(district_types_and_counts, district_names_1, district_names_2)

        for district_type_name in districts_by_type.keys():
            districts = districts_by_type[district_type_name]
            district_type = district_types[district_type_name]

            # Pull out school information for this type of district
            # Here we get info on the types of schools to create
            school_types_and_ratios = district_type[config_module.SCHOOL_TYPES_AND_RATIOS]

            # Here we get info on the number of schools to create
            school_counts = district_type[config_module.SCHOOL_COUNTS]

            for district in districts:
                # TODO: should we add some randomness here? What are acceptable numbers? 5-10? 10-20?
                number_of_district_level_staff = 10
                district_level_staff = generate_non_teaching_staff(number_of_district_level_staff, state_code=current_state.state_code,
                                                                   district_guid=district.district_guid)
                schools_by_type = create_school_dictionary(school_counts, school_types_and_ratios, school_names_1, school_names_2)
                for school_type_name in schools_by_type.keys():
                    schools = schools_by_type[school_type_name]
                    school_type = school_types[school_type_name]
                    student_counts = school_type[config_module.STUDENTS]
                    student_min = student_counts[config_module.MIN]
                    student_max = student_counts[config_module.MAX]
                    student_avg = student_counts[config_module.AVG]
                    for school in schools:
                        institution_hierarchy = generate_institution_hierarchy_from_helper_entities(current_state, district, school)
                        institution_hierarchies.append(institution_hierarchy)
                        students_in_school = []
                        sections_in_school = []
                        staff_in_school = []
                        # TODO: should we add some randomness here? What are acceptable numbers? 5-10? 10-20?
                        number_of_school_level_staff = 5
                        school_level_staff = generate_non_teaching_staff(number_of_school_level_staff, state_code=current_state.state_code,
                                                                         district_guid=district.district_guid, school_guid=school.school_guid)
                        staff_in_school += school_level_staff
                        for grade in school_type[config_module.GRADES]:
                            number_of_students_in_grade = calculate_number_of_students(student_min, student_max, student_avg)
                            for subject_name in constants.SUBJECTS:
                                # TODO: Figure out how to calculate number_of_sections
                                number_of_sections = calculate_number_of_sections(number_of_students_in_grade)
                                sections_in_grade = generate_sections(number_of_sections, subject_name, grade, current_state.state_code, district.district_guid, school.school_guid)
                                sections_in_school += sections_in_grade
                                for section in sections_in_grade:
                                    # TODO: More accurate math for num_of_students
                                    # TODO: Do we need to account for the percentages of kids that take ELA or MATH here?
                                    number_of_students = number_of_students_in_grade // number_of_sections
                                    students_in_section = generate_students_from_institution_hierarchy(number_of_students, institution_hierarchy, grade, section.section_guid, name_list_dictionary[BIRDS])
                                    students_in_school += students_in_section
                                    # TODO: should we add some randomness here? What are acceptable numbers? 1-2? 1-3?
                                    number_of_staff_in_section = 1
                                    teachers_in_section = generate_teaching_staff_from_institution_hierarchy(number_of_staff_in_section, institution_hierarchy, section.section_guid)
                                    staff_in_school += teachers_in_section
                        create_csv(students_in_school, ENTITY_TO_PATH_DICT[Student])
                        create_csv(sections_in_school, ENTITY_TO_PATH_DICT[Section])
                        create_csv(staff_in_school, ENTITY_TO_PATH_DICT[Staff])
    create_csv(institution_hierarchies, ENTITY_TO_PATH_DICT[InstitutionHierarchy])


# TODO: Can we think of a more appropriate file for this function?
def prepare_csv_files(entity_to_path_dict):
    for entity in entity_to_path_dict:
        path = entity_to_path_dict[entity]
        # By opening the file for writing, we implicitly delete the file contents
        with open(path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            # Here we write the header the the given entity
            csv_writer.writerow(entity.getHeader())

def generate_name_list_dictionary(list_name_to_path_dictionary):
    name_list_dictionary = {}
    for list_name in list_name_to_path_dictionary:
        path = list_name_to_path_dictionary[list_name]
        name_list = util_2.create_list_from_file(path)
        name_list_dictionary[list_name] = name_list
    return name_list_dictionary

def generate_district_dictionary(district_types_and_counts, district_names_1, district_names_2):
    district_dictionary = {}
    for district_type in district_types_and_counts:
        district_count = district_types_and_counts[district_type]
        district_list = []
        for i in range(district_count):
            district = generate_district(district_names_1, district_names_2)
            district_list.append(district)
        district_dictionary[district_type] = district_list
    return district_dictionary

def create_school_dictionary(school_counts, school_types_and_ratios, school_names_1, school_names_2):
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
            school = generate_school(school_type_name, school_names_1, school_names_2)
            school_list.append(school)
        school_dictionary[school_type_name] = school_list
    return school_dictionary


def generate_institution_hierarchy_from_helper_entities(state, district, school):
    state_name = state.state_name
    state_code = state.state_code
    district_guid = district.district_guid
    district_name = district.district_name
    school_guid = school.school_guid
    school_name = school.school_name
    school_category = school.school_category
    # TODO: generate from_date more intelligently
    from_date = datetime.date.today()
    # TODO: generate most_recent more intelligently
    most_recent = True

    institution_hierarchy = generate_institution_hierarchy(state_name, state_code,
                                                           district_guid, district_name,
                                                           school_guid, school_name, school_category,
                                                           from_date, most_recent)
    return institution_hierarchy


def generate_students_from_institution_hierarchy(number_of_students, institution_hierarchy, grade, section_guid, street_names):
    state_code = institution_hierarchy.state_code
    district_guid = institution_hierarchy.district_guid
    school_guid = institution_hierarchy.school_guid
    school_name = institution_hierarchy.school_name
    students = generate_students(number_of_students, section_guid, grade, state_code, district_guid, school_guid, school_name, street_names)
    return students


def generate_teaching_staff_from_institution_hierarchy(number_of_staff, institution_hierarchy, section_guid):
    state_code = institution_hierarchy.state_code
    district_guid = institution_hierarchy.district_guid
    school_guid = institution_hierarchy.school_guid
    hier_user_type = 'Teacher'
    staff_list = generate_multiple_staff(number_of_staff, section_guid, hier_user_type, state_code, district_guid, school_guid)
    return staff_list

def generate_non_teaching_staff(number_of_staff, state_code=None, district_guid=None, school_guid=None):
    hier_user_type = 'Staff'
    staff_list = generate_multiple_staff(number_of_staff, hier_user_type, state_code, district_guid, school_guid)
    return staff_list



def calculate_number_of_schools(num_schools_min, num_schools_avg, num_schools_max):
    # TODO: implement me
    return 10


def calculate_number_of_students(student_min, student_max, student_avg):
    # TODO: implement me
    return 15

def calculate_number_of_sections(number_of_students):
    # TODO: implement me
    return 1


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


