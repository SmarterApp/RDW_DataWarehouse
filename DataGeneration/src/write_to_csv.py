import csv

file_names = ['states.csv', 'districts.csv', 'schools.csv', 'students.csv', 'stu_sections.csv', 'tea_sections.csv']


def create_states_csv(state):
    with open(file_names[0], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['STATE NAME', 'STATE CODE'])
        spamwriter.writerow([state.name, state.code])
        
def create_districts_csv(dist_list):
    with open(file_names[1], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['STATE NAME', 'DISTRICT NAME', 'ADDRESS 1'])
        for i in dist_list:
            spamwriter.writerow([i.state_name, i.dist_name, i.address_1])

def create_schools_csv(school_list):
    with open(file_names[2], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['DISTRICT NAME', 'SCHOOL NAME', 'ADDRESS 1', 'SCHOOL_TYPE'])
        for s in school_list:
            spamwriter.writerow([s.dist_name, s.school_name, s.address1, s.school_type])        
    
def create_students_csv(stu_list):
    with open(file_names[3], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['SCHOOL NAME', 'LAST NAME', 'FIRST NAME'])
        for stu in stu_list:
            spamwriter.writerow([stu.lastname, stu.firstname])


def create_sections_stuandtea_csv(state_code, class_list, grade_num, school_name, dis_name):
    with open(file_names[4], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for cla in class_list:
            for sec, stus in cla.section_stu_map.items():
                for stu in stus:
                    spamwriter.writerow([state_code, dis_name, school_name, grade_num, cla.title, sec, stu.lastname, stu.firstname])
   
    with open(file_names[5], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for cla in class_list:
            for sec, teachers in cla.section_tea_map.items():
                for tea in teachers:
                    spamwriter.writerow([state_code, dis_name, school_name, grade_num, cla.title, sec, tea.lastname, tea.firstname])


def clear_files():
    for f in file_names:
        cur_file = open(f, "w")
        cur_file.truncate()
        cur_file.close()
