'''
load_data.py
Script for loading csv's to a database schema.

main at bottom of page
If module is being imported use:
load_csvs_to_database()

Created on Mar 12, 2013

@author: swimberly
'''

import os
import re
import subprocess
import time
import argparse
import csv

from sqlalchemy import create_engine, MetaData

__all__ = ['load_csvs_to_database']


def load_csvs_to_database(schema, passwd, csvdir=None, database='edware', host='127.0.0.1', user='edware', port=5432, truncate=False):
    '''
    Entry point for this being used as a module
    @param schema: the name of the schema to use
    @param passwd: the password to use to connect to the db
    @param csvdir: the directory that contains the csv files. If no directory provided assumes the current working directory
    @param database: the name of the database to use
    @param host: the host address or name
    @param user: the username to be used
    @param port: the port to use when connecting to the db
    @param truncate: truncate the tables before doing data load
    @return: None
    '''
    input_args = {
        'schema': schema,
        'passwd': passwd,
        'csvdir': csvdir,
        'database': database,
        'host': host,
        'user': user,
        'port': port,
        'truncate': truncate
    }

    load_data_main(input_args)


def system(*args, **kwargs):
    '''
    Method for running system calls
    Taken from the pre-commit file for python3 in the scripts directory
    '''
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _err = proc.communicate()
    return out


def get_input_args():
    '''
    Creates parser for command line args
    @return: vars(args) -- A dict of the command line args
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


def setup_pg_passwd_file(host, database, user, passwd, directory, port=5432):
    '''
    Create the '~/.pgpass' file and set necessary attributes to allow
    connection to the postgres db
    @param host: should be or format host (ie "127.0.0.1")
    @param database: database to use
    @param user: username
    @param passwd: password to set
    @param directory: the directory to store the pgpass file
    @param port: the port to use for postgres
    @return: env -- the dict containing the environment vars to use when running psql command
    '''

    string = '{host}:{port}:{db}:{user}:{passwd}'.format(host=host, port=port, db=database, user=user, passwd=passwd)
    filename = os.path.join(directory, 'tmppgpass')

    with open(filename, 'w') as f:
        f.write(string)

    system('chmod', '600', filename)

    env = dict(os.environ)
    env['PGPASSFILE'] = filename

    return env


def remove_pg_passwd_file(filename):
    '''
    Cleanup: remove the file used to store the pg password
    @param filename: the name (path) of the pgpass file to remove
    @return: None
    '''
    try:
        os.remove(filename)
    except FileNotFoundError:
        print('Unable to locate file %s, the file may still remain.' % filename)
        print('Consider removing manually.')


def get_table_order(host, database, user, passwd, schema, port=5432):
    '''
    Connect to the db and get the tables for the given schema
    @param schema: value which identify a specific database instance
    @param user: value which identify a specific database instance
    @param host: value which identify a specific database instance
    @param database: value which identify a specific database instance
    @param passwd: value which identify a specific database instance
    @param port: value which identify a specific database instance
    @return: table_names -- a list of table names ordered by foreign key dependency
    '''

    db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=user, passwd=passwd, host=host, port=port, database=database)
    engine = create_engine(db_string)
    metadata = MetaData()
    metadata.reflect(engine, schema)

    table_names = [x.name for x in metadata.sorted_tables]
    return table_names


def get_csv_list(csvpath):
    '''
    Gets the list of csv files in the specified directory
    @param csvpath: path to search for *.csv files : if not specified assumed to be current directory
    @return: csvpath, files -- csvpath: see above, files: list of file names found in csvpath which end with '.csv' : NOTE '.csv' is trimmed off
    @raise AttributeError: There are no CSV files in this Directory
    '''

    if not csvpath:
        csvpath = os.getcwd()

    csvs = re.compile(b'(?P<name>.*\.csv)', re.MULTILINE)
    files = system('ls', '-1', csvpath)
    files = csvs.findall(files)

    if not files:
        raise AttributeError('There are no CSV files in this Directory: %s' % csvpath)

    #transform names from byte strings to strings and remove '.csv'
    files = [x.decode("utf-8").split('.')[0] for x in files]

    return files, csvpath


def truncate_db_tables(tables, schema, user, host, database, env):
    '''
    truncate all the tables in the list of tables
    Within the identified database instance, all tables named in the supplied list ('tables') are truncated
    @param tables: list of table names
    @param schema: value which identify a specific database instance
    @param user: value which identify a specific database instance
    @param host: value which identify a specific database instance
    @param database: value which identify a specific database instance
    @return: None
    '''

    for table in tables:
        truncate_string = "TRUNCATE {schema}.{name} CASCADE".format(schema=schema, name=table)
        system('psql', '-U', user, '-h', host, '-d', database, '-c', truncate_string, env=env)


def copy_db_tables(tables, csvpath, schema, user, host, database, env):
    '''
    run psql copy command for each of the tables in the list
    Data is copied to the database instance for each table supplied in the ('tables') list
    @param tables: list of table names
    @param schema: values which identify a specific database instance
    @param user: values which identify a specific database instance
    @param host: values which identify a specific database instance
    @param database: values which identify a specific database instance
    @return: None
    '''

    for table in tables:
        filename = os.path.join(csvpath, table + '.csv')

        # Check that the csv exists
        try:
            with open(filename, 'r') as fp:
                csv_reader = csv.reader(fp)
                column_list_str = str(tuple(next(csv_reader)))
                column_list_str = column_list_str.replace("'", "")
        except IOError:
            print("Skipping file load to '%s'. No CSV file found" % table)
            continue

        copy_string = "\copy {schema}.{name} {col_list} from {filename} USING DELIMITERS ',' CSV HEADER".format(schema=schema, name=table, filename=filename, col_list=column_list_str)
        #print('copy_string:', copy_string)
        start = time.time()
        print('Loading table:', table)

        # Load data from csv using psql \copy command
        system('psql', '-U', user, '-h', host, '-d', database, '-c', copy_string, env=env)
        tot_time = time.time() - start
        print('Loaded table: %s in %.2f' % (table, tot_time))
        print()


def load_data_main(csvdir, host, database, user, passwd, schema, port=5432, truncate=False):
    '''
    Main method for all the work that is to be done.
    @param input_args: a dictionary of all of the parameters received by the arg parser
    @return: None
    @raise AttributeError: The following table(s) are not present in one of the locations
    '''

    # get csv file names and the path to csvs
    try:
        csv_file_names, csvpath = get_csv_list(csvdir)
    except AttributeError:
        exit('Unable to locate any csv files')

    # get a copy of the environment that includes 'PGPASSFILE' that points to the new password file
    env = setup_pg_passwd_file(host, database, user, passwd, csvpath, port)

    # get an ordered list of tables
    ordered_tables = get_table_order(host, database, user, passwd, schema, port)

    # truncate tables
    if truncate:
        truncate_db_tables(ordered_tables, schema, user, host, database, env)

    # copy csvs to tables
    copy_db_tables(ordered_tables, csvpath, schema, user, host, database, env)

    # clean up
    remove_pg_passwd_file(env['PGPASSFILE'])

    print('Data Load Complete')


if __name__ == '__main__':
    input_args = get_input_args()
    load_data_main(input_args['csvdir'], input_args['host'], input_args['database'], input_args['user'], input_args['passwd'], input_args['schema'], input_args['port'], input_args['truncate'])
