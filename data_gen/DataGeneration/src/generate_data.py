'''
Created on Aug 5, 2013

@author: swimberly
'''

from importlib import import_module
from uuid import uuid4
import datetime
import argparse
import os
import math
import random
import yaml
import pprint

from DataGeneration.src.demographics.demographics import Demographics, ALL_DEM, L_GROUPING, L_TOTAL, L_PERF_1, L_PERF_4, OVERALL_GROUP
from DataGeneration.src.generators.generate_entities import (generate_assessments, generate_institution_hierarchy, generate_sections,
                                                             generate_multiple_staff, generate_assessment_outcomes_from_student_info,
                                                             generate_students_from_student_info)
from DataGeneration.src.writers.write_to_csv import create_csv, prepare_csv_files
from DataGeneration.src.models.state_population import StatePopulation, apply_pld_to_grade_demographics, add_list_of_district_populations
import DataGeneration.src.constants.constants as constants
from DataGeneration.src.generators.generate_scores import generate_overall_scores
from DataGeneration.src.models.entities import (InstitutionHierarchy, Section, Assessment, AssessmentOutcome,
                                                Staff, ExternalUserStudent, Student)
from DataGeneration.src.generators.generate_helper_entities import generate_district, generate_school, generate_state
from DataGeneration.src.models.helper_entities import StudentInfo
from DataGeneration.src.utils.print_state_population import print_state_population
import DataGeneration.src.utils.util as util
from DataGeneration.src.utils.assign_students_subjects_scores import assign_scores_for_subjects
from DataGeneration.src.utils.idgen import IdGen
import DataGeneration.src.calc.claim_score_calculation as claim_score_calculation
from DataGeneration.src.utils.print_student_info_pool import print_student_info_pool_counts
from DataGeneration.src.models.landing_zone_data_format import output_generated_districts_to_lz_format, prepare_lz_csv_file, output_generated_asmts_to_json
from DataGeneration.src.writers.output_asmt_outcome import initialize_csv_file, output_data, output_from_dict_of_lists


IDEAL_DISTRICT_CHUNK = 100000
DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
components = DATAFILE_PATH.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])
DEFAULT_OUTPUT_DIR = os.path.join(DATAFILE_PATH, 'datafiles', 'csv')

#ENTITY_TO_PATH_DICT = {InstitutionHierarchy: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_inst_hier.csv'),
#                       Section: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_section.csv'),
#                       Assessment: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_asmt.csv'),
#                       AssessmentOutcome: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'fact_asmt_outcome.csv'),
#                       Staff: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_staff.csv'),
#                       ExternalUserStudent: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'external_user_student_rel.csv'),
#                       Student: os.path.join(DATAFILE_PATH, 'datafiles', 'csv', 'dim_student.csv')}
#
#CSV_FILE_NAMES = {InstitutionHierarchy: 'dim_inst_hier.csv',
#                  Section: 'dim_section.csv',
#                  Assessment: 'dim_asmt.csv',
#                  AssessmentOutcome: 'fact_asmt_outcome.csv',
#                  Staff: 'dim_staff.csv',
#                  ExternalUserStudent: 'external_user_student_rel.csv',
#                  Student: 'dim_student.csv'}

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


def generate_data_from_config_file(config_module, output_dict, output_config, do_pld_adjustment=True, district_chunk_size=0):
    """
    Main function that drives the data generation process
    Collects all relevant info from the config files and calls methods to generate states and remaining data

    @param config_module: module that contains all configuration information for the data creation process
    @return nothing
    """

    # generate one batch_guid for all records
    batch_guid = uuid4()

    (demographics_info, district_names, school_names, street_names, states_config, state_types, district_types,
     school_types, scores_details, from_date, to_date, most_recent, error_band_dict) = get_values_from_config(config_module)

    # Generate Assessment CSV File
    flat_grades_list = get_flat_grades_list(school_types, constants.GRADES)
    assessments = generate_assessments(flat_grades_list, scores_details[constants.CUT_POINTS],
                                       scores_details[constants.CLAIM_CUT_POINTS],
                                       from_date, most_recent, to_date=to_date)

    # output assessments
    asmt_output_dicts = {}
    for asmt in assessments:
        util.combine_dicts_of_lists(asmt_output_dicts, output_data(output_config, output_dict, assessment=asmt, write_data=False))
    output_from_dict_of_lists(asmt_output_dicts)

    # Generate the all the data
    print('Generating State Population Counts')
    state_populations = generate_state_populations(states_config, state_types, demographics_info, assessments, district_types,
                                                   school_types, district_names, school_names, error_band_dict, from_date,
                                                   most_recent, to_date, do_pld_adjustment)

    for state_population in state_populations:
        # generate districts in chunks and write to file
        district_chunk_size = district_chunk_size if district_chunk_size >= 1 else calculate_dist_chunk(state_population)
        print('district_chunk size', district_chunk_size)
        generate_districts_in_chunks(state_population, assessments, error_band_dict, district_names, school_names,
                                     demographics_info, from_date, most_recent, to_date, street_names, batch_guid,
                                     output_dict, output_config, max_chunk=district_chunk_size)

        state = generate_state(state_population.state_name, state_population.state_code)
        create_state_level_staff(state, from_date, most_recent, to_date, number_of_state_level_staff=10)

        # output state level staff
        all_staff_dict = {}
        for staff_member in state.staff:
            util.combine_dicts_of_lists(all_staff_dict, output_data(output_config, output_dict, batch_guid=batch_guid, staff=staff_member, write_data=False))
        output_from_dict_of_lists(all_staff_dict)

    return True


def output_generated_data_to_csv(states, assessments, batch_guid, output_dict, from_date, most_recent, to_date, gen_dim_asmt=False):
    """
    """
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

    if gen_dim_asmt:
        create_csv(staff, output_dict[Staff])


def output_data_to_selected_format(districts, state, batch_guid, output_dict, from_date, most_recent, to_date,
                                   star_format=True, landing_zone_format=False, single_file=True, gen_dim_asmt=False):
    """
    """
    print('Writing data to file: %s districts' % len(districts))
    if star_format:
        output_generated_districts_to_csv(districts, state, batch_guid, output_dict, from_date,
                                          most_recent, to_date, gen_dim_asmt)
    if landing_zone_format:
        output_generated_districts_to_lz_format(districts, state, batch_guid, output_dict, from_date,
                                                most_recent, to_date, single_file)
    print('Data write complete')


def output_generated_districts_to_csv(districts, state, batch_guid, output_dict, from_date, most_recent, to_date, output_config, gen_dim_asmt=False):
    """

    :param districts:
    :param state:
    :param batch_guid:
    :param output_dict:
    :param from_date:
    :param most_recent:
    :param to_date:
    :param gen_dim_asmt:
    """
    staff = []
    sections = []
    all_data_output_dict = {}

    for district in districts:
        staff += district.staff
        for school in district.schools:
            staff += school.teachers
            sections += school.sections
            inst_hier = generate_institution_hierarchy_from_helper_entities(state, district, school, from_date,
                                                                            most_recent, to_date)
            # add inst_hier to all data dict
            inst_hier_output = output_data(output_config, output_dict, inst_hier=inst_hier, write_data=False)
            all_data_output_dict = util.combine_dicts_of_lists(all_data_output_dict, inst_hier_output)

            # get output data for
            for student_in in school.student_info:
                data_output_dict = output_data(output_config, output_dict, school=school, state_population=state,
                                               batch_guid=batch_guid, student_info=student_in, inst_hier=inst_hier, write_data=False)
                all_data_output_dict = util.combine_dicts_of_lists(all_data_output_dict, data_output_dict)

    # get output data for staff and sections
    for staff_member in staff:
        staff_data_dict = output_data(output_config, output_dict, staff=staff_member, batch_guid=batch_guid, write_data=False)
        all_data_output_dict = util.combine_dicts_of_lists(all_data_output_dict, staff_data_dict)
    for section in sections:
        section_out_dict = output_data(output_config, output_dict, section=section, batch_guid=batch_guid, write_data=False)
        all_data_output_dict = util.combine_dicts_of_lists(all_data_output_dict, section_out_dict)

    # write all created dicts to file
    output_from_dict_of_lists(all_data_output_dict)


def get_values_from_config(config_module):
    """
    Given a config module pull out all information that is necessary for the generation of data
    In some cases also will create the relevant objects
    """

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
                               district_names, school_names, error_band_dict, from_date, most_recent, to_date, do_pld_adjustment):
    """
    Take all relevant information and loop through the states to generate the relevant data
    """

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
        state_population = StatePopulation(state_name, state_code, state_type_name, do_pld_adjustment=do_pld_adjustment)
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


def generate_districts_in_chunks(state_population, assessments, error_band_dict, district_names, school_names,
                                 demographics_info, from_date, most_recent, to_date, street_names, batch_guid,
                                 output_dict, output_config, max_chunk=10):
    """
    """
    for chunk_position in range(0, len(state_population.districts), max_chunk):
        new_state_population = get_district_chunk(state_population, max_chunk, chunk_position)
        print('Generating %s districts' % len(new_state_population.districts))
        districts = generate_districts_for_state_population_chunk(new_state_population, assessments, error_band_dict, district_names, school_names,
                                                                  demographics_info, from_date, most_recent, to_date, street_names)
        # write district to file
        output_generated_districts_to_csv(districts, state_population, batch_guid, output_dict, from_date, most_recent, to_date, output_config)


def get_district_chunk(state_population, chunk_size, start_pos):
    """
    """
    districts = state_population.districts
    if start_pos > len(districts):
        return

    new_districts = districts[start_pos: start_pos + chunk_size]
    new_state_population = create_state_population_from_districts(new_districts, state_population)
    return new_state_population


def create_state_population_from_districts(district_list, state_population):
    """
    create a new state population object from a subset of districts
    """
    state_demographic_totals = add_list_of_district_populations(district_list)

    new_state_population = StatePopulation(state_population.state_name, state_population.state_code, state_population.state_type, state_population.subject,
                                           state_population.do_pld_adjustment, state_demographic_totals, district_list,
                                           state_population.subject_percentages, state_population.demographics_id)
    return new_state_population


def generate_districts_for_state_population_chunk(state_populations_chunk, assessments, error_band_dict, district_names, school_names,
                                                  demographics_info, from_date, most_recent, to_date, street_names):
    """
    Generate a real state with districts, schools, students, sections and teachers
    """

    #for state_population in state_populations:
    demographics_id = state_populations_chunk.demographics_id
    subject_percentages = state_populations_chunk.subject_percentages

    # generate pool of students for state
    student_info_dict = generate_students_info_from_demographic_counts(state_populations_chunk, assessments, error_band_dict)
    print_student_info_pool_counts(student_info_dict, demographics_info, demographics_id)
    # create districts
    print('Creating the actual districts')
    districts = create_districts(state_populations_chunk, district_names[0], district_names[1], school_names[0],
                                 school_names[1], student_info_dict, subject_percentages, demographics_info,
                                 demographics_id, assessments, error_band_dict, state_populations_chunk.state_name,
                                 state_populations_chunk.state_code, from_date, most_recent, to_date, street_names)
    return districts


def create_state_level_staff(state, from_date, most_recent, to_date, number_of_state_level_staff=10):
    """
    Create the state-level staff
    """
    state_level_staff = generate_non_teaching_staff(number_of_state_level_staff, from_date, most_recent, to_date, state_code=state.state_code)
    state.staff = state_level_staff
    return state


def get_school_population(school, student_info_dict, subject_percentages, demographics_info, demographics_id, assessments,
                          error_band_dict, state_name, state_code, from_date, most_recent, to_date, street_names, pld_adjustment):
    """
    create teachers, students and sections for a school
    @param school: a school object
    """
    eb_min_perc = error_band_dict[constants.MIN_PERC]
    eb_max_perc = error_band_dict[constants.MAX_PERC]
    eb_rand_adj_lo = error_band_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = error_band_dict[constants.RAND_ADJ_PNT_HI]

    school_counts = school.grade_performance_level_counts

    students_in_school = []

    sections_in_school = []
    teachers_in_school = []

    for grade in school_counts:

        subject_sections_map = {}
        subject_teachers_map = {}

        for subject in constants.SUBJECTS:
            # create sections
            sections = generate_sections(constants.NUMBER_OF_SECTIONS, subject, grade, state_code, school.district_guid,
                                         school.school_guid, from_date, most_recent, to_date=to_date)
            subject_sections_map[subject] = sections

            # create teachers
            staff = generate_teachers_for_sections(constants.STAFF_PER_SECTION, sections, from_date, most_recent,
                                                   to_date, school, state_code)
            subject_teachers_map[subject] = staff

        # Generate Students that have Math scores and demographics
        students = get_students_by_counts(grade, school_counts[grade], student_info_dict)

        # Get ELA assessment information
        math_assessment = util.select_assessment_from_list(assessments, grade, constants.MATH)
        math_date_taken = util.generate_date_given_assessment(math_assessment)
        math_asmt_type = math_assessment.asmt_type
        math_asmt_year = math_assessment.asmt_period_year
        ela_assessment = util.select_assessment_from_list(assessments, grade, constants.ELA)
        ela_date_taken = util.generate_date_given_assessment(ela_assessment)
        ela_asmt_type = ela_assessment.asmt_type
        ela_asmt_year = ela_assessment.asmt_period_year
        min_score = ela_assessment.asmt_score_min
        max_score = ela_assessment.asmt_score_max

        cut_points = util.get_list_of_cutpoints(ela_assessment)
        # Create list of cutpoints that includes min and max score values
        inclusive_cut_points = [min_score] + cut_points + [max_score]
        claim_cut_points = util.get_list_of_claim_cutpoints(ela_assessment)

        all_grade_demo_info = demographics_info.get_grade_demographics(demographics_id, constants.ELA, grade)
        adjusted_demographics = apply_pld_to_grade_demographics(pld_adjustment, all_grade_demo_info)
        ela_perf = {demo_name: demo_list[L_PERF_1:] for demo_name, demo_list in adjusted_demographics.items()}
        assign_scores_for_subjects(students, ela_perf, inclusive_cut_points, min_score, max_score, grade, constants.ELA,
                                   ela_assessment, eb_min_perc, eb_max_perc,
                                   eb_rand_adj_lo, eb_rand_adj_hi, claim_cut_points)

        assign_students_sections(students, subject_sections_map[constants.MATH], subject_sections_map[constants.ELA])
        set_student_institution_information(students, school, from_date, most_recent, to_date, street_names,
                                            subject_teachers_map[constants.MATH][0], subject_teachers_map[constants.ELA][0], state_code)
        set_students_asmt_info(students, [constants.ELA, constants.MATH], [ela_assessment.asmt_rec_id, math_assessment.asmt_rec_id],
                               [ela_assessment.asmt_guid, math_assessment.asmt_guid], [ela_date_taken, math_date_taken],
                               [ela_asmt_year, math_asmt_year], [ela_asmt_type, math_asmt_type])
        apply_subject_percentages(subject_percentages, students)

        students_in_school += students

        sections_in_school += [j for i in subject_sections_map.values() for j in i]
        teachers_in_school += [j for i in subject_teachers_map.values() for j in i]

    return students_in_school, teachers_in_school, sections_in_school


def generate_teachers_for_sections(staff_per_section, sections, from_date, most_recent, to_date, school, state_code):
    """
    """
    all_staff = []
    for section in sections:
        staff = generate_multiple_staff(staff_per_section, 'Teacher', from_date, most_recent,
                                        state_code=state_code, district_guid=school.district_guid,
                                        school_guid=school.school_guid, section_guid=section.section_guid,
                                        to_date=to_date)

        all_staff += staff

    return all_staff


def set_student_institution_information(students, school, from_date, most_recent, to_date, street_names, math_teacher, ela_teacher, state_code):
    """
    For each student assigned to a school. Set the relevant information
    """
    id_generator = IdGen()
    for student in students:
        city_name_1 = random.choice(street_names)
        city_name_2 = random.choice(street_names)

        student.student_rec_ids = {constants.MATH: id_generator.get_id(), constants.ELA: id_generator.get_id()}
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
        student.teachers = {constants.MATH: math_teacher, constants.ELA: ela_teacher}

    return students


def assign_students_sections(students, math_sections, ela_sections):
    """
    For a list of students and sections. Assign each student a section for math and ela
    """
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


def set_students_asmt_info(students, subjects, asmt_rec_ids, asmt_guids, dates_taken, years, types):
    """
    take a list of students and assign them assessment record ids.
    subjects and asmt_rec_ids are lists that should match
    """
    for student in students:
        for i in range(len(subjects)):
            student.asmt_rec_ids[subjects[i]] = asmt_rec_ids[i]
            student.asmt_guids[subjects[i]] = asmt_guids[i]
            student.asmt_dates_taken[subjects[i]] = dates_taken[i]
            student.asmt_years[subjects[i]] = years[i]
            student.asmt_types[subjects[i]] = types[i]
            student.asmt_subjects[subjects[i]] = subjects[i]
    return students


def apply_subject_percentages(subject_percentages, students):
    """
    based on the percentages for each student taking an assessment, remove a subject
    record for that percentage of students
    """
    # For each subject, calculate the number of students that should not have
    # this assessment record
    for subject in subject_percentages:
        percentage = subject_percentages[subject]

        student_size = len(students)
        students_with_out_subject = student_size - int(percentage * student_size)

        # sample the correct students and remove their assessment score
        for student in random.sample(students, students_with_out_subject):
            del student.asmt_scores[subject]
    return students


def get_students_by_counts(grade, grade_counts, student_info_dict):
    """
    @param grade_counts: A five element list that contains the performance level counts for a grade
    [total, pl1, pl2, pl3, pl4]
    """
    students = []
    short_sum = 0
    total = grade_counts[0]

    for pl in range(len(grade_counts)):
        if pl == 0:
            continue
        pl_count = grade_counts[pl]
        for i in range(pl_count):
            if len(student_info_dict[grade][pl]) <= 0:
                short_sum += pl_count - i
                break
            index = random.randint(0, len(student_info_dict[grade][pl]) - 1)
            students.append(student_info_dict[grade][pl].pop(index))

    #if short_sum:
        #print('short_sum\t', short_sum, '\tout of', total, '\tgrade', grade)
    return students


def create_schools(district, school_names_1, school_names_2, student_info_dict, subject_percentages,
                   demographics_info, demographics_id, assessments, error_band_dict, state_name,
                   state_code, from_date, most_recent, to_date, street_names):
    """
    create and return a list of schools from a list of districts
    """
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
                                                from_date, most_recent, to_date, street_names, sch_pop.pld_adjustment)
        students, teachers, sections = population_data
        # students = set_student_additional_info(school, street_names, students)

        school.student_info = students
        school.teachers = teachers
        school.sections = sections
        schools.append(school)

    return schools


def create_districts(state_population, district_names_1, district_names_2, school_names_1, school_names_2, student_info_dict,
                     subject_percentages, demographics_info, demographics_id, assessments, error_band_dict, state_name,
                     state_code, from_date, most_recent, to_date, street_names):
    """
    create and return a list of districts
    """
    districts = []
    district_populations = state_population.districts

    for dist_pop in district_populations:
        district = generate_district(district_names_1, district_names_2, dist_pop)
        print('Generating %s schools' % len(district.school_populations))
        district.schools = create_schools(district, school_names_1, school_names_2, student_info_dict, subject_percentages,
                                          demographics_info, demographics_id, assessments, error_band_dict, state_name,
                                          state_code, from_date, most_recent, to_date, street_names)

        # generate district staff
        district.staff = generate_non_teaching_staff(constants.NUMBER_OF_DISTRICT_LEVEL_STAFF, from_date, most_recent, to_date,
                                                     state_code=state_code, district_guid=district.district_guid)
        districts.append(district)

    return districts


def generate_students_info_from_demographic_counts(state_population, assessments, error_band_dict):
    """
    Construct pools of students for each grade and performance level with assigned demographics
    @param state_population: A state population object that has been populated with demographic data
    @param assessments: A list of assessment objects
    @param error_band_dict: A dictionary containing the error band information
    @return: A dictionary of students with the following form {<grade>: {'PL1': [students], 'PL2': [students], ...} }
    """

    demographic_totals = state_population.state_demographic_totals

    subject = state_population.subject
    eb_min_perc = error_band_dict[constants.MIN_PERC]
    eb_max_perc = error_band_dict[constants.MAX_PERC]
    eb_rand_adj_lo = error_band_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = error_band_dict[constants.RAND_ADJ_PNT_HI]

    state_student_dict = {}

    for grade in demographic_totals:
        grade_demographic_totals = demographic_totals[grade]
        assessment = util.select_assessment_from_list(assessments, grade, subject)
        min_score = assessment.asmt_score_min
        max_score = assessment.asmt_score_max

        cut_points = util.get_list_of_cutpoints(assessment)
        claim_cut_points = util.get_list_of_claim_cutpoints(assessment)
        # Create list of cutpoints that includes min and max score values
        inclusive_cut_points = [min_score]
        inclusive_cut_points.extend(cut_points)
        inclusive_cut_points.append(max_score)

        overall_counts = grade_demographic_totals[ALL_DEM]
        total_students = math.ceil(overall_counts[L_TOTAL])
        # Generate 5% more than the actual count
        perf_lvl_surplus = .05
        perf_lvl_counts = []
        for i in range(L_PERF_1, L_PERF_4 + 1):
            count = math.ceil(overall_counts[i])
            surplus = int(perf_lvl_surplus * count)
            count += surplus
            perf_lvl_counts.append(count)
        #perf_lvl_counts = [math.ceil(overall_counts[i]) for i in range(L_PERF_1, L_PERF_4 + 1)]

        raw_scores = generate_overall_scores(perf_lvl_counts, inclusive_cut_points, min_score, max_score, total_students, False)
        asmt_scores = claim_score_calculation.translate_scores_to_assessment_score(raw_scores, cut_points, assessment, eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi, claim_cut_points)

        score_pool_dict = create_asmt_score_pool_dict(asmt_scores)
        student_info_dict = generate_students_with_demographics(score_pool_dict, grade_demographic_totals, grade)

        state_student_dict[grade] = student_info_dict
    return state_student_dict


def generate_students_with_demographics(score_pool, demographic_totals, grade):
    """
    Given a set of scores and the demographic numbers. Create studentInfo objects that match
    the given values
    @param score_pool: A dict of scores by performance levels
    @param demographic_totals: A dictionary of numbers for each performance level by demographic
    """

    gender_group = 1
    groupings = sorted({count_list[L_GROUPING] for count_list in demographic_totals.values() if count_list[L_GROUPING] not in [OVERALL_GROUP, gender_group]})  # TODO: Could pull out and define list as a constant elsewhere

    # Create new student info objects with a gender assigned and scores
    student_info_dict = create_student_info_dict(gender_group, score_pool, demographic_totals, grade)
    print('Generating Student in Grade:', grade)
    for group in groupings:
        assign_demographics_for_grouping(group, student_info_dict, demographic_totals)

    return student_info_dict


def create_student_info_dict(group_num, score_pool, demographic_totals, grade):
    """
    Create a dictionary of student info objects
    """
    student_info_dict = {perf_lvl: [] for perf_lvl in score_pool}
    ordered_names = sorted(demographic_totals, key=lambda k: demographic_totals[k][L_TOTAL])

    # loop through possible genders and create the appropriate number of students for each Performance Level
    for demo_name in ordered_names:
        demo_list = demographic_totals[demo_name]
        if demo_list[L_GROUPING] != group_num:
            continue
        for i in range(L_PERF_1, L_PERF_4 + 1):
            perf_lvl_count = math.ceil(demo_list[i])
            perf_lvl = i - 1
            generated_student_info = create_student_infos_by_gender(demo_name, perf_lvl_count, perf_lvl,
                                                                    score_pool, grade)
            student_info_dict[perf_lvl] += generated_student_info

    return student_info_dict


def create_student_infos_by_gender(gender, count, performance_level, score_pool, grade):
    """
    Create a list of students all with the same gender and assign them scores
    """
    student_info_list = []
    score_list = score_pool[performance_level]
    for _i in range(count):
        if len(score_list) <= 0:
            #print('short by: ', count - _i, '\tperf_lvl was:', performance_level, '\tgrade:', grade, '\tdemographic_name:', gender)
            break
        index = random.randint(0, len(score_list) - 1)
        score = score_list.pop(index)
        asmt_score_dict = {'Math': score}
        student_info = StudentInfo(grade, gender, asmt_score_dict)
        student_info_list.append(student_info)

    return student_info_list


def assign_demographics_for_grouping(group_num, student_info_pool, demographic_totals):
    """
    Assign students demographics based on the totals passed in
    """
    # Copy student_info pools lists
    student_info_dict = {perf_lvl: student_info_pool[perf_lvl][:] for perf_lvl in student_info_pool}

    # sort names by the number to be generated
    ordered_demo_names = sorted(demographic_totals, key=lambda k: demographic_totals[k][L_TOTAL])

    for demo_name in ordered_demo_names:
        demo_list = demographic_totals[demo_name]
        if demo_list[L_GROUPING] != group_num:
            continue
        for i in range(L_PERF_1, L_PERF_4 + 1):
            perf_lvl_count = math.ceil(demo_list[i])
            perf_lvl = i - 1
            assign_demographic_to_students(demo_name, student_info_dict, perf_lvl_count, perf_lvl)


def assign_demographic_to_students(demographic_name, student_pool, count, performance_level):
    """
    Assign a number of students that are in the given performance level the given demographic
    """
    student_list = student_pool[performance_level]
    for _i in range(count):
        if len(student_list) <= 0:
            #print('short by:', count - _i, '\tperf_lvl was:', performance_level, '\tdemographic_name:', demographic_name)
            break
        index = random.randint(0, len(student_list) - 1)
        student_info = student_list.pop(index)
        setattr(student_info, demographic_name, True)
    # set 'dmg_eth_2rm' to StudentInfo
    for student_info in student_list:
        student_info.set_dmg_eth_2mr()


def create_asmt_score_pool_dict(assessment_scores):
    """
    Given a list of assessment score objects, split them into pools based on performance level
    @param assessment_scores: A list of assessmentScore objects
    @return: A dictionary with Performance Level numbers as keys. Where the values are a list of assessmentScores
    """

    score_pl_dict = {}

    for asmt_score in assessment_scores:
        perf_lvl = asmt_score.perf_lvl
        score_pl_dict[perf_lvl] = score_pl_dict.get(perf_lvl, []) + [asmt_score]

    return score_pl_dict


def get_flat_grades_list(school_config, grade_key):
    """
    pull out grades from score_config and place in flat list
    @param school_config: A dictionary of school info
    @return: list of grades
    """
    grades = []

    for school_type in school_config:
        grades.extend(school_config[school_type][grade_key])

    # remove duplicates
    grades = list(set(grades))

    return grades


def generate_non_teaching_staff(number_of_staff, from_date, most_recent, to_date, state_code='NA', district_guid='NA', school_guid='NA'):
    """
    Generate staff that are not teachers
    @param number_of_staff: The number of staff memebers to generate
    @keyword state_code: The state code to use for the staff memeber. If applicable.
    @keyword district_guid: The guid to the district the staff member is in. If applicable.
    @keyword school_guid: The guid to the school the staff member is in. If applicable.
    @return: a list of Staff objects
    """
    hier_user_type = 'Staff'
    staff_list = generate_multiple_staff(number_of_staff, hier_user_type, from_date, most_recent, state_code=state_code,
                                         district_guid=district_guid, school_guid=school_guid, to_date=to_date)
    return staff_list


def generate_institution_hierarchy_from_helper_entities(state_population, district, school, from_date, most_recent, to_date):
    """
    Create an InstitutionHierarchy object from the helper entities provided
    @param state_population: a State population
    @param district: A District object
    @param school: A School object
    """
    state_name = state_population.state_name
    state_code = state_population.state_code
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
    """
    create a dictionary that specifies the output path for all csv files
    @param output_path: the path to where to store the files
    @type output_path: str
    @return: A dict containing all ouput paths
    @rtype: dict
    """
    out_dict = {}

    for fname in CSV_FILE_NAMES:
        out_dict[fname] = os.path.join(output_path, CSV_FILE_NAMES[fname])

    return out_dict


def calculate_dist_chunk(state_population):
    """
    using the state population object and the number of students present, determine how large a chunk should be.
    """
    avg_district_size = state_population.total_students_in_state / len(state_population.districts)
    district_chunk = IDEAL_DISTRICT_CHUNK / avg_district_size
    return max(1, int(district_chunk))


def generate_name_list_dictionary(list_name_to_path_dictionary):
    """
    Create a dictionary that contains naming lists as keys and a list of file
    lines as values
    @param list_name_to_path: a dictionary mapping names to file paths
    @return:  a dictionary mapping name to file paths
    """
    name_list_dictionary = {}
    for list_name in list_name_to_path_dictionary:
        path = list_name_to_path_dictionary[list_name]
        name_list = util.create_list_from_file(path)
        name_list_dictionary[list_name] = name_list
    return name_list_dictionary


def read_datagen_output_format_yaml(output_format_config_file):
    """
    Reads the yaml file and returns the config as python dict
    @param config_file_path: path to the yaml config file
    """
    print(output_format_config_file)
    output_format = yaml.load(open(output_format_config_file))
    return output_format


def main(output_format_config_file, config_mod_name='dg_types', output_path=DEFAULT_OUTPUT_DIR, do_pld_adjustment=True, district_chunk_size=0):
    t1 = datetime.datetime.now()
    config_module = import_module(config_mod_name)

    output_format_dict = read_datagen_output_format_yaml(output_format_config_file)
    yaml_output_dict = initialize_csv_file(output_format_dict, output_path)

    # generate_data
    generate_data_from_config_file(config_module, yaml_output_dict, output_format_dict, do_pld_adjustment, district_chunk_size)

    # print time
    t2 = datetime.datetime.now()
    print()
    print("data_generation starts\t\t", t1)
    print("data_generation ends\t\t", t2)
    print('data_generation total time\t', t2 - t1)
    print()

    return output_path


if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate fixture data from a configuration file.')
    parser.add_argument('--config', dest='config_module', action='store', default='configs.dg_types',
                        help='Specify the configuration module that informs that data creation process.',
                        required=False)
    parser.add_argument('--format', dest='output_format', action='store',
                        default=os.path.join(DATAFILE_PATH, 'src', 'configs', 'datagen_output_format_default.yaml'),
                        help='Specify the DataGen output format needed.',
                        required=False)
    parser.add_argument('--output', dest='output_path', action='store',
                        default=DEFAULT_OUTPUT_DIR,
                        help='Specify the location of the output csv files. Default: "datafiles/csv/"')
    parser.add_argument('-d', '--district-chunk-size', type=int, default=0,
                        help='The number of district to generate and output at a time. If this value is'
                             ' less than 1 this will be calculated at run time. Default: 0')
    parser.add_argument('-N', '--no-pld-adjustment', dest='do_pld_adjustment', action='store_false',
                        help='Specify this flag to generate data without applying the performance level adjustments')
    args = parser.parse_args()

    main(args.output_format, args.config_module, args.output_path, args.do_pld_adjustment, args.district_chunk_size)
