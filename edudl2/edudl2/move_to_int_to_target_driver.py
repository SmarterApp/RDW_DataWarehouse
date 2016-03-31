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

from edudl2.udl2.W_load_json_to_integration import task as task_1
from edudl2.udl2.W_load_to_integration_table import task as task_2
from celery import chain
import argparse
from edudl2.udl2.W_load_from_integration_to_star import explode_to_dims,\
    explode_to_facts


def main():
    parser = argparse.ArgumentParser(description='Move data from staging to integration, and to target')
    parser.add_argument("-b", "--guid_batch", type=str, default='00000000-0000-0000-0000-000000000000', help="guid batch")
    parser.add_argument("-j", "--json_file", type=str, required=True, help="json file")
    args = parser.parse_args()

    batch = {'guid_batch': args.guid_batch,
             'file_to_load': args.json_file,
             'load_to_integration_table_type': 'staging_to_integration_sbac_asmt_outcome'}

    # in the chain:
    # 1. load json file into INT_SBAC_ASMT
    # 2. move data from STG_SBAC_ASMT_OUTCOME to INT_SBAC_ASMT_OUTCOME
    # 3. move data from INT_SBAC_ASMT, INT_SBAC_ASMT_OUTCOME to dim and fact tables in star schema
    result_uuid = chain(task_1.s(batch), task_2.s(), explode_to_dims.s(), explode_to_facts.s())()
    result_value = result_uuid.get()
    print(result_value)

if __name__ == '__main__':
    main()
