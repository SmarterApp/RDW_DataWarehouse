import csv

path = "../datafiles/"
file_names = [path + 'states.csv', path + 'districts.csv', path + 'schools.csv', path + 'stu_sections.csv', path + 'tea_sections.csv', path + 'parents.csv', path + 'assessments.csv']


def create_states_csv(state):
    '''
    take a list of states and write them to a csv file
    '''
    with open(file_names[0], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['STATE NAME', 'STATE CODE'])
        spamwriter.writerow([state.name, state.code])


def create_districts_csv(dist_list):
    '''
    take a list of districts and write them to a csv file
    '''
    with open(file_names[1], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['STATE NAME', 'DISTRICT NAME', 'ADDRESS 1'])
        for i in dist_list:
            spamwriter.writerow([i.state_name, i.dist_name, i.address_1])


def create_schools_csv(school_list):
    '''
    take a list of schools and write them to a csv file
    '''
    with open(file_names[2], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # spamwriter.writerow(['DISTRICT NAME', 'SCHOOL NAME', 'ADDRESS 1', 'SCHOOL_TYPE'])
        for s in school_list:
            spamwriter.writerow([s.dist_name, s.school_name, s.address1, s.school_type])


def create_sections_stuandtea_csv(state_code, class_list, grade_num, school_name, dis_name):
    '''
    write to csv file for: students with section, class, grade, school, district and state
                           teachers with section, class, grade, school, district and state
    '''
    with open(file_names[3], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for cla in class_list:
            for sec, stus in cla.section_stu_map.items():
                for stu in stus:
                    spamwriter.writerow([state_code, dis_name, school_name, grade_num, cla.title, sec, stu.firstname, stu.middlename, stu.lastname])

    with open(file_names[4], 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for cla in class_list:
            for sec, teachers in cla.section_tea_map.items():
                for tea in teachers:
                    spamwriter.writerow([state_code, dis_name, school_name, grade_num, cla.title, sec, tea.firstname, tea.middlename, tea.lastname])


def create_parent_csv(parent_list):
    '''
    take a list of parents and write them to a csv file
    '''
    with open(file_names[5], 'a', newline='') as csvfile:
        parentwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for par in parent_list:
            parentwriter.writerow([par.parent_id, par.firstname, par.middlename, par.lastname])

def create_assessment_csv(assessment_list):
    '''
    take a list of assessments and write them to a csv file
    '''
    with open(file_names[6], 'a', newline='') as csvfile:
        assessment_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for asmt in assessment_list:
            assessment_writer.writerow([asmt.id, asmt.subject, asmt.type, asmt.period, asmt.version, asmt.grade])

def clear_files():
    for f in file_names:
        cur_file = open(f, "w")
        cur_file.truncate()
        cur_file.close()
