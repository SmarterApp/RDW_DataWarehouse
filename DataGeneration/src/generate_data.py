import math
from datetime import date
import random

import py1
from queries import *
from write_to_csv import *
from entities import *
from datetime import datetime
from test.test_iterlen import len
from genpeople import generate_people, STUDENT, TEACHER
from idgen import IdGen
from gen_assessments import generate_assessment_types, ASSESSMENT_TYPES_LIST
from constants import *
from dbconnection import get_db_conn
from assessment import generate_assmts_for_students
from xmlrpc.client import MAXINT

birds_list = []
mammals_list = []
fish_list = []

# total count for state, districts, schools, students, teachers
total_count = [0, 0, 0, 0, 0]
idgen = IdGen()


def generate():
    '''
    Generate data.
    First step: read files into lists for making names, addresses
    Second step: get statistical data from database
    Third step: if first two steps are successful, start generate data process.
    (including generate: state, district, school, class, section, student,
    and teacher)
    '''
    read_files = prepare_data()
    db_states = get_statistic()

    if(read_files is False or db_states is None or len(db_states) == 0):
        print("Initializing....Error")
        return

    generate_data(db_states)


def prepare_data():
    '''
    Read files into lists, which is used for making names, addresses, etc
    '''
    # clear old files
    clear_files()

    try:
        birds_list.extend(read_names(BIRDS_FILE))
        mammals_list.extend(read_names(MAMMALS_FILE))
        fish_list.extend(read_names(FISH_FILE))
    except IOError as e:
        print("Exception for reading files: " + str(e))
        return False
    return True


def get_statistic():
    db = get_db_conn()
    db_states = []
    dist_count = db.prepare('select * from school_generate_stat')
    for row in dist_count:
        db_states.append(dict(zip(STAT_COLUMNS, row)))
    db.close()
    return db_states


def generate_data(db_states_stat):
    '''
    Main function to generate actual data with input statistical data
    '''
    # generate all assessment types
    assessment_types = generate_assessment_types()
    create_csv(assessment_types, ASSESSMENT_TYPES)

    c = 0
    record_states = []
    for state in db_states_stat:
        # create state
        created_state = State(state['state_code'], state['state_name'], state['total_district'], state['state_code'])
        total_count[0] += 1
        record_states.append(created_state)

        # generate school distribution in districts
        min_dis = max(1, math.ceil(state['total_district'] * DIST_LOW_VALUE))
        max_dis = round(state['total_district'] * DIST_HIGH_VALUE)
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

        # print out
        print("************** State ", created_state.state_name, " **************")
        print("                     Real     Generated")
        print("Number of districts ", state['total_district'], "    ", len(school_num_in_dist_made))
        print("Number of schools   ", state['total_school'], "    ", sum(school_num_in_dist_made))
        print("Number of students  ", state['total_student'], "    ", sum(stu_num_in_school_made))
        # continue
        # create districts for each state
        created_dist_list = create_districts(created_state.state_id, school_num_in_dist_made, c)
        total_count[1] += len(created_dist_list)
        create_csv(created_dist_list, DISTRICTS)
        shift = 0

        for dist in created_dist_list:
            # create school for each district
            school_list, wheretaken_list = create_schools(stu_num_in_school_made[shift: shift + dist.num_of_schools],
                                                          stutea_ratio_in_school_made[shift: shift + dist.num_of_schools],
                                                          dist, school_type_in_state)
            total_count[2] += len(school_list)
            create_csv(school_list, SCHOOLS)
            create_csv(wheretaken_list, WHERETAKEN)

            shift += dist.num_of_schools

            # create classes, grades, sections, teachers students, parents and assessment scores for each school
            for sch in school_list:
                create_classes_grades_sections(sch, created_state)

        # if just need one state data
        if(c == 0):
            break
        c += 1

    create_csv(record_states, STATES)

    print("**************Results***********************")
    print("generated number of states    ", total_count[0])
    print("generated number of districts ", total_count[1])
    print("generated number of schools   ", total_count[2])
    print("generated number of students  ", total_count[3])
    print("generated number of teachers  ", total_count[4])


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
            count.append(round(total * perc[i]))
            repeat_types.extend([SCHOOL_LEVELS_INFO[i][0]] * count[-1])
            control = sum(count)

        count.append(max(total - control, 0))
        repeat_types.extend([SCHOOL_LEVELS_INFO[i][0]] * count[-1])

    return repeat_types


def create_districts(state_code, school_num_in_dist_made, pos):
    '''
    Main function to generate list of district for a state
    '''
    total_school = 0
    districts_list = []
    n = len(school_num_in_dist_made)

    if(n > 0):
        # generate random district names
        try:
            names = generate_names_from_lists(n, birds_list, mammals_list)
        except ValueError:
            print("ValueError: Not enough list to create", n, " number of district names", n, len(birds_list), len(mammals_list))
            return []

        # generate random district addresses
        address = generate_address_from_list(n, fish_list)

        # generate random district zip range
        zip_init, zip_dist = cal_zipvalues(pos, n)

        # generate each district
        for i in range(n):
            # generate random city names for a district
            try:
                city_names = generate_names_from_lists(school_num_in_dist_made[i], birds_list, fish_list)
            except ValueError:
                print("ValueError: Not enough list to create", school_num_in_dist_made[i], " number of city names")
                return []

            # create district object
            district_id = idgen.get_id()
            district_external_id = 'district_external_id'
            district_name = names[i] + " " + random.choice(DIST_SUFFIX)
            address1 = address[i]
            dist = District(district_id, district_external_id, district_name, state_code, school_num_in_dist_made[i], (zip_init, (zip_init + zip_dist)), city_names, address1, zip_init)
            districts_list.append(dist)
            total_school += dist.num_of_schools
            zip_init += zip_dist

    return districts_list


def create_schools(stu_num_in_school_made, stutea_ratio_in_school_made, distr, school_type_in_state):
    '''
    Main function to generate list of schools for a district
    '''
    count = distr.num_of_schools
    # generate random school names
    try:
        names = generate_names_from_lists(count, fish_list, mammals_list)
    except ValueError:
        print("ValueError: Not enough list to create", count, " number of school names")
        return [], []

    # generate addresses
    address = generate_address_from_list(count, birds_list)

    # generate zipcode and citynames
    city_zipcode_map = generate_city_zipcode(distr.city_names, distr.zipcode_range, count)

    school_list = []
    wheretaken_list = []

    # generate each school and where-taken row
    for i in range(count):
        # get categories
        school_categories_type = random.choice(school_type_in_state)
        suf = random.choice(SCHOOL_LEVELS_INFO[SCHOOL_ORDER_MAP.get(school_categories_type)][1])
        grade_range = random.choice(SCHOOL_LEVELS_INFO[SCHOOL_ORDER_MAP.get(school_categories_type)][2])
        low_grade = grade_range[0]
        high_grade = grade_range[1]

        # create common fields
        sch_name = names[i] + " " + suf
        address_1 = address[i]
        city = random.choice(list(city_zipcode_map.items()))
        city_name = city[0]
        zip_code = random.choice(range(city[1][0], city[1][1]))

        # create one row of where-taken
        wheretaken_id = idgen.get_id()
        wheretaken_name = 'wheretaken_name'
        where_taken = WhereTaken(wheretaken_id, wheretaken_name, distr.district_name, address_1, city_name, zip_code, distr.state_code, 'US')
        wheretaken_list.append(where_taken)

        # create one row of school
        sch_id = idgen.get_id()
        school_external_id = 'school_external_id'
        school_type = random.choice(SCHOOL_TYPES)
        school = School(sch_id, school_external_id, sch_name, distr.district_name, distr.state_code,
                        stu_num_in_school_made[i], stutea_ratio_in_school_made[i], low_grade, high_grade,
                        school_categories_type, school_type, address_1, city_name, zip_code)
        school_list.append(school)

    return school_list, wheretaken_list


def generate_city_zipcode(city_names, zipcode_range, num_of_schools):
    '''
    Generate zip code range for cities
    '''
    maxnum_of_city = min((zipcode_range[1] - zipcode_range[0]), num_of_schools)
    num_of_city = 1
    if(num_of_schools > 1 and maxnum_of_city > 1):
        num_of_city = random.choice(range(1, maxnum_of_city))

    city_cand = random.sample(city_names, num_of_city)
    ziprange_incity = (zipcode_range[1] - zipcode_range[0]) // num_of_city
    zip_start = zipcode_range[0]

    city_zip_map = {}
    for i in range(len(city_cand) - 1):
        zip_end = (int)(zip_start + ziprange_incity)
        city_zip_map[city_cand[i]] = [zip_start, zip_end]
        zip_start = zipcode_range[0] + ziprange_incity * (i + 1)

    city_zip_map[city_cand[len(city_cand) - 1]] = [zip_start, (int)(zipcode_range[1])]

    return city_zip_map


def generate_names_from_lists(count, list1, list2):
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

        names = [str(name1) + " " + str(name2) for name1 in names1 for name2 in names2]

    new_list = []
    new_list.extend(names[0:count])
    return new_list


def generate_address_from_list(count, words_list):
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
        adds = [str(no[i]) + " " + str(road_name[i % len(road_name)]) + " " + random.choice(ADD_SUFFIX) for i in range(count)]
    return adds


def cal_zipvalues(pos, n):
    '''
    Input: pos: greater than 0
           n: total number of zip. It is greater than 0
    Output: zip_init: the starting zipcode
            zio_dist: the basic distance of zipcode
    '''

    zip_init = (pos + 1) * ZIPCODE_START
    zip_dist = max(1, (ZIPCODE_RANG_INSTATE // n))
    return zip_init, zip_dist


def create_classes_grades_sections(sch, state):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''
    # generate teacher list for a school
    num_of_teacher = max(1, round(sch.num_of_student // sch.stu_tea_ratio))
    teacher_list = generate_people(TEACHER, num_of_teacher, sch, state.state_id, random.choice(GENDER_RARIO))
    total_count[4] += len(teacher_list)
    create_csv(teacher_list, TEACHERS)

    # calculate number of students and teachers in each grade
    stu_num_in_grade = max(1, round(sch.num_of_student / (sch.high_grade - sch.low_grade + 1)))
    tea_num_in_grade = max(1, round(num_of_teacher / (sch.high_grade - sch.low_grade + 1)))

    # for each grade
    j = 0
    for grade in range(sch.low_grade, sch.high_grade + 1):
        # generate student list for a grade
        grade_students = generate_people(STUDENT, stu_num_in_grade, sch, state.state_id, random.choice(GENDER_RARIO), grade)
        create_csv(grade_students, STUDENTS)
        j += len(grade_students)
        total_count[3] += len(grade_students)
        if(grade == sch.high_grade - 1):
            stu_num_in_grade = sch.num_of_student - j

        # assign teachers in the school to current grade
        grade_teachers = teacher_list
        if(tea_num_in_grade < len(teacher_list)):
            grade_teachers = random.sample(teacher_list, tea_num_in_grade)

        # create classes, sections for the current grade
        classforgrade_list = create_classes_for_grade(grade_students, grade_teachers)

        # create_sections_stuandtea_csv(state['code'], classforgrade_list, grade, sch.sch_id, sch.dist_name, idgen)
        student_temporal_list = create_student_temporal_data(state.state_id, classforgrade_list, grade, sch.sch_id, sch.dist_name)
        create_csv(student_temporal_list, STUDENT_SECTIONS)
        create_csv(classforgrade_list, CLASSES)

        scores = generate_assmts_for_students(len(grade_students), grade, state.state_name)
        assessment_outcome_list = []
        hist_assessment_outcome_list = []

        dates_taken1 = generate_dates_taken(2000)
        dates_taken2 = generate_dates_taken(2000)
        print("len of grade students ", len(grade_students), "len of classforgrade_list ", len(classforgrade_list),
              "len of student_temporal_list ", len(student_temporal_list), "len of scores ", len(scores))
        for stu_tmprl in student_temporal_list:
            for score in scores.items():
                asmt_id = int(score[0].split('_')[1])
                year = score[0].split('_')[0]
                asmt = [x for x in ASSESSMENT_TYPES_LIST if x.assmt_id == asmt_id][0]
                subject = stu_tmprl.student_class.sub_name
                if subject == 'Math':
                    subject = 'MATH'
                if int(year) == date.today().year and stu_tmprl.student_class.sub_name == asmt.subject:
                    new_id = idgen.get_id()
                    teacher_list = list(stu_tmprl.student_class.section_tea_map.values())
                    teacher_list = [item for sub in teacher_list for item in sub]  # flatten teacher_list
                    teacher = teacher_list[0]
                    teacher_id = teacher.teacher_id

                    date_taken = None
                    if asmt.period == 'BOY':
                        date_taken = dates_taken1['BOY']
                    elif asmt.period == 'MOY':
                        date_taken = dates_taken1['MOY']
                    elif asmt.period == 'EOY':
                        date_taken = dates_taken1['EOY']
                    date_taken = date_taken.replace(year=int(year))
                    if (len(score[1]) == 0):
                        print("*********Import**********", new_id, asmt_id, stu_tmprl.student_id, stu_tmprl.student_tmprl_id, teacher_id, date_taken, sch.place_id)
                    outcome = AssessmentOutcome(new_id, asmt_id, stu_tmprl.student_id, stu_tmprl.student_tmprl_id, teacher_id, date_taken, sch.sch_id, score[1].pop(), 'cdate?')
                    assessment_outcome_list.append(outcome)
                elif stu_tmprl.student_class.sub_name == asmt.subject:
                    new_id = idgen.get_id()
                    teacher_list = list(stu_tmprl.student_class.section_tea_map.values())
                    teacher_list = [item for sub in teacher_list for item in sub]  # flatten teacher_list
                    teacher = teacher_list[0]
                    teacher_id = teacher.teacher_id

                    date_taken = None
                    if asmt.period == 'BOY':
                        date_taken = dates_taken2['BOY']
                    elif asmt.period == 'MOY':
                        date_taken = dates_taken2['MOY']
                    elif asmt.period == 'EOY':
                        date_taken = dates_taken2['EOY']
                    date_taken = date_taken.replace(year=int(year))

                    if (len(score[1]) == 0):
                        print("*********Import**********", new_id, asmt_id, stu_tmprl.student_id, stu_tmprl.student_tmprl_id, teacher_id, date_taken, sch.place_id)

                    outcome = HistAssessmentOutcome(new_id, asmt_id, stu_tmprl.student_id, stu_tmprl.student_tmprl_id, date_taken, sch.sch_id, score[1].pop(), 'cdate?', 'hdate?')
                    hist_assessment_outcome_list.append(outcome)

        create_csv(assessment_outcome_list, ASSESSMENT_OUTCOME)
        create_csv(hist_assessment_outcome_list, HIST_ASSESSMENT_OUTCOME)


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
                tmprl_id = idgen.get_id()
                student_temporal = StudentTemporalData(tmprl_id, stu.student_id, grade, dist_name, school_id, cls, sect)
                temporal_list.append(student_temporal)

    return temporal_list


def create_classes_for_grade(grade_students, teacher_list):
    '''
    Main function to generate classes for a grade
    '''
    stu_tea_ratio = len(grade_students) / len(teacher_list)

    # calculate max number of class for a subject
    max_num_of_class = max(1, round(len(grade_students) / MIN_CLASS_SIZE))

    total_classes = []
    for subj in SUBJECTS:
        # calculate number of classes for a subject
        if(max_num_of_class >= 2):
            class_num = random.choice(range((int)(round(max_num_of_class / 2)), max_num_of_class))
        else:
            class_num = max_num_of_class

        # calculate number of teacher for a subject
        teacher_num = min(len(teacher_list), max(1, round(len(teacher_list) / len(SUBJECTS))))
        subject_teachers = random.sample(teacher_list, teacher_num)

        subject_classes = create_classes(subj, class_num, grade_students, subject_teachers, stu_tea_ratio)
        total_classes.extend(subject_classes)

    return total_classes


def create_classes(sub_name, count, stu_list, tea_list, stu_tea_ratio):
    '''
    Main function to create classes for a grade of a subject
    '''
    # distribute students in each class
    distribute_stu_inclass = list_to_chucks(stu_list, count)
    assert (0 <= len(distribute_stu_inclass) <= count)

    # create classes
    class_list = [create_one_class(sub_name, i, distribute_stu_inclass[i], tea_list, stu_tea_ratio) for i in range(len(distribute_stu_inclass))]

    return class_list


def create_one_class(sub_name, class_count, distribute_stu_inaclass, tea_list, stu_tea_ratio):
    '''
    Main function to create one class in a grade of a subject.
    Students and teachers are associated with sections
    '''
    # calculate number of sections
    num_of_stu_in_class = len(distribute_stu_inaclass)
    section_num = round(num_of_stu_in_class // stu_tea_ratio)
    if(num_of_stu_in_class < MIN_SECTION_SIZE or section_num < 2):
        section_num = 1

    # distribute student in each section
    distribute_stu_insection = list_to_chucks(distribute_stu_inaclass, section_num)
    title = sub_name + " " + str(class_count)

    section_stu_map = {}
    section_tea_map = {}

    class_id = idgen.get_id()
    # for each section, add students and teachers
    for i in range(len(distribute_stu_insection)):
        section_id = idgen.get_id()
        section_stu_map[str(section_id)] = distribute_stu_insection[i]
        # one section has only one teacher
        section_tea_map[str(i)] = random.sample(tea_list, 1)

    # create class, with sections
    eclass = Class(class_id, title, sub_name, section_stu_map, section_tea_map)

    return eclass


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
    for i in range(RETRY_CAL_STAT):
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
    t1 = datetime.now()
    generate()
    # print(get_statistic3())
    # print(make_school_types([0.5, 0.3, 0.1, 0.1], 100))
    t2 = datetime.now()
    print("starts ", t1)
    print("ends   ", t2)
