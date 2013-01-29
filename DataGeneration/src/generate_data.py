import math
import random
import py1
from queries import *
from write_to_csv import *
from entities import *
import postgresql.driver.dbapi20 as dbapi
from datetime import datetime
from test.test_iterlen import len
from genpeople import generate_people, STUDENT, TEACHER
from gen_assessments import generate_assessments
from constants import *

birds_list = []
manmals_list = []
fish_list = []

# total count for state, districts, schools, students, teachers
total_count = [0, 0, 0, 0, 0]


def generate():
    '''
    Generate data.
    First step: read files into lists for making names, addresses
    Second step: get statistical data from database
    Third step: if first two steps are successful, start generate data process.
    (including generate: state, district, school, class, section, student, and teacher)
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
    Get statistical data from database, which will be used in generating the actual data
    '''
    db = dbapi.connect(user='postgres', database='generate_data', port=5432, password='3423346', host="localhost")
    dist_num_in_state = []
    db_states = []
    dist_count = db.prepare(query0)
    for count in dist_count:
        db_states.append((str(count['state_name']), str(count['state_code'])))
        dist_num_in_state.append(count['dist_num'])
    dist_num_in_state_made = makeup(dist_num_in_state, len(dist_num_in_state))

    print("Real      -- number of dist in states ", dist_num_in_state, " total ", sum(dist_num_in_state))
    print("Generated -- number of dist in states ", dist_num_in_state_made, " total ", sum(dist_num_in_state_made))

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


def generate_data(db_states):
    '''
    Main function to generate actual data with input statistical data
    '''
    c = 0
    for state in db_states:
        print("This is state ", state['name'])

        # create state
        created_state = State(state['name'], state['code'], state['dist_num_in_state'])
        total_count[0] += 1
        create_states_csv(created_state)

        # generate school distribution in districts
        school_num_in_dist = state['school_num_in_dist']
        school_num_in_dist_made = makeup(school_num_in_dist, state['dist_num_in_state'])

        # generate student distribution in schools
        stu_num_in_school = state['stu_num_in_school']
        stu_num_in_school_made = makeup(stu_num_in_school, sum(school_num_in_dist_made))

        # generate teacher distribution in schools
        stutea_ratio_in_school = state['stutea_ratio_in_school']
        stutea_ratio_in_school_made = makeup(stutea_ratio_in_school, sum(school_num_in_dist_made))
        tea_num_in_school_made = make_teacher_num(stu_num_in_school_made, stutea_ratio_in_school_made)

        # list of lists. For each list in it, it maps to district level
        school_type_in_dist = state['school_type_in_dist']
        assert(len(stu_num_in_school_made) == sum(school_num_in_dist_made))

        # print out
        print("************** State ", created_state.name, " **************")
        print("                     Real     Generated")
        print("Number of districts ", len(school_num_in_dist), "    ", len(school_num_in_dist_made))
        print("Number of schools   ", sum(school_num_in_dist), "    ", sum(school_num_in_dist_made))
        print("Number of students  ", sum(stu_num_in_school), "    ", sum(stu_num_in_school_made))
        # print("Max Number of stu   ", max(stu_num_in_school), "    ", max(stu_num_in_school_made))

        # create districts for each state
        created_dist_list = create_districts(created_state.name, school_num_in_dist_made, school_type_in_dist)
        total_count[1] += len(created_dist_list)
        create_districts_csv(created_dist_list)
        shift = 0

        for d in created_dist_list:
            # create school for each district
            school_list = create_schools(d.dist_name, stu_num_in_school_made, tea_num_in_school_made, shift, d.num_of_schools, d.school_type_in_dist)
            total_count[2] += len(school_list)
            create_schools_csv(school_list)
            shift += d.num_of_schools

            # create classes, grades, sections, teachers and students for each school
            for sch in school_list:
                create_classes_grades_sections(sch, state['code'])

        generate_assessments()

        # if just need one state data
        if(c == 0):
            break

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
        teacher_num.append((int)(round(stu_num_in_school_made[i] / stutea_ratio_in_school_made[i])))
    return teacher_num


def generate_school_type(db_school_type_list):
    school_type_in_dist = []
    types = {"Primary": 0, "Middle": 1, "High": 2, "Other": 3}
    cur_dist_name = ""
    cur_type = [0, 0, 0, 0]
    for s_type in db_school_type_list:
        if(s_type[0] != cur_dist_name and cur_dist_name != ""):
            school_type_in_dist.append(cur_type)
            cur_type = [0, 0, 0, 0]
            cur_dist_name = s_type[0]
        index = (int)(str(types.get(s_type[1].strip())))
        cur_type[index] = s_type[2]
    school_type_in_dist.append(cur_type)
    return school_type_in_dist


def create_schools(d_name, stu_num_in_school_made, tea_num_in_school_made, start, count, school_type_in_dist):
    '''
    Main function to generate list of schools for a district
    '''
    # generate random school names
    try:
        names = generate_names_from_lists(count, fish_list, manmals_list)
    except:
        ValueError
        return []
    # generate addresses
    address = generate_address_from_list(count, birds_list)
    assert(len(names) == len(address))

    school_num_for_type = cal_school_num_for_type(count, school_type_in_dist)
    assert(sum(school_num_for_type) == count)

    school_list = []
    while(count > 0):

        if(school_num_for_type[0] > 0):
            index = 0

        elif(school_num_for_type[1] > 0):
            index = 1

        elif(school_num_for_type[2] > 0):
            index = 2

        elif(school_num_for_type[3] > 0):
            index = 3

        school_num_for_type[index] -= 1
        school_type, suf, low_grade, high_grade = get_schoolattr_bytype(index)

        count -= 1
        school = School(d_name, (names[count] + " " + suf), stu_num_in_school_made[start], tea_num_in_school_made[start], address[count], school_type, low_grade, high_grade)
        start += 1
        school_list.append(school)

    return school_list


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
    if(count > 0 and sum(school_type_in_dist) > 0 and len(school_type_in_dist) == 4):
        total = sum(school_type_in_dist)
        school_for_type = [round(count * (s_num / total)) for s_num in school_type_in_dist]

        dis = sum(school_for_type) - count
        if(dis > 0):
            index = 0
            while(dis > 0):
                if(school_for_type[index] > 0):
                    school_for_type[index] -= 1
                    dis -= 1
                    index += 1
        elif(dis < 0):
            index = 0
            while(dis < 0):
                school_for_type[index] += 1
                dis += 1
                index += 1
    return school_for_type


def create_districts(state_name, school_num_in_dist_made, school_type_in_dist):
    '''
    Main function to generate list of district for a state
    '''
    total_school = 0
    districts_list = []
    n = len(school_num_in_dist_made)
    if(n > 0):
        # generate random district names, and address
        try:
            names = generate_names_from_lists(n, birds_list, manmals_list)
        except:
            ValueError
            return []

        address = generate_address_from_list(n, fish_list)
        for i in range(n):
            dist = District(state_name, names[i] + " " + random.choice(DIST_SUFFIX), school_num_in_dist_made[i], address[i], school_type_in_dist[i % len(school_type_in_dist)])
            districts_list.append(dist)
            total_school += dist.num_of_schools

    assert(total_school == sum(school_num_in_dist_made))
    return districts_list


def generate_names_from_lists(count, list1, list2):
    names = []
    if(count > 0):
        base = math.ceil(math.sqrt(count))
        if(base < len(list1) and base < len(list2)):
            names1 = random.sample(list1, base)
            names2 = random.sample(list2, base)
            names = [str(name1) + " " + str(name2) for name1 in names1 for name2 in names2]
        else:
            print("not enough...", base, " ", len(list1), " ", len(list2))
            raise ValueError
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


def create_classes_grades_sections(sch, state_code):
    '''
    Main function to generate classes, grades, sections, students and teachers for a school
    '''
    # calculate number of students in each grade
    stu_num_in_grade = round(sch.num_of_student / (sch.high_grade - sch.low_grade + 1))
    end = stu_num_in_grade

    # generate teacher list for a school
    # teacher_list = create_teachers(sch.school_name, sch.num_of_teacher)
    teacher_list = generate_people(TEACHER, sch.num_of_teacher, random.choice(GENDER_RARIO))
    total_count[4] += len(teacher_list)

    # for each grade
    stu_tea_ratio = sch.num_of_student / sch.num_of_teacher
    j = 0
    for grade in range(sch.low_grade, sch.high_grade + 1):
        # generate student list for a grade
        # grade_students = create_students(sch.school_name, end)
        grade_students = generate_people(STUDENT, end, random.choice(GENDER_RARIO), grade)
        j += len(grade_students)
        total_count[3] += len(grade_students)
        if(grade == sch.high_grade - 1):
            end = sch.num_of_student - j
        classforgrade_list = create_classes_for_grade(grade_students, teacher_list, stu_tea_ratio)
        create_sections_stuandtea_csv(state_code, classforgrade_list, grade, sch.school_name, sch.dist_name)


def create_classes_for_grade(grade_students, teacher_list, stu_tea_ratio):
    '''
    Main function to generate classes for a grade
    '''
    # calculate number of class for a subject
    num_of_subjects = len(SUBJECTS)
    max_num_of_class = round(num_of_subjects * len(grade_students) / MIN_ASSMT_SCORE)
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
        num_of_teacher = (int)(round(len(grade_students) / stu_tea_ratio))
        if(num_of_teacher < 1):
            num_of_teacher = 1

        subject_teachers = random.sample(teacher_list, num_of_teacher)
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
    Main function to create one class in a grade of a subject. Students and teachers are associated with sections
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

    # for each section, add students and teachers
    for i in range(len(distribute_stu_insection)):
        section_stu_map[str(i)] = distribute_stu_insection[i]
        num_of_tea = max(1, (int)(round(len(distribute_stu_insection[i]) / stu_tea_ratio)))
        num_of_tea = min(num_of_tea, len(tea_list))
        section_tea_map[str(i)] = random.sample(tea_list, num_of_tea)
        # print(title, "section ", i, "stu_num ", len(distribute_stu_insection[i]), "teacher num ", num_of_tea, "ratio ", stu_tea_ratio)

    # create class, with sections
    eclass = Class(title, sub_name, section_stu_map, section_tea_map)

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
    avg1 = py1.avg(seqin)
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
    # print(generate_address_from_list(3, ["a", "b", "c", "d"]))
    print("starts ", t1)
    print("ends   ", t2)
