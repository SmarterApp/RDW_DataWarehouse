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
    AssessmentOutcome, SectionSubject, Assessment, Staff, Student, ExternalUserStudent)
from helper_entities import State, District, WhereTaken
from gen_assessments import generate_dim_assessment
from genpeople import generate_teacher, generate_student_bio_info, generate_staff, generate_student
from idgen import IdGen
from write_to_csv import clear_files, create_csv
import constants
import py1
import argparse
import small_set_data_input
from gen_assessment_outcome import generate_assessment_outcomes


ENTITY_TO_PATH_DICT = {InstitutionHierarchy: constants.DATAFILE_PATH + '/datafiles/csv/dim_inst_hier.csv',
                       SectionSubject: constants.DATAFILE_PATH + '/datafiles/csv/dim_section_subject.csv',
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


def generate(f_get_name_lists, f_get_state_stats, is_small_data_mode):
    '''
    Generate data.
    First step: read files into lists for making names, addresses
    Second step: get statistical data from database
    Third step: if first two steps are successful, start generate data process.
    (including generate: state, district, school, class, section, student,
    and teacher)
    '''
    name_lists = f_get_name_lists()
    state_stats = f_get_state_stats()

    if(name_lists is None or state_stats is None or len(name_lists) == 0 or len(state_stats) == 0):
        print("Initializing....Error")
        return None

    return generate_data(name_lists, state_stats, is_small_data_mode)


def generate_data(name_lists, db_states_stat, is_small_data_mode):
    '''
    Main function to generate actual data with input statistical data
    '''
    # total count for state, districts, schools, students, student_sections
    total_count = {'state_count': 0, 'district_count': 0, 'school_count': 0, 'student_count': 0, 'student_section_count': 0}

    # add headers to all csv files
    add_headers_to_csvs()

    # generate all assessment types
    asmt_list = generate_dim_assessment()
    create_csv(asmt_list, ENTITY_TO_PATH_DICT[Assessment])

    c = 0
    for state in db_states_stat:
        # create a state
        created_state = State(state['state_code'], state['state_name'], state['total_district'])
        total_count['state_count'] += 1

        if is_small_data_mode:
            school_num_in_dist_made = small_set_data_input.SMALL_SET_SCHOOL_NUM_IN_DIST
            stu_num_in_school_made = small_set_data_input.SMALL_SET_STUDENT_NUM_IN_SCHOOL
            stutea_ratio_in_school_made = small_set_data_input.SMALL_SET_STUDENT_TEACHER_RATIO_IN_SCHOOL
            school_type_in_state = small_set_data_input.SMALL_SET_SCHOOL_TYPE_IN_STATE
        else:
            school_num_in_dist_made, stu_num_in_school_made, stutea_ratio_in_school_made, school_type_in_state = generate_distribution_lists(state)

        # print out result for a state
        print("************** State ", created_state.state_name, " **************")
        print("                     Real     To Be Generated")
        print("Number of districts ", state['total_district'], "    ", len(school_num_in_dist_made))
        print("Number of schools   ", state['total_school'], "    ", sum(school_num_in_dist_made))
        print("Number of students  ", state['total_student'], "    ", sum(stu_num_in_school_made))

        # create districts for each state
        created_dist_list = create_districts(created_state.state_code, created_state.state_name, school_num_in_dist_made, c, name_lists)
        total_count['district_count'] += len(created_dist_list)

        # generate non-teaching state_staff
        # assuming here between 2 and 4 staff per district at the state level
        num_of_state_staff = len(created_dist_list) * random.choice(range(2, 4))
        state_staff_list = [generate_staff(constants.HIER_USER_TYPE[1], created_state.state_code)for _i in range(num_of_state_staff)]
        create_csv(state_staff_list, ENTITY_TO_PATH_DICT[Staff])

        # TODO: should be more explicit. What is shift?
        shift = 0
        dist_count = 0
        for district in created_dist_list:
            dist_count += 1
            # TODO: Misleading. Isn't district already created?
            print("creating district %d of %d for state %s" % ((dist_count), len(created_dist_list), state['state_name']))

            # create school for each district
            school_list, wheretaken_list = create_institution_hierarchies(stu_num_in_school_made[shift: shift + district.number_of_schools],
                                                                          stutea_ratio_in_school_made[shift: shift + district.number_of_schools],
                                                                          district, school_type_in_state, name_lists, is_small_data_mode)
            create_csv(school_list, ENTITY_TO_PATH_DICT[InstitutionHierarchy])

            # TODO: wheretaken still necessary?
            # associate wheretaken_list to current district
            district.wheretaken_list = wheretaken_list

            # create district staff
            num_of_district_staff = len(school_list) * random.choice(range(2, 4))
            district_staff_list = [generate_staff(constants.HIER_USER_TYPE[1], created_state.state_code, district.district_id)for _i in range(num_of_district_staff)]
            create_csv(district_staff_list, ENTITY_TO_PATH_DICT[Staff])

            total_count['school_count'] += len(school_list)
            shift += district.number_of_schools

            # create sections, teachers, students and assessment scores for each school
            # TODO: use of 'institution_hierarchy' and 'school' is confusing
            for school in school_list:
                create_classes_for_school(district, school, created_state, name_lists[2], total_count, asmt_list, is_small_data_mode)

        # if just need one state data
        if c == 0:
            break
        c += 1

    print("**************Results***********************")
    print("generated number of states    ", total_count['state_count'])
    print("generated number of districts ", total_count['district_count'])
    print("generated number of schools   ", total_count['school_count'])
    print("generated number of students  ", total_count['student_count'])

    return total_count


def generate_distribution_lists(state):
    # generate school distribution in districts
    min_dis = max(1, math.floor(state['total_district'] * constants.DIST_LOW_VALUE))
    max_dis = math.ceil(state['total_district'] * constants.DIST_HIGH_VALUE)
    num_of_dist = min_dis
    if(min_dis < max_dis):
        num_of_dist = random.choice(range(min_dis, max_dis))
    school_num_in_dist_made = makeup_list(state['avg_school_per_district'], state['std_school_per_district'],
                                          state['min_school_per_district'], state['max_school_per_district'],
                                          num_of_dist, state['total_school'])
    # for test
    # print("real four numbers      ", state['avg_school_per_district'], state['std_school_per_district'], state['min_school_per_district'], state['max_school_per_district'])
    # print("generated four numbers ", py1.avg(school_num_in_dist_made), py1.std(school_num_in_dist_made), min(school_num_in_dist_made), max(school_num_in_dist_made))

    # generate student distribution in schools
    stu_num_in_school_made = makeup_list(state['avg_student_per_school'], state['std_student_per_school'],
                                         state['min_student_per_school'], state['max_student_per_school'],
                                         sum(school_num_in_dist_made), state['total_student'])
    # for test
    # print("real four numbers      ", state['avg_student_per_school'], state['std_student_per_school'], state['min_student_per_school'], state['max_student_per_school'])
    # print("generated four numbers ", py1.avg(stu_num_in_school_made), py1.std(stu_num_in_school_made), min(stu_num_in_school_made), max(stu_num_in_school_made))

    # generate student teacher ratio distribution in schools
    stutea_ratio_in_school_made = py1.makeup_core(state['avg_stutea_ratio_per_school'], state['std_stutea_ratio_per_school'],
                                                  state['min_stutea_ratio_per_school'], state['max_stutea_ratio_per_school'],
                                                  sum(school_num_in_dist_made))

    # generate school type distribution in state
    school_type_in_state = make_school_types([state['primary_perc'], state['middle_perc'],
                                              state['high_perc'], state['other_perc']], sum(school_num_in_dist_made))

    return school_num_in_dist_made, stu_num_in_school_made, stutea_ratio_in_school_made, school_type_in_state


def make_school_types(perc, total):

    '''
    Given percentage of different types of school, and total number of schools
    Returns absolute number for each type of school
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
        zip_init, zip_dist = cal_zipvalues(pos, number_of_districts)

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
    Main function to generate list of schools for a district
    Database table is institution_hierarchies
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

        # if is_small_data_mode:
        #    low_grade = small_set_data_input.SMALL_SET_SHOOL_TYPE_GRADES[school_categories_type][0]
        #    high_grade = small_set_data_input.SMALL_SET_SHOOL_TYPE_GRADES[school_categories_type][1]
        # else:
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


def cal_zipvalues(pos, n):
    '''
    Input: pos: greater than 0
           n: total number of zip. It is greater than 0
    Output: zip_init: the starting zipcode
            zip_dist: the basic distance of zipcode
    '''

    zip_init = (pos + 1) * constants.ZIPCODE_START
    zip_dist = max(1, (constants.ZIPCODE_RANG_INSTATE // n))
    return zip_init, zip_dist


def create_classes_for_school(district, school, state, name_list, total_count, asmt_list, is_small_data_mode):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''

    # generate teachers for a school
    maximum_num_of_teachers = round(school.number_of_students / max(1, school.student_teacher_ratio))
    # we want one or more teachers
    number_of_teachers = max(1, maximum_num_of_teachers)
    teachers_in_school = generate_teachers(number_of_teachers, state, district)

    # generate school non-teaching staff
    if is_small_data_mode:
        num_of_school_staff = small_set_data_input.SMALL_SET_SCHOOL_STAFF_NUM_IN_SCHOOL
    else:
        staff_percentage = random.uniform(.1, .3)
        num_of_school_staff = int(math.floor(staff_percentage * number_of_teachers))
    school_staff_list = [generate_staff(constants.HIER_USER_TYPE[1], district.state_code, district.district_id, school.school_id)for _i in range(num_of_school_staff)]
    create_csv(school_staff_list, ENTITY_TO_PATH_DICT[Staff])

    number_of_grades = school.high_grade - school.low_grade + 1
    number_of_students = school.number_of_students

    # calculate number of students and teachers in each grade
    number_of_students_per_grade = max(1, math.floor(number_of_students / number_of_grades))
    number_of_teachers_per_grade = max(1, math.floor(number_of_teachers / number_of_grades))

    generated_student_count = 0
    # iterate through all the grades in the school
    for grade in range(school.low_grade, school.high_grade + 1):

        # generate student list for a grade
        students_in_grade, external_users = generate_students(number_of_students_per_grade, state, district, school, grade, name_list)
        create_csv(external_users, ENTITY_TO_PATH_DICT[ExternalUserStudent])

        # TODO: get rid of this code? Necessary?
        # Each parent of the student will have a row in external_user_student
        # So, create 1 or 2 external_user_student rows per student
        '''
        external_user_students = []
        for student in students_in_grade:
            parent_logins = generate_external_user_student(student.student_id)
            external_user_students = external_user_students + parent_logins
        create_csv(external_user_stus, constants.EXTERNAL_USER_STUDENT)
        '''

        generated_student_count += len(students_in_grade)
        total_count['student_count'] += len(students_in_grade)

        # TODO: We should explain this condition more clearly
        if grade == (school.high_grade - 1):
            number_of_students_per_grade = school.number_of_students - generated_student_count

        # assign teachers in the school to current grade
        # if there are enough teachers in the school, assign a subset
        # of them to the current grade
        # otherwise, assign all of them to the current grade
        if number_of_teachers_per_grade < len(teachers_in_school):
            teachers_in_grade = random.sample(teachers_in_school, number_of_teachers_per_grade)
        else:
            teachers_in_grade = teachers_in_school

        # randomly pick one where_taken in current district for this grade
        where_taken = random.choice(district.wheretaken_list)
        # create classes for the current grade
        create_classes_for_grade(students_in_grade, teachers_in_grade, school, grade, asmt_list, where_taken, total_count, is_small_data_mode)


def map_asmt_date_to_period(period, dates_taken, year, asmt_type):
    '''
    returns a date given the attributes
    period -- the period that the asmt was taken
    dates_taken -- a dict of dates whose keys are periods
    year -- the year the asmt was taken
    '''
    # year_int = int(year)
    if period == 'BOY':
        date_taken = dates_taken['BOY']
    elif period == 'MOY':
        date_taken = dates_taken['MOY']
    elif period == 'EOY':
        date_taken = dates_taken['EOY']
    # if asmt_type.upper() == 'SUMMATIVE':
    #    year_int += 1
    return date_taken
    # return date_taken.replace(year=year_int)


def generate_teachers(num_teachers, state, district):
    teachers = []

    for _loop_variable_not_used in range(num_teachers):
        teacher = generate_teacher(state, district)
        teachers.append(teacher)

    return teachers


def generate_students(num_students, state, district, school, grade, fish_names):
    students = []
    external_users = []

    for _loop_variable_not_used in range(num_students):
        stu, ext_user = generate_student_bio_info(state, district, school, grade, fish_names)
        students.append(stu)
        external_users.append(ext_user)

    return students, external_users


def create_classes_for_grade(students_in_grade, teachers_in_grade, school, grade, assessment_list, where_taken, total_count, is_small_data_mode):
    '''
    Function to generate classes for a grade, assign students in sections in each class, and associate student with assessment scores
    '''

    # calculate max number of classes per subject (based on the number of students)
    # we want one or more classes as our max
    max_number_of_classes = max(1, round(len(students_in_grade) / constants.MIN_CLASS_SIZE))

    # calculate minimum number of classes per subject
    # roughly 1/3 of the maximum
    min_number_of_classes = max(1, int(round(max_number_of_classes / 3)))

    # for each subject of a grade
    for subject in constants.SUBJECTS:

        # select a number of classes for each subject
        # it should be in between our minimum and our maximum
        if max_number_of_classes >= 2:
            number_of_classes = random.choice(range(min_number_of_classes, max_number_of_classes))
        else:
            number_of_classes = max_number_of_classes

        # Whatever is larger: 1 or (teachers divided by subjects)
        max_number_of_teachers = max(1, round(len(teachers_in_grade) / len(constants.SUBJECTS)))
        # calculate number of teachers for a subject
        number_of_teachers = min(len(teachers_in_grade), max_number_of_teachers)
        subject_teachers = random.sample(teachers_in_grade, number_of_teachers)

        students = create_students_for_subject(subject, number_of_classes, students_in_grade, subject_teachers, school, grade, assessment_list)

        # TODO: change 'student_section_count' key to 'student_count'
        total_count['student_section_count'] += len(students)

        assessment_outcome_list = generate_assessment_outcomes(assessment_list, students, grade, subject, school.inst_hier_rec_id, where_taken)
        create_csv(assessment_outcome_list, ENTITY_TO_PATH_DICT[AssessmentOutcome])


def generate_single_claim_score():
    pass


def create_students_for_subject(subject_name, number_of_classes, students, teachers, school, grade, asmt_list):
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


def create_sections_in_one_class(subject_name, class_count, distribute_stu_inaclass, tea_list, school, grade):
    '''
    Main function to create one class in a grade of a subject.
    '''
    # calculate number of sections
    num_of_stu_in_class = len(distribute_stu_inaclass)
    section_num = round(num_of_stu_in_class / max(1, school.student_teacher_ratio))
    if(num_of_stu_in_class < constants.MIN_SECTION_SIZE or section_num < 2):
        section_num = 1

    # distribute student in each section
    distribute_stu_insection = split_list(distribute_stu_inaclass, section_num)
    class_name = subject_name + " " + str(class_count)

    section_stu_map = {}
    section_tea_map = {}

    # class_id = IdGen().get_id()
    section_subject_list = []
    # teacher_section_list = []
    student_section_list = []
    staff_list = []

    # for each section, add students and teachers
    for i in range(len(distribute_stu_insection)):
        section_id = IdGen().get_id()
        section_rec_id = IdGen().get_id()
        section_stu_map[str(section_id)] = distribute_stu_insection[i]
        teacher_for_section = tea_list[i % len(tea_list)]
        section_tea_map[str(i)] = [teacher_for_section]

        # create section_subject object
        section_name = 'section ' + str(i + 1)
        section_subject_params = {
            'section_rec_id': section_rec_id,
            'section_id': section_id,
            'section_name': section_name,
            'grade': grade,
            'class_name': class_name,
            'subject_name': subject_name,
            'state_code': school.state_code,
            'district_id': school.district_id,
            'school_id': school.school_id,
            'from_date': '20120901',
            'most_recent': True,
            'to_date': '20120901'
        }
        section_subject = SectionSubject(**section_subject_params)
        section_subject_list.append(section_subject)

        # create a teaching-staff object
        staff = generate_staff(constants.HIER_USER_TYPE[0], school.state_code, school.district_id, school.school_id, section_id,
                               teacher_for_section.first_name, teacher_for_section.middle_name, teacher_for_section.last_name, teacher_for_section.teacher_id)
        staff_list.append(staff)

        # create students
        for student in section_stu_map[str(section_id)]:
            student = generate_student(student, section_rec_id, section_id, grade, teacher_for_section.teacher_id)
            student_section_list.append(student)

    # write subjects into csv
    create_csv(section_subject_list, ENTITY_TO_PATH_DICT[SectionSubject])
    create_csv(staff_list, ENTITY_TO_PATH_DICT[Staff])
    create_csv(student_section_list, ENTITY_TO_PATH_DICT[Student])

    return student_section_list


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


def get_test_state_stats():
    db = get_db_conn()
    db_states = []
    q = 'select * from ' + queries.SCHEMA + '.school_generate_stat where state_code = \'TS\''
    dist_count = db.prepare(q)
    for row in dist_count:
        db_states.append(dict(zip(constants.STAT_COLUMNS, row)))
    db.close()

    return db_states


def get_sds_stats():
    db = get_db_conn()
    db_states = []
    q = 'select * from ' + queries.SCHEMA + '.school_generate_stat where state_code = \'TS\''
    dist_count = db.prepare(q)
    for row in dist_count:
        db_states.append(dict(zip(constants.STAT_COLUMNS, row)))
    db.close()

    return db_states


def get_sds_state_stats():
    db = get_db_conn()
    db_states = []
    q = 'select * from ' + queries.SCHEMA + '.school_generate_stat where state_code = \'NY\''
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
    parser = argparse.ArgumentParser(description='Generate fixture data.')
    parser.add_argument('--validate', dest='do_validation', action='store_true', default=False,
                        help='Only generate data for "Test State." This creates a small set of data meant for the validation tool',
                        required=False)
    parser.add_argument('--sds', dest='small_data_set', action='store_true', default=False,
                        help='Create a small data set.', required=False)
    # TODO: Add flag to turn headers off
    args = parser.parse_args()

    # Determine which function to use to get state statistical data
    is_small_data_mode = False
    if args.do_validation:
        state_statistic_function = get_test_state_stats
    elif args.small_data_set:
        if validate_small_set_data():
            state_statistic_function = get_sds_state_stats
            is_small_data_mode = True
        else:
            print("Please provide valid data in small_set_data_input.py to generate small set of data")
            exit(-1)
    else:
        state_statistic_function = get_state_stats

    t1 = datetime.datetime.now()
    generate(get_name_lists, state_statistic_function, is_small_data_mode)
    t2 = datetime.datetime.now()

    print("data_generation starts ", t1)
    print("data_generation ends   ", t2)
