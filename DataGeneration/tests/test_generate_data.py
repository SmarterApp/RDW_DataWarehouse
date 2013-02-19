import unittest
import math
import generate_data
import random
from entities import District, Student, Teacher, State, School, WhereTaken
from constants import SUBJECTS, ZIPCODE_START, ZIPCODE_RANG_INSTATE, SCHOOL_LEVELS_INFO, ADD_SUFFIX, \
    BIRDS_FILE
import uuid
from gen_assessments import generate_assessment_types
import os.path
import datetime


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

    # test generate_address_from_list()
    def test_generate_address_from_list_uniqueroadname(self):
        count = 10
        words_list = ['road' + str(i) for i in range(100, 200)]

        expected_add = generate_data.generate_address_from_list(count, words_list)
        self.assertEqual(len(expected_add), count)
        expected_roadword = []
        for add in expected_add:
            expected_roadword.append((add.split(' '))[1])
            suf = (add.split(' '))[2]
            for part in (add.split(' '))[3:]:
                suf = suf + ' ' + part
            self.assertTrue(suf in ADD_SUFFIX)
        self.assertEqual(len(set(expected_roadword)), len(expected_add))

    def test_generate_address_from_list_duproadname(self):
        count = 1000
        words_list = ['road' + str(i) for i in range(100, 221)]

        expected_add = generate_data.generate_address_from_list(count, words_list)
        self.assertEqual(len(expected_add), count)
        expected_roadname_count = {}
        for add in expected_add:
            road_name = (add.split(' '))[1]
            if(road_name in expected_roadname_count.keys()):
                expected_roadname_count[road_name] += 1
            else:
                expected_roadname_count[road_name] = 1
        self.assertEqual(len(expected_roadname_count), len(words_list))

        for k, v in expected_roadname_count.items():
            self.assertTrue(k in words_list)
            self.assertTrue(v in [(count // len(words_list)), ((count // len(words_list)) + 1)])

    def test_generate_address_from_list_longerName(self):
        add_length = 15
        count = 10
        words_list = ['road' + str(i) for i in range(100, 200)]
        expected_add = generate_data.generate_address_from_list(count, words_list, add_length)
        self.assertEqual(len(expected_add), count)
        expected_roadword = []
        for add in expected_add:
            print(add)
            expected_roadword.append((add.split(' '))[1])
            suf = (add.split(' '))[2]
            for part in (add.split(' '))[3:]:
                suf = suf + ' ' + part
            self.assertTrue(suf in ADD_SUFFIX)
            self.assertTrue(len(add) <= add_length)

    # test calculate_zipvalues(pos, n)
    def test_cal_zipvalues_firststate(self):
        pos = 0
        n = 12

        expected_zipinit, expected_zipdist = generate_data.cal_zipvalues(pos, n)

        self.assertEqual(ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, (ZIPCODE_RANG_INSTATE // n))

    def test_cal_zipvalues_thirdstate(self):
        pos = 2
        n = 12

        expected_zipinit, expected_zipdist = generate_data.cal_zipvalues(pos, n)

        self.assertEqual(3 * ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, (ZIPCODE_RANG_INSTATE // n))

    def test_cal_zipvalues_bigN(self):
        pos = 2
        n = 10000

        expected_zipinit, expected_zipdist = generate_data.cal_zipvalues(pos, n)

        self.assertEqual(3 * ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, 1)

    # test district generation
    def test_create_districts(self):
        state_code = "CA"
        school_num_in_dist = [25, 67, 10, 128, 245, 199]
        pos = 0
        created_dist_list = generate_data.create_districts(state_code, school_num_in_dist, pos, make_namelists(1000, 1000, 1000))
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))

        expected_zipinit = ZIPCODE_START
        expected_zipdist = ZIPCODE_RANG_INSTATE // len(school_num_in_dist)
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_code, state_code)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertTrue(len(d.district_name) > 0)
            self.assertTrue(len(d.address_1) > 0)
            self.assertEqual(d.zipcode, expected_zipinit)
            expected_zipinit += expected_zipdist
            c += 1

    def test_create_empty_districts(self):
        state_code = "CA"
        school_num_in_dist = []
        pos = 1
        created_dist_list = generate_data.create_districts(state_code, school_num_in_dist, pos, make_namelists(1000, 1000, 1000))
        self.assertEqual(len(created_dist_list), 0)

    def test_create_districts_withNotEnoughNames(self):
        name_lists = make_namelists(1, 1, 1)
        state_code = "CA"
        school_num_in_dist = [25, 67, 10, 128, 15]

        created_dist_list = generate_data.create_districts(state_code, school_num_in_dist, 0, name_lists)
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, len(school_num_in_dist), name_lists[0], name_lists[1])

    def test_create_districts_withNotEnoughAddName(self):
        state_code = "CA"
        school_num_in_dist = [25, 67, 10, 128, 15]
        pos = 2

        created_dist_list = generate_data.create_districts(state_code, school_num_in_dist, pos, make_namelists(1000, 1000, 1))
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))

        expected_zipinit = (pos + 1) * ZIPCODE_START
        expected_zipdist = max(1, (ZIPCODE_RANG_INSTATE // len(school_num_in_dist)))
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_code, state_code)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertTrue(len(d.district_name) > 0)
            self.assertTrue(len(d.address_1) > 0)
            self.assertEqual(d.zipcode, expected_zipinit)
            expected_zipinit = expected_zipinit + expected_zipdist
            c += 1

    def test_create_districts_withNotEnoughCityName(self):
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        pos = 2
        name_lists = make_namelists(1, 1000, 1)

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, pos, name_lists)
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, school_num_in_dist[0], name_lists[0], name_lists[2])

    def test_generate_city_zipcode_city(self):
        zipcode_range = (2000, 2025)
        num_of_schools = 100

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertTrue(1 <= len(generated_zipmap) <= (zipcode_range[1] - zipcode_range[0]))
        for city, ziprange in generated_zipmap.items():
            self.assertTrue(zipcode_range[0] <= ziprange[0] and ziprange[1] <= zipcode_range[1])
        self.assertTrue(len(generated_zipmap) <= num_of_schools)

    def test_generate_city_zipcode_onezip(self):
        zipcode_range = [1000, 1001]
        num_of_schools = 1900

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertEqual(1, len(generated_zipmap))

        for city, ziprange in generated_zipmap.items():
            self.assertEqual(zipcode_range, ziprange)

        self.assertEqual(len(generated_zipmap), 1)

    def test_generate_city_zipcode_wrongzip(self):
        zipcode_range = [1000, 234]
        num_of_schools = 1900

        generated_zipmap = generate_data.generate_city_zipcode(zipcode_range[0], zipcode_range[1], num_of_schools, make_namelists(1000, 1000, 1000))
        self.assertEqual(1, len(generated_zipmap))

        for city, ziprange in generated_zipmap.items():
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

        for city, ziprange in generated_zipmap.items():
            self.assertEqual(zipcode_range, ziprange)

        self.assertEqual(len(generated_zipmap), num_of_schools)

    # test school generation
    def test_create_schools(self):

        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)

        dist_name = 'dist1'
        dist_id = 1234
        dist_exte_id = uuid.uuid4()
        state_id = 'CA'
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        name_list = make_namelists(1000, 1000, 1000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_list)
        distObj = District(dist_id, dist_exte_id, dist_name, state_id, sch_num, city_zip_map, 'address1', 50000)
        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat, name_list)

        self.assertEqual(sch_num, len(created_school_list))
        self.assertEqual(sch_num, len(created_wheretaken_list))
        expected_school_categories_type = [sch_level[0] for sch_level in SCHOOL_LEVELS_INFO]

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_name, dist_name)
            self.assertEqual(created_school_list[i].district_id, dist_id)
            self.assertEqual(created_school_list[i].state_code, state_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[i])
            self.assertTrue(len(created_school_list[i].address1) > 0)
            self.assertTrue(created_school_list[i].school_categories_type in expected_school_categories_type)

        for j in range(len(created_wheretaken_list)):
            self.assertTrue(len(created_wheretaken_list[j].address_1) > 0)
            self.assertEqual(created_wheretaken_list[j].address_1, created_school_list[j].address1)
            self.assertTrue(created_wheretaken_list[j].zip_code >= zip_range[0])
            self.assertTrue(created_wheretaken_list[j].zip_code <= zip_range[1])
            self.assertEqual(created_wheretaken_list[j].state_code, state_id)
            self.assertEqual(created_wheretaken_list[j].country_id, 'US')

    def test_create_schools_withNotEnoughNames(self):
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
        dist_exte_id = uuid.uuid4()
        state_id = 'CA'
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_lists)
        distObj = District(dist_id, dist_exte_id, dist_name, state_id, sch_num, city_zip_map, 'address1', 50000)

        created_school_list, wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat, name_lists)
        self.assertTrue(len(created_school_list) == 0)
        self.assertTrue(len(wheretaken_list) == 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, sch_num, name_lists[2], name_lists[1])

    def test_create_schools_withNotEnoughAddName(self):
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
        dist_exte_id = uuid.uuid4()
        state_id = 'CA'
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_lists)
        distObj = District(dist_id, dist_exte_id, dist_name, state_id, sch_num, city_zip_map, 'address1', 50000)
        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat, name_lists)
        self.assertEqual(sch_num, len(created_school_list))
        expected_sch_types = [sch_level[0] for sch_level in SCHOOL_LEVELS_INFO]

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_name, dist_name)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[i])
            self.assertTrue(len(created_school_list[i].address1) > 0)
            self.assertTrue(created_school_list[i].school_categories_type in expected_sch_types)

        for j in range(len(created_wheretaken_list)):
            self.assertTrue(len(created_wheretaken_list[j].address_1) > 0)
            self.assertTrue(created_wheretaken_list[j].zip_code >= zip_range[0])
            self.assertTrue(created_wheretaken_list[j].zip_code <= zip_range[1])
            self.assertEqual(created_wheretaken_list[j].state_code, state_id)
            self.assertEqual(created_wheretaken_list[j].country_id, 'US')

    def test_list_to_chucks_average(self):
        list1 = [9, 8, 62, 123, 345, 1, 2, 98, 100]
        size1 = 3

        chunks1 = generate_data.list_to_chucks(list1, size1)
        self.assertEqual(size1, len(chunks1))

        for little in chunks1:
            self.assertEqual(3, len(little))

    def test_list_to_chucks_notaverage(self):
        list1 = [9, 8, 62, 123, 345, 1, 2, 98]
        size1 = 3
        chunks1 = generate_data.list_to_chucks(list1, size1)
        self.assertEqual(size1, len(chunks1))

        for little in chunks1[:-1]:
            self.assertEqual(3, len(little))
        self.assertEqual(2, len(chunks1[-1]))

    def test_list_to_chucks_one(self):
        list2 = [1, 2, 3]
        size2 = 1
        chunks2 = generate_data.list_to_chucks(list2, size2)
        self.assertEqual(size2, len(chunks2))

        for little in chunks2:
            for item in little:
                self.assertTrue(item in list2)

    def test_create_classes(self):
        sub_name = "Math"
        count = 10
        stu_list = make_students(800, make_district(make_state()))
        tea_list = make_teachers(45)
        stu_tea_ratio = round(len(stu_list) / len(tea_list))
        school_id = 98123

        expected_classes = generate_data.create_classes(sub_name, count, stu_list, tea_list, stu_tea_ratio, school_id)

        self.assertEqual(len(expected_classes), count)

        expected_stu_num = 0
        expected_tea_num = 0
        for i in range(len(expected_classes)):
            self.assertEqual(expected_classes[i].title, sub_name + " " + str(i))
            self.assertEqual(expected_classes[i].sub_name, sub_name)
            for value in expected_classes[i].section_stu_map.values():
                expected_stu_num += len(value)
            for value in expected_classes[i].section_tea_map.values():
                expected_tea_num += len(value)
        self.assertEqual(expected_stu_num, 800)
        self.assertTrue(expected_tea_num <= 45)

    def test_create_classes_smallstudents(self):
        sub_name = "Math"
        count = 2
        stu_list = make_students(16)
        tea_list = make_teachers(1)
        stu_tea_ratio = round(len(stu_list) / len(tea_list))
        school_id = 98123

        expected_classes = generate_data.create_classes(sub_name, count, stu_list, tea_list, stu_tea_ratio, school_id)

        self.assertEqual(len(expected_classes), count)

        expected_stu_num = 0
        for i in range(len(expected_classes)):
            self.assertEqual(expected_classes[i].title, sub_name + " " + str(i))
            self.assertEqual(expected_classes[i].sub_name, sub_name)
            for value in expected_classes[i].section_stu_map.values():
                expected_stu_num += len(value)
        self.assertEqual(expected_stu_num, 16)

    def test_create_classes_for_grade(self):
        stu_list = make_students(160)
        tea_list = make_teachers(12)
        school_id = 912343
        ratio = len(stu_list) / len(tea_list)

        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list, school_id, ratio)
        expected_max_class_for_sub = 8

        for generated_class in expected_classes:
            split = generated_class.title.split(' ')
            self.assertTrue(split[0] in SUBJECTS)
            self.assertTrue((int)(split[1]) < expected_max_class_for_sub)

    def test_create_classes_for_grade_samllstudents(self):
        stu_num = 20
        stu_list = make_students(stu_num)
        tea_list = make_teachers(1)
        school_id = 912343
        ratio = len(stu_list) / len(tea_list)

        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list, school_id, ratio)
        self.assertEqual(len(expected_classes), len(SUBJECTS))
        for i in range(len(expected_classes)):
            self.assertEqual(expected_classes[i].title, SUBJECTS[i] + " " + str(0))
            self.assertEqual(len(expected_classes[i].section_stu_map), 1)
            section_id = list(expected_classes[i].section_stu_map.keys())
            self.assertEqual(len(section_id), 1)
            self.assertEqual(len(expected_classes[i].section_stu_map[section_id[0]]), stu_num)
            self.assertEqual(expected_classes[i].section_stu_map[section_id[0]], stu_list)

    def test_create_one_class_severalsections(self):
        sub_name = "Math"
        class_count = 2
        distribute_stu_inaclass = make_students(45)
        tea_list = make_teachers(10)
        stu_tea_ratio = 15
        school_id = 87123

        expected_class = generate_data.create_one_class(sub_name, class_count, distribute_stu_inaclass, tea_list, stu_tea_ratio, school_id)
        expected_sec_num = math.floor(45 // stu_tea_ratio)

        self.assertEqual(expected_class.sub_name, sub_name)
        self.assertEqual(expected_class.title, sub_name + " " + str(class_count))
        self.assertEqual(len(expected_class.section_stu_map), expected_sec_num)

        expected_students = []
        for value in expected_class.section_stu_map.values():
            self.assertEqual(len(value), 15)
            expected_students.extend(value)

        self.assertEqual(len(expected_class.section_tea_map), expected_sec_num)
        for value in expected_class.section_tea_map.values():
            self.assertEqual(len(value), 1)
            self.assertTrue(value[0] in tea_list)
        self.assertEqual(len(expected_students), len(distribute_stu_inaclass))
        for g_stu in expected_students:
            self.assertTrue(g_stu in distribute_stu_inaclass)

    def test_create_one_class_onesection(self):
        sub_name = "Math"
        class_count = 2
        distribute_stu_inaclass = make_students(45)
        tea_list = make_teachers(5)
        stu_tea_ratio = 78
        school_id = 87123

        expected_class = generate_data.create_one_class(sub_name, class_count, distribute_stu_inaclass, tea_list, stu_tea_ratio, school_id)
        expected_sec_num = 1

        self.assertEqual(expected_class.sub_name, sub_name)
        self.assertEqual(expected_class.title, sub_name + " " + str(class_count))
        self.assertEqual(len(expected_class.section_stu_map), expected_sec_num)

        for value in expected_class.section_stu_map.values():
            self.assertEqual(len(value), 45)

        self.assertEqual(len(expected_class.section_tea_map), expected_sec_num)
        for value in expected_class.section_tea_map.values():
            self.assertEqual(len(value), 1)
            self.assertTrue(value[0] in tea_list)

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

    # test create_classes_grades_sections
    def test_create_classes_grades_sections(self):
        # make assessment list
        asmt_list = generate_assessment_types()
        total_count = [0, 0, 0, 0, 0, 0]
        name_lists = make_namelists(1000, 1000, 1000)

        # make a state
        state = State('DE', 'Delaware', 39, 'DE')

        # make a district
        dist_name = 'dist1'
        dist_id = 1234
        dist_exte_id = uuid.uuid4()
        state_id = 'CA'
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        sch_num = len(stu_num_in_school)
        zip_range = (50000, 60000)
        city_zip_map = generate_data.generate_city_zipcode(zip_range[0], zip_range[1], sch_num, name_lists)
        distObj = District(dist_id, dist_exte_id, dist_name, state_id, sch_num, city_zip_map, 'address1', 50000)

        # make a school
        stu_num = 120
        school = School(random.randint, uuid.uuid4(), 'ABC Primary', distObj.district_name, distObj.district_id,
                        distObj.state_code, stu_num, 23, 1, 6, 'category_t', address1='450 west 78th street', city='city123', zip_code='50897')

        # make a wheretaken
        where_taken_list = []
        for i in range(0, sch_num - 1):
            where_taken = WhereTaken(random.randint, school.school_name + str(i), distObj.district_name, school.address1 + str(i), school.city + str(i), int(school.zip_code) + i, distObj.state_code, 'US')
            where_taken_list.append(where_taken)

        where_taken = WhereTaken(random.randint, school.school_name, distObj.district_name, school.address1, school.city, school.zip_code, distObj.state_code, 'US')
        where_taken_list.append(where_taken)
        distObj.wheretaken_list = where_taken_list

        generate_data.create_classes_grades_sections(distObj, school, state, name_lists[2], total_count, asmt_list)

        expected_teacher_number = 5
        expected_student_number = stu_num

        self.assertEqual(total_count[3], expected_student_number)
        self.assertEqual(total_count[4], expected_teacher_number)
        self.assertEqual(total_count[5], expected_student_number * 2)

    # test read files
    def test_read_names(self):
        basepath = os.path.dirname(__file__)
        file_name = os.path.abspath(os.path.join(basepath, '..', 'datafiles', 'name_lists', 'birds.txt'))
        generated_names = generate_data.read_names(file_name)
        self.assertTrue(len(generated_names) > 0)

    # test generate_date
    def test_generate_date(self):
        generated_date = generate_data.generate_date()
        print(generated_date)
        self.assertTrue(generated_date <= datetime.date.today())

    def test_get_name_lists_nofiles(self):
        # rename file into wrong file
        bird_file = BIRDS_FILE
        rename_file = bird_file.split('.')[0] + '_test' + '.txt'
        os.rename(bird_file, rename_file)
        result = generate_data.get_name_lists()
        self.assertFalse(result)
        os.rename(rename_file, bird_file)

    def test_generate_nonedbstat(self):
        generate_count = generate_data.generate(generate_data.get_name_lists, mock_f_get_state_stats_fail)
        self.assertEqual(generate_count, None)

    def test_generate_emptystatdata(self):
        generate_count = generate_data.generate(generate_data.get_name_lists, mock_f_get_state_stats_emptydb)
        self.assertEqual(generate_count, None)

    def test_generate_onestate(self):
        generate_count = generate_data.generate(generate_data.get_name_lists, mock_f_get_state_stats_onestate)
        self.assertEqual(generate_count[0], 1)
        for i in range(1, len(generate_count)):
            self.assertTrue(generate_count[i] > 0)

    def test_generate_twostates(self):
        generate_count = generate_data.generate(generate_data.get_name_lists, mock_f_get_state_stats_twostates)
        # self.assertEqual(generate_count[0], 2)
        for i in range(1, len(generate_count)):
            self.assertTrue(generate_count[i] > 0)

    def test_generate_notEnoughNameLists1(self):
        generate_count = generate_data.generate(mock_f_get_name_lists_shortlists1, mock_f_get_state_stats_onestate)
        self.assertEqual(generate_count, [1, 0, 0, 0, 0, 0])


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
    distObj = District(random.choice(range(1000, 2000)), 'dist_external_id', 'dist1', state.state_id, sch_num, city_zip_map, 'address1', 1000)
    return distObj


def make_school(district):
    num_of_stu = 100
    stu_tea_ratio = 25
    low_grade = 1
    high_grade = 6
    school = School(random.randint, uuid.uuid4(), 'school_test_name', district.district_name, district.district_id, district.state_code, num_of_stu, stu_tea_ratio, low_grade, high_grade, 'category_t')
    return school


def make_students(count, district=None):
    student_list = []
    sta = make_state()
    dis = make_district(sta)
    sch = make_school(dis)
    while(count > 0):
        student = Student(count, 2 * count, ('first_name' + str(count)), ('last_name' + str(count)), ('address1' + str(count)), '08/02/2000', dis, sta, 'male', 'email', sch)
        count -= 1
        student_list.append(student)
    return student_list


def make_teachers(count):
    teacher_list = []
    sta = make_state()
    dis = make_district(sta)
    while(count > 0):
        teacher = Teacher('tfirst_name' + str(count), 'tlast_name' + str(count), dis.district_id, sta.state_id, teacher_id=count)
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
