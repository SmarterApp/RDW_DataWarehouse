__author__ = 'abrien'

from DataGeneration.src.models.entities import InstitutionHierarchy, Student, Section, Assessment, Staff, AssessmentOutcome
from DataGeneration.src.utils.idgen import IdGen
from DataGeneration.src.generators.generate_names import generate_first_or_middle_name, generate_last_name, possibly_generate_middle_name
from DataGeneration.src.demographics.demographic_derived import derive_demographic
from uuid import uuid4
import DataGeneration.src.constants.constants as constants
import DataGeneration.src.utils.util as util
import random


def generate_students_from_student_info(student_info_list):
    '''
    Given a student info object, create a list of student entities
    '''

    student_list = []

    for student_info in student_info_list:
        for subject in student_info.asmt_scores:
            params = {
                'student_rec_id': student_info.student_rec_ids.pop(),
                'student_id': student_info.student_id,
                'section_guid': student_info.section_guids[subject],
                'first_name': student_info.first_name,
                'last_name': student_info.last_name,
                'address_1': student_info.address_1,
                'city': student_info.city,
                'zip_code': student_info.zip_code,
                'gender': student_info.gender,
                'email': student_info.email,
                'dob': student_info.dob,
                'grade': student_info.grade,
                'state_code': student_info.state_code,
                'district_id': student_info.district_id,
                'school_id': student_info.school_id,
                'from_date': student_info.from_date,
                'most_recent': student_info.most_recent,
                'middle_name': student_info.middle_name,
                'to_date': student_info.to_date
            }

            # create new student from dict
            student_list.append(Student(**params))

    return student_list


def generate_assessment_outcomes_from_student_info(student_info_list, batch_guid, inst_hierarchy):
    '''
    '''
    outcome_list = []
    idgen = IdGen()

    for student_info in student_info_list:
        for subject in student_info.asmt_scores:
            asmt_score_obj = student_info.asmt_scores[subject]
            date_taken = student_info.asmt_dates_taken[subject]
            claim_scores = asmt_score_obj.claim_scores
            status = 'C'

            params = {
                'asmnt_outcome_rec_id': idgen.get_id(),
                'asmt_rec_id': student_info.asmt_rec_ids[subject],
                'student_id': student_info.student_id,
                'teacher_guid': student_info.teacher_guids[subject],
                'state_code': student_info.state_code,
                'district_id': student_info.district_id,
                'school_id': student_info.school_id,
                'section_guid': student_info.section_guids[subject],
                'inst_hier_rec_id': inst_hierarchy.inst_hier_rec_id,
                'section_rec_id': student_info.section_rec_ids[subject],
                'where_taken_id': student_info.school_id,
                'where_taken_name': inst_hierarchy.school_name,
                'asmt_grade': student_info.grade,
                'enrl_grade': student_info.grade,
                'date_taken': date_taken.strftime('%Y%m%d'),
                'date_taken_day': date_taken.day,
                'date_taken_month': date_taken.month,
                'date_taken_year': date_taken.year,
                'asmt_score': asmt_score_obj.overall_score,
                'asmt_score_range_min': asmt_score_obj.interval_min,
                'asmt_score_range_max': asmt_score_obj.interval_max,
                'asmt_perf_lvl': asmt_score_obj.perf_lvl,
                'asmt_claim_1_score': claim_scores[0].claim_score,
                'asmt_claim_1_score_range_min': claim_scores[0].claim_score_interval_minimum,
                'asmt_claim_1_score_range_max': claim_scores[0].claim_score_interval_maximum,
                'asmt_claim_1_perf_lvl': claim_scores[0].perf_lvl,
                'asmt_claim_2_score': claim_scores[1].claim_score,
                'asmt_claim_2_score_range_min': claim_scores[1].claim_score_interval_minimum,
                'asmt_claim_2_score_range_max': claim_scores[1].claim_score_interval_maximum,
                'asmt_claim_2_perf_lvl': claim_scores[1].perf_lvl,
                'asmt_claim_3_score': claim_scores[2].claim_score,
                'asmt_claim_3_score_range_min': claim_scores[2].claim_score_interval_minimum,
                'asmt_claim_3_score_range_max': claim_scores[2].claim_score_interval_maximum,
                'asmt_claim_3_perf_lvl': claim_scores[2].perf_lvl,
                'asmt_claim_4_score': claim_scores[3].claim_score if len(claim_scores) > 3 else None,
                'asmt_claim_4_score_range_min': claim_scores[3].claim_score_interval_minimum if len(claim_scores) > 3 else None,
                'asmt_claim_4_score_range_max': claim_scores[3].claim_score_interval_maximum if len(claim_scores) > 3 else None,
                'asmt_claim_4_perf_lvl': claim_scores[3].perf_lvl if len(claim_scores) > 3 else None,
                'status': status,
                'most_recent': student_info.most_recent,
                'batch_guid': batch_guid,
                'asmt_type': student_info.asmt_types[subject],
                'asmt_year': student_info.asmt_years[subject],
                'asmt_subject': student_info.asmt_subjects[subject],
                'gender': student_info.gender,
                'dmg_eth_hsp': student_info.dmg_eth_hsp,
                'dmg_eth_ami': student_info.dmg_eth_ami,
                'dmg_eth_asn': student_info.dmg_eth_asn,
                'dmg_eth_blk': student_info.dmg_eth_blk,
                'dmg_eth_pcf': student_info.dmg_eth_pcf,
                'dmg_eth_wht': student_info.dmg_eth_wht,
                'dmg_prg_iep': student_info.dmg_prg_iep,
                'dmg_prg_lep': student_info.dmg_prg_lep,
                'dmg_prg_504': student_info.dmg_prg_504,
                'dmg_prg_tt1': student_info.dmg_prg_tt1,
                'dmg_eth_derived': derive_demographic(student_info.get_stu_demo_list())
            }
            outcome_list.append(AssessmentOutcome(**params))

    return outcome_list


def generate_institution_hierarchy(state_name, state_code,
                                   district_id, district_name,
                                   school_id, school_name, school_category,
                                   from_date, most_recent, to_date=None):
    '''
    Generate an InstitutionHierarchy entity

    @type state_name: L{str}
    @param state_name: The name of the state of the InstitutionHierarchy
    @type state_code: L{str}
    @param state_code: The 2 letter abbreviation of the state
    @type district_id: L{UUID}
    @param district_id: Globally Unique Identifier for the InstitutionHierarchy's district
    @type district_name: L{str}
    @param district_name: The name of the InstitutionHierarchy's district
    @type school_id: L{UUID}
    @param school_id: Globally Unique Identifier for the InstitutionHierarchy's school
    @type school_name: L{str}
    @param school_name: The name of the InstituionHierarchy's school
    @type school_category: L{str}
    @param school_category: The type of school (Elementary School, Middle School, High School)
    @type from_date: L{datetime.date}
    @param from_date: The starting date of the InstitutionHierarchy row.
    @type most_recent: L{bool}
    @param most_recent: Whether or not this is the most recent row for this particular InstitutionHierarchy
    @type to_date: L{datetime.date}
    @param to_date: The concluding date of this InstitutionHierarchy row, if applicable.
    @return: An InstitutionHierarchy object
    '''

    id_generator = IdGen()
    inst_hier_rec_id = id_generator.get_id()

    return InstitutionHierarchy(inst_hier_rec_id, state_name, state_code,
                                district_id, district_name,
                                school_id, school_name, school_category,
                                from_date, most_recent, to_date)


def generate_student(section_guid, grade, state_code, district_id, school_id, school_name, street_names,
                     from_date, most_recent, to_date=None):
    '''
    Creates a student using necessary parameters and fills in remaining parameters.
    Fills in student ids, gender, names, address, city, zipcode, email, dob

    @return: A student object
    '''
    id_generator = IdGen()
    student_rec_id = id_generator.get_id()
    student_id = uuid4()
    gender = random.choice(constants.GENDERS)
    first_name = generate_first_or_middle_name(gender)
    middle_name = possibly_generate_middle_name(gender)
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

    student = Student(student_rec_id, student_id, first_name, last_name, address_1, city, zip_code,
                      gender, email, dob, section_guid, grade, state_code, district_id, school_id,
                      from_date, most_recent, middle_name=middle_name, to_date=to_date)
    return student


def generate_students(number_of_students, section_guid, grade, state_code, district_id, school_id, school_name, street_names, from_date, most_recent, to_date=None):
    '''
    Generates 'number_of_students' amount of students within the same section

    @return: a list of student objects
    '''
    students = []
    for _i in range(number_of_students):
        student = generate_student(section_guid, grade, state_code, district_id, school_id, school_name, street_names,
                                   from_date, most_recent, to_date)
        students.append(student)
    return students


def generate_section(subject_name, grade, state_code, district_id, school_id, section_number, class_number,
                     from_date, most_recent, to_date=True):
    '''
    Creates a Section object from necessary fields passed through parameters and fills in remaining fields
    Fills in section ids, section_name, class_name
    '''
    id_generator = IdGen()
    section_rec_id = id_generator.get_id()
    section_guid = uuid4()
    section_name = 'Section ' + str(section_number)
    class_name = subject_name + '_' + str(class_number)

    section = Section(section_rec_id, section_guid, section_name, grade, class_name, subject_name, state_code,
                      district_id, school_id, from_date, most_recent, to_date=to_date)
    return section


def generate_sections(number_of_sections, subject_name, grade, state_code, district_id, school_id,
                      from_date, most_recent, to_date=None):
    '''
    Creates 'number_of_sections' amount of section objects for a given subject-grade combo

    @return: a list of section objects
    '''
    # TODO: figure out class and section names
    sections = []
    for i in range(number_of_sections):
        section = generate_section(subject_name, grade, state_code, district_id, school_id, i, i,
                                   from_date, most_recent, to_date=to_date)
        sections.append(section)
    return sections


def generate_assessment(asmt_type, asmt_period, asmt_period_year, asmt_subject, asmt_grade,
                        asmt_cut_point_1, asmt_cut_point_2, asmt_cut_point_3, asmt_cut_point_4,
                        claim_cut_point_1, claim_cut_point_2,
                        from_date, most_recent, to_date=None):
    '''
    Given Assessment information, create an Assessment object

    @return: An assessment object
    '''

    id_generator = IdGen()

    asmt_rec_id = id_generator.get_id()
    asmt_guid = uuid4()

    asmt_version = 'V1'

    performance_levels = constants.PERFORMANCE_LEVELS

    # TODO: decouple constants from this function
    claim_defs = constants.CLAIM_DEFINITIONS[asmt_subject]
    claim_perf_level = constants.CLAIM_PERFORMANCE_LEVELS
    score_min = constants.MINIMUM_ASSESSMENT_SCORE
    score_max = constants.MAXIMUM_ASSESSMENT_SCORE

    asmt_score_min = score_min
    asmt_score_max = score_max

    asmt_claim_1_name = claim_defs[0]['claim_name']
    asmt_claim_2_name = claim_defs[1]['claim_name']
    asmt_claim_3_name = claim_defs[2]['claim_name']
    asmt_claim_4_name = None

    asmt_claim_1_score_min = asmt_score_min
    asmt_claim_2_score_min = asmt_score_min
    asmt_claim_3_score_min = asmt_score_min
    asmt_claim_4_score_min = 0

    asmt_claim_1_score_max = asmt_score_max
    asmt_claim_2_score_max = asmt_score_max
    asmt_claim_3_score_max = asmt_score_max
    asmt_claim_4_score_max = 0

    asmt_claim_1_score_weight = claim_defs[0]['claim_weight']
    asmt_claim_2_score_weight = claim_defs[1]['claim_weight']
    asmt_claim_3_score_weight = claim_defs[2]['claim_weight']
    asmt_claim_4_score_weight = 0

    if len(claim_defs) > 3:
        asmt_claim_4_name = claim_defs[3]['claim_name']
        asmt_claim_4_score_min = asmt_score_min
        asmt_claim_4_score_max = asmt_score_max
        asmt_claim_4_score_weight = claim_defs[3]['claim_weight']

    asmt_perf_lvl_name_1 = performance_levels[0]
    asmt_perf_lvl_name_2 = performance_levels[1]
    asmt_perf_lvl_name_3 = performance_levels[2]
    asmt_perf_lvl_name_4 = performance_levels[3]
    asmt_perf_lvl_name_5 = performance_levels[4] if len(performance_levels) > 4 else None

    asmt_claim_perf_lvl_name_1 = claim_perf_level[0]
    asmt_claim_perf_lvl_name_2 = claim_perf_level[1]
    asmt_claim_perf_lvl_name_3 = claim_perf_level[2]

    asmt = Assessment(asmt_rec_id, asmt_guid, asmt_type, asmt_period, asmt_period_year, asmt_version, asmt_subject,
                      asmt_grade, from_date, most_recent,
                      asmt_claim_1_name, asmt_claim_2_name, asmt_claim_3_name, asmt_claim_4_name,
                      asmt_perf_lvl_name_1, asmt_perf_lvl_name_2, asmt_perf_lvl_name_3, asmt_perf_lvl_name_4, asmt_perf_lvl_name_5,
                      asmt_score_min, asmt_score_max, asmt_claim_1_score_min, asmt_claim_1_score_max, asmt_claim_1_score_weight,
                      asmt_claim_2_score_min, asmt_claim_2_score_max, asmt_claim_2_score_weight,
                      asmt_claim_3_score_min, asmt_claim_3_score_max, asmt_claim_3_score_weight,
                      asmt_claim_4_score_min, asmt_claim_4_score_max, asmt_claim_4_score_weight,
                      asmt_cut_point_1, asmt_cut_point_2, asmt_cut_point_3, asmt_cut_point_4,
                      claim_cut_point_1, claim_cut_point_2,
                      to_date, asmt_claim_perf_lvl_name_1, asmt_claim_perf_lvl_name_2, asmt_claim_perf_lvl_name_3)

    return asmt


def generate_assessments(grades, cut_points, claim_cut_points, from_date, most_recent, to_date=None):
    '''
    Generate all possible assessments for the given grades

    @return: A list of assessment objects
    '''
    assessments = []
    asmt_cut_point_1 = cut_points[0]
    asmt_cut_point_2 = cut_points[1]
    asmt_cut_point_3 = cut_points[2]
    asmt_cut_point_4 = cut_points[3] if len(cut_points) > 3 else None

    claim_cut_point_1 = claim_cut_points[0]
    claim_cut_point_2 = claim_cut_points[1]

    asmt_years = sorted(constants.ASSMT_SCORE_YEARS)
    # TODO: de-couple constants from this method.  Pass the constant values in via parameters.
    for asmt_grade in grades:
        for asmt_type in constants.ASSMT_TYPES:
            # INTERIM assessment has 3 periods, SUMMATIVE assessment has 1 'EOY' period
            periods = constants.ASSMT_PERIODS if asmt_type == 'INTERIM' else ['Spring']
            for asmt_period in periods:
                for asmt_subject in constants.SUBJECTS:
                    for index_of_year in range(len(asmt_years)):
                        most_recent = (index_of_year == len(asmt_years) - 1)
                        asmt_period_year = asmt_years[index_of_year]
                        assessment = generate_assessment(asmt_type, asmt_period + ' ' + str(asmt_period_year),
                                                         asmt_period_year, asmt_subject, asmt_grade,
                                                         asmt_cut_point_1, asmt_cut_point_2, asmt_cut_point_3,
                                                         asmt_cut_point_4, claim_cut_point_1, claim_cut_point_2,
                                                         from_date, most_recent, to_date=to_date)
                        assessments.append(assessment)
    return assessments


def generate_staff(hier_user_type, from_date, most_recent, state_code='NA', district_id='NA', school_id='NA', section_guid='NA', to_date=None):
    '''
    Given necessary staff information, fills in remaining staff fields, and creates a staff object
    Fills in staff ids, gender, names

    @return a staff object
    '''

    id_generator = IdGen()
    staff_rec_id = id_generator.get_id()
    staff_guid = uuid4()
    gender = random.choice(constants.GENDERS)
    first_name = generate_first_or_middle_name(gender)
    middle_name = possibly_generate_middle_name(gender)
    last_name = generate_last_name()
    staff = Staff(staff_rec_id, staff_guid, first_name, last_name, section_guid, hier_user_type, state_code,
                  district_id, school_id, from_date, most_recent, middle_name=middle_name, to_date=to_date)

    return staff


def generate_multiple_staff(number_of_staff, hier_user_type, from_date, most_recent, state_code='NA', district_id='NA',
                            school_id='NA', section_guid='NA', to_date=None):
    '''
    Given basic staff information, fills in remaining staff fields and creates 'number_of_staff' amount of staff objects.
    Staff can exist at any hierarchy level (State, District, School, Section), so hierarchy fields are given the default
    'NA'. For example, School Level staff will have a valid state_code, district_id, and school_id, but section_guid
    will be 'NA' for not applicable.
    '''
    staff_list = []
    for _i in range(number_of_staff):
        staff_member = generate_staff(hier_user_type, from_date, most_recent, state_code=state_code,
                                      district_id=district_id, school_id=school_id,
                                      section_guid=section_guid, to_date=to_date)
        staff_list.append(staff_member)
    return staff_list
