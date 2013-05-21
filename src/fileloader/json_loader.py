'''
Created on May 16, 2013

@author: swimberly
'''

import argparse
import json

from sqlalchemy.engine import create_engine

import fileloader.prepare_queries as queries
from fileloader.file_loader import execute_queries
from udl2_util.udl_mappings import get_json_to_asmt_tbl_mappings


DBDRIVER = "postgresql"


def load_json(conf):
    '''
    Main method for loading json into the integration table
    @param conf: The configuration dictionary
    '''

    json_dict = read_json_file(conf['json_file'])
    flattened_json = flatten_json_dict(json_dict, conf['mappings'])
    load_to_table(flattened_json, conf['batch_id'], conf['db_host'], conf['db_name'], conf['db_user'],
                  conf['db_port'], conf['db_password'], conf['integration_table'], conf['integration_schema'])


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
        value = value[loc_key]

    return value


def load_to_table(data_dict, batch_id, db_host, db_name, db_user, db_port, db_password, int_table, int_schema):
    '''
    Load the table into the proper table
    @param data_dict: the dictionary containing the data to be loaded
    @param batch_id: the id for the batch
    @param db_host: the database host
    @param db_name: the name of the database
    @param db_user: the username for the database
    @param db_port: the port to connect to
    @param db_password: the password to use
    @param int_table: the name of the integration table
    @param int_schema: the name of the integration schema
    '''

    conn, _engine = connect_db(db_user, db_password, db_host, db_name)
    # create sequence name, use table_name and a random number combination

    headers = list(data_dict.keys())
    data = list(data_dict.values())
    headers.insert(0, 'batch_id')
    data.insert(0, str(conf['batch_id']))
    insert_into_int_table = queries.create_insert_assessment_into_integration_query(headers, data, batch_id, int_schema, int_table)  # apply_rules, csv_table_columns, header_types, staging_schema, staging_table, csv_schema, csv_table, start_seq, seq_name)

    # TODO: ececute the query
#     execute_queries(conn, [insert_into_int_table], 'Exception in loading assessment data -- ')


def connect_db(user, passwd, host, db_name):
    '''
    Connect to database via sqlalchemy
    '''

    db_string = DBDRIVER + '://{db_user}:{db_password}@{db_host}/{db_name}'.format(db_user=user, db_password=passwd, db_host=host, db_name=db_name)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    return db_connection, engine


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='source_json', required=True, help="path to the source file")
    args = parser.parse_args()

    mapping = get_json_to_asmt_tbl_mappings()

    # conf from file_loader
    conf = {
            'json_file': args.source_json,
            'mappings': mapping,
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'udl2',
            'db_name': 'udl2',
            'db_password': 'udl2abc1234',
            'integration_schema': 'udl2',
            'integration_table': 'INT_SBAC_ASMT',
            'batch_id': 100
    }
    load_json(conf)
