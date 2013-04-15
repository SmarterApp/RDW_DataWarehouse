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
    from_date = datetime.date.today().strftime('%Y%m%d')
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
    from_date = datetime.date.today().strftime('%Y%m%d')
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


def generate_assessment(asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject, asmt_grade,
                        asmt_claim_1_name, asmt_claim_2_name, asmt_claim_3_name, asmt_claim_4_name,
                        asmt_perf_lvl_name_1, asmt_perf_lvl_name_2, asmt_perf_lvl_name_3, asmt_perf_lvl_name_4, asmt_perf_lvl_name_5,
                        asmt_score_min, asmt_score_max, asmt_claim_1_score_min, asmt_claim_1_score_max, asmt_claim_1_score_weight,
                        asmt_claim_2_score_min, asmt_claim_2_score_max, asmt_claim_2_score_weight,
                        asmt_claim_3_score_min, asmt_claim_3_score_max, asmt_claim_3_score_weight,
                        asmt_claim_4_score_min, asmt_claim_4_score_max, asmt_claim_4_score_weight,
                        asmt_custom_metadata, asmt_cut_point_1, asmt_cut_point_2, asmt_cut_point_3, asmt_cut_point_4):

    id_generator = IdGen()

    asmt_rec_id = id_generator.get_id()
    asmt_guid = id_generator.get_id()

    from_date = datetime.date.today().strftime('%Y%m%d')
    to_date = datetime.date.today().strftime('%Y%m%d')
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


def generate_staff(hier_user_type, state_code=None, district_guid=None, school_guid=None, section_guid=None):

    id_generator = IdGen()
    staff_rec_id = id_generator.get_id()
    staff_guid = id_generator.get_id()
    gender = random.choice(constants.GENDERS)
    first_name = generate_first_or_middle_name(gender)
    last_name = generate_last_name()
    # TODO: Set date and most recent more intelligently
    from_date = datetime.date.today().strftime('%Y%m%d')
    most_recent = True
    staff = Staff(staff_rec_id, staff_guid, first_name, last_name, section_guid, hier_user_type, state_code,
                  district_guid, school_guid, from_date, most_recent)

    return staff


def generate_multiple_staff(number_of_staff, hier_user_type, state_code=None, district_guid=None, school_guid=None, section_guid=None):
    staff_list = []
    for i in range(number_of_staff):
        staff_member = generate_staff(hier_user_type, state_code, district_guid, school_guid, section_guid)
        staff_list.append(staff_member)
    return staff_list


def generate_fact_assessment_outcome(asmt_rec_id, student_guid, teacher_guid, state_code, district_guid, school_guid, section_guid,
                                     inst_hier_rec_id, section_rec_id, where_taken_id, where_taken_name, asmt_grade, enrl_grade,
                                     date_taken, asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                                     asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                                     asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                                     asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                                     asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max):
    id_generator = IdGen()
    asmnt_outcome_rec_id = id_generator.get_id()

    date_taken_day = date_taken.day
    date_taken_month = date_taken.month
    date_taken_year = date_taken.year
    asmt_create_date = datetime.date.today()
    status = 'C'
    most_recent = True

    asmt_outcome = AssessmentOutcome(asmnt_outcome_rec_id, asmt_rec_id, student_guid,
                                     teacher_guid, state_code, district_guid, school_guid, section_guid, inst_hier_rec_id, section_rec_id,
                                     where_taken_id, where_taken_name, asmt_grade, enrl_grade, date_taken, date_taken_day,
                                     date_taken_month, date_taken_year, asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                                     asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                                     asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                                     asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                                     asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max,
                                     asmt_create_date, status, most_recent)

    return asmt_outcome


def generate_fact_assessment_outcomes(students, scores, asmt_rec_id, teacher_guid, state_code, district_guid, school_guid, section_guid,
                                     inst_hier_rec_id, section_rec_id, where_taken_id, where_taken_name, asmt_grade, enrl_grade,
                                     date_taken):

    outcomes = []

    for student in students:
        score = scores.pop()
        claim_scores = score.claim_scores

        student_guid = student.student_guid
        asmt_score = score.overall_score
        asmt_score_range_min = score.interval_min
        asmt_score_range_max = score.interval_max
        asmt_perf_lvl = score.perf_lvl
        asmt_claim_1_score = claim_scores[0].claim_score
        asmt_claim_2_score = claim_scores[1].claim_score
        asmt_claim_3_score = claim_scores[2].claim_score
        asmt_claim_4_score = claim_scores[3].claim_score if len(claim_scores) > 3 else None
        asmt_claim_1_score_range_min = claim_scores[0].claim_score_interval_minimum
        asmt_claim_2_score_range_min = claim_scores[1].claim_score_interval_minimum
        asmt_claim_3_score_range_min = claim_scores[2].claim_score_interval_minimum
        asmt_claim_4_score_range_min = claim_scores[3].claim_score_interval_minimum if len(claim_scores) > 3 else None
        asmt_claim_1_score_range_max = claim_scores[0].claim_score_interval_maximum
        asmt_claim_2_score_range_max = claim_scores[1].claim_score_interval_maximum
        asmt_claim_3_score_range_max = claim_scores[2].claim_score_interval_maximum
        asmt_claim_4_score_range_max = claim_scores[3].claim_score_interval_maximum if len(claim_scores) > 3 else None

        asmt_outcome = generate_fact_assessment_outcome(asmt_rec_id, student_guid, teacher_guid, state_code, district_guid, school_guid, section_guid,
                                     inst_hier_rec_id, section_rec_id, where_taken_id, where_taken_name, asmt_grade, enrl_grade,
                                     date_taken, asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                                     asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                                     asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                                     asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                                     asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max)
        outcomes.append(asmt_outcome)

    return outcomes
