'''
Created on Mar 12, 2013

@author: swimberly
'''

import os
import re
import subprocess
import time
import argparse

from sqlalchemy import create_engine, MetaData

__all__ = ['load_csvs_to_database']


def load_csvs_to_database(schema, passwd, csvdir=None, database='edware', host='127.0.0.1', user='edware', port=5432):
    '''
    Entry point for this being used as a module
    INPUT:
    schema -- the name of the schema to use
    passwd -- the password to use to connect to the db
    csvdir -- the directory that contains the csv files. If no directory provided assumes the current working directory
    database -- the name of the database to use
    host -- the host address or name
    user -- the username to be used
    port -- the port to use when connecting to the db
    '''
    input_args = {
        'schema': schema,
        'passwd': passwd,
        'csvdir': csvdir,
        'database': database,
        'host': host,
        'user': user,
        'port': port
    }

    load_data(input_args)


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _err = proc.communicate()
    return out


def get_input_args():
    '''
    Creates parser for command line args
    RETURNS vars(args) -- A dict of the command line args
    '''
    parser = argparse.ArgumentParser(description='Script to load csv files to a db schema')
    parser.add_argument("schema", help="set schema name.  required")
    parser.add_argument("passwd", help="postgre password")
    parser.add_argument("-c", "--csvdir", default=None, help="The directory where the csv's are stored. If not specified it will assume you are already there")
    parser.add_argument("-d", "--database", default="edware", help="set database name default[edware]")
    parser.add_argument("--host", default="127.0.0.1", help="postgres host default[127.0.0.1]")
    parser.add_argument("-u", "--user", default="edware", help="postgre username default[edware]")
    parser.add_argument("--port", default=5432, help="postgres port default[5432]")
    parser.add_argument("-t", "--truncate", action='store_true', help='if flag is set will remove all data from tables before loading data')

    args = parser.parse_args()
    return vars(args)


def set_postres_passwd(host, database, user, passwd, directory, port=5432):
    '''
    Create the '~/.pgpass' file and set necessary attributes to allow
    connection to the postgres db
    INPUT:
    host -- should be or format host (ie "127.0.0.1")
    database -- database to use
    user -- username
    passwd -- password to set
    directory -- the directory to store the pgpass file
    port -- the port to use for postgres
    RETURNS:
    filename -- the name and path to the file
    '''

    string = '{host}:{port}:{db}:{user}:{passwd}'.format(host=host, port=port, db=database, user=user, passwd=passwd)
    filename = os.path.join(directory, 'tmppgpass')

    with open(filename, 'w') as f:
        f.write(string)

    system('chmod', '600', filename)

    return filename


def get_table_order(input_args):
    '''
    Connect to the db and get the tables for the given schema
    RETURN:
    table_names -- a list of table names ordered by foreign key dependency
    '''

    db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(**input_args)
    engine = create_engine(db_string)
    metadata = MetaData()
    metadata.reflect(engine, input_args['schema'])

    table_names = [x.name for x in metadata.sorted_tables]
    return table_names


def load_data(input_args):
    '''
    Main method for all the work that is to be done.
    INPUT:
    input_args -- a dictionary of all of the parameters received by the arg parser
    '''
    csvpath = input_args.get('csvdir')

    if not csvpath:
        csvpath = os.getcwd()

    csvs = re.compile(b'(?P<name>.*\.csv)', re.MULTILINE)
    files = system('ls', '-1', csvpath)
    files = csvs.findall(files)

    if not files:
        raise AttributeError('There are no CSV files in this Directory: %s' % csvpath)

    pgpass_file = set_postres_passwd(input_args['host'], input_args['database'], input_args['user'], input_args['passwd'], csvpath, input_args['port'])
    env = dict(os.environ)
    env['PGPASSFILE'] = pgpass_file

    ordered_tables = get_table_order(input_args)

    #transform names from byte strings to strings
    files = [x.decode("utf-8") for x in files]

    fileset = {x.split('.')[0] for x in files}
    missing_tables = fileset ^ set(ordered_tables)

    if missing_tables:
        raise AttributeError('The following table(s) are not present in one of the locations %s' % missing_tables)

    # truncate tables
    if input_args['truncate']:
        for table in ordered_tables:
            truncate_string = "TRUNCATE {schema}.{name} CASCADE".format(schema=input_args['schema'], name=table)
            system('psql', '-U', input_args['user'], '-h', input_args['host'], '-d', input_args['database'], '-c', truncate_string, env=env)

    for table in ordered_tables:
        filename = os.path.join(csvpath, table + '.csv')
        copy_string = "\copy {schema}.{name} from {filename} USING DELIMITERS ',' CSV HEADER".format(schema=input_args['schema'], name=table, filename=filename)

        start = time.time()
        print('Loading table:', table)

        # Load data from csv using psql \copy command
        system('psql', '-U', input_args['user'], '-h', input_args['host'], '-d', input_args['database'], '-c', copy_string, env=env)
        tot_time = time.time() - start
        print('Loaded table: %s in %.2f' % (table, tot_time))
        print()
        break

    os.remove(pgpass_file)


if __name__ == '__main__':
    load_data(get_input_args())
