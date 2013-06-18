'''
Created on Jun 6, 2013

@author: swimberly
'''
from udl2_util.measurement import measure_cpu_plus_elasped_time
from udl2_util.database_util import get_sqlalch_table_object
from rule_maker.rules.transformation_code_generator import generate_transformations


@measure_cpu_plus_elasped_time
def populate_ref_column_map(conf_dict, db_engine, conn, schema_name, col_map_table):
    '''
    Take a dict containing the data to be loaded
    '''
    col_map_table = get_sqlalch_table_object(db_engine, schema_name, col_map_table)
    col_map_data = conf_dict['column_mappings']
    col_map_columns = conf_dict['column_definitions']
    data_list = []

    for row in col_map_data:
        row_map = {}
        for i in range(len(row)):
            if row[i] is not None:
                row_map[col_map_columns[i]] = row[i]
        data_list.append(row_map)

    conn.execute(col_map_table.insert(), data_list)


@measure_cpu_plus_elasped_time
def populate_stored_proc(engine, conn, ref_schema, ref_table_name):
    '''
    Generate and load stored procedures into the database
    @return: The names of all the generated stored procedures
    @rtype: list
    '''

    proc_list = generate_transformations()
    generated_functions = []
    for proc in proc_list:
        if proc:
            proc_name = proc.replace('CREATE OR REPLACE FUNCTION ', '')
            proc_name = proc_name.split('\n')[0]
            print('Creating function:', proc_name)
            conn.execute(proc)
            generated_functions.append(proc_name)

    return generated_functions
