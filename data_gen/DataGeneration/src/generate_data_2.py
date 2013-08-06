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

from demographics import Demographics, DemographicStatus, generate_students_from_demographic_counts
from generate_entities import generate_assessments
from write_to_csv import create_csv
from state_population import StatePopulation
import constants
from entities import (InstitutionHierarchy, Section, Assessment, AssessmentOutcome,
                      Staff, ExternalUserStudent, Student)


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


def generate_data_from_config_file(config_module, output_dict):
    '''
    Main function that drives the data generation process

    @param config_module: module that contains all configuration information for the data creation process
    @return nothing
    '''

    # Setup demographics object
    demographics_info = Demographics(config_module.get_demograph_file())

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

    for state in states:
        # Pull out basic state information
        state_name = state[constants.NAME]
        state_code = state[constants.STATE_CODE]

        # Pull out information on districts within this state
        state_type_name = state[constants.STATE_TYPE]
        state_type = state_types[state_type_name]
        district_types_and_counts = state_type[constants.DISTRICT_TYPES_AND_COUNTS]
        subject_percentages = state_type[constants.SUBJECT_AND_PERCENTAGES]
        demographics_id = state_type[constants.DEMOGRAPHICS]

        # Create State Population object
        state_population = StatePopulation(state_name, state_code, state_type_name)
        # calculate the states total number of object
        state_population.populate_state(state_type, district_types, school_types)
        # Calculate the Math Demographic numbers for the state
        state_population.get_state_demographics(demographics_info, demographics_id)

        generate_students_from_demographic_counts(state_population, assessments)


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
