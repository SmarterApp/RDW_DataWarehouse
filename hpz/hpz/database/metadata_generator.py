__author__ = 'tshewchuk'
"""
This module sets up/tears down the HPZ database.
"""

import argparse
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import CreateSchema, DropSchema
from hpz.database.metadata import generate_metadata

DBDRIVER = "postgresql+pypostgresql"
DEBUG = 0
VERBOSE = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create New Schema for HPZ')
    parser.add_argument("-s", "--schema", help="set schema name.  required")
    parser.add_argument("-m", "--metadata", help="hpz")
    parser.add_argument("-d", "--database", default="hpz", help="set database name default[hpz]")
    parser.add_argument("--host", default="127.0.0.1:5432", help="postgre host default[127.0.0.1:5432]")
    parser.add_argument("-u", "--user", default="hpz", help="postgre username default[hpz]")
    parser.add_argument("-p", "--passwd", default="hpz", help="postgre password default[hpz]")
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
        if __metadata != 'hpz':
            print('Please specify hpz for -m or --metadata')
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
    print("       URL:" + __URL)
    print("####################")
    engine = create_engine(__URL, echo=True)
    connection = engine.connect()

    if __action == 'setup':
        connection.execute(CreateSchema(__schema))
        metadata = generate_metadata(schema_name=__schema, bind=engine)
        metadata.create_all(engine)
    elif __action == 'teardown':
        metadata = generate_metadata(schema_name=__schema, bind=engine)
        metadata.drop_all(engine)
        connection.execute(DropSchema(__schema, cascade=True))
