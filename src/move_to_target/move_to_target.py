import move_to_target.column_mapping as col_map
from fileloader.file_loader import connect_db
import datetime

DBDRIVER = "postgresql+pypostgresql"


def explode_data_to_target(conf):
    """
    This function will NOT be used in Celery Worker. It is used from main in this script
    This function starts to explode dim and fact table to target (star schema)
    The equivalent component is the W_move_to_target.py which is used in UDL pipeline framework
    """
    # connect to db
    conn, _engine = connect_db(conf)

    # copy data from integration table to dim tables
    column_map = col_map.get_column_mapping()
    for target_table in col_map.get_target_tables_parallel():
        explode_data_to_one_table(conn, conf['source_table'], target_table, column_map[target_table])

    # copy data from integration table to fact table
    target_table = col_map.get_target_table_callback()
    explode_data_to_one_table(conn, conf['source_table'], target_table, column_map[target_table])

    # close db connection
    conn.close()


def explode_data_to_one_table(conf, target_table, column_mapping):
    '''
    Will use parameters passed in to create query with sqlalchemy
    '''
    print("In explode_data_to_one_table****, %s, %s" % (str(conf), str(target_table)))
    # create db connection

    # create insertion query
    query = create_insert_query(conf['batch_id'], conf['source_schema'], conf['source_table'], conf['target_schema'], target_table, column_mapping)

    # execute the query
    print(query)


def create_insert_query(batch_id, source_schema, source_table, target_schema, target_table, column_mapping):
    print("Is here ***************")
    insert_sql = ["INSERT INTO \"{target_schema}\".\"{target_table}\"(",
             ",".join(column_mapping.keys()),
             ") SELECT ",
             ",".join(column_mapping.values()),
             " FROM \"{source_schema}\".\"{source_table}\" WHERE batch_id={batch_id}",
            ]
    insert_sql = "".join(insert_sql).format(target_schema=target_schema, target_table=target_table, source_schema=source_schema, source_table=source_table, batch_id=batch_id)
    return insert_sql


if __name__ == "__main__":
    conf = {
            # TBD
            'source_table': 'INT_SBAC_ASMT_OUTCOME',
            'source_schema': 'udl2',
            'target_schema': 'udl2',

            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'udl2',
            'db_name': 'udl2',
            'db_password': 'udl2abc1234',
    }
    start_time = datetime.datetime.now()
    # main function to move data from integration table to target(star schema)
    explode_data_to_target(conf)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time
    print("\nSpend time --", spend_time)
