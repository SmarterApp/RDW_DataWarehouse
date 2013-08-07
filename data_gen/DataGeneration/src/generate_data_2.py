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
from demographics import Demographics, DemographicStatus, ALL_DEM, L_GROUPING, L_TOTAL, L_PERF_1, L_PERF_4, OVERALL_GROUP
from generate_entities import generate_assessments
from write_to_csv import create_csv
from state_population import StatePopulation
import constants
from generate_scores import generate_overall_scores
from entities import (InstitutionHierarchy, Section, Assessment, AssessmentOutcome,
                      Staff, ExternalUserStudent, Student)
from errorband import calc_eb_params, calc_eb
from generate_helper_entities import generate_claim_score, generate_assessment_score, generate_district, generate_school
from helper_entities import StudentInfo
from print_state_population import print_state_population
import util
from assign_students_subjects_scores import assign_scores_for_subjects


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

    @param config_module: module that contains all configuration information for the data creation process
    @return nothing
    '''

    # Setup demographics object
    demographics_info = Demographics(config_module.get_demograph_file())

    # Next, prepare lists that are used to name various entities
    name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)

    # We're going to use the birds and fish list to name our districts
    district_names_1 = name_list_dictionary[ANIMALS]
    district_names_2 = name_list_dictionary[ANIMALS]

    # We're going to use mammals and birds to names our schools
    school_names_1 = name_list_dictionary[ANIMALS]
    school_names_2 = name_list_dictionary[ANIMALS]

    # First thing: prep the csv files by deleting their contents and adding appropriate headers
    prepare_csv_files(output_dict)

    # Get information from the config module
    school_types = config_module.get_school_types()
    district_types = config_module.get_district_types()
    state_types = config_module.get_state_types()
    states = config_module.get_states()
    scores_details = config_module.get_scores()

    # generate one batch_guid for all records
    batch_guid = uuid4()

    # Get temporal information
    temporal_information = config_module.get_temporal_information()
    from_date = temporal_information[constants.FROM_DATE]
    most_recent = temporal_information[constants.MOST_RECENT]
    to_date = temporal_information[constants.TO_DATE]

    # Generate Assessment CSV File
    flat_grades_list = get_flat_grades_list(school_types, constants.GRADES)
    assessments = generate_assessments(flat_grades_list, scores_details[constants.CUT_POINTS],
                                       from_date, most_recent, to_date=to_date)
    create_csv(assessments, output_dict[Assessment])

    # Get Error Band Information from config_module
    error_band_dict = config_module.get_error_band()

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
        print_state_population(state_population)

        student_info_dict = generate_students_from_demographic_counts(state_population, assessments, error_band_dict)

        districts = create_districts(state_population, district_names_1, district_names_2)
        schools = create_schools(districts, school_names_1, school_names_2)

        populate_schools(schools, student_info_dict, subject_percentages, demographics_info, demographics_id, assessments, error_band_dict, state_name, state_code)


def populate_schools(school_list, student_info_dict, subject_percentages, demographics_info, demographics_id, assessments, error_band_dict, state_name, state_code):
    '''
    '''
    eb_min_perc = error_band_dict[constants.MIN_PERC]
    eb_max_perc = error_band_dict[constants.MAX_PERC]
    eb_rand_adj_lo = error_band_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = error_band_dict[constants.RAND_ADJ_PNT_HI]

    print('school_list', len(school_list))
    for school in school_list:
        school_counts = school.grade_performance_level_counts
        students_in_school = []
        # TODO:
        # create_institution_hierarchies

        for grade in school_counts:

            # TODO:
            # create subject sections
            # create teachers

            # Generate Students that have Math scores and demographics
            students = get_students_by_counts(grade, school_counts[grade], student_info_dict)

            # Get ELA assessment information
            ela_subject = 'ELA'
            assessment = select_assessment_from_list(assessments, grade, ela_subject)
            min_score = assessment.asmt_score_min
            max_score = assessment.asmt_score_max

            cut_points = get_list_of_cutpoints(assessment)
            # Create list of cutpoints that includes min and max score values
            inclusive_cut_points = [min_score]
            inclusive_cut_points.extend(cut_points)
            inclusive_cut_points.append(max_score)

            all_grade_demo_info = demographics_info.get_grade_demographics(demographics_id, ela_subject, grade)
            ela_perf = {demo_name: demo_list[L_PERF_1:] for demo_name, demo_list in all_grade_demo_info.items()}
            assign_scores_for_subjects(students, ela_perf, inclusive_cut_points, min_score, max_score, grade, ela_subject,
                                       assessment, eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi)

            apply_subject_percentages(subject_percentages, students)
            students_in_school += students
            # TODO:
            # place students in sections
            # create assessment records
            # create student records

        #write_dim_student_and_fact_asmt(students_in_school, school, state_name, state_code)


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


def write_dim_student_and_fact_asmt(students, school, state_name, state_code):
    print('writing files')


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


def create_schools(districts, school_names_1, school_names_2):
    '''
    create and return a list of schools
    '''
    schools = []

    for district in districts:
        for sch_pop in district.school_populations:
            grade_perf_lvl_counts = {}
            # Loop through grades counts and get the overall counts
            for grade, demo_dict in sch_pop.school_demographics.items():
                grade_counts = demo_dict[ALL_DEM][L_TOTAL:]
                grade_perf_lvl_counts[grade] = [round(x) for x in grade_counts]

            school = generate_school(sch_pop.school_type_name, school_names_1, school_names_2,
                                     grade_perf_lvl_counts, district.district_name, district.district_guid)
            schools.append(school)

    return schools


def create_districts(state_population, district_names_1, district_names_2):
    '''
    create and return a list of districts
    '''
    districts = []
    district_populations = state_population.districts

    for dist_pop in district_populations:
        district = generate_district(district_names_1, district_names_2, dist_pop)
        districts.append(district)

    return districts


def generate_students_from_demographic_counts(state_population, assessments, error_band_dict):
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
