__author__ = 'abrien'

from entities_2 import InstitutionHierarchy, Student, Section
from idgen import IdGen
from constants_2 import GENDERS
from generate_names import generate_first_or_middle_name, generate_last_name
import util_2 as util
import random
import datetime


def generate_institution_hierarchy(state_name, state_code,
                                   district_guid, district_name,
                                   school_guid, school_name, school_category,
                                   from_date, most_recent, to_date=None):
    id_generator = IdGen()
    inst_hier_rec_id = id_generator.get_id()

    return InstitutionHierarchy(inst_hier_rec_id, state_name, state_code,
                                district_guid, district_name,
                                school_guid, school_name, school_category,
                                from_date, most_recent, to_date)


def generate_student(section_guid, grade, state_code, district_guid, school_guid, school_name, street_names):
    id_generator = IdGen()
    student_rec_id = id_generator.get_id()
    # TODO: maybe change to UUID
    student_guid = id_generator.get_id()
    gender = random.choice(GENDERS)
    first_name = generate_first_or_middle_name(gender)
    last_name = generate_last_name()
    address_1 = util.generate_address(street_names)
    # TODO: change city name
    city_name_1 = random.choice(street_names)
    city_name_2 = random.choice(street_names)
    city = city_name_1 + ' ' + city_name_2
    # TODO: implement city-zip map
    zip_code = random.randint(10000, 99999)
    email = util.generate_email_address(first_name, last_name, school_name)
    dob = util.generate_dob(grade)
    # TODO: Set date and most recent more intelligently
    from_date = datetime.date.today()
    most_recent = True

    student = Student(student_rec_id, student_guid, first_name, last_name, address_1, city, zip_code,
                      gender, email, dob, section_guid, grade, state_code, district_guid, school_guid, from_date, most_recent)
    return student


def generate_students(number_of_students, section_guid, grade, state_code, district_guid, school_guid, school_name, street_names):
    students = []
    for _i in range(number_of_students):
        student = generate_student(section_guid, grade, state_code, district_guid, school_guid, school_name, street_names)
        students.append(student)
    return students


def generate_section(subject_name, grade, state_code, district_guid, school_guid, section_number, class_number):
    id_generator = IdGen()
    section_rec_id = id_generator.get_id()
    section_guid = id_generator.get_id()
    section_name = 'Section ' + str(section_number)
    class_name = subject_name + '_' + str(class_number)
    # TODO: Set date and most recent more intelligently
    from_date = datetime.date.today()
    most_recent = True

    section = Section(section_rec_id, section_guid, section_name, grade, class_name, subject_name, state_code,
                      district_guid, school_guid, from_date, most_recent)
    return section


def generate_sections(number_of_sections, subject_name, grade, state_code, district_guid, school_guid):
    #TODO: figure out class and section names
    sections = []
    for i in range(number_of_sections):
        section = generate_section(subject_name, grade, state_code, district_guid, school_guid, i, i)
        sections.append(section)
    return sections
