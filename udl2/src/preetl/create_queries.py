

def insert_batch_row_query(schema, batch_table, **para_dict):
    '''
    Create the sql to insert a row into the batch table.
    It is expected that items in the para_dict do not have None values
    '''
    column_list = []
    value_list = []
    # split pair of column name, and value in the same order
    for column, value in sorted(para_dict.items()):
        column_list.append(column)
        value_list.append("'" + value + "'" if isinstance(value, str) else str(value))
    column_list = ",".join(column_list)
    value_list = ",".join(value_list)
    return 'INSERT INTO "{schema}"."{batch_table}"({column_list}) VALUES ({value_list})'.format(schema=schema, batch_table=batch_table,
                                                                                                column_list=column_list,
                                                                                                value_list=value_list)
