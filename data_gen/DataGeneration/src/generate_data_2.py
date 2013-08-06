'''
Created on Aug 5, 2013

@author: swimberly
'''

from demographics import Demographics, DemographicStatus
from state_population import StatePopulation
from uuid import uuid4
import constants
import datetime
from importlib import import_module
import argparse
import os

from entities import (InstitutionHierarchy, Section, Assessment, AssessmentOutcome,
                      Staff, ExternalUserStudent, Student)


DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))

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

    # Get information from the config module
    school_types = config_module.get_school_types()
    district_types = config_module.get_district_types()
    state_types = config_module.get_state_types()
    states = config_module.get_states()
    scores_details = config_module.get_scores()

    # generate one batch_guid for all records
    batch_guid = uuid4()

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

        print(state_population.state_demographic_totals)


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
