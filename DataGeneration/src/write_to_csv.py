import csv

path = "../datafiles/"
file_names = [path + 'states.csv', path + 'districts.csv', path + 'schools.csv', path + 'stu_sections.csv', path + 'tea_sections.csv', path + 'parents.csv', path + 'assessments.csv']


def create_csv(entities, type):
    with open(file_names[0], 'a', newline='') as csvfile:
        entity_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for e in entities:
            row = e.getRow()
            entity_writer.write_row(row)

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


def clear_files():
    for f in file_names:
        cur_file = open(f, "w")
        cur_file.truncate()
        cur_file.close()
