import unittest
import generate_data
import random
from entities import InstitutionHierarchy, Student
from helper_entities import District, State, Teacher, WhereTaken, StudentBioInfo
from constants import ZIPCODE_START, ZIPCODE_RANG_INSTATE, SCHOOL_LEVELS_INFO, \
    BIRDS_FILE
from gen_assessments import generate_dim_assessment
import os.path


class TestGenerateData(unittest.TestCase):

    # test make_school_types(perc, total)
    def test_make_school_types1(self):
        perc = [0.47, 0.38, 0.13, 0.02]
        total = 10
        expected = ['Elementary School', 'Elementary School', 'Elementary School', 'Elementary School', 'Elementary School',
                    'Middle School', 'Middle School', 'Middle School', 'Middle School',
                    'High School'
                    ]

        generated_count = generate_data.make_school_types(perc, total)
        self.assertEqual(expected, generated_count)

    def test_make_school_types2(self):
        perc = [0.33, 0.25, 0.21, 0.15]
        total = 11
        expected = ['Elementary School', 'Elementary School', 'Elementary School', 'Elementary School',
                    'Middle School', 'Middle School', 'Middle School',
                    'High School', 'High School',
                    'Other', 'Other'
                    ]

        generated_count = generate_data.make_school_types(perc, total)

        self.assertEqual(expected, generated_count)

    def test_make_school_types3(self):
        perc = [0.3, 0.25, 0.1, 0.35]
        total = 15
        expected = ['Elementary School', 'Elementary School', 'Elementary School', 'Elementary School',
                    'Middle School', 'Middle School', 'Middle School', 'Middle School',
                    'High School', 'High School',
                    'Other', 'Other', 'Other', 'Other', 'Other'
                    ]
        generated_count = generate_data.make_school_types(perc, total)
        self.assertEqual(expected, generated_count)

    # test generate_names_from_lists()
    def test_generate_names_from_lists_enough(self):
        count = 10
        list1 = [str(i) for i in range(100, 200)]
        list2 = [str(i) for i in range(1000, 2000)]

        expected_names = generate_data.generate_names_from_lists(count, list1, list2)
        self.assertEqual(len(expected_names), count)
        for name in expected_names:
            two_parts = name.split(' ')
            self.assertTrue(str(two_parts[0]) in list1)
            self.assertTrue(str(two_parts[1]) in list2)

    def test_generate_names_from_lists_halfenough(self):
        count = 36
        list1 = [str(i) for i in range(100, 102)]
        list2 = [str(i) for i in range(1000, 2000)]

        expected_names = generate_data.generate_names_from_lists(count, list1, list2)
        self.assertEqual(len(expected_names), count)
        one_set = []
        for name in expected_names:
            two_parts = name.split(' ')
            self.assertTrue(str(two_parts[0]) in list1)
            self.assertTrue(str(two_parts[1]) in list2)
            one_set.append(str(two_parts[0]))
        self.assertEqual(set(list1), set(one_set))

    def test_generate_names_from_lists_notenough(self):
        count = 144
        list1 = ['p1' + str(i) for i in range(100, 102)]
        list2 = ['p2' + str(i) for i in range(1000, 1005)]
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, count, list1, list2)

    def test_generate_names_from_lists_longerName(self):
        name_length = 8
        count = 10
        list1 = ['p1' + str(i) for i in range(100, 200)]
        list2 = ['p2' + str(i) for i in range(1000, 2000)]

        expected_names = generate_data.generate_names_from_lists(count, list1, list2, name_length)
        self.assertEqual(len(expected_names), count)
        for name in expected_names:
            self.assertTrue(len(name) <= name_length)

    def test_cal_zipvalues_thirdstate(self):
        pos = 2
        n = 12

        expected_zipinit, expected_zipdist = generate_data.calculate_zip_values(pos, n)

        self.assertEqual(3 * ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, (ZIPCODE_RANG_INSTATE // n))

    def test_cal_zipvalues_bigN(self):
        pos = 2
        n = 10000

        expected_zipinit, expected_zipdist = generate_data.calculate_zip_values(pos, n)

        self.assertEqual(3 * ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, 1)

    # test district generation
    def test_create_districts(self):
        state_code = "DE"
        state_name = 'Delaware'
        school_num_in_dist = [25, 67, 10, 128, 245, 199]
        pos = 0
        created_dist_list = generate_data.create_districts(state_code, state_name, school_num_in_dist, pos, make_namelists(1000, 1000, 1000))
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))

        expected_zipinit = ZIPCODE_START
        expected_zipdist = ZIPCODE_RANG_INSTATE // len(school_num_in_dist)
        c = 0
        for district in created_dist_list:
            self.assertIsInstance(district, District)
            self.assertEqual(district.state_code, state_code)
            self.assertEqual(district.state_name, state_name)
            self.assertTrue(district.district_id > 0)
            self.assertTrue(len(district.district_name) > 0)
            self.assertEqual(district.number_of_schools, school_num_in_dist[c])
            expected_zipinit += expected_zipdist
            c += 1

    def test_create_empty_districts(self):
        state_code = "CA"
        state_name = "California"
        school_num_in_dist = []
        pos = 1
        created_dist_list = generate_data.create_districts(state_code, state_name, school_num_in_dist, pos, make_namelists(1000, 1000, 1000))
        self.assertEqual(len(created_dist_list), 0)

    def test_create_districts_withNotEnoughNames(self):
        name_lists = make_namelists(1, 1, 1)
        state_code = "CA"
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]

        created_dist_list = generate_data.create_districts(state_code, state_name, school_num_in_dist, 0, name_lists)
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, len(school_num_in_dist), name_lists[0], name_lists[1])

    def test_create_districts_withNotEnoughAddName(self):
        state_code = "DE"
        state_name = "Delaware"
        school_num_in_dist = [25, 67, 10, 128, 15]
        pos = 2

        created_dist_list = generate_data.create_districts(state_code, state_name, school_num_in_dist, pos, make_namelists(1000, 1000, 1))
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))

        expected_zipinit = (pos + 1) * ZIPCODE_START
        expected_zipdist = max(1, (ZIPCODE_RANG_INSTATE // len(school_num_in_dist)))
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_code, state_code)
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.number_of_schools, school_num_in_dist[c])
            self.assertTrue(len(d.district_name) > 0)
            self.assertTrue(d.district_id > 0)
            expected_zipinit = expected_zipinit + expected_zipdist
            c += 1

    def test_create_districts_withNotEnoughCityName(self):
        state_name = "California"
        state_code = "CA"
        school_num_in_dist = [25, 67, 10, 128, 15]
        pos = 2
        name_lists = make_namelists(1, 1000, 1)

        created_dist_list = generate_data.create_districts(state_code, state_name, school_num_in_dist, pos, name_lists)
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, school_num_in_dist[0], name_lists[0], name_lists[2])

    # test generate_city_zipcode()
    def test_generate_city_zipcode_city(self):
        zipcode_range = (2000, 2025)
        num_of_schools = 100

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertTrue(1 <= len(generated_zipmap) <= (zipcode_range[1] - zipcode_range[0]))
        for ziprange in generated_zipmap.values():
            self.assertTrue(zipcode_range[0] <= ziprange[0] and ziprange[1] <= zipcode_range[1])
        self.assertTrue(len(generated_zipmap) <= num_of_schools)

    def test_generate_city_zipcode_onezip(self):
        zipcode_range = [1000, 1001]
        num_of_schools = 1900

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertEqual(1, len(generated_zipmap))

        for ziprange in generated_zipmap.values():
            self.assertEqual(zipcode_range, ziprange)

        self.assertEqual(len(generated_zipmap), 1)

    def test_generate_city_zipcode_wrongzip(self):
        zipcode_range = [1000, 234]
        num_of_schools = 1900

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertEqual(1, len(generated_zipmap))

        for ziprange in generated_zipmap.values():
            self.assertEqual(zipcode_range, ziprange)

        self.assertEqual(len(generated_zipmap), 1)

    def test_generate_city_withNotEnoughCityName(self):
        name_lists = make_namelists(1, 1, 1)
        zipcode_range = [1000, 5000]
        num_of_schools = 5

        generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, name_lists)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, num_of_schools, name_lists[0], name_lists[1])

    def test_generate_city_onecity(self):
        zipcode_range = [1000, 5000]
        num_of_schools = 1

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertEqual(1, len(generated_zipmap))

        for ziprange in generated_zipmap.values():
            self.assertEqual(zipcode_range, ziprange)

        self.assertEqual(len(generated_zipmap), num_of_schools)

    # test institution_hierarchies(school) generation
    def test_create_institution_hierarchies(self):
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)

        dist_name = 'dist1'
        dist_id = 1234
        state_code = 'DE'
        state_name = 'Delaware'
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        name_list = make_namelists(1000, 1000, 1000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_list)
        distObj = District(dist_id, dist_name, state_code, state_name, sch_num, city_zip_map)

        created_school_list, created_wheretaken_list = generate_data.create_institution_hierarchies(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat, name_list, False)

        self.assertEqual(sch_num, len(created_school_list))
        self.assertEqual(sch_num, len(created_wheretaken_list))

        for i in range(len(created_school_list)):
            self.assertIsInstance(created_school_list[i], InstitutionHierarchy)
            self.assertEqual(created_school_list[i].number_of_students, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].student_teacher_ratio, stutea_ratio_in_school[i])
            self.assertTrue(created_school_list[i].low_grade >= 0)
            self.assertTrue(created_school_list[i].high_grade < 13)

            self.assertEqual(created_school_list[i].state_code, state_code)
            self.assertEqual(created_school_list[i].state_name, state_name)
            self.assertEqual(created_school_list[i].district_name, dist_name)
            self.assertEqual(created_school_list[i].district_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertTrue(created_school_list[i].school_id > 0)
            self.assertTrue(len(created_school_list[i].school_category) > 0)
            self.assertTrue(created_school_list[i].inst_hier_rec_id > 0)
            self.assertIsNotNone(created_school_list[i].from_date)

        for j in range(len(created_wheretaken_list)):
            self.assertIsInstance(created_wheretaken_list[j], WhereTaken)
            self.assertEqual(created_wheretaken_list[i].where_taken_name, created_school_list[i].school_name)
            self.assertTrue(created_wheretaken_list[i].where_taken_id > 0)

    def test_create_institution_hierarchies_withNotEnoughNames(self):
        name_lists = make_namelists(1000, 1, 1)

        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)

        dist_name = 'dist1'
        dist_id = 1234
        state_code = 'CA'
        state_name = 'California'
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_lists)
        distObj = District(dist_id, dist_name, state_code, state_name, sch_num, city_zip_map)

        created_school_list, wheretaken_list = generate_data.create_institution_hierarchies(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat, name_lists, False)
        self.assertTrue(len(created_school_list) == 0)
        self.assertTrue(len(wheretaken_list) == 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, sch_num, name_lists[2], name_lists[1])
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, sch_num, name_lists[2], name_lists[1])

    def test_create_institution_hierarchies_withNotEnoughAddName(self):
        name_lists = make_namelists(1, 1000, 1000)
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)

        dist_name = 'dist1'
        dist_id = 1234
        state_code = 'CA'
        state_name = 'California'
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_lists)
        distObj = District(dist_id, dist_name, state_code, state_name, sch_num, city_zip_map)
        created_school_list, created_wheretaken_list = generate_data.create_institution_hierarchies(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat, name_lists, False)
        self.assertEqual(sch_num, len(created_school_list))

        for i in range(len(created_school_list)):
            self.assertIsInstance(created_school_list[i], InstitutionHierarchy)
            self.assertEqual(created_school_list[i].number_of_students, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].student_teacher_ratio, stutea_ratio_in_school[i])
            self.assertTrue(created_school_list[i].low_grade >= 0)
            self.assertTrue(created_school_list[i].high_grade < 13)

            self.assertEqual(created_school_list[i].state_code, state_code)
            self.assertEqual(created_school_list[i].state_name, state_name)
            self.assertEqual(created_school_list[i].district_name, dist_name)
            self.assertEqual(created_school_list[i].district_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertTrue(created_school_list[i].school_id > 0)
            self.assertTrue(len(created_school_list[i].school_category) > 0)
            self.assertTrue(created_school_list[i].inst_hier_rec_id > 0)
            self.assertIsNotNone(created_school_list[i].from_date)

        for j in range(len(created_wheretaken_list)):
            self.assertIsInstance(created_wheretaken_list[j], WhereTaken)
            self.assertEqual(created_wheretaken_list[i].where_taken_name, created_school_list[i].school_name)
            self.assertTrue(created_wheretaken_list[i].where_taken_id > 0)

    # test split_list()
    def test_split_list_average(self):
        list1 = [9, 8, 62, 123, 345, 1, 2, 98, 100]
        size1 = 3

        chunks1 = generate_data.split_list(list1, size1)
        self.assertEqual(size1, len(chunks1))

        for little in chunks1:
            self.assertEqual(3, len(little))

    def test_split_list_notaverage(self):
        list1 = [9, 8, 62, 123, 345, 1, 2, 98]
        size1 = 3
        chunks1 = generate_data.split_list(list1, size1)
        self.assertEqual(size1, len(chunks1))

        for little in chunks1[:-1]:
            self.assertEqual(3, len(little))
        self.assertEqual(2, len(chunks1[-1]))

    def test_split_list_one(self):
        list2 = [1, 2, 3]
        size2 = 1
        chunks2 = generate_data.split_list(list2, size2)
        self.assertEqual(size2, len(chunks2))

        for little in chunks2:
            for item in little:
                self.assertTrue(item in list2)

    # test create_students_for_subject()
    def test_create_students_for_subject(self):
        sub_name = "Math"
        class_count = 2
        student_num = 90
        teacher_num = 5
        ratio = student_num / teacher_num
        grade = 9
        school = InstitutionHierarchy(student_num, ratio, 7, 9, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)

        state = State('DE', 'Delaware', 10)
        students_list = make_students(student_num, state, None, school)
        self.assertTrue(len(students_list), student_num)
        teachers_list = make_teachers(teacher_num, state)

        expected_students_inclass = student_num / class_count
        expected_section_num = round(expected_students_inclass / school.student_teacher_ratio)
        expected_student_sections_for_subject = generate_data.create_students_for_subject(sub_name, class_count, students_list, teachers_list, school, grade)
        expected_section_list = []
        self.assertEqual(len(expected_student_sections_for_subject), student_num)
        for student_section in expected_student_sections_for_subject:
            self.assertIsInstance(student_section, Student)
            expected_section_list.append(student_section.section_id)
        self.assertTrue(len(set(expected_section_list)) == expected_section_num * class_count)

    # test create_classes_for_grade()
    def test_create_classes_for_grade(self):
        student_num = 160
        teacher_num = 12
        ratio = student_num / teacher_num

        grade = 8
        asmt_list = generate_dim_assessment()
        school = InstitutionHierarchy(student_num, ratio, 7, 9, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)
        where_taken = WhereTaken('where_taken_id', 'where_taken_name')
        state = State('DE', 'Delaware', 10)
        students_list = make_students(student_num, state, None, school)
        teachers_list = make_teachers(teacher_num, state)

        total_count = {'state_count': 0, 'district_count': 0, 'school_count': 0, 'student_count': 0}
        generate_data.create_classes_for_grade(students_list, teachers_list, school, grade, asmt_list, where_taken, total_count, False)
        self.assertEqual(school.number_of_students * 2, total_count['student_count'])

    # test create_sections_in_one_class()
    def test_create_sections_in_one_class_severalsections(self):
        student_num = 160
        teacher_num = 12
        ratio = student_num / teacher_num
        sub_name = "Math"
        class_count = 2
        school = InstitutionHierarchy(student_num, ratio, 7, 9, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)
        state = State('DE', 'Delaware', 10)
        students_list = make_students(student_num, state, None, school)
        teachers_list = make_teachers(teacher_num, state)
        grade = 8

        expected_create_sections = generate_data.create_sections_in_one_class(sub_name, class_count, students_list, teachers_list, school, grade)

        expected_section_num = round(student_num / ratio)

        self.assertEqual(len(expected_create_sections), student_num)

        expected_section_list = []
        for student_section in expected_create_sections:
            self.assertIsInstance(student_section, Student)
            expected_section_list.append(student_section.section_id)
        self.assertTrue(len(set(expected_section_list)) == expected_section_num)

    def test_create_sections_in_one_class_onesection(self):

        student_num = 45
        teacher_num = 5
        ratio = 78
        sub_name = "Math"
        class_count = 2
        school = InstitutionHierarchy(student_num, ratio, 7, 9, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)
        state = State('DE', 'Delaware', 10)
        students_list = make_students(student_num, state, None, school)
        teachers_list = make_teachers(teacher_num, state)
        grade = 8

        expected_create_sections = generate_data.create_sections_in_one_class(sub_name, class_count, students_list, teachers_list, school, grade)

        expected_section_num = 1

        self.assertEqual(len(expected_create_sections), student_num)

        expected_section_list = []
        for student_section in expected_create_sections:
            self.assertIsInstance(student_section, Student)
            expected_section_list.append(student_section.section_id)
        self.assertTrue(len(set(expected_section_list)) == expected_section_num)

    # test makeup_list()
    def test_makeup_list(self):
        avgin = 5.32
        stdin = 6.76
        minin = 1
        maxin = 28
        countin = 30
        target_sum = 220

        generate_makeup_list = generate_data.makeup_list(avgin, stdin, minin, maxin, countin, target_sum)
        self.assertEqual(len(generate_makeup_list), countin)

    # test create_classes_for_school
    def test_create_classes_for_school(self):
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        # stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]

        # make assessment list
        asmt_list = generate_dim_assessment()
        total_count = {'state_count': 0, 'district_count': 0, 'school_count': 0, 'student_count': 0, 'student_section_count': 0}
        name_lists = make_namelists(1000, 1000, 1000)

        # make a state
        state_code = 'DE'
        state_name = 'Delaware'
        state = State(state_code, state_name, 39)

        # make a district
        dist_name = 'dist1'
        dist_id = 1234
        school_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], school_num, name_lists)
        distObj = District(dist_id, dist_name, state_code, state_name, school_num, city_zip_map)

        # make a school
        student_num = 120
        ratio = 13
        school = InstitutionHierarchy(student_num, ratio, 7, 9, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)

        # make where_taken
        where_taken_list = []
        for i in range(0, school_num - 1):
            where_taken = WhereTaken(random.randint, school.school_name + str(i))
            where_taken_list.append(where_taken)

        where_taken = WhereTaken(random.randint, school.school_name)
        where_taken_list.append(where_taken)
        distObj.wheretaken_list = where_taken_list

        generate_data.create_classes_for_school(distObj, school, state_code, name_lists[2], total_count, asmt_list, False)
        expected_student_number = student_num

        self.assertEqual(total_count['student_count'], expected_student_number * 2)

    # test read files
    def test_read_names(self):
        basepath = os.path.dirname(__file__)
        file_name = os.path.abspath(os.path.join(basepath, '..', 'datafiles', 'name_lists', 'birds.txt'))
        generated_names = generate_data.read_names(file_name)
        self.assertTrue(len(generated_names) > 0)

    def test_get_name_lists_nofiles(self):
        # rename file into wrong file
        bird_file = BIRDS_FILE
        rename_file = bird_file.split('.')[0] + '_test' + '.txt'
        os.rename(bird_file, rename_file)
        result = generate_data.get_name_lists()
        self.assertFalse(result)
        os.rename(rename_file, bird_file)

    def test_prepare_generation_parameters_nonedbstat(self):
        self.assertRaises(Exception, generate_data.prepare_generation_parameters, generate_data.get_name_lists, mock_f_get_state_stats_emptydb, False)

    def test_prepare_generation_parameters_emptystatdata(self):
        self.assertRaises(Exception, generate_data.prepare_generation_parameters, generate_data.get_name_lists, mock_f_get_state_stats_emptydb, False)

    def test_prepare_generation_parameters_onestate(self):
        generate_count = generate_data.prepare_generation_parameters(generate_data.get_name_lists, mock_f_get_state_stats_onestate, False)
        self.assertEqual(generate_count['state_count'], 1)
        for value in generate_count.values():
            self.assertTrue(value > 0)

    def test_prepare_generation_parameters_twostates(self):
        generate_count = generate_data.prepare_generation_parameters(generate_data.get_name_lists, mock_f_get_state_stats_twostates, False)
        # self.assertEqual(generate_count[0], 2)
        for value in generate_count.values():
            self.assertTrue(value > 0)

    def test_prepare_generation_parameters_notEnoughNameLists1(self):
        generate_count = generate_data.prepare_generation_parameters(mock_f_get_name_lists_shortlists1, mock_f_get_state_stats_onestate, False)
        self.assertEqual(generate_count, {'state_count': 1, 'district_count': 0, 'school_count': 0, 'student_count': 0})


def mock_f_get_name_lists_shortlists1():
    return make_namelists(1, 1, 1)


def mock_f_get_state_stats_emptydb():
    return []


def mock_f_get_state_stats_fail():
    return None


def mock_f_get_state_stats_onestate():
    return [{'state_code': 'DE',
             'state_name': 'Delaware',
             'total_district': 2,
             'total_school': 10,
             'total_student': 6441,
             'total_teacher': 436,
             'min_school_per_district': 1,
             'max_school_per_district': 4,
             'std_school_per_district': 2.759419404987443,
             'avg_school_per_district': 5,
             'min_student_per_school': 3,
             'max_student_per_school': 100,
             'std_student_per_school': 17.5283806160176,
             'avg_student_per_school': 33.3333333333333,
             'min_stutea_ratio_per_school': 1.71,
             'max_stutea_ratio_per_school': 22.24,
             'std_stutea_ratio_per_school': 3.0400201846801003,
             'avg_stutea_ratio_per_school': 14.754455445544567,
             'primary_perc': 0.5643564356435643,
             'middle_perc': 0.19306930693069307,
             'high_perc': 0.16831683168316833,
             'other_perc': 0.07425742574257421}
            ]


def mock_f_get_state_stats_twostates():
    return [{'state_code': 'DE',
             'state_name': 'Delaware',
             'total_district': 2,
             'total_school': 10,
             'total_student': 6441,
             'total_teacher': 436,
             'min_school_per_district': 1,
             'max_school_per_district': 4,
             'std_school_per_district': 2.759419404987443,
             'avg_school_per_district': 5,
             'min_student_per_school': 3,
             'max_student_per_school': 100,
             'std_student_per_school': 17.5283806160176,
             'avg_student_per_school': 33.3333333333333,
             'min_stutea_ratio_per_school': 1.71,
             'max_stutea_ratio_per_school': 22.24,
             'std_stutea_ratio_per_school': 3.0400201846801003,
             'avg_stutea_ratio_per_school': 14.754455445544567,
             'primary_perc': 0.5643564356435643,
             'middle_perc': 0.19306930693069307,
             'high_perc': 0.16831683168316833,
             'other_perc': 0.07425742574257421},
            {'state_code': 'KA',
             'state_name': 'Kansas',
             'total_district': 2,
             'total_school': 10,
             'total_student': 6441,
             'total_teacher': 436,
             'min_school_per_district': 1,
             'max_school_per_district': 4,
             'std_school_per_district': 2.759419404987443,
             'avg_school_per_district': 5,
             'min_student_per_school': 3,
             'max_student_per_school': 100,
             'std_student_per_school': 17.5283806160176,
             'avg_student_per_school': 33.3333333333333,
             'min_stutea_ratio_per_school': 1.71,
             'max_stutea_ratio_per_school': 22.24,
             'std_stutea_ratio_per_school': 3.0400201846801003,
             'avg_stutea_ratio_per_school': 14.754455445544567,
             'primary_perc': 0.5643564356435643,
             'middle_perc': 0.19306930693069307,
             'high_perc': 0.16831683168316833,
             'other_perc': 0.07425742574257421}
            ]


def make_state():
    state = State('DE', 'Delaware', 20, 'DE')
    return state


def make_district(state):
    sch_num = 10
    zip_s = 50000
    zip_e = 60000
    city_zip_map = generate_data.generate_city_zipcode(zip_s, zip_e, sch_num, make_namelists(1000, 1000, 1000))
    distObj = District(random.choice(range(1000, 2000)), 'dist1', state.state_code, state.state_name, sch_num, city_zip_map)
    return distObj


def make_students(count, state, district, school):
    if(district is None):
        district = make_district(state)
    student_list = []
    while(count > 0):
        student = StudentBioInfo(count, 2 * count, ('first_name' + str(count)), ('last_name' + str(count)), ('address1' + str(count)), '08/02/2000', district.district_id, state.state_code, 'male', 'email', school.school_id, 94108, 'city_1')
        count -= 1
        student_list.append(student)
    return student_list


def make_teachers(count, state, district=None):
    if(district is None):
        district = make_district(state)
    teacher_list = []
    while(count > 0):
        teacher = Teacher('tfirst_name' + str(count), 'tlast_name' + str(count), district.district_id, state.state_code, teacher_guid=count)
        count -= 1
        teacher_list.append(teacher)
    return teacher_list


def make_namelists(b_count, m_count, f_count):
    name_lists = []

    birds_list = ['bird' + str(i) for i in range(b_count)]
    mammals_list = ['mammal' + str(i) for i in range(m_count)]
    fish_list = ['fish' + str(i) for i in range(f_count)]

    name_lists.append(birds_list)
    name_lists.append(mammals_list)
    name_lists.append(fish_list)

    return name_lists

if __name__ == "__main__":
    unittest.main()
