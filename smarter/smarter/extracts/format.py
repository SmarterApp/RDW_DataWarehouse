'''
Created on Nov 14, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from config.ref_table_data import ref_table_conf
from copy import deepcopy


# A map of map that contains star schema table name, column to udl input name
# ex. {'dim_student': {'student_id': 'guid_student'}}
json_column_mapping = {}
csv_column_mapping = {}


def setup_input_file_format():
    '''
    Read from udl input file format from ref_column_mapping tables to get column mapping for star schema columns
    '''
    ref_table = ref_table_conf
    phases = {}
    # Create a dict of list that separates each phase of udl pipeline
    for row in ref_table['column_mappings']:
        current_phase = row[0]
        if phases.get(current_phase) is None:
            phases[current_phase] = []
        # converts tuple into dictionary
        phases[current_phase].append(dict(zip(ref_table['column_definitions'], row)))

    # We need to process csv and json separately
    csv_mapping = process_input_file_format(phases, 'lz_csv')
    json_mapping = process_input_file_format(phases, 'lz_json')

    global csv_column_mapping
    global json_column_mapping
    csv_column_mapping = format_mappings(csv_mapping)
    json_column_mapping = format_mappings(json_mapping)
    # create_empty_json_metadata_template()


def process_input_file_format(phases, input_source):
    phases = deepcopy(phases)
    mapping = {}
    keys = sorted(list(phases.keys()), key=int)
    initial_load = True
    for key in keys:
        for row in phases[key]:
            src_table = row['source_table']
            src_col = row['source_column']
            # Sometimes, source table or source column are placeholders and have no value
            if src_table is None or src_col is None:
                continue
            src_key = src_table + "|" + src_col
            tar_key = row['target_table'] + "|" + row['target_column']
            if initial_load and src_table == input_source:
                # Save everything if it's the first load
                mapping[src_key] = tar_key
            else:
                # We only care about table/columns that already exist from the previous phases
                # Add an entry to mapping
                # We don't need to delete existing mapping as it may be map to more than one column
                cur_value = mapping.get(src_key)
                if cur_value is not None:
                    mapping[tar_key] = cur_value
        if initial_load:
            initial_load = False
            # inverse it so the key is the source table of the next phase, and value is the input file format column
            mapping = {v: k for k, v in mapping.items()}
    return mapping


def format_mappings(mapping):
    # Format based on column_mapping schema mapping. Currently, only format for these tables
    column_mapping = {Constants.DIM_ASMT: {}, Constants.DIM_STUDENT: {}, Constants.FACT_ASMT_OUTCOME_VW: {}, Constants.DIM_INST_HIER: {}}
    for k, v in mapping.items():
        table_column_index = k.index('|')
        star_table = k[:table_column_index]
        star_column = k[table_column_index + 1:]
        tar_table_column_index = v.index('|') + 1
        if star_table in column_mapping.keys():
            column_mapping[star_table][star_column] = v[tar_table_column_index:]
    return column_mapping


def get_column_mapping(table_name, json_mapping=False):
    '''
    Given a star schema table name, return the column mapping for that table
    By Default, it returns csv mapping

    :params bool json_mapping:  True if json mapping should be returned
    '''
    mapping = json_column_mapping if json_mapping else csv_column_mapping
    return mapping.get(table_name, {})
