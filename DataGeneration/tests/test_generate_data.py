import unittest, math
import generate_data
from entities import Student
from generate_data import subjects

class TestGenerateData(unittest.TestCase):
    
    def setUp(self):
        generate_data.birds_list = ["birds1", "birds2", "birds3", "birds4", "birds5", "birds6", "birds7"]
        generate_data.manmals_list = ["flowers1", "flowers2", "flowers3", "flowers4", "flowers5", "flowers6", "flowers7"]
        generate_data.fish_list = ["fish1", "fish2", "fish3", "fish4", "fish5", "fish6", "fish7"]
        
    # test district generation
    def test_create_districts(self):
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 245]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist);
        
        self.assertTrue(len(created_dist_list) == len(school_num_in_dist))
        c = 0
        for d in created_dist_list:
            # print(d)
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertEqual(d.school_type_in_dist, school_type_in_dist[c % len(school_type_in_dist)])
            self.assertTrue(len(d.dist_name) > 0)
            self.assertTrue(len(d.address_1) > 0)
            c += 1
    
    def test_create_empty_districts(self):
        state_name = "California"
        school_num_in_dist = []
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist);
        self.assertTrue(len(created_dist_list) == 0)
   

    def test_create_districts_withNotEnoughNames(self):
        generate_data.birds_list = ["birds1", ]
        generate_data.manmals_list = ["flowers1"]
        generate_data.fish_list = ["fish1"]
        
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist);
        self.assertTrue(len(created_dist_list) == 0)         
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, len(school_num_in_dist), generate_data.birds_list, generate_data.manmals_list)
        
        

    def test_create_districts_withNotEnoughAddName(self):
        generate_data.fish_list = ["fish1"]
        
        state_name = "California"
        school_num_in_dist = [25, 67, 10, 128, 15]
        school_type_in_dist = [[14, 6, 2, 3], [38, 14, 13, 2], [4, 5, 1, 0], [40, 42, 41, 5]]

        created_dist_list = generate_data.create_districts(state_name, school_num_in_dist, school_type_in_dist);
        self.assertEqual(len(created_dist_list), len(school_num_in_dist))                
        c = 0
        for d in created_dist_list:
            self.assertEqual(d.state_name, state_name)
            self.assertEqual(d.num_of_schools, school_num_in_dist[c])
            self.assertEqual(d.school_type_in_dist, school_type_in_dist[c % len(school_type_in_dist)])
            self.assertTrue(len(d.dist_name) > 0)
            self.assertTrue(len(d.address_1) > 0)
            c += 1
    
    
    # test school generation
    def test_create_schools(self):
        dist_name = "bridge center district"
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        tea_num_in_school = [23, 12, 430, 10, 10, 15, 20, 5, 6, 7, 39, 65, 19]
        start = 2
        count = 7
        school_type = [1, 2, 3, 0]
        
        created_school_list = generate_data.create_schools(dist_name, stu_num_in_school, tea_num_in_school, start, count, school_type)
        self.assertTrue(count == len(created_school_list))
        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_name, dist_name)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[start + i])
            self.assertTrue(created_school_list[i].school_type in ["Primary", "High", "Middle", "All", "Other"])

    def test_create_schools_withNotEnoughNames(self):
        generate_data.birds_list = ["birds1"]
        generate_data.manmals_list = ["flowers1"]
        generate_data.fish_list = ["fish1"]
        
        dist_name = "bridge center district"
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        tea_num_in_school = [23, 12, 430, 10, 10, 15, 20, 5, 6, 7, 39, 65, 19]
        start = 2
        count = 7
        school_type = [1, 2, 3, 0]
        
        created_school_list = generate_data.create_schools(dist_name, stu_num_in_school, tea_num_in_school, start, count, school_type)
        self.assertTrue(len(created_school_list) == 0)
        self.assertRaises(ValueError, generate_data.generate_names_from_lists, count, generate_data.fish_list, generate_data.manmals_list)

    
    def test_create_schools_withNotEnoughAddName(self):
        generate_data.birds_list = ["bird1"]
        
        dist_name = "bridge center district"
        stu_num_in_school = [234, 123, 4309, 100, 103, 105, 200, 59, 69, 75, 391, 651, 129]
        tea_num_in_school = [23, 12, 430, 10, 10, 15, 20, 5, 6, 7, 39, 65, 19]
        start = 2
        count = 7
        school_type = [1, 2, 3, 0]

        created_school_list = generate_data.create_schools(dist_name, stu_num_in_school, tea_num_in_school, start, count, school_type)
        self.assertEqual(count, len(created_school_list))                
        for i in range(len(created_school_list)):
            self.assertEqual(created_school_list[i].dist_name, dist_name)
            self.assertEqual(created_school_list[i].num_of_student, stu_num_in_school[start + i])
            
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

        self.assertEqual(0, len(generate_type1))         
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
        
        devided = len(expected_classes) / len(generate_data.subjects)
        first_part = devided * (len(generate_data.subjects) - 1)
        for i in range(len(expected_classes)):
            if(i < first_part):
                self.assertEqual(expected_classes[i].title, generate_data.subjects[math.floor((int)(i / devided))] + " " + str((int)(i % devided)))
            else:
                self.assertEqual(expected_classes[i].title, generate_data.subjects[len(generate_data.subjects) - 1] + " " + str((int)(i % devided)))


    def test_create_classes_for_grade_samllstudents(self):
        stu_num = 20
        stu_list = make_stus_or_teas(stu_num)
        tea_list = make_stus_or_teas(1)
        stu_tea_ratio = round(len(stu_list) / len(tea_list))  
        
        expected_classes = generate_data.create_classes_for_grade(stu_list, tea_list, stu_tea_ratio)
        self.assertEqual(len(expected_classes), len(generate_data.subjects))
        for i in range(len(expected_classes)):
            self.assertEqual(expected_classes[i].title, subjects[i] + " " + str(0))
    
    
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
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
