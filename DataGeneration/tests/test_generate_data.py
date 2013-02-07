import unittest
import math
import generate_data
import random
from entities import District, School, State, Student
from constants import SUBJECTS, INST_CATEGORIES, ZIPCODE_START, ZIPCODE_RANG_INSTATE, SCHOOL_LEVELS_INFO, ADD_SUFFIX


class TestGenerateData(unittest.TestCase):

    def setUp(self):
        for i in range(1000):
            generate_data.birds_list.append('bird' + str(i))
            generate_data.manmals_list.append('flower' + str(i))
            generate_data.fish_list.append('fish' + str(i))

    # test make_school_types(perc, total)
    def test_make_school_types1(self):
        perc = [0.47, 0.38, 0.13, 0.02]
        total = 10
        expected = ['Primary', 'Primary', 'Primary', 'Primary', 'Primary',
                    'Middle', 'Middle', 'Middle', 'Middle',
                    'High'
                    ]

        generated_count = generate_data.make_school_types(perc, total)
        self.assertEqual(expected, generated_count)

        # test make_school_types(perc, total)
    def test_make_school_types2(self):
        perc = [0.33, 0.25, 0.21, 0.15]
        total = 11
        expected = ['Primary', 'Primary', 'Primary', 'Primary',
                    'Middle', 'Middle', 'Middle',
                    'High', 'High',
                    'Other', 'Other'
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
        list1 = [str(i) for i in range(100, 102)]
        list2 = [str(i) for i in range(1000, 1005)]
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, count, list1, list2)

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

    # test generate_address_from_list()
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

    # test calculate_zipvalues(pos, n)
    def test_cal_zipvalues_firststate(self):
        pos = 0
        n = 12

        expected_zipinit, expected_zipdist = generate_data.cal_zipvalues(pos, n)

        self.assertEqual(ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, (ZIPCODE_RANG_INSTATE // n))

    # test calculate_zipvalues(pos, n)
    def test_cal_zipvalues_thirdstate(self):
        pos = 2
        n = 12

        expected_zipinit, expected_zipdist = generate_data.cal_zipvalues(pos, n)

        self.assertEqual(3 * ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, (ZIPCODE_RANG_INSTATE // n))

    # test calculate_zipvalues(pos, n)
    def test_cal_zipvalues_bigN(self):
        pos = 2
        n = 10000

        expected_zipinit, expected_zipdist = generate_data.cal_zipvalues(pos, n)

        self.assertEqual(3 * ZIPCODE_START, expected_zipinit)
        self.assertEqual(expected_zipdist, 1)

    # test district generation
    def test_create_districts(self):
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 245, 199]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]
        pos = 0
        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, pos);
        self.assertTrue(len(created_dist_list) == len(school_num_in_dist))

        expected_zipinit = ZIPCODE_START
        expected_zipdist = ZIPCODE_RANG_INSTATE // len(school_num_in_dist)
        expected_zipbigmax = expected_zipinit + ZIPCODE_RANG_INSTATE
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertTrue(len(d.dist_name) > 0)
            self.assertTrue(len(d.address_1) > 0)
            self.assertEqual(d.zipcode_range, (expected_zipinit, expected_zipinit + expected_zipdist))
            self.assertEqual(len(d.city_names), school_num_in_dist[c])
            self.assertTrue(d.zipcode_range[0] < d.zipcode_range[1] and d.zipcode_range[1] <= expected_zipbigmax)
            expected_zipinit = expected_zipinit + expected_zipdist
            c += 1

    def test_create_empty_districts(self):
        state_name = "California"
        school_num_in_dist = []
        pos = 1
        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, pos);
        self.assertTrue(len(created_dist_list) == 0)

    def test_create_districts_withNotEnoughNames(self):
        generate_data.birds_list = ["birds1", ]
        generate_data.manmals_list = ["flowers1"]
        generate_data.fish_list = ["fish1"]

        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, 0);
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, len(school_num_in_dist), generate_data.birds_list, generate_data.manmals_list)

    def test_create_districts_withNotEnoughAddName(self):
        generate_data.fish_list = ['fish1']
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        pos = 2

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, pos);
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))

        expected_zipinit = (pos + 1) * ZIPCODE_START
        expected_zipdist = max(1, (ZIPCODE_RANG_INSTATE // len(school_num_in_dist)))
        expected_zipbigmax = expected_zipinit + ZIPCODE_RANG_INSTATE
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertTrue(len(d.dist_name) > 0)
            self.assertTrue(len(d.address_1) > 0)
            self.assertEqual(d.zipcode_range, (expected_zipinit, expected_zipinit + expected_zipdist))
            self.assertEqual(len(d.city_names), school_num_in_dist[c])
            self.assertTrue(d.zipcode_range[0] < d.zipcode_range[1] and d.zipcode_range[1] <= expected_zipbigmax)
            expected_zipinit = expected_zipinit + expected_zipdist
            c += 1

    def test_create_districts_withNotEnoughCityName(self):
        generate_data.fish_list = ['fish1']
        generate_data.birds_list = ['bird1']
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]
        pos = 2

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, pos);
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, school_num_in_dist[0], generate_data.birds_list, generate_data.fish_list)

    def test_generate_city_zipcode_cityMoreThanZiprange(self):
        city_names = ['city' + str(i) for i in range(100, 200)]
        zipcode_range = (2000, 2025)
        num_of_schools = 100
        self.assertTrue(len(city_names), num_of_schools)

        generated_zipmap = generate_data.generate_city_zipcode(city_names, zipcode_range, num_of_schools)
        self.assertTrue(1 <= len(generated_zipmap) <= (zipcode_range[1] - zipcode_range[0]))
        for city, ziprange in generated_zipmap.items():
            self.assertTrue(city in city_names)
            self.assertTrue(zipcode_range[0] <= ziprange[0] and ziprange[1] <= zipcode_range[1])
        self.assertTrue(len(generated_zipmap) <= num_of_schools)

    def test_generate_city_zipcode_onezip(self):
        city_names = ['city' + str(i) for i in range(100, 2000)]
        zipcode_range = [1000, 1001]
        num_of_schools = 1900

        generated_zipmap = generate_data.generate_city_zipcode(city_names, zipcode_range, num_of_schools)
        self.assertEqual(1, len(generated_zipmap))

        for city, ziprange in generated_zipmap.items():
            self.assertTrue(city in city_names)
            self.assertEqual(zipcode_range, ziprange)

        self.assertTrue(len(generated_zipmap) <= num_of_schools)

    def test_generate_city_cityLessThanZiprange(self):
        city_names = ['city' + str(i) for i in range(100, 105)]
        zipcode_range = [1000, 5000]
        num_of_schools = 5

        generated_zipmap = generate_data.generate_city_zipcode(city_names, zipcode_range, num_of_schools)
        self.assertTrue(1 <= len(generated_zipmap) <= len(city_names))

        for city, ziprange in generated_zipmap.items():
            self.assertTrue(city in city_names)
            self.assertTrue(zipcode_range[0] <= ziprange[0] and ziprange[1] <= zipcode_range[1])

        self.assertTrue(len(generated_zipmap) <= num_of_schools)

    def test_generate_city_onecity(self):
        city_names = ['city' + str(i) for i in range(100, 101)]
        zipcode_range = [1000, 5000]
        num_of_schools = 1

        generated_zipmap = generate_data.generate_city_zipcode(city_names, zipcode_range, num_of_schools)
        self.assertEqual(1, len(generated_zipmap))

        for city, ziprange in generated_zipmap.items():
            self.assertTrue(city in city_names)
            self.assertEqual(zipcode_range, ziprange)

        self.assertEqual(len(generated_zipmap), num_of_schools)

    # test school generation
    def test_create_schools(self):
        dist_id = 5555
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)

        count = 7
        city_names = random.sample(generate_data.birds_list, len(stu_num_in_school))
        zip_range = (1000, 5000)
        distObj = District(dist_id, 'CA', 'name1', count, 'add1', zip_range, city_names, INST_CATEGORIES[2])
        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat)
        self.assertEqual(count, len(created_school_list))
        self.assertEqual(count, len(created_wheretaken_list))
        expected_sch_types = [sch_level[0] for sch_level in SCHOOL_LEVELS_INFO]

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[i])
            self.assertTrue(len(created_school_list[i].address1) > 0)
            self.assertTrue(created_school_list[i].school_type in expected_sch_types)
            self.assertTrue(created_school_list[i].school_type in school_type_in_stat)
            self.assertEqual(created_school_list[i].category, INST_CATEGORIES[3])

        for j in range(len(created_wheretaken_list)):
            self.assertTrue(len(created_wheretaken_list[j].address_1) > 0)
            self.assertEqual(created_wheretaken_list[j].address_1, created_school_list[j].address1)
            self.assertTrue(len(created_wheretaken_list[j].address_2) == 0)
            self.assertTrue(len(created_wheretaken_list[j].address_3) == 0)
            self.assertTrue(created_wheretaken_list[j].city in city_names)
            self.assertTrue(created_wheretaken_list[j].zip >= zip_range[0])
            self.assertTrue(created_wheretaken_list[j].zip <= zip_range[1])
            self.assertEqual(created_wheretaken_list[j].state, 'CA')
            self.assertEqual(created_wheretaken_list[j].country, 'US')

    def test_create_schools_shortlength(self):
        dist_id = 5555
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)
        count = 2
        city_names = random.sample(generate_data.birds_list, len(stu_num_in_school))
        zip_range = (1000, 5000)
        distObj = District(dist_id, 'CA', 'name1', count, 'add1', zip_range, city_names, INST_CATEGORIES[2])
        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat)
        self.assertEqual(count, len(created_school_list))
        self.assertEqual(count, len(created_wheretaken_list))

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[i])
            self.assertTrue(len(created_school_list[i].address1) > 0)
            self.assertTrue(created_school_list[i].school_type in school_type_in_stat)
            self.assertEqual(created_school_list[i].category, INST_CATEGORIES[3])

        for j in range(len(created_wheretaken_list)):
            self.assertTrue(len(created_wheretaken_list[j].address_1) > 0)
            self.assertEqual(created_wheretaken_list[j].address_1, created_school_list[j].address1)
            self.assertTrue(len(created_wheretaken_list[j].address_2) == 0)
            self.assertTrue(len(created_wheretaken_list[j].address_3) == 0)
            self.assertTrue(created_wheretaken_list[j].city in city_names)
            self.assertTrue(created_wheretaken_list[j].zip >= zip_range[0])
            self.assertTrue(created_wheretaken_list[j].zip <= zip_range[1])
            self.assertEqual(created_wheretaken_list[j].state, 'CA')
            self.assertEqual(created_wheretaken_list[j].country, 'US')

    def test_create_schools_withNotEnoughNames(self):
        # generate_data.birds_list = ["birds1"]
        generate_data.manmals_list = ["flowers1"]
        generate_data.fish_list = ["fish1"]

        dist_id = 5555
        dist_name = 'name1'
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)
        count = 7
        distObj = District(dist_id, 'CA', dist_name, count, 'add1', (1000, 5000), random.sample(generate_data.birds_list, len(stu_num_in_school)), INST_CATEGORIES[2])

        created_school_list, wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat)
        self.assertTrue(len(created_school_list) == 0)
        self.assertTrue(len(wheretaken_list) == 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, count, generate_data.fish_list, generate_data.manmals_list)

    def test_create_schools_withNotEnoughAddName(self):
        generate_data.birds_list = ["bird1"]

        dist_id = 5555
        dist_name = 'name1'
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        school_type_in_stat = []
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[0][0]] * 13)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[1][0]] * 7)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[2][0]] * 3)
        school_type_in_stat.extend([SCHOOL_LEVELS_INFO[3][0]] * 2)
        count = 7
        city_names = random.sample(generate_data.fish_list, len(stu_num_in_school))
        zip_range = (1000, 5000)
        distObj = District(dist_id, 'CA', dist_name, count, 'add1', zip_range, city_names, INST_CATEGORIES[2])

        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, distObj, school_type_in_stat)
        self.assertEqual(count, len(created_school_list))
        expected_sch_types = [sch_level[0] for sch_level in SCHOOL_LEVELS_INFO]

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[i])
            self.assertTrue(len(created_school_list[i].address1) > 0)
            self.assertTrue(created_school_list[i].school_type in expected_sch_types)
            self.assertEqual(created_school_list[i].category, INST_CATEGORIES[3])

        for j in range(len(created_wheretaken_list)):
            self.assertTrue(len(created_wheretaken_list[j].address_1) > 0)
            self.assertTrue(len(created_wheretaken_list[j].address_2) == 0)
            self.assertTrue(len(created_wheretaken_list[j].address_3) == 0)
            self.assertTrue(created_wheretaken_list[j].city in city_names)
            self.assertTrue(created_wheretaken_list[j].zip >= zip_range[0])
            self.assertTrue(created_wheretaken_list[j].zip <= zip_range[1])
            self.assertEqual(created_wheretaken_list[j].state, 'CA')
            self.assertEqual(created_wheretaken_list[j].country, 'US')

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
        stu_list = make_stus_or_teas(800)
        tea_list = make_stus_or_teas(45)
        stu_tea_ratio = round(len(stu_list) / len(tea_list))

        expected_classes = generate_data.create_classes(sub_name, count, stu_list, tea_list, stu_tea_ratio)

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
        stu_list = make_stus_or_teas(16)
        tea_list = make_stus_or_teas(1)
        stu_tea_ratio = round(len(stu_list) / len(tea_list))

        expected_classes = generate_data.create_classes(sub_name, count, stu_list, tea_list, stu_tea_ratio)

        self.assertEqual(len(expected_classes), count)

        expected_stu_num = 0
        for i in range(len(expected_classes)):
            self.assertEqual(expected_classes[i].title, sub_name + " " + str(i))
            self.assertEqual(expected_classes[i].sub_name, sub_name)
            for value in expected_classes[i].section_stu_map.values():
                expected_stu_num += len(value)
        self.assertEqual(expected_stu_num, 16)

    def test_create_classes_for_grade(self):
        stu_list = make_stus_or_teas(160)
        tea_list = make_stus_or_teas(12)

        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list)
        expected_max_class_for_sub = 8

        for generated_class in expected_classes:
            split = generated_class.title.split(' ')
            self.assertTrue(split[0] in SUBJECTS)
            self.assertTrue((int)(split[1]) < expected_max_class_for_sub)

    def test_create_classes_for_grade_samllstudents(self):
        stu_num = 20
        stu_list = make_stus_or_teas(stu_num)
        tea_list = make_stus_or_teas(1)

        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list)
        self.assertEqual(len(expected_classes), len(SUBJECTS))
        for i in range(len(expected_classes)):
            self.assertEqual(expected_classes[i].title, SUBJECTS[i] + " " + str(0))

    def test_create_one_class_severalsections(self):
        sub_name = "Math"
        class_count = 2
        distribute_stu_inaclass = make_stus_or_teas(45)
        tea_list = make_stus_or_teas(10)
        stu_tea_ratio = 15

        expected_class = generate_data.create_one_class(sub_name, class_count, distribute_stu_inaclass, tea_list, stu_tea_ratio)
        expected_sec_num = math.floor(45 // stu_tea_ratio)

        self.assertEqual(expected_class.sub_name, sub_name)
        self.assertEqual(expected_class.title, sub_name + " " + str(class_count))
        self.assertEqual(len(expected_class.section_stu_map), expected_sec_num)

        for key, value in expected_class.section_stu_map.items():
            self.assertEqual(len(value), 15)

        self.assertEqual(len(expected_class.section_tea_map), expected_sec_num)
        for key, value in expected_class.section_tea_map.items():
            self.assertEqual(len(value), 1)

    def test_create_one_class_onesection(self):
        sub_name = "Math"
        class_count = 2
        distribute_stu_inaclass = make_stus_or_teas(45)
        tea_list = make_stus_or_teas(5)
        stu_tea_ratio = 78

        expected_class = generate_data.create_one_class(sub_name, class_count, distribute_stu_inaclass, tea_list, stu_tea_ratio)
        expected_sec_num = 1

        self.assertEqual(expected_class.sub_name, sub_name)
        self.assertEqual(expected_class.title, sub_name + " " + str(class_count))
        self.assertEqual(len(expected_class.section_stu_map), expected_sec_num)

        for key, value in expected_class.section_stu_map.items():
            self.assertEqual(len(value), 45)

        self.assertEqual(len(expected_class.section_tea_map), expected_sec_num)
        for key, value in expected_class.section_tea_map.items():
            self.assertEqual(len(value), 1)


def make_stus_or_teas(count):
    student_list = []
    while(count > 0):
        student = Student("test_school_name")
        count -= 1
        student_list.append(student)
    return student_list


if __name__ == "__main__":
    unittest.main()
