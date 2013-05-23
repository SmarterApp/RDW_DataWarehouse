import datetime
from udl2_util.database_util import connect_db, execute_queries
from move_to_integration.column_mapping import get_column_mapping

def move_data_from_staging_to_integration(conf):
    (conn, engine) = connect_db()
    map_type = 'sbac_staging_to_integration'
    column_mapping = get_column_mapping(map_type)
    move_data_from_staging_to_integration(conf)
    sql_query = ""
    except_msg = "problem when load data from staging table to integration table"
    execute_queries(conn, [sql_query], except_msg)



if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("")
    
    end_time = datetime.datetime.now()