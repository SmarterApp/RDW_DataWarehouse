'''
Created on Jun 6, 2013

@author: swimberly
'''

from udl2_util.database_util import get_sqlalch_table_object


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
