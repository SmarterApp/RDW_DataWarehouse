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

import json
import edudl2.udl2_util.database_util as db_util
from edudl2.udl2 import message_keys as mk
from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql.expression import select, and_
from psycopg2.extensions import QuotedString
from edudl2.udl2.constants import Constants

def load_json(conf):
    '''
    Main method for loading json into the integration table
    @param conf: The configuration dictionary
    '''

    json_dict = read_json_file(conf.get(mk.FILE_TO_LOAD))
    flattened_json = flatten_json_dict(json_dict, conf.get(mk.MAPPINGS))
    return load_to_table(flattened_json, conf.get(mk.GUID_BATCH),
                         conf.get(mk.TARGET_DB_TABLE), conf.get(mk.TENANT_NAME),
                         conf.get(mk.TARGET_DB_SCHEMA))


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


def load_to_table(data_dict, guid_batch, int_table, tenant_name, udl_schema):
    '''
    Load the table into the proper table
    @param data_dict: the dictionary containing the data to be loaded
    @param guid_batch: the id for the batch
    @param int_table: the name of the integration table
    @param tenant_name: name of the tenant
    @param udl_schema: udl schema name
    '''
    # Create sqlalchemy connection and get table information from sqlalchemy
    ref_column_mapping_columns = {}
    with get_udl_connection() as conn:
        data_dict[mk.GUID_BATCH] = guid_batch
        data_dict = fix_empty_strings(data_dict)
        ref_table = conn.get_table('ref_column_mapping')
        s_int_table = conn.get_table(int_table)
        column_mapping_query = select([ref_table.c.target_column,
                                       ref_table.c.stored_proc_name],
                                      from_obj=ref_table).where(and_(ref_table.c.source_table == 'lz_json',
                                                                     ref_table.c.target_table == int_table))
        results = conn.get_result(column_mapping_query)
        for result in results:
            target_column = result['target_column']
            stored_proc_name = result['stored_proc_name']
            value = data_dict.get(target_column)
            if value:
                if stored_proc_name:
                    if stored_proc_name.startswith('sp_'):
                        ref_column_mapping_columns[target_column] = stored_proc_name + '(' + QuotedString(value if type(value) is str else str(value)).getquoted().decode('utf-8') + ')'
                    else:
                        format_value = dict()
                        format_value['value'] = QuotedString(value if type(value) is str
                                                             else str(value)).getquoted().decode('utf-8')
                        if s_int_table.c[target_column].type.python_type is str:
                            format_value['length'] = s_int_table.c[target_column].type.length
                        ref_column_mapping_columns[target_column] = stored_proc_name.format(**format_value)
                    continue
            ref_column_mapping_columns[target_column] = value

        record_sid = 'nextval(\'{schema_name}.{tenant_sequence_name}\')'.\
            format(schema_name=udl_schema, tenant_sequence_name=Constants.TENANT_SEQUENCE_NAME(tenant_name))
        from_select_column_names = ['record_sid']
        from_select_select_values = [record_sid]
        for column in s_int_table.c:
            value = data_dict.get(column.name)
            if value:
                from_select_column_names.append(column.name)
                from_select_select_values.append(
                    ref_column_mapping_columns.get(column.name,
                                                   QuotedString(value if type(value) is str else str(value)).getquoted().decode('utf-8')))
        insert_into_int_table = s_int_table.insert().from_select(from_select_column_names,
                                                                 select(from_select_select_values))
        # create insert statement and execute
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
