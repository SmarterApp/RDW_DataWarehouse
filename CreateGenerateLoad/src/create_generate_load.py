'''
Created on May 13, 2013

@author: swimberly
'''

from argparse import ArgumentParser
from importlib import import_module
import time
import os
import sys
import inspect
import subprocess

DATA_INFO_MODULE = 'DataGeneration.dataload.datainfo'
LOAD_DATA_MODULE = 'DataGeneration.dataload'
DATA_GENERATION_MODULE = 'DataGeneration.src'
HENSHIN_MODULE = 'Henshin.src'


def main(schema, database, host, user, passwd, port=5432, create=True, landing_zone=True, best_worst=True, config_file=None):
    '''
    '''
    start_time = time.time()

    if create:
        print('Creating schema "%s" in database "%s" at "%s"' % (schema, database, host))
        create_schema(schema, database, host, user, passwd)

    print('Generating New Data')
    generate_data(config_file)

    print('Loading New Data')
    csv_dir = 'tbd'
    load_data(csv_dir, schema, database, host, user, passwd, port)

    print('Transforming to landing zone')
    transform_to_landing_zone(csv_dir, schema, database, host, user, passwd, port)

    print('Getting Best and worst assessment performances')
    get_data_info(schema, database, host, user, passwd, port)

    tot_time = time.time() - start_time
    print('All steps completed in %.2fs' % tot_time)


def create_schema(schema_name, database, host, user, passwd):
    print('cloning edware repo to run the ed_schema code')
    folder = get_ed_schema_code()
    ed_schema_file = os.path.join(folder, 'edware', 'edschema', 'edschema', 'ed_metadata.py')
    system('python', ed_schema_file, '-s', schema_name, '-d', database, '--host', host, '-u', user, '-p', passwd)


def generate_data(config_file=None):
    pass


def load_data(csv_dir, schema, database, host, user, passwd, port):
    pass


def get_data_info(schema, database, host, user, passwd, port):
    pass


def transform_to_landing_zone(csv_dir, schema, database, host, user, passwd, port):
    pass


def get_input_args():
    '''
    Creates parser for command line args
    @return: args A namespace of the command line args
    '''

    parser = ArgumentParser(description='Script to get best or worst Students, Districts and Schools')
    parser.add_argument('-c', '--create', action='store_true', help='create a new schema')
    parser.add_argument('-l', '--landing-zone', action='store_true', help='flag generate landing zone file format')
    parser.add_argument('-b', '--best-worst', action='store_true', help='flag to create csv files that show the best and worst performers in the data')
    parser.add_argument('-s', '--schema', help='the name of the schema to use')
    parser.add_argument('-d', '--database', default='edware', help='the name of the database to connect to. Default: "edware"')
    parser.add_argument('-u', '--username', default='edware', help='the username for the database')
    parser.add_argument('-p', '--passwd', default='edware', help='the password to use for the database')
    parser.add_argument('--host', default='localhost', help='the host to connect to. Default: "localhost"')
    parser.add_argument('--port', default=5432, help='the port number')
    parser.add_argument('--data-gen-config-file', help='a configuration file to use for data generation')

    return parser.parse_args()


def get_ed_schema_code(tmp_folder='ed_schema_temp'):
    '''
    Clone edware repository so that the schema creation can be done.
    @keyword tmp_folder: the name of the directory to store the edware repo
    @return: tmp_folder -- the name of the folder where the folder was clone
    '''
    repo_path = 'git@github.wgenhq.net:Ed-Ware-SBAC/edware.git'
    system('git', 'clone', repo_path, tmp_folder)
    return tmp_folder


def system(*args, **kwargs):
    '''
    Method for running system calls
    Taken from the pre-commit file for python3 in the scripts directory
    '''
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _err = proc.communicate()
    return out


if __name__ == '__main__':
    input_args = get_input_args()
    #main(input_args.schema, input_args.database, input_args.host, input_args.user, input_args.passwd, input_args.port, input_args.create, input_args.landing_zone, input_args.best_worst, input_args.data_gen_config_file)
    cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
    cmd_folder = cmd_folder.replace('CreateGenerateLoad/src', '')
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)
        load_data_module = import_module(LOAD_DATA_MODULE)
        data_info_module = import_module(DATA_INFO_MODULE)
        data_gen_module = import_module(DATA_GENERATION_MODULE, 'src.generate_data')
        henshin_module = import_module(HENSHIN_MODULE)
        data_gen_module.generate_data.generate_data_from_config_file('dg_types')
        print(load_data_module, data_info_module, data_gen_module, henshin_module, sep='\n')
    print(cmd_folder)
