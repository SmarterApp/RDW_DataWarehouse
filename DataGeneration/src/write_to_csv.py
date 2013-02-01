import csv
from constants import *


def create_csv(entities, filename):
    with open(filename, 'a', newline='') as csvfile:
        entity_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for e in entities:
            row = e.getRow()
            entity_writer.writerow(row)


def create_sections_stuandtea_csv(state_code, class_list, grade_num, sch_id, dist_id, idgen):
    '''
    write to four csv files for: classes  with class_id, class_title
                                 sections with section_id, class_id
                                 students with section, class, grade, school, district and state
                                 teachers with section, class, grade, school, district and state
    '''
    # classes.csv
    with open(CLASSES, 'a', newline='') as csvfile3:
        spamwriter3 = csv.writer(csvfile3, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for cla in class_list:
            spamwriter3.writerow([cla.class_id, cla.title])
            # write to sections.csv
            with open(SECTIONS, 'a', newline='') as csvfile4:
                spamwriter4 = csv.writer(csvfile4, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for sec, stus in cla.section_stu_map.items():
                    spamwriter4.writerow([sec, cla.title, cla.class_id])
                    with open(STUDENT_SECTIONS, 'a', newline='') as csvfile1:
                        spamwriter1 = csv.writer(csvfile1, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                        for stu in stus:
                            row_id = idgen.get_id()
                            spamwriter1.writerow([row_id, stu.student_id, grade_num, sch_id, dist_id, cla.class_id, sec])

            with open(TEACHER_SECTIONS, 'a', newline='') as csvfile2:
                spamwriter2 = csv.writer(csvfile2, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for sec, teachers in cla.section_tea_map.items():
                    for tea in teachers:
                        spamwriter2.writerow([state_code, dist_id, sch_id, grade_num, cla.class_id, sec, tea.firstname, tea.middlename, tea.lastname])


def create_students_csv(stu_list, state_code, sch_id):
    '''
    take a list of students and write them to a csv file
    '''
    with open(STUDENTS, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for stu in stu_list:
            spamwriter.writerow([stu.student_id, stu.firstname, stu.middlename, stu.lastname, state_code, sch_id])


def clear_files():
    for f in ENT_LIST:
        cur_file = open(f, "w")
        cur_file.truncate()
        cur_file.close()
