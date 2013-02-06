import math
import random
from datetime import date

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

birds_list = []
manmals_list = []
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
        manmals_list.extend(read_names(MANMALS_FILE))
        fish_list.extend(read_names(FISH_FILE))
    except:
        print("Exception for reading files")
        return False
    return True


def get_statistic():
    '''
    Get statistical data from database, which will be used in
    generating the actual data
    '''
    db = get_db_conn()
    dist_num_in_state = []
    db_states = []
    dist_count = db.prepare(query0)
    for count in dist_count:
        db_states.append((str(count['state_name']), str(count['state_code'])))
        dist_num_in_state.append(count['dist_num'])
    dist_num_in_state_made = makeup(dist_num_in_state, len(dist_num_in_state))

    print("Real      -- number of dist in states ", dist_num_in_state,
          " total ", sum(dist_num_in_state))
    print("Generated -- number of dist in states ", dist_num_in_state_made,
          " total ", sum(dist_num_in_state_made))

    actual_states = []
    c = 0
    for db_state_name in db_states:
        cur_state = {
                    'name': db_state_name[0],
                    'code': db_state_name[1],
                    'dist_num_in_state': dist_num_in_state_made[c],
                    'school_num_in_dist': [],
                    'stu_num_in_school': [],
                    'stutea_ratio_in_school': [],
                    'school_type_in_dist': []
                    }
        # get actual school_num distribution in state
        school_num = db.prepare(query2_first + db_state_name[0] + query2_second)
        for num in school_num:
            cur_state['school_num_in_dist'].append(num[0])

        # get actual student_num distribution in state
        stu_num = db.prepare(query3_first + db_state_name[0] + query3_second)
        for num in stu_num:
            cur_state['stu_num_in_school'].append(num[2])

        # get actual teacher_num distribution in state
        stutea_ratio = db.prepare(query6_first + db_state_name[0] + query6_second)
        for num in stutea_ratio:
            cur_state['stutea_ratio_in_school'].append(num[2])

        # get actual school_type distribution in state
        school_type = db.prepare(query4_first + db_state_name[0] + query4_second)
        cur_state['school_type_in_dist'] = generate_school_type(school_type)
        actual_states.append(cur_state)

        c += 1

    db.close()

    return actual_states


def generate_school_type(db_school_type_list):
    '''
    Input: database results, which has 3 columns: district_name, school_level, count
    Output: List of list. Each list has 4 items. Each item is the number of certain type of schools for a district
    '''
    school_type_in_dist = []
    types = {"Primary": 0, "Middle": 1, "High": 2, "Other": 3}
    cur_dist_name = ""
    cur_type = [0, 0, 0, 0]
    for s_type in db_school_type_list:
        if(s_type[0] != cur_dist_name):
            if(cur_dist_name != ""):
                school_type_in_dist.append(cur_type)
            cur_type = [0, 0, 0, 0]
            cur_dist_name = s_type[0]
        index = (int)(str(types.get(s_type[1].strip())))
        cur_type[index] = s_type[2]
    school_type_in_dist.append(cur_type)
    return school_type_in_dist


def generate_data(db_states):
    '''
    Main function to generate actual data with input statistical data
    '''
    c = 0
    record_states = []
    for state in db_states:
        print("This is state ", state['name'])

        # create state
        created_state = State(state['code'], state['name'], state['dist_num_in_state'])
        total_count[0] += 1
        record_states.append(created_state)

        # generate school distribution in districts
        school_num_in_dist = state['school_num_in_dist']
        school_num_in_dist_made = makeup(school_num_in_dist, state['dist_num_in_state'])

        # generate student distribution in schools
        stu_num_in_school = state['stu_num_in_school']
        stu_num_in_school_made = makeup(stu_num_in_school, sum(school_num_in_dist_made))

        # generate teacher distribution in schools
        stutea_ratio_in_school = state['stutea_ratio_in_school']
        stutea_ratio_in_school_made = makeup(stutea_ratio_in_school, sum(school_num_in_dist_made))
        # tea_num_in_school_made = make_teacher_num(stu_num_in_school_made, stutea_ratio_in_school_made)

        # list of lists. For each list in it, it maps to district level
        school_type_in_dist = state['school_type_in_dist']

        # print out
        print("************** State ", created_state.state_name, " **************")
        print("                     Real     Generated")
        print("Number of districts ", len(school_num_in_dist), "    ", len(school_num_in_dist_made))
        print("Number of schools   ", sum(school_num_in_dist), "    ", sum(school_num_in_dist_made))
        print("Number of students  ", sum(stu_num_in_school), "    ", sum(stu_num_in_school_made))

        # create districts for each state
        created_dist_list = create_districts(created_state.state_name, school_num_in_dist_made, school_type_in_dist, c)
        total_count[1] += len(created_dist_list)
        create_csv(created_dist_list, INSTITUTIONS)
        shift = 0

        for d in created_dist_list:
            # create school for each district
            school_list, wheretaken_list = create_schools(stu_num_in_school_made, stutea_ratio_in_school_made, shift, d)
            total_count[2] += len(school_list)
            create_csv(school_list, INSTITUTIONS)
            create_csv(wheretaken_list, WHERETAKEN)

            shift += d.num_of_schools

            # create classes, grades, sections, teachers and students for each school
            for sch in school_list:
                create_classes_grades_sections(sch, state)

        assessment_types = generate_assessment_types()
        create_csv(assessment_types, ASSESSMENT_TYPES)

        # if just need one state data
        if(c == 0):
            break
        c += 1

    create_csv(record_states, STATES)

    print("*************************************")
    print("generated number of states    ", total_count[0])
    print("generated number of districts ", total_count[1])
    print("generated number of schools   ", total_count[2])
    print("generated number of students  ", total_count[3])
    print("generated number of teachers  ", total_count[4])


def make_teacher_num(stu_num_in_school_made, stutea_ratio_in_school_made):
    '''
    input: stu_num_in_school_made:       list of student number in each school
           stutea_ratio_in_school_made:  list of student_teacher_ratio in each school

    output: list of teacher number in each school calculates as: student_number/student_teacher_ratio
    '''
    assert(len(stu_num_in_school_made) == len(stutea_ratio_in_school_made))
    teacher_num = []
    for i in range(len(stu_num_in_school_made)):
        teacher_num.append(max(1, (int)(round(stu_num_in_school_made[i] / stutea_ratio_in_school_made[i]))))
    return teacher_num


def create_districts(state_name, school_num_in_dist_made, school_type_in_dist, pos):
    '''
    Main function to generate list of district for a state
    '''
    total_school = 0
    districts_list = []
    n = len(school_num_in_dist_made)
    # assert(n == len(school_type_in_dist_made[0]))
    if(n > 0):
        # generate random district names
        try:
            names = generate_names_from_lists(n, birds_list, manmals_list)
        except ValueError:
            print("ValueError: Not enough list to create", n, " number of district names", n, len(birds_list), len(manmals_list))

            return []

        # generate random district addresses
        address = generate_address_from_list(n, fish_list)

        # generate random district zip range
        zip_init = (pos + 1) * ZIPCODE_START
        zip_dist = max(1, (ZIPCODE_RANG_INSTATE // n))

        # generate each district
        for i in range(n):
            # generate district id
            dist_id = idgen.get_id()
            # generate random city names for a district
            try:
                city_names = generate_names_from_lists(school_num_in_dist_made[i], birds_list, fish_list)
            except ValueError:
                print("ValueError: Not enough list to create", school_num_in_dist_made[i], " number of city names")
                return []

            # calculate school_type
            # school_type = [school_type_in_dist_made[t][i] for t in range(len(school_type_in_dist_made))]

            # create district object
            dist = District(dist_id, state_name, (names[i] + " " + random.choice(DIST_SUFFIX)),
                            school_num_in_dist_made[i], address[i], school_type_in_dist[i % len(school_type_in_dist)],
                            (zip_init, (zip_init + zip_dist)), city_names, INST_CATEGORIES[2])
            districts_list.append(dist)
            total_school += dist.num_of_schools
            zip_init += zip_dist

    assert(total_school == sum(school_num_in_dist_made))

    return districts_list


def create_schools(stu_num_in_school_made, stutea_ratio_in_school_made, start, distr):
    '''
    Main function to generate list of schools for a district
    '''
    count = distr.num_of_schools
    # generate random school names
    try:
        names = generate_names_from_lists(count, fish_list, manmals_list)
    except ValueError:
        print("ValueError: Not enough list to create", count, " number of school names")
        return [], []

    # generate addresses
    address = generate_address_from_list(count, birds_list)

    # generate number of schools for each type
    school_num_for_type = cal_school_num_for_type(count, distr.school_type_in_dist)
    assert(count == sum(school_num_for_type))

    # generate zipcode and citynames
    city_zipcode_map = generate_city_zipcode(distr.city_names, distr.zipcode_range, count)

    school_list = []
    wheretaken_list = []

    sch_type_index = 0
    s_index = 0
    e_index = school_num_for_type[sch_type_index]

    # generate each school and where-taken row
    while(count > 0):
        if(e_index > s_index):
            for i in range(s_index, e_index):
                # get school_type
                school_type, suf, low_grade, high_grade = get_schoolattr_bytype(sch_type_index)
                count -= 1

                # create one row of where-taken
                sch_add1 = address[count]
                place_id = idgen.get_id()
                r_city = random.choice(list(city_zipcode_map.items()))
                r_zip = random.choice(range(r_city[1][0], r_city[1][1]))
                where_taken = WhereTaken(place_id, sch_add1, '', '', r_city[0], distr.state_name, r_zip, 'US')
                wheretaken_list.append(where_taken)

                # create one row of school
                sch_id = idgen.get_id()
                sch_name = names[count] + " " + suf
                school = School(sch_id, distr.dist_id, sch_name, stu_num_in_school_made[start + i],
                        stutea_ratio_in_school_made[start + i], sch_add1, school_type,
                        low_grade, high_grade, place_id, INST_CATEGORIES[3])
                school_list.append(school)

        sch_type_index += 1
        s_index = e_index
        if(sch_type_index < len(school_num_for_type)):
            e_index = s_index + school_num_for_type[sch_type_index]

    return school_list, wheretaken_list


def generate_city_zipcode(city_names, zipcode_range, num_of_schools):
    maxnum_of_city = min((zipcode_range[1] - zipcode_range[0]), num_of_schools)
    num_of_city = 1
    if(num_of_schools > 1):
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


def get_schoolattr_bytype(pos):
    if(0 <= pos <= 3):
        school_type = SCHOOL_LEVELS_INFO[pos][0]
        suf = random.choice(SCHOOL_LEVELS_INFO[pos][1])
        grade_range = random.choice(SCHOOL_LEVELS_INFO[pos][2])
        low_grade = grade_range[0]
        high_grade = grade_range[1]
    return school_type, suf, low_grade, high_grade


def cal_school_num_for_type(count, school_type_in_dist):
    school_for_type = []
    if(count > 0 and len(school_type_in_dist) == 4):
        total = sum(school_type_in_dist)
        if(total == 0):
            school_type_in_dist[0] = count
            total = sum(school_type_in_dist)

        school_type_in_dist.sort(reverse=True)
        school_for_type = [round(count * (s_num / total)) for s_num in school_type_in_dist[:-1]]
        school_for_type.append(count - sum(school_for_type))

    return school_for_type


def generate_names_from_lists(count, list1, list2):
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


def create_classes_grades_sections(sch, state):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''
    # calculate number of students in each grade
    stu_num_in_grade = round(sch.num_of_student / (sch.high_grade - sch.low_grade + 1))
    end = stu_num_in_grade

    # generate teacher list for a school
    num_of_teacher = max(1, (sch.num_of_student // sch.stu_tea_ratio))
    teacher_list = generate_people(TEACHER, num_of_teacher, sch, state['code'], random.choice(GENDER_RARIO))
    num_of_tea_for_grade = max(1, (num_of_teacher // (sch.high_grade - sch.low_grade + 1)))
    #print("num_of_tea_for_grade1 ", num_of_tea_for_grade, (num_of_teacher // (sch.high_grade - sch.low_grade + 1)))
    num_of_tea_for_grade = min(len(teacher_list), num_of_tea_for_grade)
    #print("num_of_tea_for_grade2 ", num_of_tea_for_grade, len(teacher_list), num_of_tea_for_grade)

    total_count[4] += len(teacher_list)
    create_csv(teacher_list, TEACHERS)

    j = 0
    for grade in range(sch.low_grade, sch.high_grade + 1):
        # generate student list for a grade
        grade_students = generate_people(STUDENT, end, sch, state['code'], random.choice(GENDER_RARIO), grade)
        create_csv(grade_students, STUDENTS)

        j += len(grade_students)
        total_count[3] += len(grade_students)
        if(grade == sch.high_grade - 1):
            end = sch.num_of_student - j

        teach = teacher_list
        if(num_of_tea_for_grade < len(teacher_list)):
            teach = random.sample(teacher_list, num_of_tea_for_grade)

        classforgrade_list = create_classes_for_grade(grade_students, teach, sch.stu_tea_ratio)

        # create_sections_stuandtea_csv(state['code'], classforgrade_list, grade, sch.sch_id, sch.dist_name, idgen)
        student_temporal_list = create_student_temporal_data(state['code'], classforgrade_list, grade, sch.sch_id, sch.dist_id)
        create_csv(student_temporal_list, STUDENT_SECTIONS)
        create_csv(classforgrade_list, CLASSES)

        scores = generate_assmts_for_students(len(grade_students), grade, state['name'])
        assessment_outcome_list = []
        hist_assessment_outcome_list = []

        dates_taken1 = generate_dates_taken(2000)
        dates_taken2 = generate_dates_taken(2000)

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

                    outcome = AssessmentOutcome(new_id, asmt_id, stu_tmprl.student_id, stu_tmprl.student_tmprl_id, teacher_id, date_taken, sch.place_id, score[1].pop(), 'cdate?')
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

                    outcome = HistAssessmentOutcome(new_id, asmt_id, stu_tmprl.student_id, stu_tmprl.student_tmprl_id, date_taken, sch.place_id, score[1].pop(), 'cdate?', 'hdate?')
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


def create_student_temporal_data(state_code, class_list, grade, school_id, district_id):
    '''
    Creates and returns a list of StudentTemporalData objects
    '''
    temporal_list = []

    for cls in class_list:

        for sect, stus in cls.section_stu_map.items():
            for stu in stus:
                tmprl_id = idgen.get_id()
                student_temporal = StudentTemporalData(tmprl_id, stu.student_id, grade, district_id, school_id, cls, sect)
                temporal_list.append(student_temporal)

    return temporal_list


def create_classes_for_grade(grade_students, teacher_list, stu_tea_ratio):
    '''
    Main function to generate classes for a grade
    '''
    # calculate number of class for a subject
    num_of_subjects = len(SUBJECTS)
    max_num_of_class = round(num_of_subjects * len(grade_students) / MIN_CLASS_SIZE)
    num_of_class = num_of_subjects
    if(max_num_of_class > num_of_subjects):
        # num_of_class = random.choice(range(num_of_subjects, max_num_of_class))
        num_of_class = random.choice(range((int)(round(max_num_of_class / 2)), max_num_of_class))
    if(num_of_subjects == 0 or round(num_of_class / num_of_subjects) < 1):
        class_num = 1
    else:
        class_num = round(num_of_class / num_of_subjects)

    # create classes for a subject
    total_classes = []
    for subj in SUBJECTS:
        num_of_teacher_forsub = min(len(teacher_list), max(1, (len(teacher_list) // len(SUBJECTS))))

        subject_teachers = random.sample(teacher_list, num_of_teacher_forsub)
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
    section_num = math.floor(num_of_stu_in_class // stu_tea_ratio)
    if(num_of_stu_in_class < MIN_SECTION_SIZE or section_num < 2):
        section_num = 1

    if(num_of_stu_in_class / section_num > 100):
        print("big section", section_num, stu_tea_ratio, num_of_stu_in_class)

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
        num_of_tea = max(1, (int)(round(len(distribute_stu_insection[i]) / stu_tea_ratio)))
        num_of_tea = min(num_of_tea, len(tea_list))
        section_tea_map[str(i)] = random.sample(tea_list, num_of_tea)

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
    chunk_length = len(list1) // n
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


def makeup(seqin, lengh):
    # avg1 = py1.avg(seqin)
    mean1 = py1.mean(seqin)
    std1 = py1.std(seqin)
    min1 = min(seqin)
    max1 = max(seqin)
    out1 = py1.makeup_core(mean1, std1, min1, max1, lengh)
    out_data1 = fit_in_order(out1, seqin)
    return out_data1


def fit_in_order(data_list, orig_list):
    index_list = get_index(orig_list)
    sorted_data = sorted(data_list)
    len_dis = len(data_list) - len(orig_list)
    d = dict(zip(index_list, sorted_data))
    v = []
    for dd in d.values():
        v.append(dd)
    while(len_dis > 0):
        cur = sorted_data[len(sorted_data) - len_dis]
        len_dis -= 1
        v.insert(random.randint(1, len(v) - 1), cur)
    return v


def get_index(seqin):
    d = {}
    for i in range(len(seqin)):
        d[i] = seqin[i]
    res = sorted(d.items(), key=lambda x: x[1])
    final = [x[0] for x in res]
    return final


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
    # print(read_names("../datafiles/temp.txt"))
    t2 = datetime.now()
    print("starts ", t1)
    print("ends   ", t2)
