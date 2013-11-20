'''
Created on Nov 14, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from ref_table_data import ref_table_conf


# A map of map that contains star schema table name, column to udl input name
# ex. {'dim_student': {'student_guid': 'guid_student'}}
column_mapping = {}


def setup_input_file_format():
    '''
    Read from udl input file format from ref_column_mapping tables to get column mapping for star schema columns
    '''
    global column_mapping
    ref_table = ref_table_conf
    mapping = {}
    phases = {}
    # Create a dict of list that separates each phase of udl pipeline
    for row in ref_table['column_mappings']:
        current_phase = row[0]
        if phases.get(current_phase) is None:
            phases[current_phase] = []
        # converts tuple into dictionary
        phases[current_phase].append(dict(zip(ref_table['column_definitions'], row)))

    keys = sorted(list(phases.keys()), key=int)
    initial_load = False
    for key in keys:
        for row in phases[key]:
            src_table = row['source_table']
            src_col = row['source_column']
            # Sometimes, source table or source column are placeholders and have no value
            if src_table is not 'LZ_JSON' and (src_table is None or src_col is None):
                continue
            src_key = src_table + "|" + src_col
            tar_key = row['target_table'] + "|" + row['target_column']
            if not initial_load:
                # Save everything if it's the first load
                mapping[src_key] = tar_key
            else:
                # We only care about table/columns that already exist from the previous phases
                # Add an entry to mapping
                # We don't need to delete existing mapping as it may be map to more than one column
                cur_value = mapping.get(src_key)
                if cur_value is not None:
                    mapping[tar_key] = cur_value
        if not initial_load:
            initial_load = True
            # inverse it so the key is the source table of the next phase, and value is the input file format column
            mapping = {v: k for k, v in mapping.items()}
    # Format based on column_mapping schema mapping. Currently, only format for these tables
    column_mapping = {Constants.DIM_ASMT: {}, Constants.DIM_STUDENT: {}, Constants.FACT_ASMT_OUTCOME: {}, Constants.DIM_INST_HIER: {}}
    for k, v in mapping.items():
        table_column_index = k.index('|')
        star_table = k[:table_column_index]
        star_column = k[table_column_index + 1:]
        tar_table_column_index = v.index('|') + 1
        if star_table in column_mapping.keys():
            column_mapping[star_table][star_column] = v[tar_table_column_index:]


def get_column_mapping(table_name):
    '''
    Given a star schema table name, return the column mapping for that table
    '''
    return column_mapping.get(table_name, {})
