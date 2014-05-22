'''
Created on Jun 19, 2013

@author: tosako
'''
import argparse
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema
from edschema.metadata.ed_metadata import generate_ed_metadata
from edschema.metadata.stats_metadata import generate_stats_metadata

DBDRIVER = "postgresql+pypostgresql"
DEBUG = 0
VERBOSE = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create New Schema for EdWare')
    parser.add_argument("-s", "--schema", help="set schema name.  required")
    parser.add_argument("-m", "--metadata", help="edware or stats")
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
    parser.add_argument("--host", default="127.0.0.1:5432", help="postgre host default[127.0.0.1:5432]")
    parser.add_argument("-u", "--user", default="edware", help="postgre username default[edware]")
    parser.add_argument("-p", "--passwd", default="edware", help="postgre password default[edware]")
    parser.add_argument("-a", "--action", default="setup", help="action, default is setup, use teardown to drop all tables")

    args = parser.parse_args()

    __schema = args.schema
    __metadata = args.metadata
    __database = args.database
    __host = args.host
    __user = args.user
    __passwd = args.passwd
    __action = args.action

    if __metadata is None:
        print('Please specify --metadata option')
        exit(-1)
    else:
        if __metadata != 'edware' and __metadata != "stats":
            print('Please specify edware or udl_stats for -m or --metadata')
    if __schema is None:
        print("Please specify --schema option")
        exit(-1)
    __URL = DBDRIVER + "://" + __user + ":" + __passwd + "@" + __host + "/" + __database
    print("DB Driver:" + DBDRIVER)
    print("     User:" + __user)
    print("  Password:" + __passwd)
    print("      Host:" + __host)
    print("  Database:" + __database)
    print("    Schema:" + __schema)
    print("####################")
    engine = create_engine(__URL, echo=True)
    connection = engine.connect()

    if __action == 'setup':
        connection.execute(CreateSchema(__schema))
        if __metadata == 'edware':
            metadata = generate_ed_metadata(schema_name=__schema, bind=engine)
            connection.execute('CREATE SEQUENCE "' + __schema + '"."global_udl2_seq"')
        else:
            metadata = generate_stats_metadata(schema_name=__schema, bind=engine)
        metadata.create_all(engine)
    elif __action == 'teardown':
        metadata = generate_ed_metadata(schema_name=__schema, bind=engine)
        metadata.drop_all(engine)
        connection.execute(DropSchema(__schema, cascade=True))
