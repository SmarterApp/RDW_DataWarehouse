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
import os

from mongoengine import connect
from pymongo import Connection

import generate_data as generate_data
import sbac_data_generation.generators.hierarchy as sbac_hier_gen


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

    # Start the generation of data
    for state_cfg in generate_data.STATES:
        # Create the state object
        state = sbac_hier_gen.generate_state(state_cfg['type'], state_cfg['name'], state_cfg['code'])
        print('Created State: %s' % state.name)

        # Process the state
        generate_data.generate_state_data(state)

    # Record now current (end) time
    tend = datetime.datetime.now()

    # Print statistics
    print()
    print('Run began at:  %s' % tstart)
    print('Run ended at:  %s' % tend)
    print('Run run took:  %s' % (tend - tstart))
    print()