import datetime
from udl2_util.database_util import connect_db, execute_queries

def move_data_from_staging_to_integration(conf, src_database, src_schema, src_table, err_table,
                                          int_database, int_schema, int_table):
    (conn, engine) = connect_db()
    sql_query = ""
    except_msg = "problem when load data from staging table to integration table"
    execute_queries(conn, [sql_query], except_msg)



if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print("")
    
    end_time = datetime.datetime.now()