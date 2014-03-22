"""
The multi-processed data generator for the SBAC project. Ultimately, this version relies heavily on the regular
data generator, but attempts to achieve performance improvements related to using the multiprocess library from Python.

Command line arguments:
  --team TEAM_NAME: Name of team to generate data for (expects sonics or arkanoids)
  --state_name STATE_NAME: Name of state to generate data for (defaults to 'North Carolina')
  --state_code STATE_CODE: Code of state to generate data for (defaults to 'NC')
  --state_type STATE_TYPE_NAME: Name of state type to generate data for (expects devel, typical_1, california)

@author: nestep
@date: March 22, 2014
"""

import argparse
import datetime
import multiprocessing
import os
import queue
import random

from mongoengine import connect
from pymongo import Connection

import generate_data as generate_data
import sbac_data_generation.config.cfg as sbac_in_config
import sbac_data_generation.generators.hierarchy as sbac_hier_gen


def generate_state_district_hierarchy():
    """
    Create the the states and districts to generate data for.

    @returns: A list of tuples suitable to be fed into a worker
    """
    district_tuples = []

    # Start with states
    for state_cfg in generate_data.STATES:
        # Create the state object
        state = sbac_hier_gen.generate_state(state_cfg['type'], state_cfg['name'], state_cfg['code'])
        print('Created State: %s' % state.name)

        # Grab the assessment rates by subjects
        asmt_skip_rates_by_subject = state.config['subject_skip_percentages']

        # Create the assessment objects
        assessments = {}
        for year in generate_data.ASMT_YEARS:
            for subject in sbac_in_config.SUBJECTS:
                for grade in generate_data.GRADES_OF_CONCERN:
                    # Create the summative assessment
                    asmt_key_summ = str(year) + 'summative' + str(grade) + subject
                    assessments[asmt_key_summ] = generate_data.create_assessment_object('SUMMATIVE', 'Spring', year,
                                                                                        subject)

                    # Create the interim assessments
                    for period in generate_data.INTERIM_ASMT_PERIODS:
                        asmt_key_intrm = str(year) + 'interim' + period + str(grade) + subject
                        asmt_intrm = generate_data.create_assessment_object('INTERIM COMPREHENSIVE', period, year,
                                                                            subject)
                        assessments[asmt_key_intrm] = asmt_intrm

        # Build the districts
        for district_type, dist_type_count in state.config['district_types_and_counts'].items():
            for _ in range(dist_type_count):
                # Create the district
                district = sbac_hier_gen.generate_district(district_type, state)
                print('  Created District: %s (%s District)' % (district.name, district.type_str))
                district_tuples.append((district, assessments, asmt_skip_rates_by_subject))

    # Return the districts
    return district_tuples


def district_pool_worker(worker_args):
    """
    Process a single district. This is basically a wrapper for generate_data.generate_district_date that is designed to
    be called through a multiprocessor.Pool construct.

    @param worker_args: A tuple of the district, assessments, and skip_rates to pass on
    """
    # Parse out the arguments
    district, assessments, skip_rates = worker_args

    # Note that we are processing
    print('PROCESSING BEGINNING (%s)' % district.name)

    # Start the processing
    generate_data.generate_district_data(district.state, district,
                                         random.choice(generate_data.REGISTRATION_SYSTEM_GUIDS), assessments,
                                         skip_rates)


if __name__ == '__main__':
    # Argument parsing for task-specific arguments
    parser = argparse.ArgumentParser(description='SBAC data generation task.')
    parser.add_argument('-t', '--team', dest='team_name', action='store', default='sonics',
                        help='Specify the name of the team to generate data for (sonics, arkanoids)',
                        required=False)
    parser.add_argument('-sn', '--state_name', dest='state_name', action='store', default='North Carolina',
                        help='Specify the name of the state to generate data for (default=North Carolina)',
                        required=False)
    parser.add_argument('-sc', '--state_code', dest='state_code', action='store', default='NC',
                        help='Specify the code of the state to generate data for (default=NC)',
                        required=False)
    parser.add_argument('-st', '--state_type', dest='state_type', action='store', default='devel',
                        help='Specify the type of state to generate data for (devel (default), typical_1, california)',
                        required=False)
    args, unknown = parser.parse_known_args()

    # Set team-specific configuration options
    generate_data.assign_team_configuration_options(args.team_name, args.state_name, args.state_code, args.state_type)

    # Record current (start) time
    tstart = datetime.datetime.now()

    # Verify output directory exists
    if not os.path.exists(generate_data.OUT_PATH_ROOT):
        os.makedirs(generate_data.OUT_PATH_ROOT)

    # Connect to MongoDB and drop an existing datagen database
    c = Connection()
    if 'datagen' in c.database_names():
        c.drop_database('datagen')

    # Clean output directory
    for file in os.listdir(generate_data.OUT_PATH_ROOT):
        file_path = os.path.join(generate_data.OUT_PATH_ROOT, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            pass

    # Connect to MongoDB, datagen database
    connect('datagen')

    # Prepare the output files
    generate_data.prepare_output_files(generate_data.YEARS)

    # Create the registration systems
    generate_data.REGISTRATION_SYSTEM_GUIDS = generate_data.build_registration_systems(generate_data.YEARS)

    # Build the states and districts
    districts = generate_state_district_hierarchy()

    # Go
    pool = multiprocessing.Pool(processes=4)
    pool.map(district_pool_worker, districts)
    pool.close()
    pool.join()

    # Record now current (end) time
    tend = datetime.datetime.now()

    # Print statistics
    print()
    print('Run began at:  %s' % tstart)
    print('Run ended at:  %s' % tend)
    print('Run run took:  %s' % (tend - tstart))
    print()