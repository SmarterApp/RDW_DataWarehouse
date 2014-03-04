def get_filtered_tables(connector, table_name_prefix=None):
    """This function returns list of tables starting with table_name_prefix from schema metadata

    :param connector: The connection to the database
    :returns : A list of table names
             [dim_section, dim_student]
    """
    all_tables = []
    for table in connector.get_metadata().tables.keys():
        if '.' in table:
            all_tables.append(table.split('.')[1])
        else:
            all_tables.append(table)
    if table_name_prefix is not None:
        all_tables = [table for table in all_tables if table.lower().startswith(table_name_prefix.lower())]
    return all_tables


def cleanup_table(connector, column_name, value, table_name):
    """
    cleanup table for the given column and value
    """
    table = connector.get_table(table_name)
    if column_name in table.columns:
        delete_query = table.delete(table.c[column_name] == value)
        connector.execute(delete_query)

def cleanup_all_tables(connector, column_name, value, table_name_prefix=None, tables=None):
    """
    cleanup all tables for the given column and matching value
    
    All rows matching the given guid_batch will be delted from all the tables
    in the given connector schema
    """
    tables_to_cleanup = get_filtered_tables(connector, table_name_prefix) if tables is None else tables
    for table in tables_to_cleanup:
        cleanup_table(connector, column_name, value, table)
