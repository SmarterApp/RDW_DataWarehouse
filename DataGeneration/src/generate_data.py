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

from assessment import generate_assmts_for_students
from dbconnection import get_db_conn
from entities import (
    State, District, WhereTaken, School, Class,
    AssessmentOutcome, StudentTemporalData, Section, TeacherSection)
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
    dist_count = db.prepare('select * from school_generate_stat')
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
    record_states = []
    for state in db_states_stat:
        # create a state
        created_state = State(state['state_code'], state['state_name'], state['total_district'], state['state_code'])
        total_count[0] += 1
        record_states.append(created_state)

        school_num_in_dist_made, stu_num_in_school_made, stutea_ratio_in_school_made, school_type_in_state = generate_distribution_lists(state)

        # print out result for a state
        print("************** State ", created_state.state_name, " **************")
        print("                     Real     To Be Generated")
        print("Number of districts ", state['total_district'], "    ", len(school_num_in_dist_made))
        print("Number of schools   ", state['total_school'], "    ", sum(school_num_in_dist_made))
        print("Number of students  ", state['total_student'], "    ", sum(stu_num_in_school_made))
        # continue
        # create districts for each state
        created_dist_list = create_districts(created_state.state_id, school_num_in_dist_made, c, name_lists)
        total_count[1] += len(created_dist_list)
        create_csv(created_dist_list, constants.DISTRICTS)
        shift = 0

        dist_count = 0
        for dist in created_dist_list:
            print("creating district %d of %d for state %s" % ((dist_count + 1), len(created_dist_list), state['state_name']))
            dist_count += 1

            # create school for each district
            school_list, wheretaken_list = create_schools(stu_num_in_school_made[shift: shift + dist.num_of_schools],
                                                          stutea_ratio_in_school_made[shift: shift + dist.num_of_schools],
                                                          dist, school_type_in_state, name_lists)
            total_count[2] += len(school_list)
            create_csv(school_list, constants.SCHOOLS)
            create_csv(wheretaken_list, constants.WHERETAKEN)
            shift += dist.num_of_schools

            # associate wheretaken_list to current district
            dist.wheretaken_list = wheretaken_list

            # create classes, grades, sections, teachers students, parents and assessment scores for each school
            for sch in school_list:
                create_classes_grades_sections(dist, sch, created_state, name_lists[2], total_count, asmt_list)

        # if just need one state data
        # if(c == 0):
        #    break
        c += 1

    create_csv(record_states, constants.STATES)

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


def create_districts(state_id, school_num_in_dist_made, pos, name_lists):
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
                'district_external_id': uuid.uuid4(),
                'district_name': names[i] + " " + random.choice(constants.DIST_SUFFIX),
                'state_code': state_id,
                'num_of_schools': school_num_in_dist_made[i],
                'city_zip_map': city_zip_map,
                'address_1': address[i],
                'zipcode': zip_init
            }

            # dist = District(district_id, district_external_id, district_name, state_id, school_num_in_dist_made[i], city_zip_map, address1, zip_init)
            dist = District(**params)
            districts_list.append(dist)
            total_school += dist.num_of_schools
            zip_init += zip_dist

    return districts_list


def create_schools(stu_num_in_school_made, stutea_ratio_in_school_made, distr, school_type_in_state, name_lists):
    '''
    Main function to generate list of schools for a district
    '''
    count = distr.num_of_schools
    # generate random school names
    try:
        names = generate_names_from_lists(count, name_lists[2], name_lists[1], constants.DIST_SCHOOL_NAME_LENGTH)
    except ValueError:
        print("ValueError: Not enough list to create", count, " number of school names")
        return [], []

    # generate addresses
    address = generate_address_from_list(count, name_lists[0], constants.ADDRESS_LENGTH)

    school_list = []
    wheretaken_list = []

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
        address_1 = address[i]
        city = random.choice(list(distr.city_zip_map.items()))
        city_name = city[0]
        zip_code = city[1][0]
        if(city[1][0] < city[1][1]):
            zip_code = random.choice(range(city[1][0], city[1][1]))

        # create one row of where-taken
        # wheretaken_id = idgen.get_id()
        # wheretaken_name = sch_name
        params_wheretaken = {
            'wheretaken_id': IdGen().get_id(),
            'wheretaken_name': sch_name,
            'district_name': distr.district_name,
            'address_1': address_1,
            'city_name': city_name,
            'zip_code': zip_code,
            'state_code': distr.state_code,
            'country_id': 'US'
        }
        # where_taken = WhereTaken(wheretaken_id, wheretaken_name, distr.district_name, address_1, city_name, zip_code, distr.state_code, 'US')
        where_taken = WhereTaken(**params_wheretaken)
        wheretaken_list.append(where_taken)

        # create one row of school
        params = {
            'sch_id': IdGen().get_id(),
            'school_external_id': uuid.uuid4(),
            'school_name': sch_name,
            'dist_name': distr.district_name,
            'district_id': distr.district_id,
            'state_code': distr.state_code,
            'num_of_student': stu_num_in_school_made[i],
            'stu_tea_ratio': stutea_ratio_in_school_made[i],
            'low_grade': low_grade,
            'high_grade': high_grade,
            'school_categories_type': school_categories_type,
            'school_type': random.choice(constants.SCHOOL_TYPES),
            'address1': address_1,
            'city': city_name,
            'zip_code': zip_code
        }

        school = School(**params)
        school_list.append(school)

    return school_list, wheretaken_list


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


def create_classes_grades_sections(district, sch, state, fish_names, total_count, asmt_list):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''

    # generate teacher list for a school
    num_of_teacher = max(1, round(sch.num_of_student / sch.stu_tea_ratio))
    teacher_list = generate_teachers(num_of_teacher, state, district)
    total_count[4] += len(teacher_list)
    create_csv(teacher_list, constants.TEACHERS)

    # generate staff for a school
    prc = random.uniform(.4, .6)
    num_of_staff = int(math.floor(prc*num_of_teacher))
    staff_list = generate_multiple_staff(num_of_staff, state, district, sch)
    # total count?
    create_csv(staff_list, constants.STAFF)

    # calculate number of students and teachers in each grade
    stu_num_in_grade = max(1, math.floor(sch.num_of_student / (sch.high_grade - sch.low_grade + 1)))
    tea_num_in_grade = max(1, math.floor(num_of_teacher / (sch.high_grade - sch.low_grade + 1)))

    # for each grade
    j = 0
    for grade in range(sch.low_grade, sch.high_grade + 1):
        # generate student list for a grade

        grade_students, parentz, external_user_stus = generate_students(stu_num_in_grade, state, district, sch, grade, fish_names)
        create_csv(grade_students, constants.STUDENTS)
        create_csv(parentz, constants.PARENTS)
        create_csv(external_user_stus, constants.EXTERNAL_USER_STUDENT)

        j += len(grade_students)
        total_count[3] += len(grade_students)
        total_count[5] += len(parentz)
        if(grade == sch.high_grade - 1):
            stu_num_in_grade = sch.num_of_student - j

        # assign teachers in the school to current grade
        grade_teachers = teacher_list
        if(tea_num_in_grade < len(teacher_list)):
            grade_teachers = random.sample(teacher_list, tea_num_in_grade)

        # create classes, sections for the current grade
        classforgrade_list = create_classes_for_grade(grade_students, grade_teachers, sch.sch_id, sch.stu_tea_ratio)

        # create_sections_stuandtea_csv(state['code'], classforgrade_list, grade, sch.sch_id, sch.dist_name, idgen)
        student_temporal_list = create_student_temporal_data(state.state_id, classforgrade_list, grade, sch.sch_id, sch.dist_name)
        # create_csv(student_temporal_list, STUDENT_SECTIONS)
        # create_csv(classforgrade_list, CLASSES)
        scores = generate_assmts_for_students(len(grade_students), grade, state.state_name, asmt_list)

        wheretaken_id = (random.choice(district.wheretaken_list)).wheretaken_id
        assessment_outcome_list = associate_students_and_scores(student_temporal_list, scores, sch, wheretaken_id, asmt_list)
        create_csv(assessment_outcome_list, constants.ASSESSMENT_OUTCOME)


def associate_students_and_scores(student_temporal_list, scores, school, wheretaken_id, asmt_list):
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
                    'school_id': school.sch_id,
                    'enrl_grade_id': stu_tmprl.grade_id,
                    'enrl_grade_code': stu_tmprl.grade_id,
                    'date_taken': date_taken,
                    'where_taken_id': wheretaken_id,
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
    parents = []
    external_users = []

    for i in range(num_students):
        stu, pars, ext_user = generate_student(state, district, school, grade, fish_names)
        students.append(stu)
        external_users.append(ext_user)
        for par in pars:
            parents.append(par)

    return students, parents, external_users


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


def create_classes_for_grade(grade_students, teacher_list, school_id, stu_tea_ratio):
    '''
    Main function to generate classes for a grade
    '''
    # stu_tea_ratio = len(grade_students) / len(teacher_list)

    # calculate max number of class for a subject
    max_num_of_class = max(1, round(len(grade_students) / constants.MIN_CLASS_SIZE))

    total_classes = []
    for subj in constants.SUBJECTS:
        # calculate number of classes for a subject
        if(max_num_of_class >= 2):
            class_num = random.choice(range(int(round(max_num_of_class / 3)), max_num_of_class))
        else:
            class_num = max_num_of_class

        # calculate number of teacher for a subject
        teacher_num = min(len(teacher_list), max(1, round(len(teacher_list) / len(constants.SUBJECTS))))
        subject_teachers = random.sample(teacher_list, teacher_num)

        subject_classes = create_classes(subj, class_num, grade_students, subject_teachers, stu_tea_ratio, school_id)
        total_classes.extend(subject_classes)

    return total_classes


def create_classes(sub_name, count, stu_list, tea_list, stu_tea_ratio, school_id):
    '''
    Main function to create classes for a grade of a subject
    '''
    # distribute students in each class
    distribute_stu_inclass = list_to_chucks(stu_list, count)
    # assert (0 <= len(distribute_stu_inclass) <= count)

    # create classes
    class_list = [create_one_class(sub_name, i, distribute_stu_inclass[i], tea_list, stu_tea_ratio, school_id) for i in range(len(distribute_stu_inclass))]

    return class_list


def create_one_class(sub_name, class_count, distribute_stu_inaclass, tea_list, stu_tea_ratio, school_id):
    '''
    Main function to create one class in a grade of a subject.
    Students and teachers are associated with sections
    '''
    # calculate number of sections
    num_of_stu_in_class = len(distribute_stu_inaclass)
    section_num = round(num_of_stu_in_class / stu_tea_ratio)
    if(num_of_stu_in_class < constants.MIN_SECTION_SIZE or section_num < 2):
        section_num = 1

    # distribute student in each section
    distribute_stu_insection = list_to_chucks(distribute_stu_inaclass, section_num)
    class_name = sub_name + " " + str(class_count)

    section_stu_map = {}
    section_tea_map = {}

    class_id = IdGen().get_id()
    section_list = []
    teacher_section_list = []
    # for each section, add students and teachers
    for i in range(len(distribute_stu_insection)):
        section_id = IdGen().get_id()
        section_stu_map[str(section_id)] = distribute_stu_insection[i]
        # one section has only one teacher
        section_tea_map[str(i)] = random.sample(tea_list, 1)

        # create section object
        section_name = 'section ' + str(i + 1)
        section = Section(section_id, uuid.uuid4(), school_id, section_name, class_name)
        section_list.append(section)

        # create teacher_section subject
        teacher_startdata = generate_date().strftime("%Y-%m-%d")
        teacher_section = TeacherSection(IdGen().get_id(), section_tea_map[str(i)][0].teacher_id, section_id, teacher_startdata)
        teacher_section_list.append(teacher_section)

    # write section into csv
    create_csv(section_list, constants.SECTIONS)

    # write teacher_section into csv
    create_csv(teacher_section_list, constants.TEACHER_SECTIONS)

    # create class, with sections
    eclass = Class(class_id, class_name, sub_name, section_stu_map, section_tea_map)

    return eclass


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


def list_to_chucks(list1, n):
    '''
    Divide list into n parts
    '''
    if(n == 1 or len(list1) <= n):
        return [list1]
    chucks_list = []
    random.shuffle(list1)
    chunk_length = round(len(list1) // n)
    needs_extra = len(list1) % n

    start = 0
    for i in range(n):
        if i < needs_extra:
            end = start + chunk_length + 1
        else:
            end = start + chunk_length
        chucks_list.append(list1[start:end])
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
