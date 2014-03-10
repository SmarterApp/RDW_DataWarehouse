'''
Implementation for loading data from a json file to a table.

Typically usage would be to load data from an assessment json
file to the integration table.

Main Method: load_json(conf)
conf dictionary must contain the following keys:
'json_file', 'guid_batch', 'mappings', 'db_host', 'db_name', 'db_user',
'db_port', 'db_password', 'integration_table', 'integration_schema'

Created on May 16, 2013

@author: swimberly
'''

import argparse
import json
import edudl2.udl2_util.database_util as db_util
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_connector import get_udl_connection
import time
from edudl2.udl2_util.udl_mappings import get_json_table_mapping

DBDRIVER = "postgresql"


def load_json(conf):
    '''
    Main method for loading json into the integration table
    @param conf: The configuration dictionary
    '''

    json_dict = read_json_file(conf[mk.FILE_TO_LOAD])
    flattened_json = flatten_json_dict(json_dict, conf[mk.MAPPINGS])
    return load_to_table(flattened_json, conf[mk.GUID_BATCH], conf[mk.TARGET_DB_TABLE])


def read_json_file(json_file):
    '''
    Read a json file into a dictionary
    @param json_file: The path to the json file to read
    @return: A dictionary containing the data from the json file
    @rtype: dict
    '''

    with open(json_file, 'r') as jf:
        return json.load(jf)


def flatten_json_dict(json_dict, mappings):
    '''
    convert a dictionary into a corresponding flat csv format
    @param json_dict: the dictionary containing the json data
    @param mappings: A dictionary with values indicate the location of the value
    @return: A dictionary of columns mapped to values
    @rtype: dict
    '''

    flat_data = {}
    for key in mappings:
        location_list = mappings[key]
        flat_data[key] = get_nested_data(location_list, json_dict)

    return flat_data


def get_nested_data(location_list, json_dict):
    '''
    Take the location list and the json data and return the value at the end of the search path
    @param location_list: A list containing strings or ints that show the path to the desired data
    @param json_dict: The json data in a dictionary
    @return: the desired value at the end of the path
    '''

    value = json_dict
    for loc_key in location_list:
        for key in value.keys():
            if loc_key == key.lower():
                value = value[key]
                break

    return value


def load_to_table(data_dict, guid_batch, int_table):
    '''
    Load the table into the proper table
    @param data_dict: the dictionary containing the data to be loaded
    @param guid_batch: the id for the batch
    @param int_table: the name of the integration table
    '''

    # Create sqlalchemy connection and get table information from sqlalchemy
    with get_udl_connection() as conn:
        s_int_table = conn.get_table(int_table)
        data_dict = fix_empty_strings(data_dict)
        data_dict[mk.GUID_BATCH] = guid_batch

        # create insert statement and execute
        insert_into_int_table = s_int_table.insert().values(**data_dict)
        affected_row = db_util.execute_udl_queries(conn, [insert_into_int_table],
                                                   'Exception in loading json data -- ',
                                                   'json_loader', 'load_to_table')

    return affected_row[0]


def fix_empty_strings(data_dict):
    ''' Replace values which are empty string with a reference to None '''
    for k, v in data_dict.items():
        if v == '':
            data_dict[k] = None
    return data_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='source_json', required=True, help="path to the source file")
    args = parser.parse_args()
    json_file = args.source_json
    mapping = get_json_table_mapping('assessment')

    conf = {mk.FILE_TO_LOAD: json_file,
            mk.MAPPINGS: mapping,
            mk.TARGET_DB_HOST: 'localhost',
            mk.TARGET_DB_PORT: '5432',
            mk.TARGET_DB_USER: 'udl2',
            mk.TARGET_DB_NAME: 'udl2',
            mk.TARGET_DB_PASSWORD: 'udl2abc1234',
            mk.TARGET_DB_SCHEMA: 'udl2',
            mk.TARGET_DB_TABLE: 'INT_SBAC_ASMT',
            mk.GUID_BATCH: 100
            }

    start_time = time.time()
    load_json(conf)
    print('json loaded into %s in %.2fs' % (conf[mk.TARGET_DB_SCHEMA], time.time() - start_time))
