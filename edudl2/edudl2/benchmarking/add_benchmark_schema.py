'''
@baptel
'''
import argparse
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Boolean, BigInteger
from sqlalchemy.types import VARCHAR, TIMESTAMP, Interval, Time


def connect_db(schema, database, host, user, passwd, action, port):
    db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=user, passwd=passwd, host=host, port=port, database=database)
    engine = create_engine(db_string)
    db_connection = engine.connect()

    if action == 'setup':
        db_connection.execute(CreateSchema(schema))
        metadata = generate_table(schema_name=schema, bind=engine)
        metadata.create_all(engine)
    elif action == 'teardown':
        metadata = generate_table(schema_name=schema, bind=engine)
        metadata.drop_all(engine)
        db_connection.execute(DropSchema(schema, cascade=True))


def generate_table(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    Table('HISTORY_TABLE', metadata,
          Column('history_id', BigInteger, primary_key=True, nullable=False),
          Column('cpu_info', VARCHAR(50), nullable=False),
          Column('memory_info', VARCHAR(50), nullable=False),
          Column('last_UDL_run_date', TIMESTAMP(True), nullable=False),
          Column('UDL_completion_duration', VARCHAR(50), nullable=False),
          Column('file_size', VARCHAR(50), nullable=False)
          )
    Table('UDL_BATCH', metadata,
          Column('batch_sid', BigInteger, primary_key=True, nullable=False),
          Column('guid_batch', VARCHAR(256), nullable=False),
          Column('load_type', VARCHAR(50), nullable=True),
          Column('working_schema', VARCHAR(50), nullable=True),
          Column('udl_phase', VARCHAR(256), nullable=True),
          Column('udl_phase_step', VARCHAR(50), nullable=True),
          Column('udl_phase_step_status', VARCHAR(50), nullable=True),
          Column('udl_leaf', Boolean, nullable=True),
          Column('size_records', BigInteger, nullable=True),
          Column('size_units', BigInteger, nullable=True),
          Column('start_timestamp', TIMESTAMP(True), nullable=True),
          Column('end_timestamp', TIMESTAMP(True), nullable=True),
          Column('duration', Interval, nullable=True),
          Column('time_for_one_million_records', Time, nullable=True),
          Column('records_per_hour', BigInteger, nullable=True),
          Column('task_id', VARCHAR(256), nullable=True),
          Column('task_status_url', VARCHAR(256), nullable=True),
          Column('user_sid', BigInteger, nullable=True),
          Column('user_email', VARCHAR(256), nullable=True),
          Column('created_date', TIMESTAMP(True), nullable=True),
          Column('mod_date', TIMESTAMP(True), nullable=False)
          )

    return metadata


def add_data_to_history_table(connect_db, history_id, cpu_info, last_UDL_run_date, UDL_completion_duration, file_size):
    result = connect_db.execute('INSERT INTO udl_benchmark."HISTORY_TABLE"(history_id,last_UDL_run_date, UDL_completion_duration, file_size) VALUES(1,2,3,2013-08-9,4,5);')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create New Schema for EdWare')
    parser.add_argument("-s", "--schema", default="udl_benchmark", help="set schema name default[udl_benchmark]")
    parser.add_argument("-d", "--database", default="udl_benchmark", help="set database name default[udl_benchmark]")
    parser.add_argument("--host", default="127.0.0.1", help="postgre host default[127.0.0.1]")
    parser.add_argument("--port", default='5432', help="default port[5432")
    parser.add_argument("-u", "--user", default="edware", help="postgre username default[edware]")
    parser.add_argument("-p", "--passwd", default="edware2013", help="postgre password default[edware]")
    parser.add_argument("-a", "--action", default="setup", help="action, default is setup, use teardown to drop all tables")

    args = parser.parse_args()

    schema = args.schema
    database = args.database
    host = args.host
    user = args.user
    passwd = args.passwd
    action = args.action
    port = args.port

    connect_db(schema, database, host, user, passwd, action, port)
