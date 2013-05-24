import datetime
from udl2_util.database_util import connect_db, execute_queries
from move_to_integration.column_mapping import get_column_mapping

def move_data_from_staging_to_integration(conf):
    print(conf)
    (conn, engine) = connect_db(conf['db_driver_source'],
                                conf['db_user_source'],
                                conf['db_password_source'],
                                conf['db_host_source'],
                                conf['db_port_source'],
                                conf['db_name_source'])
    map_type = 'staging_to_integration_sbac_asmt_outcome'
    column_mapping = get_column_mapping(map_type)
    sql_query = create_migration_query(conf['source_schema'], column_mapping['source'], conf['target_schema'],
                                       column_mapping['target'], conf['error_schema'], 'ERR_LIST', column_mapping['mapping'],
                                       conf['batch_id'])
    print(sql_query)
    except_msg = "problem when load data from staging table to integration table"
    execute_queries(conn, [sql_query], except_msg)
    return 


def create_migration_query(source_schema, source_table, target_schema, target_table,
                           error_schema, error_table, mapping, batch_id):
    sql_template = """
    INSERT INTO "{target_schema}"."{target_table}"
         ({target_columns})
    SELECT {source_columns} 
        FROM "{source_schema}"."{source_table}" AS A LEFT JOIN 
        "{error_schema}"."{error_table}" AS B ON (A.record_sid = B.record_sid ) 
        WHERE B.record_sid IS NULL AND A.batch_id = {batch_id} 
    """
    # mapping is (target_column_name, (conversion_sql_code, source_column_name))
    target_columns = (", ".join(["{target_column}".format(target_column=k) for k in mapping.keys()]))
    source_columns = (", ".join([ k[0].format(src_field="A.{source_field}".format(source_field=k[1])) for k in mapping.values()]))     
    sql = sql_template.format(target_schema=target_schema,
                              target_table=target_table,
                              target_columns=target_columns,
                              source_columns=source_columns,
                              source_schema=source_schema,
                              source_table=source_table,
                              error_schema=error_schema,
                              error_table=error_table,
                              batch_id=batch_id)
    return sql


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("")
    
    end_time = datetime.datetime.now()