__author__ = 'abrien'

from entities_2 import InstitutionHierarchy, Student, Section, Assessment, Staff, AssessmentOutcome
from idgen import IdGen
from generate_names import generate_first_or_middle_name, generate_last_name
import constants_2 as constants
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
    gender = random.choice(constants.GENDERS)
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


def generate_assessment(asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject, asmt_grade, claim_list,
                        performance_levels, cut_points, asmt_score_min, asmt_score_max, asmt_custom_metadata):
    id_generator = IdGen()

    asmt_rec_id = id_generator.get_id()
    asmt_guid = id_generator.get_id()

    asmt_claim_1_name = claim_list[0].claim_name
    asmt_claim_1_score_min = claim_list[0].claim_score_min
    asmt_claim_1_score_max = claim_list[0].claim_score_max
    asmt_claim_1_score_weight = claim_list[0].claim_score_weight

    asmt_claim_2_name = claim_list[1].claim_name
    asmt_claim_2_score_min = claim_list[1].claim_score_min
    asmt_claim_2_score_max = claim_list[1].claim_score_max
    asmt_claim_2_score_weight = claim_list[1].claim_score_weight

    asmt_claim_3_name = claim_list[2].claim_name
    asmt_claim_3_score_min = claim_list[2].claim_score_min
    asmt_claim_3_score_max = claim_list[2].claim_score_max
    asmt_claim_3_score_weight = claim_list[2].claim_score_weight

    asmt_claim_4_name = claim_list[3].claim_name if len(claim_list) > 3 else None
    asmt_claim_4_score_min = claim_list[3].claim_score_min if len(claim_list) > 3 else None
    asmt_claim_4_score_max = claim_list[3].claim_score_max if len(claim_list) > 3 else None
    asmt_claim_4_score_weight = claim_list[3].claim_score_weight if len(claim_list) > 3 else None

    asmt_perf_lvl_name_1 = performance_levels[0]
    asmt_perf_lvl_name_2 = performance_levels[1]
    asmt_perf_lvl_name_3 = performance_levels[2]
    asmt_perf_lvl_name_4 = performance_levels[3]
    asmt_perf_lvl_name_5 = performance_levels[4] if len(performance_levels) > 4 else None

    asmt_cut_point_1 = cut_points[0]
    asmt_cut_point_2 = cut_points[1]
    asmt_cut_point_3 = cut_points[2]
    asmt_cut_point_4 = cut_points[3]

    from_date = datetime.date.today()
    to_date = datetime.date.today()
    most_recent = True

    asmt = Assessment(asmt_rec_id, asmt_guid, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject,
                 asmt_grade, from_date, asmt_claim_1_name, asmt_claim_2_name, asmt_claim_3_name, asmt_claim_4_name,
                 asmt_perf_lvl_name_1, asmt_perf_lvl_name_2, asmt_perf_lvl_name_3, asmt_perf_lvl_name_4, asmt_perf_lvl_name_5,
                 asmt_score_min, asmt_score_max, asmt_claim_1_score_min, asmt_claim_1_score_max, asmt_claim_1_score_weight,
                 asmt_claim_2_score_min, asmt_claim_2_score_max, asmt_claim_2_score_weight,
                 asmt_claim_3_score_min, asmt_claim_3_score_max, asmt_claim_3_score_weight,
                 asmt_claim_4_score_min, asmt_claim_4_score_max, asmt_claim_4_score_weight,
                 asmt_custom_metadata, asmt_cut_point_1, asmt_cut_point_2, asmt_cut_point_3, asmt_cut_point_4,
                 to_date, most_recent)

    return asmt


def generate_assessments(grades):
        pass


def generate_staff(male_first_names, female_first_names, last_names, gender, section_guid, hier_user_type, state_code, district_guid, school_guid):

    id_generator = IdGen()
    staff_rec_id = id_generator.get_id()
    staff_guid = id_generator.get_id()
    #TODO: Change to name getting algorithm
    first_name = random.choice(male_first_names if gender == 'Male' else female_first_names)
    last_name = random.choice(last_names)
    # TODO: Set date and most recent more intelligently
    from_date = datetime.date.today()
    most_recent = True
    to_date = datetime.date.today()

    staff = Staff(staff_rec_id, staff_guid, first_name, last_name, section_guid, hier_user_type, state_code,
                  district_guid, school_guid, from_date, most_recent, to_date)

    return staff


def generate_fact_assessment_outcome(assessment, student, ):
    pass


def generate_fact_assessment_outcomes():
    pass






