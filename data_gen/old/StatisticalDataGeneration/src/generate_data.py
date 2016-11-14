'''
generate_data.py

Entry point for generating all data.
'''

from xmlrpc.client import MAXINT
import datetime
import math
import random
import queries
import csv

from dbconnection import get_db_conn
from entities import (
    InstitutionHierarchy,
    AssessmentOutcome, Section, Assessment, Staff, Student, ExternalUserStudent)
from helper_entities import State, District, WhereTaken
from gen_assessments import generate_dim_assessment
from genpeople import generate_teacher, generate_single_student_bio_info, generate_staff, generate_student
from idgen import IdGen
from write_to_csv import clear_files, create_csv
import constants
import py1
import argparse
import small_set_data_input
from gen_assessment_outcome import generate_assessment_outcomes_from_student_object_list


ENTITY_TO_PATH_DICT = {InstitutionHierarchy: constants.DATAFILE_PATH + '/datafiles/csv/dim_inst_hier.csv',
                       Section: constants.DATAFILE_PATH + '/datafiles/csv/dim_section.csv',
                       Assessment: constants.DATAFILE_PATH + '/datafiles/csv/dim_asmt.csv',
                       AssessmentOutcome: constants.DATAFILE_PATH + '/datafiles/csv/fact_asmt_outcome.csv',
                       Staff: constants.DATAFILE_PATH + '/datafiles/csv/dim_staff.csv',
                       ExternalUserStudent: constants.DATAFILE_PATH + '/datafiles/csv/external_user_student_rel.csv',
                       Student: constants.DATAFILE_PATH + '/datafiles/csv/dim_student.csv'}


def get_name_lists():
    '''
    Read files into lists, which is used for making names, addresses, etc
    '''
    # clear old files
    clear_files(ENTITY_TO_PATH_DICT)

    name_lists = []
    try:
        name_lists.append(read_names(constants.BIRDS_FILE))
        name_lists.append(read_names(constants.MAMMALS_FILE))
        name_lists.append(read_names(constants.FISH_FILE))

    except IOError as e:
        print("Exception for reading bird, mammals, or fish files: " + str(e))
        return None

    return name_lists


def get_state_stats():
    '''
    Connect to db to get statistical data
    '''
    db = get_db_conn()
    db_states = []
    q = 'select * from ' + queries.SCHEMA + '.school_generate_stat'
    dist_count = db.prepare(q)
    for row in dist_count:
        db_states.append(dict(zip(constants.STAT_COLUMNS, row)))
    db.close()
    return db_states


def add_headers_to_csvs():
    '''
    Add headers to all csv files
    '''

    for entity in ENTITY_TO_PATH_DICT.keys():
        with open(ENTITY_TO_PATH_DICT[entity], 'a', newline='') as csvfile:
            entity_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            entity_writer.writerow(entity.getHeader())


def prepare_generation_parameters(get_name_list_function, get_state_stats_function, is_small_data_mode):
    '''
    Generate data.
    First step: read files into lists for making names, addresses
    Second step: get statistical data from database
    Third step: if first two steps are successful, start generate data process.
    (including generate: state, district, school, class, section, student,
    and teacher)
    '''
    name_lists = get_name_list_function()
    state_stats = get_state_stats_function()

    if(name_lists is None):
        raise Exception('name_lists is None. Cannot continue.')
    elif state_stats is None:
        raise Exception('state_stats is None. Cannot continue.')
    elif len(name_lists) == 0:
        raise Exception('name_lists is Empty. Cannot continue.')
    elif len(state_stats) == 0:
        raise Exception('state_stats is Empty. Cannot continue.')

    return generate_fixture_data(name_lists, state_stats, is_small_data_mode)


def generate_fixture_data(name_lists, db_states_stat, is_small_data_mode):
    '''
    Main function to generate actual data with input statistical data
    '''
    # total count for state, districts, schools, students, student_sections
    total_count = {'state_count': 0, 'district_count': 0, 'school_count': 0, 'student_count': 0}

    # add headers to all csv files
    add_headers_to_csvs()

    # generate all assessments
    asmt_list = generate_dim_assessment()
    create_csv(asmt_list, ENTITY_TO_PATH_DICT[Assessment])

    state_index = 0
    for state in db_states_stat:
        # create a state
        created_state = State(state['state_code'], state['state_name'], state['total_district'])
        # increment relevant counter
        total_count['state_count'] += 1

        # TODO: add comments about generate_distribution_lists
        number_of_schools_in_districts, number_of_students_in_schools, student_teacher_ratio_in_schools, school_type_in_state = generate_distribution_lists(state, is_small_data_mode)

        # print out result for a state
        print("************** State ", created_state.state_name, " **************")
        print("                     Real     To Be Generated")
        print("Number of districts ", state['total_district'], "    ", len(number_of_schools_in_districts))
        print("Number of schools   ", state['total_school'], "    ", sum(number_of_schools_in_districts))
        print("Number of students  ", state['total_student'], "    ", sum(number_of_students_in_schools))

        # create districts for each state
        created_district_list = create_districts(created_state.state_code, created_state.state_name, number_of_schools_in_districts, state_index, name_lists)
        total_count['district_count'] += len(created_district_list)

        # generate non-teaching state_staff
        # assuming here between 2 and 4 dim_staff per district at the state level
        num_of_state_staff = len(created_district_list) * random.choice(range(2, 4))
        state_staff_list = [generate_staff(constants.HIER_USER_TYPE[1], created_state.state_code) for _i in range(num_of_state_staff)]
        create_csv(state_staff_list, ENTITY_TO_PATH_DICT[Staff])

        # TODO: should be more explicit. What is shift?
        shift = 0
        dist_count = 0
        for district in created_district_list:
            dist_count += 1
            # TODO: Misleading. Isn't district already created?
            print("creating district %d of %d for state %s" % ((dist_count), len(created_district_list), state['state_name']))

            # create institution_hierarchies for each district
            # TODO: Break this down into 2 functions if possible.
            inst_hier_list, wheretaken_list = create_institution_hierarchies(number_of_students_in_schools[shift: shift + district.number_of_schools],
                                                                             student_teacher_ratio_in_schools[shift: shift + district.number_of_schools],
                                                                             district, school_type_in_state, name_lists, is_small_data_mode)
            create_csv(inst_hier_list, ENTITY_TO_PATH_DICT[InstitutionHierarchy])

            # TODO: wheretaken still necessary?
            # associate wheretaken_list to current district, used in fao
            district.wheretaken_list = wheretaken_list

            # create district dim_staff
            num_of_district_staff = len(inst_hier_list) * random.choice(range(2, 4))
            district_staff_list = [generate_staff(constants.HIER_USER_TYPE[1], created_state.state_code, district.district_id)for _i in range(num_of_district_staff)]
            create_csv(district_staff_list, ENTITY_TO_PATH_DICT[Staff])

            total_count['school_count'] += len(inst_hier_list)
            shift += district.number_of_schools

            # create sections, teachers, students and assessment scores for each school
            # TODO: use of 'institution_hierarchy' and 'school' is confusing
            for inst_hier in inst_hier_list:
                create_classes_for_school(district, inst_hier, created_state.state_code, name_lists[2], total_count, asmt_list, is_small_data_mode)

        # if we need just need one state's worth of data, set condition to state_index== 0
        if state_index == 0:
            break
        state_index += 1

    print("**************Results***********************")
    print("generated number of states    ", total_count['state_count'])
    print("generated number of districts ", total_count['district_count'])
    print("generated number of schools   ", total_count['school_count'])
    print("generated number of students  ", total_count['student_count'])

    return total_count


# TODO: add comments to this function
def generate_distribution_lists(state, is_small_data_mode):
    number_of_schools_in_district = []
    number_of_students_in_school = []
    student_teacher_ratio_in_school = []
    school_type_in_state = []

    if is_small_data_mode:
            number_of_schools_in_district = small_set_data_input.SMALL_SET_SCHOOL_NUM_IN_DIST
            number_of_students_in_school = small_set_data_input.SMALL_SET_STUDENT_NUM_IN_SCHOOL
            student_teacher_ratio_in_school = small_set_data_input.SMALL_SET_STUDENT_TEACHER_RATIO_IN_SCHOOL
            school_type_in_state = small_set_data_input.SMALL_SET_SCHOOL_TYPE_IN_STATE
    else:
        # first, calculate number of district
        number_of_district = calculate_number_of_district(state['total_district'])

        # generate school distribution in districts
        number_of_schools_in_district = makeup_list(state['avg_school_per_district'], state['std_school_per_district'],
                                                    state['min_school_per_district'], state['max_school_per_district'],
                                                    number_of_district, state['total_school'])
        # generate student distribution in schools
        number_of_students_in_school = makeup_list(state['avg_student_per_school'], state['std_student_per_school'],
                                                   state['min_student_per_school'], state['max_student_per_school'],
                                                   sum(number_of_schools_in_district), state['total_student'])

        # generate student teacher ratio distribution in schools
        student_teacher_ratio_in_school = py1.makeup_core(state['avg_stutea_ratio_per_school'], state['std_stutea_ratio_per_school'],
                                                          state['min_stutea_ratio_per_school'], state['max_stutea_ratio_per_school'],
                                                          sum(number_of_schools_in_district))

        # generate school type distribution in state
        school_type_in_state = make_school_types([state['primary_perc'], state['middle_perc'],
                                                  state['high_perc'], state['other_perc']], sum(number_of_schools_in_district))

    return number_of_schools_in_district, number_of_students_in_school, student_teacher_ratio_in_school, school_type_in_state


def calculate_number_of_district(actual_number_of_district):
    min_number_of_district = max(1, math.floor(actual_number_of_district * constants.DIST_LOW_VALUE))
    max_number_of_district = math.ceil(actual_number_of_district * constants.DIST_HIGH_VALUE)
    if(min_number_of_district < max_number_of_district):
        number_of_district = random.choice(range(min_number_of_district, max_number_of_district))
    else:
        number_of_district = min_number_of_district
    return number_of_district


def make_school_types(perc, total):

    '''
    Given percentage of different types of school, and total number of schools
    '''

    # TODO: we should comment this more heavily. Difficult to follow.
    count = []
    repeat_types = []
    if(total > 0):
        control = 0
        for i in range(len(perc) - 1):
            num = round(total * perc[i])
            if(num + control > total):
                count.append(total - control)
            else:
                count.append(num)
            repeat_types.extend([constants.SCHOOL_LEVELS_INFO[i][0]] * count[-1])
            control = sum(count)

        i += 1
        count.append(max(total - control, 0))
        repeat_types.extend([constants.SCHOOL_LEVELS_INFO[i][0]] * count[-1])

    return repeat_types


def create_districts(state_code, state_name, school_num_in_dist_made, pos, name_lists):
    '''
    Main function to generate list of district for a state
    '''
    total_school = 0
    districts_list = []

    # number_of_districts = number of districts in the state
    number_of_districts = len(school_num_in_dist_made)

    if(number_of_districts > 0):
        # generate random district names
        try:
            names = generate_names_from_lists(number_of_districts, name_lists[0], name_lists[1], constants.DIST_SCHOOL_NAME_LENGTH)
        except ValueError:
            print("ValueError: Not enough list to create", number_of_districts, " number of district names", number_of_districts, len(name_lists[0]), len(name_lists[1]))
            return []

        # generate random district zip range
        zip_init, zip_dist = calculate_zip_values(pos, number_of_districts)

        # generate each district
        for i in range(number_of_districts):
            # generate city zipcode map
            city_zip_map = generate_city_zipcode(zip_init, (zip_init + zip_dist), school_num_in_dist_made[i], name_lists)

            # TODO: Is this necessary?
            if(city_zip_map is None):
                continue

            # create district object
            params = {
                'district_id': IdGen().get_id(),
                'district_name': (names[i] + " " + random.choice(constants.DIST_SUFFIX)).title(),
                'state_code': state_code,
                'state_name': state_name,
                'number_of_schools': school_num_in_dist_made[i],
                'city_zip_map': city_zip_map,
            }

            # dist = District(district_id, district_external_id, district_name, state_id, school_num_in_dist_made[i], city_zip_map, address1, zip_init)
            dist = District(**params)
            districts_list.append(dist)

            # TODO: Is total_school ever used?
            total_school += dist.number_of_schools

            zip_init += zip_dist

    return districts_list


def create_institution_hierarchies(student_counts, student_teacher_ratios, district, school_type_in_state, name_lists, is_small_data_mode):
    '''
    Main function to generate institution_hierarchies for a district
    '''
    count = district.number_of_schools
    # generate random school names
    try:
        names = generate_names_from_lists(count, name_lists[2], name_lists[1], constants.DIST_SCHOOL_NAME_LENGTH)
    except ValueError:
        print("ValueError: Not enough list to create", count, " number of school names")
        return [], []

    institution_hierarchies = []
    wheretaken_list = []

    # generate each school and where-taken row
    for i in range(count):
        # get categories
        if is_small_data_mode:
            school_categories_type = school_type_in_state[i]
        else:
            school_categories_type = random.choice(school_type_in_state)
        suf = random.choice(constants.SCHOOL_LEVELS_INFO[constants.SCHOOL_ORDER_MAP.get(school_categories_type)][1])
        grade_range = random.choice(constants.SCHOOL_LEVELS_INFO[constants.SCHOOL_ORDER_MAP.get(school_categories_type)][2])

        if is_small_data_mode:
            low_grade = small_set_data_input.SMALL_SET_SCHOOL_TYPE_GRADES[school_categories_type][0]
            high_grade = small_set_data_input.SMALL_SET_SCHOOL_TYPE_GRADES[school_categories_type][1]
        else:
            low_grade = grade_range[0]
            high_grade = grade_range[1]

        school_name = (names[i] + " " + suf).title()
        # create one row of InstitutionHierarchy
        params = {
            'number_of_students': student_counts[i],
            'student_teacher_ratio': student_teacher_ratios[i],
            'low_grade': low_grade,
            'high_grade': high_grade,

            # columns of dim_inst_hier
            'state_name': district.state_name,
            'state_code': district.state_code,
            'district_id': district.district_id,
            'district_name': district.district_name,
            'school_id': IdGen().get_id(),
            'school_name': school_name,
            'school_category': school_categories_type,
            'from_date': '20120901',
            'to_date': '99991231',
            'most_recent': True,
        }

        institution_hierarchy = InstitutionHierarchy(**params)
        institution_hierarchies.append(institution_hierarchy)

        # create one row of where-taken which has same name as school
        params_wheretaken = {
            'where_taken_id': IdGen().get_id(),
            'where_taken_name': school_name
        }
        where_taken = WhereTaken(**params_wheretaken)
        wheretaken_list.append(where_taken)

    return institution_hierarchies, wheretaken_list


def generate_city_zipcode(zipcode_start, zipcode_end, num_of_schools, name_lists):
    '''
    Generate zip code range for cities in a district
    '''
    try:
        city_names = generate_names_from_lists(num_of_schools, name_lists[0], name_lists[2], constants.CITY_NAME_LENGTH)
    except ValueError:
        print("ValueError: Not enough list to create", num_of_schools, " number of city names in generate_city_zipcode")
        return None

    maxnum_of_city = min((zipcode_end - zipcode_start), num_of_schools)
    num_of_city = 1
    if(num_of_schools > 1 and maxnum_of_city > 1):
        num_of_city = random.choice(range(1, maxnum_of_city))

    city_cand = random.sample(city_names, num_of_city)
    ziprange_incity = (zipcode_end - zipcode_start) // num_of_city
    city_zip_map = {}
    for i in range(len(city_cand) - 1):
        zip_end = int((zipcode_start + ziprange_incity))
        city_zip_map[city_cand[i]] = [zipcode_start, zip_end]
        zipcode_start = zipcode_start + ziprange_incity
    city_zip_map[city_cand[len(city_cand) - 1]] = [zipcode_start, zipcode_end]
    return city_zip_map


def generate_names_from_lists(count, list1, list2, name_length=None):
    '''
    Generate total 'count' number of random combination of names from input lists
    '''

    # TODO: Add comments to this function. Difficult to follow.
    names = []
    if(count > 0):
        base = math.ceil(math.sqrt(count))
        if(base < len(list1) and base < len(list2)):
            names1 = random.sample(list1, base)
            names2 = random.sample(list2, base)
        elif(base < len(list1) * len(list2)):
            if(len(list1) < len(list2)):
                names1 = list1
                names2 = random.sample(list2, math.ceil(count / len(list1)))
            else:
                names2 = list2
                names1 = random.sample(list1, math.ceil(count / len(list2)))
        else:
            print("not enough...", base, " ", len(list1), " ", len(list2))
            raise ValueError

        if(name_length is not None):
            names = [(str(name1) + " " + str(name2))[0: name_length] for name1 in names1 for name2 in names2]
        else:
            names = [str(name1) + " " + str(name2) for name1 in names1 for name2 in names2]

    new_list = []
    new_list.extend(names[0:count])
    return new_list


def calculate_zip_values(pos, n):
    '''
    Input: pos: greater than 0
           n: total number of zip. It is greater than 0
    Output: zip_init: the starting zipcode
            zip_dist: the basic distance of zipcode
    '''

    zip_init = (pos + 1) * constants.ZIPCODE_START
    zip_dist = max(1, (constants.ZIPCODE_RANG_INSTATE // n))
    return zip_init, zip_dist


def create_classes_for_school(district, school, state_code, name_list, total_count, asmt_list, is_small_data_mode):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''
    # generate teachers in a school
    teachers_in_school = generate_teachers(school.number_of_students, school.student_teacher_ratio, state_code, district.district_id, school.school_id, is_small_data_mode)
    # TODO: break this function into 2 separate functions if possible
    number_of_students_in_grades, number_of_teachers_in_grades = calculate_number_of_students_teachers_per_grade(school.high_grade, school.low_grade, school.number_of_students, len(teachers_in_school))

    # iterate through all the grades in the school
    index = 0
    for grade in range(school.low_grade, school.high_grade + 1):
        # generate student list for a grade
        students_in_grade = generate_student_bio_info(number_of_students_in_grades[index], state_code, district.city_zip_map, district.district_id, school.school_id, school.school_name, grade, name_list)
        teachers_in_grade = random.sample(teachers_in_school, number_of_teachers_in_grades[index])

        # randomly pick one where_taken in current district for this grade
        where_taken = random.choice(district.wheretaken_list)
        # create classes for the current grade
        create_classes_for_grade(students_in_grade, teachers_in_grade, school, grade, asmt_list, where_taken, total_count, is_small_data_mode)
        index += 1


def generate_teachers(number_of_students, student_teacher_ratio, state_code, district_id, school_id, is_small_data_mode):
    '''
    Function to generate teachers in a school
    First, it create a list of 'Teacher' objects
    Second, it create a list of non-teaching-dim_staff for a school, and write into dim_staff.csv
    @return: list of 'Teacher' objects
    '''
    # generate school teaching-dim_staff
    maximum_num_of_teachers = round(number_of_students / max(1, student_teacher_ratio))
    # we want one or more teachers
    number_of_teachers = max(1, maximum_num_of_teachers)

    # generate teaching-dim_staff for a school
    school_teacher_list = []
    for _loop_variable_not_used in range(number_of_teachers):
        teacher = generate_teacher(state_code, district_id)
        school_teacher_list.append(teacher)

    # generate school non-teaching dim_staff
    generate_school_non_teaching_staff(is_small_data_mode, number_of_teachers, state_code, district_id, school_id)

    # return a list of teachers
    return school_teacher_list


def generate_school_non_teaching_staff(is_small_data_mode, number_of_teachers, state_code, district_id, school_id):
    '''
    Method to generate non teaching dim_staff in a school
    '''
    if is_small_data_mode:
        num_of_school_staff = small_set_data_input.SMALL_SET_SCHOOL_STAFF_NUM_IN_SCHOOL
    else:
        # take a random percentage between 0.1 to 0.3
        staff_percentage = random.uniform(.1, .3)
        # calculate number of non teaching dim_staff as: percentage * number of teachers(teachers) in school
        num_of_school_staff = int(math.floor(staff_percentage * number_of_teachers))
    school_staff_list = [generate_staff(constants.HIER_USER_TYPE[1], state_code, district_id, school_id)for _i in range(num_of_school_staff)]
    create_csv(school_staff_list, ENTITY_TO_PATH_DICT[Staff])


def calculate_number_of_students_teachers_per_grade(high_grade, low_grade, number_of_students, number_of_teachers):
    '''
    Function to calculate number of students, and number of teachers per grade
    @return: two lists.
    First list has value of number of students from low_grade to high_grade
    Second list has value of number of teachers from low_grade to high_grade
    '''
    number_of_grades = high_grade - low_grade + 1

    # calculate basic number of students and teachers in each grade
    number_of_students_per_grade = max(1, math.floor(number_of_students / number_of_grades))
    number_of_teachers_per_grade = max(1, math.floor(number_of_teachers / number_of_grades))

    # number of teachers per grade should be less than number_of_teachers
    number_of_teachers_per_grade = min(number_of_teachers_per_grade, number_of_teachers)

    # create a list to store number of students for each grade
    # from low_grade to (high_grade - 1), number of students in these grades are the same, which is: number_of_students_per_grade
    # in high_grade, number of students is number_of_students - (number of students from low_grade to high_grade - 1)
    number_of_students_in_grades = [number_of_students_per_grade] * (number_of_grades - 1)
    number_of_students_in_last_grade = number_of_students - sum(number_of_students_in_grades)
    number_of_students_in_grades.append(number_of_students_in_last_grade)

    # create a list to store number of teachers for each grade, use the number_of_teachers_per_grade for all grades
    number_of_teachers_in_grades = [number_of_teachers_per_grade] * number_of_grades

    return number_of_students_in_grades, number_of_teachers_in_grades


def generate_student_bio_info(num_students, state_code, city_zip_map, district_id, school_id, school_name, grade, fish_names):
    '''
    Function to generate a list of 'StudentBioInfo' objects
    The corresponding list external user objects is also generated, and is written into external_user_student_rel.csv
    @return: list of 'StudentBioInfo' objects
    '''
    student_bio_info_list = []
    external_users_list = []

    for _loop_variable_not_used in range(num_students):
        city_zip_map = city_zip_map
        city = random.choice(list(city_zip_map.keys()))
        zip_range = city_zip_map[city]
        zip_code = random.randint(zip_range[0], zip_range[1])

        student_bio_info, external_user = generate_single_student_bio_info(state_code, district_id, zip_code, city, school_id, school_name, grade, fish_names)
        student_bio_info_list.append(student_bio_info)
        external_users_list.append(external_user)

    # write external_users_list into external_user_student_rel.csv
    create_csv(external_users_list, ENTITY_TO_PATH_DICT[ExternalUserStudent])

    return student_bio_info_list


def create_classes_for_grade(students_in_grade, teachers_in_grade, school, grade, assessment_list, where_taken, total_count, is_small_data_mode):
    '''
    Function to generate classes for a grade, assign students in sections in each class, and generate assessment scores for students
    '''
    number_of_students_in_grade = len(students_in_grade)
    number_of_classes = calculate_number_of_classes(number_of_students_in_grade)

    # for each subject of a grade
    for subject in constants.SUBJECTS:

        subject_teachers = generate_subject_teachers(teachers_in_grade)

        students = create_students_for_subject(subject, number_of_classes, students_in_grade, subject_teachers, school, grade)
        total_count['student_count'] += len(students)

        # generate assessment_outcome
        assessment_outcome_list = generate_assessment_outcomes_from_student_object_list(assessment_list, students, subject, school.inst_hier_rec_id, where_taken)
        create_csv(assessment_outcome_list, ENTITY_TO_PATH_DICT[AssessmentOutcome])


def calculate_number_of_classes(number_of_students_in_grade):
    '''
    Function to calculate number of classes by the given number of students in grade
    '''
    # calculate max number of classes per subject (based on the number of students)
    # we want one or more classes as our max
    max_number_of_classes = max(1, round(number_of_students_in_grade / constants.MIN_CLASS_SIZE))

    # calculate minimum number of classes per subject
    # roughly 1/3 of the maximum
    min_number_of_classes = max(1, int(round(max_number_of_classes / 3)))

    # select a number of classes for each subject
    # it should be in between our minimum and our maximum
    if max_number_of_classes >= 2:
        number_of_classes = random.choice(range(min_number_of_classes, max_number_of_classes))
    else:
        number_of_classes = max_number_of_classes
    return number_of_classes


def generate_subject_teachers(teachers_in_grade):
    '''
    Function to generate list of teachers for a grade
    '''
    # Whatever is larger: 1 or (teachers divided by subjects)
    max_number_of_teachers = max(1, round(len(teachers_in_grade) / len(constants.SUBJECTS)))
    # calculate number of teachers for a subject
    number_of_teachers = min(len(teachers_in_grade), max_number_of_teachers)
    subject_teachers = random.sample(teachers_in_grade, number_of_teachers)
    return subject_teachers


def create_students_for_subject(subject_name, number_of_classes, students, teachers, school, grade):
    '''
    Function to create students for a grade of a subject
    '''
    # distribute students in each class
    # students_assigned_to_classes is a list of lists
    # each sublist represents a class, and the contents are the students within that class
    students_assigned_to_classes = split_list(students, number_of_classes)
    teachers_assigned_to_classes = split_list(teachers, number_of_classes)

    # iterate over each "class"
    student_in_sections_list = []
    for i in range(len(students_assigned_to_classes)):
        students_in_current_class = students_assigned_to_classes[i % len(students_assigned_to_classes)]
        teachers_in_current_class = teachers_assigned_to_classes[i % len(teachers_assigned_to_classes)]
        sections_in_one_class = create_sections_in_one_class(subject_name, i, students_in_current_class, teachers_in_current_class, school, grade)
        student_in_sections_list.extend(sections_in_one_class)

    # student_in_sections_list contains each student_section object
    return student_in_sections_list


def create_sections_in_one_class(subject_name, class_index, students_in_current_class, teachers_in_current_class, school, grade):
    '''
    Main function to create one class in a grade of a subject.
    '''
    # create subject section
    section_subject_list = create_sections(students_in_current_class, school.student_teacher_ratio, class_index, subject_name, school.state_code, school.district_id, school.school_id, grade)

    # create students, and teachers to place in section_subject
    student_section_list = create_students_and_staff_in_sections(students_in_current_class, teachers_in_current_class, section_subject_list, school.state_code, school.district_id, school.school_id, grade)

    return student_section_list


def create_sections(students_in_current_class, student_teacher_ratio, class_index, subject_name, state_code, district_id, school_id, grade):
    '''
    Function to create list of SectionSubject object
    '''
    # calculate number of sections
    number_of_students_in_class = len(students_in_current_class)
    number_of_sections = calculate_number_of_sections(number_of_students_in_class, student_teacher_ratio)

    section_subject_list = []
    class_name = subject_name + " " + str(class_index)
    for i in range(number_of_sections):
        section_name = 'section ' + str(i + 1)
        # create a section_subject
        section_subject = create_single_section_subject(section_name, class_name, subject_name, state_code, district_id, school_id, grade)
        section_subject_list.append(section_subject)
    create_csv(section_subject_list, ENTITY_TO_PATH_DICT[Section])

    return section_subject_list


def create_students_and_staff_in_sections(students_in_current_class, teachers_in_current_class, section_list, state_code, district_id, school_id, grade):
    '''
    Function to create list of 'Student' objects, and list of teaching 'Staff' objects
    Generated student objects are written into dim_student.csv
    Generated dim_staff objects are written into dim_staff.csv
    @return: generated list of Student objects
    '''
    number_of_sections = len(section_list)
    # distribute student in each section
    students_in_each_section = split_list(students_in_current_class, number_of_sections)

    students = []
    staff_list = []

    index = 0
    # for each section, add students and teachers
    for section in section_list:
        # create a teaching-dim_staff object
        teacher_in_current_section = teachers_in_current_class[index % len(teachers_in_current_class)]
        dim_staff = generate_staff(constants.HIER_USER_TYPE[0], state_code, district_id, school_id, section.section_guid,
                               teacher_in_current_section.first_name, teacher_in_current_section.middle_name, teacher_in_current_section.last_name, teacher_in_current_section.teacher_guid)
        staff_list.append(dim_staff)

        # create students
        students_in_current_section = students_in_each_section[index]
        for student_in_section in students_in_current_section:
            student = generate_student(student_in_section, section.section_rec_id, section.section_guid, grade, teacher_in_current_section.teacher_guid)
            students.append(student)
        index += 1

    create_csv(staff_list, ENTITY_TO_PATH_DICT[Staff])
    create_csv(students, ENTITY_TO_PATH_DICT[Student])

    return students


def calculate_number_of_sections(number_of_students_in_class, student_teacher_ratio):
    '''
    Function to calculate number of sections in a class
    '''

    number_of_sections = round(number_of_students_in_class / max(1, student_teacher_ratio))
    if(number_of_students_in_class < constants.MIN_SECTION_SIZE or number_of_sections < 2):
        number_of_sections = 1
    return number_of_sections


def create_single_section_subject(section_name, class_name, subject_name, state_code, district_id, school_id, grade):
    '''
    Function to create a single 'SectionSubject' object
    '''

    section_id = IdGen().get_id()
    section_rec_id = IdGen().get_id()

    # create a section_subject object
    section_subject_params = {
        'section_rec_id': section_rec_id,
        'section_guid': section_id,
        'section_name': section_name,
        'grade': grade,
        'class_name': class_name,
        'subject_name': subject_name,
        'state_code': state_code,
        'district_id': district_id,
        'school_id': school_id,
        # TODO: better way to set from_date, most_recent
        'from_date': '20120901',
        'most_recent': True,
        'to_date': '29990901'
    }
    section_subject = Section(**section_subject_params)
    return section_subject


def split_list(list_to_split, n):

    '''
    Function to divide a list into n chunks
    Returns a list of lists
    '''

    if(n == 1 or len(list_to_split) <= n):
        return [list_to_split]

    random.shuffle(list_to_split)

    chunk_length = round(len(list_to_split) // n)
    needs_extra = len(list_to_split) % n

    start = 0
    chucks_list = []
    for i in range(n):
        if i < needs_extra:
            end = start + chunk_length + 1
        else:
            end = start + chunk_length
        chucks_list.append(list_to_split[start:end])
        start = end

    return chucks_list


def makeup_list(avgin, stdin, minin, maxin, countin, target_sum):
    # TODO: Add comments/more helpful variable names
    min_dist = MAXINT
    candidate_list = []
    for _loop_variable_not_used in range(constants.RETRY_CAL_STAT):
        generated_list1 = py1.makeup_core(avgin, stdin, minin, maxin, countin)
        distance = abs(sum(generated_list1) - target_sum)
        if (distance < min_dist and distance != 0):
            min_dist = distance
            candidate_list = generated_list1
    return candidate_list


def read_names(file_name):
    mfile = open(file_name, 'r')
    lines = mfile.readlines()
    names = []
    for line in lines:
        names.append(line.strip())
    mfile.close()
    return names


def get_sds_state_stats():
    db = get_db_conn()
    db_states = []
    q = 'select * from ' + queries.SCHEMA + '.school_generate_stat where state_code = \'NC\''
    dist_count = db.prepare(q)
    for row in dist_count:
        db_states.append(dict(zip(constants.STAT_COLUMNS, row)))
    db.close()

    return db_states


def validate_small_set_data():
    '''
    Validate the provided value for generating small set of data
    '''
    number_of_district = len(small_set_data_input.SMALL_SET_SCHOOL_NUM_IN_DIST)
    if number_of_district > 0 and min(small_set_data_input.SMALL_SET_SCHOOL_NUM_IN_DIST) > 0:
        number_of_school = sum(small_set_data_input.SMALL_SET_SCHOOL_NUM_IN_DIST)
        if number_of_school > 0 and min(small_set_data_input.SMALL_SET_SCHOOL_NUM_IN_DIST) > 0:
            if number_of_school == len(small_set_data_input.SMALL_SET_STUDENT_NUM_IN_SCHOOL) == len(small_set_data_input.SMALL_SET_STUDENT_TEACHER_RATIO_IN_SCHOOL) == len(small_set_data_input.SMALL_SET_SCHOOL_TYPE_IN_STATE):
                if min(small_set_data_input.SMALL_SET_STUDENT_TEACHER_RATIO_IN_SCHOOL) < 1 or min(small_set_data_input.SMALL_SET_STUDENT_NUM_IN_SCHOOL) <= 0:
                    return False
                for school_type in small_set_data_input.SMALL_SET_SCHOOL_TYPE_IN_STATE:
                    if school_type not in constants.SCHOOL_ORDER_MAP.keys():
                        return False
                for key, value in small_set_data_input.SMALL_SET_SCHOOL_TYPE_GRADES.items():
                    if key not in constants.SCHOOL_ORDER_MAP.keys():
                        return False
                    if len(value) != 2 or value[0] not in range(0, 13) or value[0] > value[1] or value[1] not in range(0, 13):
                        return False
                return True
            else:
                return False
        else:
            return False
    else:
        return False

if __name__ == '__main__':

    # Argument parsing
    # TODO: do we need both test state and small data set? Maybe just use small data set?
    parser = argparse.ArgumentParser(description='Generate fixture data.')
    parser.add_argument('--sds', dest='small_data_set', action='store_true', default=False,
                        help='Create a small data set.', required=False)
    parser.add_argument('--update', dest='update', action='store_true', default=False,
                        help='Use existing enrollment data to create new FAO rows.', required=False)
    # TODO: Add flag to turn headers off
    args = parser.parse_args()

    # Determine whether we're generating a whole data set or using existing enrollment data from the db.
    # TODO: Add code here
    if args.update:
        pass
    # Generate whole data set.
    else:
        # Determine which function to use to get state statistical data
        is_small_data_mode = False
        # Generate small data set (QA purposes)
        if args.small_data_set:
            # Make sure small data set defined in 'small_set_data_input.py' is valid
            if validate_small_set_data():
                state_statistic_function = get_sds_state_stats
                is_small_data_mode = True
            else:
                print("Please provide valid data in small_set_data_input.py to generate small set of data")
                exit(-1)
        else:
            state_statistic_function = get_state_stats

        t1 = datetime.datetime.now()
        prepare_generation_parameters(get_name_lists, state_statistic_function, is_small_data_mode)
        t2 = datetime.datetime.now()

        print("data_generation starts ", t1)
        print("data_generation ends   ", t2)
