'''
@baptel
       '''
import argparse
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import SmallInteger, String, Boolean, Float, BigInteger


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

    history_table = Table('history_table', metadata,
                               Column('cpu_info', String(32), nullable=False),
                               Column('memory_info', String(20), nullable=False),
                               Column('last_UDL_run_date', String(12), nullable=False),
                               Column('UDL_completion_duration', String(20), nullable=False),
                               Column('file_size', String(20), nullable=False)
                                 )
    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create New Schema for EdWare')
    parser.add_argument("-s", "--schema", help="set schema name.  required", required=True)
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
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
