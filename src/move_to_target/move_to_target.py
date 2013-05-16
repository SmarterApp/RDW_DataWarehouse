import src.move_to_target.column_mapping as col_map
import src.fileloader.file_loader.connect_db as connect_db
import datetime

DBDRIVER = "postgresql+pypostgresql"


def explode_data_to_target(conf):
    # connect to db
    conn, _engine = connect_db(conf)

    # copy data from integration table to dim tables
    column_map = col_map.get_column_mapping()
    for target_table in col_map.get_target_tables_parallel():
        explode_table_to_one_table(conn, conf['source_table'], target_table, column_map[target_table])

    # copy data from integration table to fact table
    target_table = col_map.get_target_table_callback()
    explode_table_to_one_table(conn, conf['source_table'], target_table, column_map[target_table])

    # close db connection
    conn.close()


def explode_table_to_one_table(conn, source_table, target_table, column_mapping):
    '''
    Will use parameters passed in to create query with sqlalchemy
    '''
    pass


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
