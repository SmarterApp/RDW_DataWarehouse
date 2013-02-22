'''
generate_data.py

Entry point for generating all data.
'''

from datetime import date
from test.test_iterlen import len
from xmlrpc.client import MAXINT
import datetime
import math
import random
import uuid
import queries

from assessment import generate_assmts_for_students
from dbconnection import get_db_conn
from entities import (
    InstitutionHierarchy, Class,
    AssessmentOutcome, StudentTemporalData, SectionSubject, TeacherSection)
from helper_entities import State, District, School
from gen_assessments import generate_assessment_types
from genpeople import generate_teacher, generate_student, generate_staff
from idgen import IdGen
from write_to_csv import clear_files, create_csv
import constants
import py1


def get_name_lists():
    '''
    Read files into lists, which is used for making names, addresses, etc
    '''
    # clear old files
    clear_files()

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
    print(q)
    dist_count = db.prepare(q)
    for row in dist_count:
        db_states.append(dict(zip(constants.STAT_COLUMNS, row)))
    db.close()
    # print(db_states)
    return db_states


def generate(f_get_name_lists, f_get_state_stats):
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

    return generate_data(name_lists, state_stats)


def generate_data(name_lists, db_states_stat):
    '''
    Main function to generate actual data with input statistical data
    '''
    # total count for state, districts, schools, students, teachers, parents
    total_count = [0, 0, 0, 0, 0, 0]

    # generate all assessment types
    asmt_list = generate_assessment_types()
    create_csv(asmt_list, constants.ASSESSMENT_TYPES)

    c = 0
    for state in db_states_stat:
        # create a state
        created_state = State(state['state_code'], state['state_name'], state['total_district'])
        total_count[0] += 1

        school_num_in_dist_made, stu_num_in_school_made, stutea_ratio_in_school_made, school_type_in_state = generate_distribution_lists(state)

        # print out result for a state
        print("************** State ", created_state.state_name, " **************")
        print("                     Real     To Be Generated")
        print("Number of districts ", state['total_district'], "    ", len(school_num_in_dist_made))
        print("Number of schools   ", state['total_school'], "    ", sum(school_num_in_dist_made))
        print("Number of students  ", state['total_student'], "    ", sum(stu_num_in_school_made))
        # continue
        # create districts for each state
        created_dist_list = create_districts(created_state.state_code, created_state.state_name, school_num_in_dist_made, c, name_lists)
        total_count[1] += len(created_dist_list)

        shift = 0

        dist_count = 0
        for district in created_dist_list:
            print("creating district %d of %d for state %s" % ((dist_count + 1), len(created_dist_list), state['state_name']))
            dist_count += 1

            # create school for each district
            school_list = create_schools(stu_num_in_school_made[shift: shift + district.number_of_schools],
                                                          stutea_ratio_in_school_made[shift: shift + district.number_of_schools],
                                                          district, school_type_in_state, name_lists)

            # TODO: merge school entity and institution_hierarchy entity so we don't have to convert
            institution_hierarchy_list = []
            for school in school_list:
                institution_hierarchy = school.covert_to_institution_hierarchy()
                institution_hierarchy_list.append(institution_hierarchy)

            create_csv(institution_hierarchy_list, constants.INSTITUTION_HIERARCHY)

            # total_count[2] += len(school_list)
            shift += district.number_of_schools

            # create classes, grades, sections, teachers students, parents and assessment scores for each school
            for school in school_list:
                create_classes_for_school(district, school, created_state, name_lists[2], total_count, asmt_list)

         #if just need one state data
        if(c == 0):
            break
        c += 1

    print("**************Results***********************")
    print("generated number of states    ", total_count[0])
    print("generated number of districts ", total_count[1])
    print("generated number of schools   ", total_count[2])
    print("generated number of students  ", total_count[3])
    print("generated number of teachers  ", total_count[4])
    print("generated number of parents   ", total_count[5])

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
    Given percentage of different types of school, and total number of shools
    Returns absolute number for each type of school
    '''
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
    n = len(school_num_in_dist_made)

    if(n > 0):
        # generate random district names
        try:
            names = generate_names_from_lists(n, name_lists[0], name_lists[1], constants.DIST_SCHOOL_NAME_LENGTH)
        except ValueError:
            print("ValueError: Not enough list to create", n, " number of district names", n, len(name_lists[0]), len(name_lists[1]))
            return []

        # generate random district addresses
        address = generate_address_from_list(n, name_lists[2], constants.ADDRESS_LENGTH)

        # generate random district zip range
        zip_init, zip_dist = cal_zipvalues(pos, n)

        # generate each district
        for i in range(n):
            # generate city zipcode map
            city_zip_map = generate_city_zipcode(zip_init, (zip_init + zip_dist), school_num_in_dist_made[i], name_lists)
            if(city_zip_map is None):
                continue

            # create district object
            params = {
                'district_id': IdGen().get_id(),
                'district_name': names[i] + " " + random.choice(constants.DIST_SUFFIX),
                'state_code': state_code,
                'state_name': state_name,
                'number_of_schools': school_num_in_dist_made[i],
                'city_zip_map': city_zip_map,
            }

            # dist = District(district_id, district_external_id, district_name, state_id, school_num_in_dist_made[i], city_zip_map, address1, zip_init)
            dist = District(**params)
            districts_list.append(dist)
            total_school += dist.number_of_schools
            zip_init += zip_dist

    return districts_list


def create_schools(stu_num_in_school_made, stutea_ratio_in_school_made, district, school_type_in_state, name_lists):
    '''
    Main function to generate list of schools for a district
    '''
    count = district.number_of_schools
    # generate random school names
    try:
        names = generate_names_from_lists(count, name_lists[2], name_lists[1], constants.DIST_SCHOOL_NAME_LENGTH)
    except ValueError:
        print("ValueError: Not enough list to create", count, " number of school names")
        return [], []

    # generate addresses
    address = generate_address_from_list(count, name_lists[0], constants.ADDRESS_LENGTH)

    school_list = []

    # generate each school and where-taken row
    for i in range(count):
        # get categories
        school_categories_type = random.choice(school_type_in_state)
        suf = random.choice(constants.SCHOOL_LEVELS_INFO[constants.SCHOOL_ORDER_MAP.get(school_categories_type)][1])
        grade_range = random.choice(constants.SCHOOL_LEVELS_INFO[constants.SCHOOL_ORDER_MAP.get(school_categories_type)][2])
        low_grade = grade_range[0]
        high_grade = grade_range[1]

        # create common fields
        sch_name = names[i] + " " + suf

        # create one row of school
        params = {
            'school_id': IdGen().get_id(),
            'school_name': sch_name,
            'school_category': school_categories_type,
            'district_name': district.district_name,
            'district_id': district.district_id,
            'state_code': district.state_code,
            'state_name': district.state_name,
            'number_of_students': stu_num_in_school_made[i],
            'student_teacher_ratio': stutea_ratio_in_school_made[i],
            'low_grade': low_grade,
            'high_grade': high_grade,
        }

        school = School(**params)
        school_list.append(school)

    return school_list

def create_institution_hierarchies(stu_num_in_school_made, stutea_ratio_in_school_made, district, school_type_in_state, name_lists, state):
    '''
    Main function to generate list of schools for a district
    '''
    count = district.number_of_schools
    # generate random school names
    try:
        names = generate_names_from_lists(count, name_lists[2], name_lists[1], constants.DIST_SCHOOL_NAME_LENGTH)
    except ValueError:
        print("ValueError: Not enough list to create", count, " number of school names")
        return [], []

    # generate addresses
    address = generate_address_from_list(count, name_lists[0], constants.ADDRESS_LENGTH)

    institution_hierarchies = []

    # generate each school and where-taken row
    for i in range(count):
        # get categories
        school_categories_type = random.choice(school_type_in_state)
        suf = random.choice(constants.SCHOOL_LEVELS_INFO[constants.SCHOOL_ORDER_MAP.get(school_categories_type)][1])
        grade_range = random.choice(constants.SCHOOL_LEVELS_INFO[constants.SCHOOL_ORDER_MAP.get(school_categories_type)][2])
        low_grade = grade_range[0]
        high_grade = grade_range[1]

        # create common fields
        school_name = names[i] + " " + suf
        address_1 = address[i]
        city = random.choice(list(district.city_zip_map.items()))
        city_name = city[0]
        zip_code = city[1][0]
        if(city[1][0] < city[1][1]):
            zip_code = random.choice(range(city[1][0], city[1][1]))

        # create one row of InstitutionHierarchy
        params = {
            'state_name': state.state_name,
            'state_code': state.state_code,
            'district_id': district.district_id,
            'district_name': district.district_name,
            'school_id': IdGen.get_id(),
            'school_name': school_name,
            'school_category': school_categories_type,
            'from_date': datetime.date(2012, 9, 1),
            'most_recent': True
        }

        institution_hierarchy = InstitutionHierarchy(**params)
        institution_hierarchies.append(institution_hierarchy)

    return institution_hierarchies


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
            # print("Substring of names...")
            names = [(str(name1) + " " + str(name2))[0: name_length] for name1 in names1 for name2 in names2]
        else:
            names = [str(name1) + " " + str(name2) for name1 in names1 for name2 in names2]

    new_list = []
    new_list.extend(names[0:count])
    return new_list


def generate_address_from_list(count, words_list, name_length=None):
    '''
    input: count: total number of addresses
           words_list: a word list used for generate address
    output: list of addresses
    each address is created as: a number, a random word selected from input words_list, and a suffix
    '''
    adds = []
    if(count > 0):
        no = random.sample(range(1, count * 10), count)
        road_name = []
        if(count < len(words_list)):
            road_name = random.sample(words_list, count)

        else:
            road_name.extend(words_list)
        if(name_length is not None):
            for i in range(count):
                first_no = str(no[i])
                suff = random.choice(constants.ADD_SUFFIX)
                middle_add = str(road_name[i % len(road_name)])
                compose_add = first_no + " " + middle_add[0: (name_length - len(first_no) - len(suff) - 2)].strip() + " " + suff
                adds.append(compose_add)
        else:
            adds = [str(no[i]) + " " + str(road_name[i % len(road_name)]) + " " + random.choice(constants.ADD_SUFFIX) for i in range(count)]

    return adds


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


def create_classes_for_school(district, school, state, name_list, total_count, asmt_list):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''

    # generate TEACHERS for a school
    maximum = round(school.number_of_students / school.student_teacher_ratio)
    # we want one or more teachers
    number_of_teachers = max(1, maximum)
    teachers_in_school = generate_teachers(number_of_teachers, state, district)
    total_count[4] += len(teachers_in_school)
    create_csv(teachers_in_school, constants.TEACHERS)

    # generate STAFF for a school
    percent_of_teachers = random.uniform(.4, .6)
    # number of staff is roughly half [.4,.6] the number of teachers
    num_of_staff = int(math.floor(percent_of_teachers * number_of_teachers))
    staff_list = generate_multiple_staff(num_of_staff, state, district, school)
    create_csv(staff_list, constants.STAFF)


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
        create_csv(students_in_grade, constants.STUDENTS)

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
        total_count[3] += len(students_in_grade)

        if grade == (school.high_grade - 1):
            number_of_students_per_grade = school.number_of_students - generated_student_count

        # assign teachers in the school to current grade
        # if there are enough teachers in the school, assign a subset
        # of them to the current grade
        # otherwise, assign all of them to the current grade
        if(number_of_teachers_per_grade < len(teachers_in_school)):
            teachers_in_grade = random.sample(teachers_in_school, number_of_teachers_per_grade)
        else:
            teachers_in_grade = teachers_in_school

        # create classes for the current grade
        classes_in_grade = create_classes_for_grade(students_in_grade, teachers_in_grade, school, grade)

        student_temporal_list = create_student_temporal_data(state.state_code, classes_in_grade, grade, school.school_id, school.district_name)
        scores = generate_assmts_for_students(len(students_in_grade), grade, state.state_name, asmt_list)

        assessment_outcome_list = associate_students_and_scores(student_temporal_list, scores, school, asmt_list)
        create_csv(assessment_outcome_list, constants.ASSESSMENT_OUTCOME)


def associate_students_and_scores(student_temporal_list, scores, school, asmt_list):
    '''
    creates association between students and scores
    student_temporal_list -- a list of student_temporal objects
    scores -- a list of scores that will be mapped to students
    school -- the school that the students belong to
    wheretaken_id -- id of where taken
    returns a list of AssessmentOutcome Objects
    '''

    assessment_outcome_list = []
    dates_taken1 = generate_dates_taken(2000)
    dates_taken2 = generate_dates_taken(2000)
    prev_year = 0

    for stu_tmprl in student_temporal_list:
        for score in scores.items():
            asmt_id = int(score[0].split('_')[1])
            year = score[0].split('_')[0]
            asmt = [x for x in asmt_list if x.asmt_id == asmt_id][0]
            subject = stu_tmprl.student_class.sub_name

            if subject == 'Math':
                subject = 'MATH'

            if stu_tmprl.student_class.sub_name == asmt.asmt_subject:  # check that subjects match as there is a std_tmprl object for each subject
                new_id = IdGen().get_id()
                teacher_list = list(stu_tmprl.student_class.section_tea_map.values())
                teacher_list = [item for sub in teacher_list for item in sub]  # flatten teacher_list
                teacher = teacher_list[0]
                teacher_id = teacher.teacher_id

                date_taken = None
                if prev_year == year:
                    date_taken = map_asmt_date_to_period(asmt.asmt_period, dates_taken1, year)
                else:
                    date_taken = map_asmt_date_to_period(asmt.asmt_period, dates_taken2, year)
                prev_year = year

                params = {
                    'asmt_out_id': new_id,
                    'asmt_out_ext_id': uuid.uuid4(),
                    'assessment': asmt,
                    'student_id': stu_tmprl.student_id,
                    'teacher_id': teacher_id,
                    'state_code': school.state_code,
                    'district_id': school.district_id,
                    'school_id': school.school_id,
                    'enrl_grade_id': stu_tmprl.grade_id,
                    'enrl_grade_code': stu_tmprl.grade_id,
                    'date_taken': date_taken,
                    'asmt_score': score[1].pop(),
                    'asmt_create_date': date.today().replace(year=date.today().year - 5)
                }
                outcome = AssessmentOutcome(**params)
                assessment_outcome_list.append(outcome)

    return assessment_outcome_list


def map_asmt_date_to_period(period, dates_taken, year):
    '''
    returns a date given the attributes
    period -- the period that the asmt was taken
    dates_taken -- a dict of dates whose keys are periods
    year -- the year the asmt was taken
    '''
    if period == 'BOY':
        date_taken = dates_taken['BOY']
    elif period == 'MOY':
        date_taken = dates_taken['MOY']
    elif period == 'EOY':
        date_taken = dates_taken['EOY']
    return date_taken.replace(year=int(year))


def generate_teachers(num_teachers, state, district):
    teachers = []

    for i in range(num_teachers):
        teacher = generate_teacher(state, district)
        teachers.append(teacher)

    return teachers


def generate_students(num_students, state, district, school, grade, fish_names):
    students = []
    external_users = []

    for i in range(num_students):
        stu, ext_user = generate_student(state, district, school, grade, fish_names)
        students.append(stu)
        external_users.append(ext_user)

    return students, external_users


def generate_multiple_staff(num_staff, state, district, school):
    staff = []

    for i in range(num_staff):
        staff_member = generate_staff(district, state, school)
        staff.append(staff_member)

    return staff


def generate_dates_taken(year):
    '''
    generates a list of dates for a given year when tests are taken
    three dates correspond to BOY, MOY, EOY
    returns a dict containing three dates with keys: 'BOY', 'MOY', 'EOY'
    '''
    boy_pool = [9, 10]
    moy_pool = [11, 12, 1, 2, 3]
    eoy_pool = [4, 5, 6]

    boy_date = date(year, random.choice(boy_pool), random.randint(1, 28))

    moy_month = random.choice(moy_pool)
    moy_year = year
    if moy_month <= 3:
        moy_year += 1
    moy_date = date(moy_year, moy_month, random.randint(1, 28))
    eoy_date = date(year + 1, random.choice(eoy_pool), random.randint(1, 28))

    return {'BOY': boy_date, 'MOY': moy_date, 'EOY': eoy_date}


def create_student_temporal_data(state_code, class_list, grade, school_id, dist_name):
    '''
    Creates and returns a list of StudentTemporalData objects
    '''
    temporal_list = []

    for cls in class_list:

        for sect, stus in cls.section_stu_map.items():
            for stu in stus:
                tmprl_id = IdGen().get_id()
                student_temporal = StudentTemporalData(tmprl_id, stu.student_id, grade, dist_name, school_id, cls, sect)
                temporal_list.append(student_temporal)

    return temporal_list


def create_classes_for_grade(students_in_grade, teachers_in_grade, school, grade):
    '''
    Function to generate classes for a grade
    '''

    # calculate max number of classes per subject (based on the number of students)
    # we want one or more classes as our max
    max_number_of_classes = max(1, round(len(students_in_grade) / constants.MIN_CLASS_SIZE))

    # calculate minimum number of classes per subject
    # roughly 1/3 of the maximum
    min_number_of_classes = int(round(max_number_of_classes / 3))

    total_classes = []
    for subject in constants.SUBJECTS:

        # select a number of classes for each subject
        # it should be in between our minimum and our maximum
        if(max_number_of_classes >= 2):
            number_of_classes = random.choice(range(min_number_of_classes, max_number_of_classes))
        else:
            number_of_classes = max_number_of_classes

        # Whatever is larger: 1 or (teachers divided by subjects)
        max_number_of_teachers = max(1, round(len(teachers_in_grade) / len(constants.SUBJECTS)))
        # calculate number of teachers for a subject
        number_of_teachers = min(len(teachers_in_grade), max_number_of_teachers)
        subject_teachers = random.sample(teachers_in_grade, number_of_teachers)

        subject_classes = create_classes(subject, number_of_classes, students_in_grade, subject_teachers, school, grade)

        total_classes.extend(subject_classes)

    return total_classes


def create_classes(subject_name, number_of_classes, students, teachers, school, grade):
    '''
    Function to create classes for a grade of a subject
    '''
    
    # distribute students in each class
    # students_assigned_to_classes is a list of lists
    # each sublist represents a class, and the contents are the students within that class
    students_assigned_to_classes = split_list(students, number_of_classes)

    # create classes
    class_list = [create_one_class(subject_name, i, students_assigned_to_classes[i], teachers, school, grade) for i in range(len(students_assigned_to_classes))]

    # iterate over each "class"
    class_list = []
    for i in range(len(students_assigned_to_classes)):
        students_in_current_class = students_assigned_to_classes[i]
        current_class = create_one_class(subject_name, i, students_in_current_class, teachers, school, grade)
        class_list.append(current_class)

    return class_list


def create_one_class(subject_name, class_count, distribute_stu_inaclass, tea_list, school, grade):
    '''
    Main function to create one class in a grade of a subject.
    '''
    # calculate number of sections
    num_of_stu_in_class = len(distribute_stu_inaclass)
    section_num = round(num_of_stu_in_class / school.student_teacher_ratio)
    if(num_of_stu_in_class < constants.MIN_SECTION_SIZE or section_num < 2):
        section_num = 1

    # distribute student in each section
    distribute_stu_insection = split_list(distribute_stu_inaclass, section_num)
    class_name = subject_name + " " + str(class_count)

    section_stu_map = {}
    section_tea_map = {}

    class_id = IdGen().get_id()
    section_subject_list = []
    teacher_section_list = []
    # for each section, add students and teachers
    for i in range(len(distribute_stu_insection)):
        section_id = IdGen().get_id()
        section_stu_map[str(section_id)] = distribute_stu_insection[i]
        # one section has only one teacher
        section_tea_map[str(i)] = random.sample(tea_list, 1)

        # create section object
        section_name = 'section ' + str(i + 1)
        # section = Section(section_id, uuid.uuid4(), school_id, section_name, class_name)
        section_subject_params = {
            'section_id': section_id,
            'section_name': section_name,
            'grade': grade,
            'class_name': class_name,
            'subject_name':subject_name,
            'state_code': school.state_code,
            'district_id': school.district_id,
            'school_id': school.school_id,
            'from_date': date(2012, 9, 1),
            'most_recent': True,
            'to_date': date(2999,12,1)
        }
        section_subject = SectionSubject(**section_subject_params)
        section_subject_list.append(section_subject)

    # write section subject into csv
    create_csv(section_subject_list, constants.SECTION_SUBJECT)


def generate_date():
    '''
    Generate a random date
    '''
    today = datetime.date.today()
    current_year = today.year
    generate_year = current_year - random.randint(1, constants.YEAR_SHIFT)
    generate_month = random.randint(1, constants.MONTH_TOTAL)
    generate_day = 1
    if(generate_month in constants.MONTH_LIST_31DAYS):
        generate_day = random.choice(range(1, constants.MONTH_DAY_MAX[0]))
    elif(generate_month in constants.MONTH_LIST_30DAYS):
        generate_day = random.choice(range(1, constants.MONTH_DAY_MAX[1]))
    else:
        generate_day = random.choice(range(1, constants.MONTH_DAY_MAX[2]))

    return date(generate_year, generate_month, generate_day)


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
    min_dist = MAXINT
    candidate_list = []
    for i in range(constants.RETRY_CAL_STAT):
        generated_list1 = py1.makeup_core(avgin, stdin, minin, maxin, countin)
        # generated_list2 = py1.makeup_core(py1.avg(generated_list1), py1.std(generated_list1), min(generated_list1), max(generated_list1), countin)
        # generated_list3 = py1.makeup_core(py1.avg(generated_list2), py1.std(generated_list2), min(generated_list2), max(generated_list2), countin)
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


if __name__ == '__main__':
    t1 = datetime.datetime.now()
    generate(get_name_lists, get_state_stats)
    # get_state_stats()
    t2 = datetime.datetime.now()
    print("data_generation starts ", t1)
    print("data_generation ends   ", t2)
