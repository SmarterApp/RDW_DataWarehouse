import datetime
from udl2_util.database_util import connect_db, execute_queries
from move_to_integration.column_mapping import get_column_mapping

def move_data_from_staging_to_integration(conf):
    '''
    map sql data type in configuration file into what SQLAlchemy type is.
    @param conf: configration dictionary, the format is
          note: udl2_conf is the udl2_conf dictionary that stores all configuration settings
           conf = {   
            'batch_id': batch id, # add batch_id from msg
            'error_schema': udl2_conf['udl2_db']['staging_schema'], # error schema
            'source_schema': udl2_conf['udl2_db']['staging_schema'], # source schema
            'db_host_source': udl2_conf['udl2_db']['db_host'],  # source database setting
            'db_port_source': udl2_conf['udl2_db']['db_port'],
            'db_user_source': udl2_conf['udl2_db']['db_user'],
            'db_name_source': udl2_conf['udl2_db']['db_database'],
            'db_password_source': udl2_conf['udl2_db']['db_pass'],
            'db_driver_source': udl2_conf['udl2_db']['db_driver'],
            'target_schema': udl2_conf['udl2_db']['integration_schema'],  # target schema
            'db_host_target': udl2_conf['udl2_db']['db_host'],  # target database setting
            'db_port_target': udl2_conf['udl2_db']['db_port'],
            'db_user_target': udl2_conf['udl2_db']['db_user'],
            'db_name_target': udl2_conf['udl2_db']['db_database'],
            'db_password_target': udl2_conf['udl2_db']['db_pass'],
            'map_type': name of map type, # name of map type. see get_column_mapping in move_to_integration/column_mapping.py
        }
    '''
    (conn, engine) = connect_db(conf['db_driver_source'],
                                conf['db_user_source'],
                                conf['db_password_source'],
                                conf['db_host_source'],
                                conf['db_port_source'],
                                conf['db_name_source'])
    map_type = conf['map_type']
    column_mapping = get_column_mapping(map_type)
    sql_query = create_migration_query(conf['source_schema'], column_mapping['source'], conf['target_schema'],
                                       column_mapping['target'], conf['error_schema'], 'ERR_LIST', column_mapping['mapping'],
                                       conf['batch_id'])
    #print(sql_query)
    except_msg = "problem when load data from staging table to integration table"
    execute_queries(conn, [sql_query], except_msg)
    return 


def create_migration_query(source_schema, source_table, target_schema, target_table,
                           error_schema, error_table, mapping, batch_id):
    '''
    Create migration script in SQL text template. It will be a tech debt to migrate it to SQLAlchemy
    equivalent. Also the code may require updates after metadata definition are finalized
    
    @param source_shema: schema name where the staging table resides
    @param source_table: table name for staging data that are cleaned
    @param target_schema: schema name where the target table resides
    @param target_table: table name for integration table that holds only correct results
    @param error_schema: schema name where error table resides
    @param error_table: table name for error tables
    @param mapping: mapping between columns in staging table, target table and rules for type conversion
    @param batch_id: batch id for specific type. 
    '''
    sql_template = """
    INSERT INTO "{target_schema}"."{target_table}"
         ({target_columns})
    SELECT {source_columns} 
        FROM "{source_schema}"."{source_table}" AS A LEFT JOIN 
        "{error_schema}"."{error_table}" AS B ON (A.record_sid = B.record_sid ) 
        WHERE B.record_sid IS NULL AND A.batch_id = \'{batch_id}\' 
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
    # place holder for execute the code as shell script
    end_time = datetime.datetime.now()