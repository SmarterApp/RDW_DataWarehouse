import argparse
import datetime
import os
import csv
import random
import DataGeneration.src.utils.util as util
import DataGeneration.src.calc.stats as stats
import DataGeneration.src.constants.constants as constants
from collections import Counter
from DataGeneration.src.utils.idgen import IdGen
from DataGeneration.src.writers.write_to_csv import create_csv
from importlib import import_module
from DataGeneration.src.generators.generate_entities import (generate_institution_hierarchy, generate_sections, generate_students, generate_multiple_staff,
                                                  generate_fact_assessment_outcomes, generate_assessments)
from DataGeneration.src.generators.generate_helper_entities import generate_state, generate_district, generate_school, generate_assessment_score, generate_claim_score
from DataGeneration.src.models.entities import InstitutionHierarchy, Section, Assessment, AssessmentOutcome, \
    Staff, ExternalUserStudent, Student
from DataGeneration.src.generators.generate_scores import generate_overall_scores
from DataGeneration.src.calc.gaussian_distributions import gauss_one, guess_std
from DataGeneration.src.calc.errorband import calc_eb_params, calc_eb
from DataGeneration.src.calc.adjust import adjust_pld
#from DataGeneration.src.demographics import Demographics, DemographicStatus
from demographics import Demographics, DemographicStatus
from uuid import uuid4


DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
components = DATAFILE_PATH.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])


CSV_FILE_NAMES = {InstitutionHierarchy: 'dim_inst_hier.csv',
                  Section: 'dim_section.csv',
                  Assessment: 'dim_asmt.csv',
                  AssessmentOutcome: 'fact_asmt_outcome.csv',
                  Staff: 'dim_staff.csv',
                  ExternalUserStudent: 'external_user_student_rel.csv',
                  Student: 'dim_student.csv'}

ENTITY_TO_PATH_DICT = {InstitutionHierarchy: DATAFILE_PATH + '/datafiles/csv/dim_inst_hier.csv',
                       Section: DATAFILE_PATH + '/datafiles/csv/dim_section.csv',
                       Assessment: DATAFILE_PATH + '/datafiles/csv/dim_asmt.csv',
                       AssessmentOutcome: DATAFILE_PATH + '/datafiles/csv/fact_asmt_outcome.csv',
                       Staff: DATAFILE_PATH + '/datafiles/csv/dim_staff.csv',
                       ExternalUserStudent: DATAFILE_PATH + '/datafiles/csv/external_user_student_rel.csv',
                       Student: DATAFILE_PATH + '/datafiles/csv/dim_student.csv'}

LAST_NAMES = 'last_names'
FEMALE_FIRST_NAMES = 'female_first_names'
MALE_FIRST_NAMES = 'male_first_names'
BIRDS = 'birds'
FISH = 'fish'
MAMMALS = 'mammals'
ANIMALS = 'animals'

NAMES_TO_PATH_DICT = {BIRDS: DATAFILE_PATH + '/datafiles/name_lists/birds.txt',
                      FISH: DATAFILE_PATH + '/datafiles/name_lists/fish.txt',
                      MAMMALS: DATAFILE_PATH + '/datafiles/name_lists/mammals.txt',
                      ANIMALS: os.path.join(DATAFILE_PATH, 'datafiles', 'name_lists', 'one-word-animal-names.txt')
                      }
CONFIG_MODULE = ''


def generate_data_from_config_file(config_module, output_dict):
    '''
    Main function that drives the data generation process

    @param config_module: module that contains all configuration information for the data creation process
    @return nothing
    '''

    # Setup demographics object
    demographics = Demographics(config_module.get_demograph_file())

    # First thing: prep the csv files by deleting their contents and adding appropriate headers
    prepare_csv_files(output_dict)

    # Next, prepare lists that are used to name various entities
    name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)

    # We're going to use the birds and fish list to name our districts
    district_names_1 = name_list_dictionary[ANIMALS]
    district_names_2 = name_list_dictionary[ANIMALS]

    # We're going to use mammals and birds to names our schools
    school_names_1 = name_list_dictionary[ANIMALS]
    school_names_2 = name_list_dictionary[ANIMALS]

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

    # Generate Assessment CSV File
    flat_grades_list = get_flat_grades_list(school_types, constants.GRADES)
    assessments = generate_assessments(flat_grades_list, scores_details[constants.CUT_POINTS],
                                       from_date, most_recent, to_date=to_date)
    create_csv(assessments, output_dict[Assessment])

    # generate one batch_guid for all records
    batch_guid = uuid4()
    # Iterate over all the states we're supposed to create
    # When we get down to the school level, we'll be able to generate an InstitutionHierarchy object
    for state in states:
        # Pull out basic state information
        state_name = state[constants.NAME]
        state_code = state[constants.STATE_CODE]

        # Create state object from gathered info
        current_state = generate_state(state_name, state_code)

        # Pull out information on districts within this state
        state_type_name = state[constants.STATE_TYPE]
        state_type = state_types[state_type_name]
        district_types_and_counts = state_type[constants.DISTRICT_TYPES_AND_COUNTS]
        subject_percentages = state_type[constants.SUBJECT_AND_PERCENTAGES]
        demographics_id = state_type[constants.DEMOGRAPHICS]

        # TODO: should we add some randomness here? What are acceptable numbers? 5-10? 10-20?
        number_of_state_level_staff = 10
        # Create the state-level staff
        state_level_staff = generate_non_teaching_staff(config_module, number_of_state_level_staff, state_code=current_state.state_code)

        # Create all the districts for the given state.
        # We don't have a state, district, or school table, but we have an institution_hierarchy table.
        # Each row of this table contains all state, district, and school information.
        # districts_by_type is a dictionary such that:
        # key: <string> The type of district
        # value: <list> A list of district objects
        districts_by_type = generate_district_dictionary(district_types_and_counts, district_names_1, district_names_2)
        # All the InstitutionHierarchy objects for this state will be put in the following list

        # Debugging
        dist_counts = Counter()

        state_institution_hierarchies = []
        for district_type_name in districts_by_type.keys():
            districts = districts_by_type[district_type_name]
            district_type = district_types[district_type_name]

            # Debugging
            dist_counts[district_type_name] += len(districts)

            # Pull out school information for this type of district
            # Here we get info on the types of schools to create
            school_types_and_ratios = district_type[constants.SCHOOL_TYPES_AND_RATIOS]

            # Here we get info on the number of schools to create
            school_counts = district_type[constants.SCHOOL_COUNTS]

            for district in districts:
                print('populating district: %s: %s' % (district.district_name, district_type_name))
                # TODO: should we add some randomness here? What are acceptable numbers? 5-10? 10-20?
                number_of_district_level_staff = 10
                district_level_staff = generate_non_teaching_staff(config_module, number_of_district_level_staff, state_code=current_state.state_code,
                                                                   district_guid=district.district_guid)

                schools_by_type = create_school_dictionary(config_module, school_counts, school_types_and_ratios, school_types,
                                                           school_names_1, school_names_2)

                # Debugging
                school_counts = Counter()

                for school_type_name in schools_by_type.keys():
                    schools = schools_by_type[school_type_name]
                    school_type = school_types[school_type_name]
                    school_type_institution_hierarchies = generate_and_populate_institution_hierarchies(schools, school_type, current_state,
                                                                                                        district, assessments, subject_percentages, demographics, demographics_id, batch_guid, config_module, output_dict)
                    # Debugging
                    school_counts[school_type_name] += len(school_type_institution_hierarchies)

                    state_institution_hierarchies += school_type_institution_hierarchies

                # Write district staff to file
                create_csv(district_level_staff, ENTITY_TO_PATH_DICT[Staff])

        # Calculate total students for each grade
        student_tots_dict = get_student_totals(state_institution_hierarchies)
        print(student_tots_dict)
        student_pool_dict = generate_student_pool(student_tots_dict, assessments, demographics, demographics_id, config_module)

        # Write staff and institutions to file
        create_csv(state_level_staff, ENTITY_TO_PATH_DICT[Staff])
        create_csv(state_institution_hierarchies, ENTITY_TO_PATH_DICT[InstitutionHierarchy])


def generate_and_populate_institution_hierarchies(schools, school_type, state, district, assessments, subject_percentages, demographics, demographics_id, batch_guid, config_module, output_dict):
    '''
    Given institution information (info about state, district, school), we create InstitutionHierarchy objects.
    We create one InstitutionHierarchy object for each school given in the school list.

    In addition to this, we populate each institution hierarchy (which is functionally equivalent to a school) with
    students, teachers, staff, sections

    @type schools: list
    @param schools: list of schools that will be used to create InstitutionHierarchy objects
    @type school_type: dict
    @param school_type: dictionary that contains the grades and the number of students per grade for this school type
    @type state: State
    @param state: state object that contains state code, state name
    @type district: District
    @param district: district object that contains district information
    @type assessments: list
    @param assessments: A list of Assessment objects for generating assessment outcome objects
    '''
    institution_hierarchies = []
    for school in schools:
        institution_hierarchy = generate_institution_hierarchy_from_helper_entities(config_module, state, district, school)
        institution_hierarchies.append(institution_hierarchy)

        get_student_counts(institution_hierarchy, school_type, subject_percentages, config_module)
        # TODO: Don't populate the schools here. When this function returns, loop over the list and populate each school
        #populate_school(institution_hierarchy, school_type, assessments, subject_percentages, demographics, demographics_id, batch_guid)
    return institution_hierarchies


def get_student_counts(institution_hierarchy, school_type, subject_percentages, config_module):
    '''
    '''
    # Get student count information from config module
    student_counts = school_type[constants.STUDENTS]
    student_min = student_counts[constants.MIN]
    student_max = student_counts[constants.MAX]
    student_avg = student_counts[constants.AVG]

    stud_counts = {}
    grades = school_type[constants.GRADES]
    for grade in grades:
        number_of_students_in_grade = calculate_number_of_students(student_min, student_max, student_avg)
        stud_counts[grade] = number_of_students_in_grade

    institution_hierarchy.student_counts = stud_counts


def generate_student_pool(student_totals, assessments, demographics, demographics_id, config_module):
    '''
    '''

    all_students = []

    # Get Error Band Information from config_module
    eb_dict = config_module.get_error_band()
    eb_min_perc = eb_dict[constants.MIN_PERC]
    eb_max_perc = eb_dict[constants.MAX_PERC]
    eb_rand_adj_lo = eb_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = eb_dict[constants.RAND_ADJ_PNT_HI]

    scores_details = config_module.get_scores()

    # get name list dict for street name generation
    name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)

    # will ignore performance level adjustments for now, This may cause problems.
    # may need to factor all pld adjustments into the total pld somehow.

    for grade in student_totals:
        students_to_gen = student_totals[grade]
        students_in_grade = []
        demo_status = DemographicStatus(demographics.get_demo_names(demographics_id))

        for subject_name in constants.SUBJECTS:
            print()
            print('generating grade: %s, subject: %s' % (grade, subject_name))
            # Pull out the proper performance level percentages
            performance_level_percs = demographics.get_grade_demographics_total(demographics_id, subject_name, grade)

            print(performance_level_percs)
            # Generate Scores
            scores = generate_list_of_scores(config_module, students_to_gen, scores_details, performance_level_percs, subject_name, grade)

            # Pull out the correct assessment from the list
            assessment = select_assessment_from_list(assessments, grade, subject_name)

            # The cut_points in score details do not include min and max score. The score generator needs the min and max to be included
            cut_points = [assessment.asmt_cut_point_1, assessment.asmt_cut_point_2, assessment.asmt_cut_point_3]
            if assessment.asmt_cut_point_4:
                cut_points.append(assessment.asmt_cut_point_4)

            asmt_scores = translate_scores_to_assessment_score(scores, cut_points, assessment, eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi)

            # if assessments have not already been assigned for one grade
            if not students_in_grade:
                unassigned_studs = demographics.generate_students_and_demographics(students_to_gen, subject_name, grade, asmt_scores,
                                                                                   demographics_id, demo_status, name_list_dictionary[BIRDS])
                print(len(unassigned_studs))
                students_in_grade += unassigned_studs
            else:
                demographics.assign_scores_by_demographics(unassigned_studs, subject_name, grade, asmt_scores,
                                                           demographics_id, demo_status)

        y = [x for x in unassigned_studs if len(x.asmt_scores) != 2]
        print('y', y)

        # Add students in grade to overall student list
        all_students += students_in_grade

    exit('exit1')
    return all_students


def populate_school(institution_hierarchy, school_type, assessments, subject_percentages, demographics, demographics_id, batch_guid, config_module, output_dict):

    '''
    Populate the provided the institution with staff, students, teachers, sections

    @type institution_hierarchy: InstitutionHierarchy
    @param institution_hierarchy: InstitutionHierarchy object that contains basic information about school, district, state
    @type school_type: dict
    @param school_type: dictionary containing the grades and number of students per grade
    @type assessments: list of Assessments
    @param assessments: a list of assessment objects for creation of AssessmentOutcomes
    '''

    # Get student count information from config module
    student_counts = school_type[constants.STUDENTS]
    student_min = student_counts[constants.MIN]
    student_max = student_counts[constants.MAX]
    student_avg = student_counts[constants.AVG]

    # Get Error Band Information from config_module
    eb_dict = config_module.get_error_band()
    eb_min_perc = eb_dict[constants.MIN_PERC]
    eb_max_perc = eb_dict[constants.MAX_PERC]
    eb_rand_adj_lo = eb_dict[constants.RAND_ADJ_PNT_LO]
    eb_rand_adj_hi = eb_dict[constants.RAND_ADJ_PNT_HI]

    # Get scoring information from config module
    performance_level_dist = config_module.get_performance_level_distributions()
    scores_details = config_module.get_scores()
    pld_adjustment = school_type.get(constants.ADJUST_PLD, None)

    grades = school_type[constants.GRADES]

    students_in_school = []
    sections_in_school = []
    staff_in_school = []
    # TODO: should we add some randomness here? What are acceptable numbers? 5-10? 10-20?
    number_of_school_level_staff = 5
    school_level_staff = generate_non_teaching_staff(config_module, number_of_school_level_staff, state_code=institution_hierarchy.state_code,
                                                     district_guid=institution_hierarchy.district_guid, school_guid=institution_hierarchy.school_guid)
    staff_in_school += school_level_staff
    for grade in grades:
        asmt_outcomes_for_grade = []
        number_of_students_in_grade = calculate_number_of_students(student_min, student_max, student_avg)
        name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)
        students_in_grade = generate_students_from_institution_hierarchy(config_module, number_of_students_in_grade, institution_hierarchy, grade, -1, name_list_dictionary[BIRDS])

        demograph_id = demographics_id  # TODO: Get from config file
        subject_num = 1
        demo_status = DemographicStatus(demographics.get_demo_names(demograph_id))

        for subject_name in constants.SUBJECTS:
            number_of_sections = calculate_number_of_sections(number_of_students_in_grade)
            # TODO: figure out a way around this hack.
            temporal_information = config_module.get_temporal_information()
            from_date = temporal_information[constants.FROM_DATE]
            most_recent = temporal_information[constants.MOST_RECENT]
            to_date = temporal_information[constants.TO_DATE]
            sections_in_grade = generate_sections(number_of_sections, subject_name, grade, institution_hierarchy.state_code,
                                                  institution_hierarchy.district_guid, institution_hierarchy.school_guid,
                                                  from_date, most_recent, to_date=to_date)
            sections_in_school += sections_in_grade
            performance_level_percs = demographics.get_grade_demographics_total(demograph_id, subject_name, grade)
            score_list = generate_list_of_scores(config_module, number_of_students_in_grade, scores_details, performance_level_percs, subject_name, grade, pld_adjustment)
            students_in_subject = students_in_grade[:]
            for section in sections_in_grade:
                # TODO: More accurate math for num_of_students
                # TODO: Do we need to account for the percentages of kids that take ELA or MATH here?
                number_of_students_in_section = number_of_students_in_grade // number_of_sections
                # TODO: Set up district naming like PeopleNames to remove the following line (which is also called in generate_data)
                # name_list_dictionary = generate_name_list_dictionary(NAMES_TO_PATH_DICT)
                # students_in_section = generate_students_from_institution_hierarchy(config_module, number_of_students_in_section, institution_hierarchy, grade, section.section_guid, name_list_dictionary[BIRDS])
                students_in_section = students_in_subject[:number_of_students_in_section]
                students_in_subject[:number_of_students_in_section] = []
                set_students_rec_id_and_section_id(students_in_section, section.section_guid)
                students_in_school += students_in_section
                # TODO: should we add some randomness here? What are acceptable numbers? 1-2? 1-3?
                number_of_staff_in_section = 1
                teachers_in_section = generate_teaching_staff_from_institution_hierarchy(config_module, number_of_staff_in_section, institution_hierarchy, section.section_guid)
                staff_in_school += teachers_in_section
                assessment = select_assessment_from_list(assessments, grade, subject_name)
                teacher_guid = teachers_in_section[0].staff_guid

                percent_to_take_assessment = subject_percentages[subject_name]
                students_to_take_assessment = get_subset_of_students(students_in_section, percent_to_take_assessment)

                # if this is the first subject for this group of students
                # assign demographics based on their scores
                if subject_num == 1:
                    asmt_outcomes_in_section = generate_assessment_outcomes_from_helper_entities_and_lists(students_to_take_assessment, score_list, teacher_guid, section, institution_hierarchy, assessment,
                                                                                                           eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi, batch_guid)
                    # TODO: Remove hard coded demographic type
                    (updated_outcomes, updated_students) = demographics.assign_demographics(asmt_outcomes_in_section, students_to_take_assessment, subject_name, grade, demograph_id, demo_status)
                    subject_num += 1

                # else assign grades based on their demographics
                elif subject_num == 2:
                    (updated_students, new_scores) = demographics.assign_scores_from_demograph(students_to_take_assessment, score_list, subject_name, grade, demograph_id, demo_status, assessment)
                    asmt_outcomes_in_section = generate_assessment_outcomes_from_helper_entities_and_lists(updated_students, new_scores, teacher_guid, section, institution_hierarchy, assessment,
                                                                                                           eb_min_perc, eb_max_perc, eb_rand_adj_lo, eb_rand_adj_hi, batch_guid)
                    demographics.update_demographics(updated_students, asmt_outcomes_in_section, demograph_id)
                    subject_num += 1

                # write student objects to dim_student csv
                create_csv(students_to_take_assessment, output_dict[Student])
                asmt_outcomes_for_grade.extend(asmt_outcomes_in_section)

        # write asmt_outcomes to fact_asmt_outcome
        create_csv(asmt_outcomes_for_grade, output_dict[AssessmentOutcome])
    # create_csv(students_in_school, output_dict[Student])
    create_csv(sections_in_school, output_dict[Section])
    create_csv(staff_in_school, output_dict[Staff])


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


def generate_district_dictionary(district_types_and_counts, district_names_1, district_names_2):
    '''
    generate a dict of districts from the given info
    @param district_types_and_counts: A dictionary containing the data about district sizes from the config file
    @param district_names_1: A list of names to use when naming the districts
    @param district_names_2: Second list to use in naming
    @return: a dictionary of created districts
    '''
    district_dictionary = {}
    for district_type in district_types_and_counts:
        district_count = district_types_and_counts[district_type]
        district_list = []
        for i in range(district_count):
            district = generate_district(district_names_1, district_names_2)
            district_list.append(district)
        district_dictionary[district_type] = district_list
    return district_dictionary


def create_school_dictionary(config_module, school_counts, school_types_and_ratios, school_types_dict, school_names_1, school_names_2):
    '''
    Creates a dictionary of schools that matches the school counts and ratios
    @param school_counts: A dictionary containing school population information
    @param school_types_and_ratios: A dictionary containing ratios for schools in each school-size type
    @param school_types_dict: A dictionary taken from the config file that contains type info about school categories
    @param school_names_1: A list of names to use in naming schools
    @param school_names_2: A 2nd list of names to use in naming schools
    @return: A dictionary with school types as keys and a list of schools as values
    '''
    num_schools_min = school_counts[constants.MIN]
    num_schools_avg = school_counts[constants.AVG]
    num_schools_max = school_counts[constants.MAX]
    # TODO: Can we assume number of schools is a normal distribution?
    number_of_schools_in_district = calculate_number_of_schools(num_schools_min, num_schools_max, num_schools_avg)

    ratio_sum = sum(school_types_and_ratios.values())
    ratio_unit = (number_of_schools_in_district / ratio_sum)  # max((number_of_schools_in_district // ratio_sum), 1)

    school_dictionary = {}
    for school_type in school_types_and_ratios:
        # Get the ratio so we can calculate the number of school types to create for each district
        school_type_ratio = school_types_and_ratios[school_type]
        number_of_schools_for_type = int(max(round(school_type_ratio * ratio_unit), 1))  # int(school_type_ratio * ratio_unit)

        school_list = []
        school_type_name = school_types_dict[school_type][constants.TYPE]
        for _i in range(number_of_schools_for_type):
            school = generate_school(school_type_name, school_names_1, school_names_2)
            school_list.append(school)
        school_dictionary[school_type] = school_list
    return school_dictionary


def generate_institution_hierarchy_from_helper_entities(config_module, state, district, school):
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
    temporal_information = config_module.get_temporal_information()
    from_date = temporal_information[constants.FROM_DATE]
    most_recent = temporal_information[constants.MOST_RECENT]
    to_date = temporal_information[constants.TO_DATE]

    institution_hierarchy = generate_institution_hierarchy(state_name, state_code,
                                                           district_guid, district_name,
                                                           school_guid, school_name, school_category,
                                                           from_date, most_recent, to_date)
    return institution_hierarchy


def generate_list_of_scores(config_module, total, score_details, perf_lvl_dist, subject_name, grade, pld_adjustment=None):
    '''
    Generate a list of overall scores to use in the creation of assessment outcomes
    @type total: int
    @param total: the number of assessment scores to generate
    @type score_details: dict
    @param score_details: score information taken from the configuration file
    @type perf_lvl_dist: dict
    @param perf_lvl_dist: The dictionary of performance level information taken from the config module
    @type subject_name: str
    @param subject_name: the name of the subject that scores are being generated for
    @type grade: int
    @param grade: the grade that the scores are being generated for
    @type pld_adjustment: float
    @param pld_adjustment: The amount to adjust the performance level distribution. Taken from config file
    @return: A list of scores as ints
    '''
    min_score = score_details[constants.MIN]
    max_score = score_details[constants.MAX]
    percentage = perf_lvl_dist  # [subject_name][str(grade)][constants.PERCENTAGES]
    if pld_adjustment:
        percentage = adjust_pld(percentage, pld_adjustment)

    # The cut_points in score details do not include min and max score. The score generator needs the min and max to be included
    cut_points = score_details[constants.CUT_POINTS]
    inclusive_cut_points = [min_score]
    inclusive_cut_points.extend(cut_points)
    inclusive_cut_points.append(max_score)

    scores = generate_overall_scores(percentage, inclusive_cut_points, min_score, max_score, total)
    return scores


def generate_assessment_outcomes_from_helper_entities_and_lists(students, scores, teacher_guid, section, institution_hierarchy, assessment, ebmin, ebmax, rndlo, rndhi, batch_guid):
    '''
    Generate assessment outcomes for a list of students
    @param students: List of the students to generate outcomes for
    @param scores: List of scores to use in assignment
    @param teacher_guid: The guid of the teacher
    @param section: The section object that the student is in
    @param institution_hierarchy: the institution_hierarchy object that the student is in
    @param assessment: The assessment object that the outcome will be for
    @param ebmin: The divisor of the minimum error band, taken from the config file
    @param ebmax: The divisor of the maximum error band, taken from the config file
    @param rndlo: The lower bound for getting the random adjustment of the error band
    @param rndhi: The higher bound for getting the random adjustment of the error band
    @return: A list of assessment_outcome objects
    '''
    # The cut_points in score details do not include min and max score. The score generator needs the min and max to be included
    cut_points = [assessment.asmt_cut_point_1, assessment.asmt_cut_point_2, assessment.asmt_cut_point_3]
    if assessment.asmt_cut_point_4:
        cut_points.append(assessment.asmt_cut_point_4)

    asmt_scores = translate_scores_to_assessment_score(scores, cut_points, assessment, ebmin, ebmax, rndlo, rndhi)
    asmt_rec_id = assessment.asmt_rec_id
    state_code = institution_hierarchy.state_code
    district_guid = institution_hierarchy.district_guid
    school_guid = institution_hierarchy.school_guid
    section_guid = section.section_guid
    inst_hier_rec_id = institution_hierarchy.inst_hier_rec_id
    section_rec_id = section.section_rec_id
    where_taken_id = school_guid
    where_taken_name = institution_hierarchy.school_name
    asmt_grade = section.grade
    enrl_grade = section.grade
    date_taken = util.generate_date_given_assessment(assessment)
    date_taken_day = date_taken.day
    date_taken_month = date_taken.month
    date_taken_year = date_taken.year
    date_taken = date_taken.strftime('%Y%m%d')

    asmt_outcomes = generate_fact_assessment_outcomes(students, asmt_scores, asmt_rec_id, teacher_guid, state_code,
                                                      district_guid, school_guid, section_guid, inst_hier_rec_id,
                                                      section_rec_id, where_taken_id, where_taken_name, asmt_grade,
                                                      enrl_grade, date_taken, date_taken_day, date_taken_month, date_taken_year, batch_guid)

    return asmt_outcomes


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


def generate_students_from_institution_hierarchy(config_module, number_of_students, institution_hierarchy, grade, section_guid, street_names):
    '''
    Generates a list of students
    @param number_of_students: The number of students to generate
    @param institution_hierarchy: An InstitutionHierarchy object for the students to be apart of
    @param grade: The grade of the students
    @param section_guid: The section unique identifier
    @param street_names: A list of names to use when assigning streets to students
    @return: A list of Student objects
    '''
    state_code = institution_hierarchy.state_code
    district_guid = institution_hierarchy.district_guid
    school_guid = institution_hierarchy.school_guid
    school_name = institution_hierarchy.school_name

    temporal_information = config_module.get_temporal_information()
    from_date = temporal_information[constants.FROM_DATE]
    most_recent = temporal_information[constants.MOST_RECENT]
    to_date = temporal_information[constants.TO_DATE]

    students = generate_students(number_of_students, section_guid, grade, state_code, district_guid, school_guid, school_name, street_names, from_date, most_recent, to_date=to_date)
    return students


def set_students_rec_id_and_section_id(students, section_guid):
    '''
    Take a list of students and set their section_id and assign new rec_id
    @param students: A list of students to use
    @param section_guid: the section number to use
    @return: The list os students passed in (they are not copied, so the original objects are altered)
    '''
    id_gen = IdGen()
    for student in students:
        student.student_rec_id = id_gen.get_id()
        student.section_guid = section_guid
    return students


def generate_teaching_staff_from_institution_hierarchy(config_module, number_of_staff, institution_hierarchy, section_guid):
    '''
    Generate teachers based on the institution hierarchy object that is provided
    @param number_of_staff: The number of teachers to generate
    @param institution_hierarchy: An InstitutionHierarchy object
    @param section_guid: The Guid corresponding to the section to place the staff member in
    @return: a list of teachers as Staff objects
    '''
    state_code = institution_hierarchy.state_code
    district_guid = institution_hierarchy.district_guid
    school_guid = institution_hierarchy.school_guid
    hier_user_type = 'Teacher'
    temporal_information = config_module.get_temporal_information()
    from_date = temporal_information[constants.FROM_DATE]
    most_recent = temporal_information[constants.MOST_RECENT]
    to_date = temporal_information[constants.TO_DATE]
    staff_list = generate_multiple_staff(number_of_staff, hier_user_type, from_date, most_recent, state_code=state_code, district_guid=district_guid,
                                         school_guid=school_guid, section_guid=section_guid, to_date=to_date)
    return staff_list


def generate_non_teaching_staff(config_module, number_of_staff, state_code='NA', district_guid='NA', school_guid='NA'):
    '''
    Generate staff that are not teachers
    @param number_of_staff: The number of staff memebers to generate
    @keyword state_code: The state code to use for the staff memeber. If applicable.
    @keyword district_guid: The guid to the district the staff member is in. If applicable.
    @keyword school_guid: The guid to the school the staff member is in. If applicable.
    @return: a list of Staff objects
    '''
    hier_user_type = 'Staff'
    temporal_information = config_module.get_temporal_information()
    from_date = temporal_information[constants.FROM_DATE]
    most_recent = temporal_information[constants.MOST_RECENT]
    to_date = temporal_information[constants.TO_DATE]
    staff_list = generate_multiple_staff(number_of_staff, hier_user_type, from_date, most_recent, state_code=state_code,
                                         district_guid=district_guid, school_guid=school_guid, to_date=to_date)
    return staff_list


def calculate_number_of_schools(school_min, school_max, school_avg):
    '''
    calculate the number of schools using the gaussian function
    @param school_min: The min number of schools the school can contain
    @param school_avg: The average number of schools
    @param school_max: The Maximum number of schools the school can contain
    @return: An int representing the number of schools
    '''
    standard_dev, _r_avg = guess_std(school_min, school_max, school_avg)
    number_of_schools = gauss_one(school_min, school_max, school_avg, standard_dev)
    return int(number_of_schools)


def calculate_number_of_students(student_min, student_max, student_avg):
    '''
    Calculate the number of students to place in a school
    @param student_min: The min number of students the school can contain
    @param student_max: The Maximum number of students the school can contain
    @param student_avg: The average number of students
    @return: An int representing the number of students to use, based on a gaussian distribution
    '''
    standard_dev, _r_avg = guess_std(student_min, student_max, student_avg)
    number_of_students = gauss_one(student_min, student_max, student_avg, standard_dev)
    return int(number_of_students)


def calculate_number_of_sections(number_of_students):
    '''
    Calculate the number of sections a grade should have based on the number of students
    @param number_of_students: The number of students in the grade for a single subject
    @return: The number of students to put in each section as an int
    '''
    # TODO: Figure out how to calculate number_of_sections
    return 1


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
        if asmt.asmt_grade == grade and asmt.asmt_subject == subject:
            return asmt


def get_subset_of_students(students, percentage):
    '''
    take a list of students and return a certain percentage of those students
    meant to be used when only a subset of students should take an assessment
    @param students: A list of students (or other object)
    @param percentage: the percentage of those students to return (as a decimal)
    '''
    student_len = len(students)
    selection_size = int(student_len * percentage)
    selection = random.sample(students, selection_size)
    return selection


def get_student_totals(inst_hiers):
    '''
    take a list of institution hierarchies and sum the total students that should be generated for each grade
    @param inst_hiers: A list of InstitutionHierarchy objects
    @return: A dictionary of sums with the grade as the key
    '''

    sums = {}
    for inst in inst_hiers:
        for grade in inst.student_counts:
            if sums.get(grade):
                sums[grade] += inst.student_counts[grade]
            else:
                sums[grade] = inst.student_counts[grade]

    return sums


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
