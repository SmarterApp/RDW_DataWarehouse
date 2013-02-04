import unittest
import math
import generate_data
import random
from entities import District, School
from constants import SUBJECTS, INST_CATEGORIES, ZIPCODE_START, ZIPCODE_RANG_INSTATE, SCHOOL_LEVELS_INFO
from objects.dimensions import Student


class TestGenerateData(unittest.TestCase):

    def setUp(self):
        for i in range(1000):
            generate_data.birds_list.append('bird' + str(i))
            generate_data.manmals_list.append('flower' + str(i))
            generate_data.fish_list.append('fish' + str(i))

    # test make_teacher_num(), has 1 teacher
    def test_make_teacher_num_oneteacher(self):
        stu_num = [13, 10, 77, 19]
        ratio = [14, 19, 20, 17]

        expected = generate_data.make_teacher_num(stu_num, ratio)
        print(expected)
        for i in range(len(expected)):
            self.assertTrue(expected[i] >= 1)
            self.assertEqual(expected[i], round(stu_num[i] / ratio[i]))

    # test make_teacher_num()
    def test_make_teacher_num(self):
        stu_num = [200, 66, 77, 19]
        ratio = [14, 19, 20, 17]

        expected = generate_data.make_teacher_num(stu_num, ratio)
        print(expected)
        for i in range(len(expected)):
            self.assertTrue(expected[i] >= 1)
            self.assertEqual(expected[i], max(1, round(stu_num[i] / ratio[i])))

    # test generate_school_type()
    def test_generate_school_type_fourdists(self):
        db_school_type_list = [['dist_1', 'Primary', 10],
                               ['dist_1', 'High', 16],
                               ['dist_1', 'Middle', 29],
                               ['dist_2', 'Primary', 16],
                               ['dist_2', 'Other', 18],
                               ['dist_3', 'Primary', 100],
                               ['dist_4', 'High', 121]
                               ]
        expected = generate_data.generate_school_type(db_school_type_list)
        self.assertTrue(len(expected), 4)
        self.assertEqual(expected[0], [10, 29, 16, 0])
        self.assertEqual(expected[1], [16, 0, 0, 18])
        self.assertEqual(expected[2], [100, 0, 0, 0])
        self.assertEqual(expected[3], [0, 0, 121, 0])

    # test generate_school_type()
    def test_generate_school_type_onedist(self):
        db_school_type_list = [['dist_1', 'Other', 29],
                               ['dist_1', 'Primary', 10],
                               ['dist_1', 'High', 16]
                               ]
        expected = generate_data.generate_school_type(db_school_type_list)
        self.assertTrue(len(expected), 1)
        self.assertEqual(expected[0], [10, 0, 16, 29])

    # test district generation
    def test_create_districts(self):
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 245, 199]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]
        pos = 0
        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist, pos);
        self.assertTrue(len(created_dist_list) == len(school_num_in_dist))

        expected_zipinit = (pos + 1) * ZIPCODE_START
        expected_zipdist = max(1, (ZIPCODE_RANG_INSTATE // len(school_num_in_dist)))
        expected_zipbigmax = expected_zipinit + ZIPCODE_RANG_INSTATE
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertEqual(d.school_type_in_dist, school_type_in_dist[c % len(school_type_in_dist)])
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
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]
        pos = 1
        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist, pos);
        self.assertTrue(len(created_dist_list) == 0)

    def test_create_districts_withNotEnoughNames(self):
        generate_data.birds_list = ["birds1", ]
        generate_data.manmals_list = ["flowers1"]
        generate_data.fish_list = ["fish1"]

        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist, 0);
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, len(school_num_in_dist), generate_data.birds_list, generate_data.manmals_list)

    def test_create_districts_withNotEnoughAddName(self):
        generate_data.fish_list = ['fish1']
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]
        pos = 2

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist, pos);
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))

        expected_zipinit = (pos + 1) * ZIPCODE_START
        expected_zipdist = max(1, (ZIPCODE_RANG_INSTATE // len(school_num_in_dist)))
        expected_zipbigmax = expected_zipinit + ZIPCODE_RANG_INSTATE
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertEqual(d.school_type_in_dist, school_type_in_dist[c % len(school_type_in_dist)])
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

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist, pos);
        self.assertEqual(len(created_dist_list), 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, school_num_in_dist[0], generate_data.birds_list, generate_data.fish_list)

    # test school generation
    def test_create_schools(self):
        dist_id = 5555
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        start = 2
        count = 7
        school_type = [1, 2, 3, 0]
        city_names = random.sample(generate_data.birds_list, len(stu_num_in_school))
        zip_range = (1000, 5000)
        distObj = District(dist_id, 'CA', 'name1', count, 'add1', school_type, zip_range, city_names, INST_CATEGORIES[2])
        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, start, distObj)
        self.assertTrue(count == len(created_school_list))
        expected_sch_types = [sch_level[0] for sch_level in SCHOOL_LEVELS_INFO]

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[start + i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[start + i])
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

    def test_create_schools_withNotEnoughNames(self):
        # generate_data.birds_list = ["birds1"]
        generate_data.manmals_list = ["flowers1"]
        generate_data.fish_list = ["fish1"]

        dist_id = 5555
        dist_name = 'name1'
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        start = 2
        count = 7
        school_type = [1, 2, 3, 0]
        distObj = District(dist_id, 'CA', dist_name, count, 'add1', school_type, (1000, 5000), random.sample(generate_data.birds_list, len(stu_num_in_school)), INST_CATEGORIES[2])

        created_school_list, wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, start, distObj)
        self.assertTrue(len(created_school_list) == 0)
        self.assertTrue(len(wheretaken_list) == 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, count, generate_data.fish_list, generate_data.manmals_list)

    def test_create_schools_withNotEnoughAddName(self):
        generate_data.birds_list = ["bird1"]

        dist_id = 5555
        dist_name = 'name1'
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        stutea_ratio_in_school = [23, 12, 20, 19, 10, 15, 20, 5, 6, 7, 8, 21, 19]
        start = 2
        count = 7
        school_type = [1, 2, 3, 0]
        city_names = random.sample(generate_data.fish_list, len(stu_num_in_school))
        zip_range = (1000, 5000)
        distObj = District(dist_id, 'CA', dist_name, count, 'add1', school_type, zip_range, city_names, INST_CATEGORIES[2])

        created_school_list, created_wheretaken_list = generate_data.create_schools(stu_num_in_school, stutea_ratio_in_school, start, distObj)
        self.assertEqual(count, len(created_school_list))
        expected_sch_types = [sch_level[0] for sch_level in SCHOOL_LEVELS_INFO]

        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_id, dist_id)
            self.assertTrue(len(created_school_list[i].school_name) > 0)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[start + i])
            self.assertEqual(created_school_list[i].stu_tea_ratio, stutea_ratio_in_school[start + i])
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

    # test create_classes_grades_sections()
    def test_create_classes_grades_sections(self):
        sch_id = 1134
        dist_id = 9876
        sch_name = 'school123'
        stu_num = 358
        tea_num = 40
        sch_add1 = '50 sunflower ave'
        school_type = 'Primary'
        low_grade = 1
        high_grade = 5
        place_id = 8761
        sch = School(sch_id, dist_id, sch_name, stu_num,
                        tea_num, sch_add1, school_type,
                        low_grade, high_grade, place_id, INST_CATEGORIES[3])
        state_code = 'CA'
        expected_grade_classes = generate_data.create_classes_grades_sections(sch, state_code)

        self.assertEqual(len(expected_grade_classes), (high_grade - low_grade + 1))
        total_stu = 0
        for grade, classes in expected_grade_classes.items():
            for cla in classes:
                self.assertTrue(cla.sub_name in SUBJECTS)
                for sec, stus in cla.section_stu_map.items():
                    self.assertTrue(len(stus) > 0)
                    total_stu += len(stus)
                for sec, tea in cla.section_tea_map.items():
                    self.assertEqual(len(tea), 1)
                self.assertEqual(len(cla.section_stu_map), len(cla.section_tea_map))
        self.assertEqual(stu_num, total_stu / 2)

    # test cal_school_num_for_type
    def test_cal_school_num_for_type(self):
        count = 10
        school_type_in_dist = [4, 3, 5, 0]
        generate_type = generate_data.cal_school_num_for_type(count, school_type_in_dist)

        self.assertEqual(count, sum(generate_type))

    def test_cal_school_num_for_type_empty(self):
        count = 0
        school_type_in_dist = [4, 3, 5, 0]
        generate_type = generate_data.cal_school_num_for_type(count, school_type_in_dist)

        self.assertEqual(count, len(generate_type))

    def test_cal_school_num_for_type_WrongTypeList(self):
        count = 7
        school_type_in_dist1 = [0, 0, 0, 0]
        school_type_in_dist2 = [0, 10]
        generate_type1 = generate_data.cal_school_num_for_type(count, school_type_in_dist1)
        generate_type2 = generate_data.cal_school_num_for_type(count, school_type_in_dist2)

        self.assertEqual(count, sum(generate_type1))
        self.assertEqual(0, len(generate_type2))

    # test makeup
    def test_makeup(self):
        # sequence = [2, 3, 4, 6, 1, 6, 9, 10, 23]
        # seq_len = 13

        sequence = [38, 291, 214, 663, 287]
        seq_len = 5
        gen_seq = generate_data.makeup(sequence, seq_len)

        self.assertEqual(seq_len, len(gen_seq))
        self.assertTrue(min(gen_seq) >= min(sequence))
        self.assertTrue(max(gen_seq) <= max(sequence))
        print(sequence)
        print(gen_seq)

    def test_list_to_chucks(self):
        list1 = [9, 8, 62, 123, 345, 1, 2, 98 ]
        size1 = 3

        list2 = [1, 2, 3]
        size2 = 1
        chunks1 = generate_data.list_to_chucks(list1, size1)
        chunks2 = generate_data.list_to_chucks(list2, size2)
        self.assertEqual(size1, len(chunks1))
        self.assertEqual(size2, len(chunks2))

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
        stu_tea_ratio = round(len(stu_list) / len(tea_list))

        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list, stu_tea_ratio)

        devided = len(expected_classes) / len(SUBJECTS)
        first_part = devided * (len(SUBJECTS) - 1)
        for i in range(len(expected_classes)):
            if(i < first_part):
                self.assertEqual(expected_classes[i].title, SUBJECTS[math.floor((int)(i / devided))] + " " + str((int)(i % devided)))
            else:
                self.assertEqual(expected_classes[i].title, SUBJECTS[len(SUBJECTS) - 1] + " " + str((int)(i % devided)))

    def test_create_classes_for_grade_samllstudents(self):
        stu_num = 20
        stu_list = make_stus_or_teas(stu_num)
        tea_list = make_stus_or_teas(1)
        stu_tea_ratio = round(len(stu_list) / len(tea_list))

        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list, stu_tea_ratio)
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

    def test_generate_city_zipcode(self):
        city_names = []
        zipcode_range = [1000, 5000]
        num_of_sch = 20
        for i in range(num_of_sch):
            city_names.append('city' + str(i))

        expected_map = generate_data.generate_city_zipcode(city_names, zipcode_range, num_of_sch)

        for k, v in expected_map.items():
            print(k, v)
            self.assertTrue(k in city_names)
            self.assertTrue(v[0] >= zipcode_range[0] and v[1] <= zipcode_range[1])

        self.assertTrue(len(expected_map) <= num_of_sch)


def make_stus_or_teas(count):
    student_list = []
    while(count > 0):
        student = Student("test_school_name")
        count -= 1
        student_list.append(student)
    return student_list

if __name__ == "__main__":
    unittest.main()
