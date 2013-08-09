'''
Created on Aug 5, 2013

@author: swimberly
'''

from importlib import import_module
from uuid import uuid4
import datetime
import argparse
import os
import csv
import math
import random

import stats
from demographics import Demographics, ALL_DEM, L_GROUPING, L_TOTAL, L_PERF_1, L_PERF_4, OVERALL_GROUP
from generate_entities import (generate_assessments, generate_institution_hierarchy, generate_sections, 
                               generate_multiple_staff, generate_assessment_outcomes_from_student_info,
                               generate_students_from_student_info)
from write_to_csv import create_csv
from state_population import StatePopulation
import constants
from generate_scores import generate_overall_scores
from entities import (InstitutionHierarchy, Section, Assessment, AssessmentOutcome,
                      Staff, ExternalUserStudent, Student)
from errorband import calc_eb_params, calc_eb
from generate_helper_entities import generate_claim_score, generate_assessment_score, generate_district, generate_school, generate_state
from helper_entities import StudentInfo
from print_state_population import print_state_population
import util
from assign_students_subjects_scores import assign_scores_for_subjects
from idgen import IdGen


DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
components = DATAFILE_PATH.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])

ENTITY_TO_PATH_DICT = {InstitutionHierarchy: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_inst_hier.csv'),
                       Section: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_section.csv'),
                       Assessment: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_asmt.csv'),
                       AssessmentOutcome: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
                       Staff: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_staff.csv'),
                       ExternalUserStudent: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'external_user_student_rel.csv'),
                       Student: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_student.csv')}

CSV_FILE_NAMES = {InstitutionHierarchy: 'dim_inst_hier.csv',
                  Section: 'dim_section.csv',
                  Assessment: 'dim_asmt.csv',
                  AssessmentOutcome: 'fact_asmt_outcome.csv',
                  Staff: 'dim_staff.csv',
                  ExternalUserStudent: 'external_user_student_rel.csv',
                  Student: 'dim_student.csv'}

LAST_NAMES = 'last_names'
FEMALE_FIRST_NAMES = 'female_first_names'
MALE_FIRST_NAMES = 'male_first_names'
BIRDS = 'birds'
FISH = 'fish'
MAMMALS = 'mammals'
ANIMALS = 'animals'

NAMES_TO_PATH_DICT = {BIRDS: os.path.join(DATAFILE_PATH, 'datafiles', 'name_lists', 'birds.txt'),
                      FISH: os.path.join(DATAFILE_PATH, 'datafiles', 'name_lists', 'fish.txt'),
                      MAMMALS: os.path.join(DATAFILE_PATH, 'datafiles', 'name_lists', 'mammals.txt'),
                      ANIMALS: os.path.join(DATAFILE_PATH, 'datafiles', 'name_lists', 'one-word-animal-names.txt')
                      }


def generate_data_from_config_file(config_module, output_dict):
    '''
    Main function that drives the data generation process
    Collects all relevant info from the config files and calls methods to generate states and remaining data

    @param config_module: module that contains all configuration information for the data creation process
    @return nothing
    '''

    # generate one batch_guid for all records
    batch_guid = uuid4()

    (demographics_info, district_names, school_names, street_names, states_config, state_types, district_types,
     school_types, scores_details, from_date, to_date, most_recent, error_band_dict) = get_values_from_config(config_module)

    # Generate Assessment CSV File
    flat_grades_list = get_flat_grades_list(school_types, constants.GRADES)
    assessments = generate_assessments(flat_grades_list, scores_details[constants.CUT_POINTS],
                                       from_date, most_recent, to_date=to_date)

    # Generate the all the data
    state_populations = generate_state_populations(states_config, state_types, demographics_info, assessments, district_types,
                                                   school_types, district_names, school_names, error_band_dict, from_date,
                                                   most_recent, to_date)

    states = generate_real_states(state_populations, assessments, error_band_dict, district_names, school_names,
                                  demographics_info, from_date, most_recent, to_date, street_names)

    output_generated_data_to_csv(states, assessments, batch_guid, output_dict, from_date, most_recent, to_date)


def output_generated_data_to_csv(states, assessments, batch_guid, output_dict, from_date, most_recent, to_date):
    '''
    '''
    # First thing: prep the csv files by deleting their contents and adding appropriate headers
    prepare_csv_files(output_dict)
    print('Writing CSV files')

    create_csv(assessments, output_dict[Assessment])

    institution_hierarchies = []
    staff = []
    sections = []

    for state in states:
        staff += state.staff
        for district in state.districts:
            staff += district.staff
            for school in district.schools:
                staff += school.teachers
                sections += school.sections

                inst_hier = generate_institution_hierarchy_from_helper_entities(state, district, school, from_date,
                                                                                most_recent, to_date)
                institution_hierarchies.append(inst_hier)
                student_entities = generate_students_from_student_info(school.student_info)
                fact_assessment_entities = generate_assessment_outcomes_from_student_info(school.student_info, batch_guid, inst_hier)

                create_csv(student_entities, output_dict[Student])
                create_csv(fact_assessment_entities, output_dict[AssessmentOutcome])

    create_csv(institution_hierarchies, output_dict[InstitutionHierarchy])
    create_csv(sections, output_dict[Section])
    create_csv(staff, output_dict[Staff])


def get_values_from_config(config_module):
    '''
    Given a config module pull out all information that is necessary for the generation of data
    In some cases also will create the relevant objects
    '''

    # Setup demographics object
    demographics_info = Demographics(config_module.get_demograph_file())

    # Next, prepare lists that are used to name various entities
    name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)

    # We're going to use the birds and fish list to name our districts
    district_names = (name_list_dictionary[ANIMALS], name_list_dictionary[ANIMALS])

    # We're going to use mammals and birds to names our schools
    school_names = (name_list_dictionary[ANIMALS], name_list_dictionary[ANIMALS])

    # Use birds for street names
    street_names = name_list_dictionary[BIRDS]

    # Get information from the config module
    school_types = config_module.get_school_types()
    district_types = config_module.get_district_types()
    state_types = config_module.get_state_types()
    states = config_module.get_states()
    scores_details = config_module.get_scores()

    # Get temporal information
    temporal_information = config_module.get_temporal_information()
    from_date = temporal_information[constants.FROM_DATE]
    most_recent = temporal_information[constants.MOST_RECENT]
    to_date = temporal_information[constants.TO_DATE]

    # Get Error Band Information from config_module
    error_band_dict = config_module.get_error_band()

    derived_values = (demographics_info, district_names, school_names, street_names, states, state_types,
                      district_types, school_types, scores_details, from_date, to_date, most_recent, error_band_dict)

    return derived_values


def generate_state_populations(states, state_types, demographics_info, assessments, district_types, school_types,
                               district_names, school_names, error_band_dict, from_date, most_recent, to_date):
    '''
    Take all relevant information and loop through the states to generate the relevant data
    '''

    state_populations = []

    for state in states:
        # Pull out basic state information
        state_name = state[constants.NAME]
        state_code = state[constants.STATE_CODE]

        # Pull out information on districts within this state
        state_type_name = state[constants.STATE_TYPE]
        state_type = state_types[state_type_name]
        subject_percentages = state_type[constants.SUBJECT_AND_PERCENTAGES]
        demographics_id = state_type[constants.DEMOGRAPHICS]

        # Create State Population object
        state_population = StatePopulation(state_name, state_code, state_type_name)
        # calculate the states total number of object
        state_population.populate_state(state_type, district_types, school_types)
        # Calculate the Math Demographic numbers for the state
        state_population.get_state_demographics(demographics_info, demographics_id)
        state_population.demographics_id = demographics_id
        state_population.subject_percentages = subject_percentages

        # Print Population info
        print_state_population(state_population)

        state_populations.append(state_population)

    return state_populations


def generate_real_states(state_populations, assessments, error_band_dict, district_names, school_names,
                         demographics_info, from_date, most_recent, to_date, street_names):
    '''
    Generate a real state with districts, schools, students, sections and teachers
    '''
    real_states = []

    for state_population in state_populations:
        demographics_id = state_population.demographics_id
        subject_percentages = state_population.subject_percentages

        # generate pool of students for state
        student_info_dict = generate_students_info_from_demographic_counts(state_population, assessments, error_band_dict)

        # create districts
        districts = create_districts(state_population, district_names[0], district_names[1], school_names[0],
                                     school_names[1], student_info_dict, subject_percentages, demographics_info,
                                     demographics_id, assessments, error_band_dict, state_population.name,
                                     state_population.state_code, from_date, most_recent, to_date, street_names)

        # Create the actual state object
        state = generate_state(state_population.name, state_population.state_code, districts)

        # Create the state-level staff
        number_of_state_level_staff = 10
        state_level_staff = generate_non_teaching_staff(number_of_state_level_staff, from_date, most_recent, to_date, state_code=state.state_code)
        state.staff = state_level_staff
        real_states.append(state)
    return real_states


def get_school_population(school, student_info_dict, subject_percentages, demographics_info, demographics_id,
                          assessments, error_band_dict, state_name, state_code, from_date, most_recent, to_date, street_names):
    '''
    create teachers, students and sections for a school
    '''
    eb_min_perc = error_band_dict[constants.MIN_PERC]
    eb_max_perc = error_band_dict[constants.MAX_PERC]
    eb_rand_adj_lo = error_band_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = error_band_dict[constants.RAND_ADJ_PNT_HI]

    school_counts = school.grade_performance_level_counts
    students_in_school = []
    sections_in_school = []
    teachers_in_school = []

    for grade in school_counts:

        number_of_sections = 1
        math_sections = generate_sections(number_of_sections, constants.MATH, grade, state_code, school.district_guid,
                                          school.school_guid, from_date, most_recent, to_date=to_date)
        ela_sections = generate_sections(number_of_sections, constants.ELA, grade, state_code, school.district_guid,
                                         school.school_guid, from_date, most_recent, to_date=to_date)
        sections_in_school += math_sections + ela_sections

        # create teachers
        staff_per_section = 1
        math_staff = generate_teachers_for_sections(staff_per_section, math_sections, from_date, most_recent, to_date, school, state_code)
        ela_staff = generate_teachers_for_sections(staff_per_section, ela_sections, from_date, most_recent, to_date, school, state_code)

        # Generate Students that have Math scores and demographics
        students = get_students_by_counts(grade, school_counts[grade], student_info_dict)

        # Get ELA assessment information
        math_assessment = select_assessment_from_list(assessments, grade, constants.MATH)
        math_date_taken = util.generate_date_given_assessment(math_assessment)
        ela_assessment = select_assessment_from_list(assessments, grade, constants.ELA)
        ela_date_taken = util.generate_date_given_assessment(ela_assessment)
        min_score = ela_assessment.asmt_score_min
        max_score = ela_assessment.asmt_score_max

        cut_points = get_list_of_cutpoints(ela_assessment)
        # Create list of cutpoints that includes min and max score values
        inclusive_cut_points = [min_score] + cut_points + [max_score]

        all_grade_demo_info = demographics_info.get_grade_demographics(demographics_id, constants.ELA, grade)
        ela_perf = {demo_name: demo_list[L_PERF_1:] for demo_name, demo_list in all_grade_demo_info.items()}
        assign_scores_for_subjects(students, ela_perf, inclusive_cut_points, min_score, max_score, grade, constants.ELA,
                                   ela_assessment, eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi)

        assign_students_sections(students, math_sections, ela_sections)
        set_student_institution_information(students, school, from_date, most_recent, to_date, street_names,
                                            math_staff[0], ela_staff[0], state_code)
        set_students_asmt_info(students, [constants.ELA, constants.MATH], [ela_assessment.asmt_rec_id, math_assessment.asmt_rec_id],
                               [ela_date_taken, math_date_taken])
        apply_subject_percentages(subject_percentages, students)

        students_in_school += students

    return students_in_school, teachers_in_school, sections_in_school


def generate_teachers_for_sections(staff_per_section, sections, from_date, most_recent, to_date, school, state_code):
    '''
    '''
    all_staff = []
    for section in sections:
        staff = generate_multiple_staff(staff_per_section, 'Teacher', from_date, most_recent,
                                        state_code=state_code, district_guid=school.district_guid,
                                        school_guid=school.school_guid, section_guid=section.section_guid,
                                        to_date=to_date)

        all_staff += staff

    return all_staff


def set_student_institution_information(students, school, from_date, most_recent, to_date, street_names, math_teacher, ela_teacher, state_code):
    '''
    For each student assigned to a school. Set the relevant information
    '''
    id_generator = IdGen()
    for student in students:
        city_name_1 = random.choice(street_names)
        city_name_2 = random.choice(street_names)

        student.student_rec_ids = [id_generator.get_id(), id_generator.get_id()]
        student.school_guid = school.school_guid
        student.district_guid = school.district_guid
        student.state_code = state_code
        student.from_date = from_date
        student.most_recent = most_recent
        student.to_date = to_date
        student.email = util.generate_email_address(student.first_name, student.last_name, school.school_name)
        student.address_1 = util.generate_address(street_names)
        student.city = city_name_1 + ' ' + city_name_2
        student.teacher_guids = {constants.MATH: math_teacher.staff_guid, constants.ELA: ela_teacher.staff_guid}

    return students


def assign_students_sections(students, math_sections, ela_sections):
    '''
    For a list of students and sections. Assign each student a section for math and ela
    '''
    assert len(math_sections) == len(ela_sections)
    student_size = len(students)
    students_per_section = math.ceil(student_size / len(math_sections))

    student_index = 0

    for i in range(len(math_sections)):
        for _j in range(min(students_per_section, student_size)):
            # place the section guid in section guid dict for the student
            students[student_index].section_guids[constants.MATH] = math_sections[i].section_guid
            students[student_index].section_rec_ids[constants.MATH] = math_sections[i].section_rec_id
            students[student_index].section_guids[constants.ELA] = ela_sections[i].section_guid
            students[student_index].section_rec_ids[constants.ELA] = ela_sections[i].section_rec_id
            student_index += 1

    return students


def set_students_asmt_info(students, subjects, asmt_rec_ids, dates_taken):
    '''
    take a list of students and assign them assessment record ids.
    subjects and asmt_rec_ids are lists that should match
    '''
    for student in students:
        for i in range(len(subjects)):
            student.asmt_rec_ids[subjects[i]] = asmt_rec_ids[i]
            student.asmt_dates_taken[subjects[i]] = dates_taken[i]
    return students


def apply_subject_percentages(subject_percentages, students):
    '''
    based on the percentages for each student taking an assessment, remove a subject
    record for that percentage of students
    '''
    # For each subject, calculate the number of students that should not have
    # this assessment record
    for subject in subject_percentages:
        percentage = subject_percentages[subject]

        student_size = len(students)
        students_with_out_subject = int((1 - percentage) * student_size)

        # sample the correct students and remove their assessment score
        for student in random.sample(students, students_with_out_subject):
            del student.asmt_scores[subject]


def get_students_by_counts(grade, grade_counts, student_info_dict):
    '''
    @param grade_counts: A five element list that contains the performance level counts for a grade
    [total, pl1, pl2, pl3, pl4]
    '''
    students = []
    short_sum = 0
    for pl in range(len(grade_counts)):
        if pl == 0:
            continue
        pl_count = grade_counts[pl]
        for i in range(pl_count):
            if len(student_info_dict[grade][pl]) <= 0:
                #print(student_info_dict[grade])
                #print('i', i, 'pl_count', pl_count, 'pl', pl)
                short_sum += pl_count - i
                break
            index = random.randint(0, len(student_info_dict[grade][pl]) - 1)
            students.append(student_info_dict[grade][pl].pop(index))

    if short_sum:
        print('short_sum', short_sum)
    return students


def create_schools(district, school_names_1, school_names_2, student_info_dict, subject_percentages,
                   demographics_info, demographics_id, assessments, error_band_dict, state_name,
                   state_code, from_date, most_recent, to_date, street_names):
    '''
    create and return a list of schools from a list of districts
    '''
    schools = []

    for sch_pop in district.school_populations:
        grade_perf_lvl_counts = {}
        # Loop through grades counts and get the overall counts
        for grade, demo_dict in sch_pop.school_demographics.items():
            grade_counts = demo_dict[ALL_DEM][L_TOTAL:]
            grade_perf_lvl_counts[grade] = [round(x) for x in grade_counts]

        school = generate_school(sch_pop.school_type_name, school_names_1, school_names_2,
                                 grade_perf_lvl_counts, district.district_name, district.district_guid)

        population_data = get_school_population(school, student_info_dict, subject_percentages, demographics_info,
                                                demographics_id, assessments, error_band_dict, state_name, state_code,
                                                from_date, most_recent, to_date, street_names)
        students, teachers, sections = population_data
        #students = set_student_additional_info(school, street_names, students)

        school.student_info = students
        school.teachers = teachers
        school.sections = sections
        schools.append(school)

    return schools


# def set_student_additional_info(school, street_names, students):
#     '''
#     Set the remaining necessary information for a student
#     '''
#     id_generator = IdGen()
#     for student in students:
#         student.email = util.generate_email_address(student.first_name, student.last_name, school.school_name)
#         student.address_1 = util.generate_address(street_names)
#         city_name_1 = random.choice(street_names)
#         city_name_2 = random.choice(street_names)
#         student.city = city_name_1 + ' ' + city_name_2
#         student.student_rec_id = id_generator.get_id()
#         student.state_code = school.state_code
#
#         student.set_additional_info(email=email, address_1=address_1, city=city, student_rec_id=student_rec_id)
#
#     return students


def create_districts(state_population, district_names_1, district_names_2, school_names_1, school_names_2, student_info_dict,
                     subject_percentages, demographics_info, demographics_id, assessments, error_band_dict, state_name,
                     state_code, from_date, most_recent, to_date, street_names):
    '''
    create and return a list of districts
    '''
    districts = []
    district_populations = state_population.districts

    for dist_pop in district_populations:
        district = generate_district(district_names_1, district_names_2, dist_pop)
        district.schools = create_schools(district, school_names_1, school_names_2, student_info_dict, subject_percentages,
                                          demographics_info, demographics_id, assessments, error_band_dict, state_name,
                                          state_code, from_date, most_recent, to_date, street_names)

        # generate district staff
        number_of_district_level_staff = 10
        district.staff = generate_non_teaching_staff(number_of_district_level_staff, from_date, most_recent, to_date,
                                                           state_code=state_code, district_guid=district.district_guid)
        districts.append(district)

    return districts


def generate_students_info_from_demographic_counts(state_population, assessments, error_band_dict):
    '''
    Construct pools of students for each grade and performance level with assigned demographics
    @param state_population: A state population object that has been populated with demographic data
    @param assessments: A list of assessment objects
    @param error_band_dict: A dictionary containing the error band information
    @return: A dictionary of students with the following form {<grade>: {'PL1': [students], 'PL2': [students], ...} }
    '''

    demographic_totals = state_population.state_demographic_totals
    subject = state_population.subject
    eb_min_perc = error_band_dict[constants.MIN_PERC]
    eb_max_perc = error_band_dict[constants.MAX_PERC]
    eb_rand_adj_lo = error_band_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = error_band_dict[constants.RAND_ADJ_PNT_HI]

    state_student_dict = {}

    for grade in demographic_totals:
        grade_demographic_totals = demographic_totals[grade]
        assessment = select_assessment_from_list(assessments, grade, subject)
        min_score = assessment.asmt_score_min
        max_score = assessment.asmt_score_max

        cut_points = get_list_of_cutpoints(assessment)
        # Create list of cutpoints that includes min and max score values
        inclusive_cut_points = [min_score]
        inclusive_cut_points.extend(cut_points)
        inclusive_cut_points.append(max_score)

        overall_counts = grade_demographic_totals[ALL_DEM]
        total_students = math.ceil(overall_counts[L_TOTAL])
        perf_lvl_counts = [math.ceil(overall_counts[i]) for i in range(L_PERF_1, L_PERF_4 + 1)]

        raw_scores = generate_overall_scores(perf_lvl_counts, inclusive_cut_points, min_score, max_score, total_students, False)
        asmt_scores = translate_scores_to_assessment_score(raw_scores, cut_points, assessment, eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi)

        score_pool_dict = create_asmt_score_pool_dict(asmt_scores)
        student_info_dict = generate_students_with_demographics(score_pool_dict, grade_demographic_totals, grade)

        state_student_dict[grade] = student_info_dict
    return state_student_dict


def generate_students_with_demographics(score_pool, demographic_totals, grade):
    '''
    Given a set of scores and the demographic numbers. Create studentInfo objects that match
    the given values
    @param score_pool: A dict of scores by performance levels
    @param demographic_totals: A dictionary of numbers for each performance level by demographic
    '''

    gender_group = 1
    groupings = sorted({count_list[L_GROUPING] for _x, count_list in demographic_totals.items()})

    # Create new student info objects with a gender assigned and scores
    student_info_dict = create_student_info_dict(gender_group, score_pool, demographic_totals, grade)

    for group in groupings:
        if group == OVERALL_GROUP or group == gender_group:
            continue
        assign_demographics_for_grouping(group, student_info_dict, demographic_totals)

    return student_info_dict


def create_student_info_dict(group_num, score_pool, demographic_totals, grade):
    '''
    Create a dictionary of student info objects
    '''
    student_info_dict = {perf_lvl: [] for perf_lvl in score_pool}

    # loop through possible genders and create the appropriate number of students for each Performance Level
    for demo_name, demo_list in demographic_totals.items():
        if demo_list[L_GROUPING] != group_num:
            continue
        for i in range(L_PERF_1, L_PERF_4 + 1):
            perf_lvl_count = math.ceil(demo_list[i])
            perf_lvl = i - 1
            student_info_dict[perf_lvl] += create_student_infos_by_gender(demo_name, perf_lvl_count, perf_lvl,
                                                                          score_pool, grade)

    return student_info_dict


def create_student_infos_by_gender(gender, count, performance_level, score_pool, grade):
    '''
    Create a list of students all with the same gender and assign them scores
    '''
    student_info_list = []
    score_list = score_pool[performance_level]
    for _i in range(count):
        if len(score_list) <= 0:
            print('demographic_name', gender)
            print('short by', count - _i, 'perf_lvl was', performance_level, 'grade', grade)
            break
        index = random.randint(0, len(score_list) - 1)
        score = score_list.pop(index)
        asmt_score_dict = {'Math': score}
        student_info = StudentInfo(grade, gender, asmt_score_dict)
        student_info_list.append(student_info)

    return student_info_list


def assign_demographics_for_grouping(group_num, student_info_pool, demographic_totals):
    '''
    Assign students demographics based on the totals passed in
    '''
    # Copy student_info pools lists
    student_info_dict = {perf_lvl: student_info_pool[perf_lvl][:] for perf_lvl in student_info_pool}

    for demo_name, demo_list in demographic_totals.items():
        if demo_list[L_GROUPING] != group_num:
            continue
        for i in range(L_PERF_1, L_PERF_4 + 1):
            perf_lvl_count = math.ceil(demo_list[i])
            perf_lvl = i - 1
            assign_demographic_to_students(demo_name, student_info_dict, perf_lvl_count, perf_lvl)


def assign_demographic_to_students(demographic_name, student_pool, count, performance_level):
    '''
    Assign a number of students that are in the given performance level the given demographic
    '''
    student_list = student_pool[performance_level]
    for _i in range(count):
        if len(student_list) <= 0:
            print('demographic_name', demographic_name)
            print('short by', count - _i, 'perf_lvl was', performance_level)
            break
        index = random.randint(0, len(student_list) - 1)
        student_info = student_list.pop(index)
        setattr(student_info, demographic_name, True)
    # set 'dmg_eth_2rm' to StudentInfo
    for student_info in student_list:
        student_info.set_dmg_eth_2mr()


def create_asmt_score_pool_dict(assessment_scores):
    '''
    Given a list of assessment score objects, split them into pools based on performance level
    @param assessment_scores: A list of assessmentScore objects
    @return: A dictionary with Performance Level numbers as keys. Where the values are a list of assessmentScores
    '''

    score_pl_dict = {}

    for asmt_score in assessment_scores:
        perf_lvl = asmt_score.perf_lvl
        if not score_pl_dict.get(perf_lvl):
            score_pl_dict[perf_lvl] = []
        score_pl_dict[perf_lvl].append(asmt_score)

    return score_pl_dict


def translate_scores_to_assessment_score(scores, cut_points, assessment, ebmin, ebmax, rndlo, rndhi):
    '''
    Translate a list of assessment scores to AssessmentScore objects
    @param scores: list containing score integers
    @param cut_points: list of cutpoint scores as integers
    @param assessment: The assessment object that the outcome will be for
    @param ebmin: The divisor of the minimum error band, taken from the config file
    @param ebmax: The divisor of the maximum error band, taken from the config file
    @param rndlo: The lower bound for getting the random adjustment of the error band
    @param rndhi: The higher bound for getting the random adjustment of the error band
    @return: list of AssessmentScore objects
    '''
    score_list = []

    score_min = assessment.asmt_score_min
    score_max = assessment.asmt_score_max

    for score in scores:
        perf_lvl = None
        for i in range(len(cut_points)):
            if score < cut_points[i]:
                perf_lvl = i + 1  # perf lvls are >= 1
                break
        if perf_lvl is None and score >= cut_points[-1]:
            perf_lvl = len(cut_points) + 1

        scenter, ebmin, ebstep = calc_eb_params(score_min, score_max, ebmin, ebmax)
        ebleft, ebright, _ebhalf = calc_eb(score, score_min, score_max, scenter, ebmin, ebstep, rndlo, rndhi)
        claim_scores = calculate_claim_scores(score, assessment, ebmin, ebmax, rndlo, rndhi)
        asmt_create_date = datetime.date.today().strftime('%Y%m%d')
        asmt_score = generate_assessment_score(score, perf_lvl, round(ebleft), round(ebright), claim_scores, asmt_create_date)

        score_list.append(asmt_score)
    return score_list


def get_flat_grades_list(school_config, grade_key):
    '''
    pull out grades from score_config and place in flat list
    @param school_config: A dictionary of school info
    @return: list of grades
    '''
    grades = []

    for school_type in school_config:
        grades.extend(school_config[school_type][grade_key])

    # remove duplicates
    grades = list(set(grades))

    return grades


def select_assessment_from_list(asmt_list, grade, subject):
    '''
    select the proper assessment from a list
    @param asmt_list: A list of Assessment objects
    @param grade: The grade to search for in the assessment list
    @param subject: The subject to search for in the assessment list
    @return: A single assessment object that has the grade and subject specified. None if no match found
    '''
    for asmt in asmt_list:
        if asmt.asmt_grade == grade and asmt.asmt_subject.lower() == subject.lower():
            return asmt


def get_list_of_cutpoints(assessment):
    '''
    Given an assessment object, return a list of cutpoints
    @param assessment: the assessment to create the list of cutpoints from
    @return: A list of cutpoints
    '''
    # The cut_points in score details do not include min and max score.
    # The score generator needs the min and max to be included
    cut_points = [assessment.asmt_cut_point_1, assessment.asmt_cut_point_2, assessment.asmt_cut_point_3]
    if assessment.asmt_cut_point_4:
        cut_points.append(assessment.asmt_cut_point_4)
    return cut_points


def generate_non_teaching_staff(number_of_staff, from_date, most_recent, to_date, state_code='NA', district_guid='NA', school_guid='NA'):
    '''
    Generate staff that are not teachers
    @param number_of_staff: The number of staff memebers to generate
    @keyword state_code: The state code to use for the staff memeber. If applicable.
    @keyword district_guid: The guid to the district the staff member is in. If applicable.
    @keyword school_guid: The guid to the school the staff member is in. If applicable.
    @return: a list of Staff objects
    '''
    hier_user_type = 'Staff'
    staff_list = generate_multiple_staff(number_of_staff, hier_user_type, from_date, most_recent, state_code=state_code,
                                         district_guid=district_guid, school_guid=school_guid, to_date=to_date)
    return staff_list


def generate_institution_hierarchy_from_helper_entities(state, district, school, from_date, most_recent, to_date):
    '''
    Create an InstitutionHierarchy object from the helper entities provided
    @param state: a State object
    @param district: A District object
    @param school: A School object
    '''
    state_name = state.state_name
    state_code = state.state_code
    district_guid = district.district_guid
    district_name = district.district_name
    school_guid = school.school_guid
    school_name = school.school_name
    school_category = school.school_category

    institution_hierarchy = generate_institution_hierarchy(state_name, state_code,
                                                           district_guid, district_name,
                                                           school_guid, school_name, school_category,
                                                           from_date, most_recent, to_date)
    return institution_hierarchy


def create_output_dict(output_path):
    '''
    create a dictionary that specifies the output path for all csv files
    @param output_path: the path to where to store the files
    @type output_path: str
    @return: A dict containing all ouput paths
    @rtype: dict
    '''
    out_dict = {}

    for fname in CSV_FILE_NAMES:
        out_dict[fname] = os.path.join(output_path, CSV_FILE_NAMES[fname])

    return out_dict


def calculate_claim_scores(asmt_score, assessment, ebmin, ebmax, rndlo, rndhi):
    '''
    Calculate a students claim scores from their overall score. Calculate the associated
    claim error bands as well and store in ClaimScore Objects.
    @param asmt_score: The integer value representing the students score on the assessment
    @param assessment: the assessment object corresponding to the student's score
    @param ebmin: The divisor of the minimum error band, taken from the config file
    @param ebmax: The divisor of the maximum error band, taken from the config file
    @param rndlo: The lower bound for getting the random adjustment of the error band
    @param rndhi: The higher bound for getting the random adjustment of the error band
    @return: a list of ClaimScore objects for the given score and assessment
    '''
    claim_scores = []
    claim_list = [(assessment.asmt_claim_1_score_min, assessment.asmt_claim_1_score_max, assessment.asmt_claim_1_score_weight),
                  (assessment.asmt_claim_2_score_min, assessment.asmt_claim_2_score_max, assessment.asmt_claim_2_score_weight),
                  (assessment.asmt_claim_3_score_min, assessment.asmt_claim_3_score_max, assessment.asmt_claim_3_score_weight)]
    percentages = [assessment.asmt_claim_1_score_weight, assessment.asmt_claim_2_score_weight, assessment.asmt_claim_3_score_weight]
    if assessment.asmt_claim_4_name:
        claim_list.append((assessment.asmt_claim_4_score_min, assessment.asmt_claim_4_score_max, assessment.asmt_claim_4_score_weight))
        percentages.append(assessment.asmt_claim_4_score_weight)

    range_min = assessment.asmt_claim_1_score_min
    range_max = assessment.asmt_claim_1_score_max
    weighted_claim_scores = stats.distribute_by_percentages(asmt_score, range_min, range_max, percentages)

    for i in range(len(claim_list)):
        # Get basic claim information from claim tuple
        claim_minimum_score = claim_list[i][0]
        claim_maximum_score = claim_list[i][1]
        scaled_claim_score = weighted_claim_scores[i]

        # calculate the claim score

        scenter, ebmin, ebstep = calc_eb_params(claim_minimum_score, claim_maximum_score, ebmin, ebmax)
        ebleft, ebright, _ebhalf = calc_eb(scaled_claim_score, claim_minimum_score, claim_maximum_score, scenter, ebmin, ebstep, rndlo, rndhi)
        claim_score = generate_claim_score(scaled_claim_score, round(ebleft), round(ebright))
        claim_scores.append(claim_score)

    return claim_scores


def prepare_csv_files(entity_to_path_dict):
    '''
    Erase each csv file and then add appropriate header

    @type entity_to_path_dict: dict
    @param entity_to_path_dict: Each key is an entity's class, and each value is the path to its csv file
    '''
    for entity in entity_to_path_dict:
        path = entity_to_path_dict[entity]
        # By opening the file for writing, we implicitly delete the file contents
        with open(path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            # Here we write the header the the given entity
            csv_writer.writerow(entity.getHeader())


def generate_name_list_dictionary(list_name_to_path_dictionary):
    '''
    Create a dictionary that contains naming lists as keys and a list of file
    lines as values
    @param list_name_to_path: a dictionary mapping names to file paths
    @return:  a dictionary mapping name to file paths
    '''
    name_list_dictionary = {}
    for list_name in list_name_to_path_dictionary:
        path = list_name_to_path_dictionary[list_name]
        name_list = util.create_list_from_file(path)
        name_list_dictionary[list_name] = name_list
    return name_list_dictionary


def main(config_mod_name='dg_types', output_path=None):
    t1 = datetime.datetime.now()
    config_module = import_module(config_mod_name)

    # setup output path dict
    output_dict = ENTITY_TO_PATH_DICT
    if output_path:
        output_dict = create_output_dict(output_path)
    # generate_data
    generate_data_from_config_file(config_module, output_dict)

    # print time
    t2 = datetime.datetime.now()
    print("data_generation starts ", t1)
    print("data_generation ends   ", t2)

    # extract the output folder path
    output_components = list(output_dict.values())[0].split(os.sep)
    output_folder = str.join(os.sep, output_components[:-1])
    return output_folder


if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate fixture data from a configuration file.')
    parser.add_argument('--config', dest='config_module', action='store', default='dg_types',
                        help='Specify the configuration module that informs that data creation process.', required=False)
    parser.add_argument('--output', dest='output_path', action='store',
                        help='Specify the location of the output csv files', required=False)
    args = parser.parse_args()

    main(args.config_module, args.output_path)
