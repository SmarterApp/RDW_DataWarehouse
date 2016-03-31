# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

from edudl2.udl2.W_load_from_integration_to_star import explode_to_dims, explode_to_facts
from celery import chain
import argparse


def main():
    '''
    Main function to start the stage of moving data from integration tables to target tables
    '''
    parser = argparse.ArgumentParser(description='Move to Target Worker')
    parser.add_argument("-b", "--guid_batch", type=str, default='8866c6d5-7e5e-4c54-bf4e-775abc4021b2', help="Batch id")
    args = parser.parse_args()

    batch = {'guid_batch': args.guid_batch}

    # First, explode the data into dim tables by celery group
    # Then, explode the data into fact table
    # These two steps are connected by celery chain
    result_uuid = chain(explode_to_dims.s(batch), explode_to_facts.s())()
    result_value = result_uuid.get()
    print(result_value)

if __name__ == '__main__':
    main()
