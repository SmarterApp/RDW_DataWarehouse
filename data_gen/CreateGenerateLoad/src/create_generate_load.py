'''
Created on May 13, 2013

@author: swimberly
'''

from argparse import ArgumentParser
from importlib import import_module
import time
import os
import inspect
import subprocess

import DataGeneration.src.generate_data as generate_data
import dataload.load_data as load_data
import datainfo.best_worst_results as best_worst_results
import Henshin.src.henshin as henshin
# import load_data
# import best_worst_results
# import henshin

CMD_FOLDER = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
DATA_GEN_OUTPUT = os.path.join(CMD_FOLDER, 'datafiles')
EDSCHEMA_PATH = os.path.join(CMD_FOLDER, '..', '..', '..', 'edschema', 'edschema', 'metadata_generator.py')

HENSHIN_FOLDER = os.path.join(CMD_FOLDER, '../../', 'Henshin', 'src')
DATA_LOAD_FOLDER = os.path.join(CMD_FOLDER, '../../', 'DataGeneration', 'dataload')
DATA_INFO_MODULE = 'datainfo.best_worst_results'
LOAD_DATA_MODULE = 'load_data'
HENSHIN_MODULE = 'henshin'


def main(schema, database, host, user, passwd, port=5432, create=True, landing_zone=True, best_worst=True, config_file=None, data_gen_output=None, pld_off=False, generated_path=None):
    '''
    Main function to chain these processes in sequence:
    0. generate schema if the given create = True
    1. generate data by running data generator
    2. load generated data into given database and schema
    3. create landing zone files by running Henshin for the generated data
    4. report on data performance results
    '''
    start_time = time.time()
    if create is True:
        print('Step 0 -- Creating schema "%s" in database "%s" at "%s"' % (schema, database, host))
        create_schema(schema, database, host, user, passwd)

    csv_dir = generated_path
    print(csv_dir)
    if not csv_dir:
        print('Step 1 -- Generating New Data')
        csv_dir = generate_data_to_csv(config_file, pld_off)

    print('Step 2 -- Loading New Data into star schema')
    load_data_to_db(csv_dir, schema, database, host, user, passwd, port)

    if landing_zone is True:
        print('\nStep 3 -- Transforming generated data to landing zone format')
        transform_to_landing_zone(csv_dir, schema, database, host, user, passwd, port)

    if best_worst:
        print('\nStep 4 -- Getting Best and worst assessment performances')
        get_data_info(schema, database, host, user, passwd, port)

    tot_time = time.time() - start_time
    print('All steps completed in %.2fs' % tot_time)


def create_schema(schema_name, database, host, user, passwd):
    output = system('python', EDSCHEMA_PATH, '-s', schema_name, '-d', database, '--host', host, '-u', user, '-p', passwd, '-m', 'edware')
    print(output.decode('UTF-8'))


def generate_data_to_csv(config_file=None, pld_off=False):
    '''
    generate data by calling the generate data script.
    '''
    print('Generating Data')

    do_pld_adjustment = not pld_off

    if config_file:
        gen_data_output = generate_data.main(config_mod_name=config_file, output_path=DATA_LOAD_FOLDER, do_pld_adjustment=do_pld_adjustment)
        # output = system('python', gen_data_loc, '--config', config_file)
    else:
        gen_data_output = generate_data.main(output_path=DATA_LOAD_FOLDER, do_pld_adjustment=do_pld_adjustment)
        # output = system('python', gen_data_loc)

    # print(output.decode('UTF-8'))
    print('\nData Generation Complete\n')
    return gen_data_output


def load_data_to_db(csv_dir, schema, database, host, user, passwd, port):
    '''
    Load data into schema
    '''
    load_data.load_data_main(csv_dir, host, database, user, passwd, schema, port=port, truncate=True)


def get_data_info(schema, database, host, user, passwd, port):
    '''
    run the data info script
    '''
    best_worst_results.main(password=passwd, schema=schema, server=host, database=database, username=user, port=port)
#     data_info_path = os.path.join(CMD_FOLDER, '..', '..', 'DataGeneration', 'dataload', 'datainfo', 'best_worst_results.py')
#
#     output = system('python', data_info_path, '--password', passwd, '--schema', schema, '-s', host, '-d', database, '-u', user, '--csv', '--bestworst')
#     print(output.decode('UTF-8'))


def transform_to_landing_zone(csv_dir, schema, database, host, user, passwd, port):
    '''
    Call the Henshin script. Return the path to the output.
    '''
    # henshin_path = os.path.join(CMD_FOLDER, '..', '..', 'Henshin', 'src', 'henshin.py')
    output_path = os.path.join(CMD_FOLDER, 'henshin_out')
    dim_asmt_path = os.path.join(csv_dir, 'dim_asmt.csv')
    print("Henshin output path: %s" % output_path)

    henshin.henshin(dim_asmt_path, user, passwd, host, database, schema, output_path)

    # output = system('python', henshin_path, '-d', dim_asmt_path, '-o', output_path, '--password', passwd, '--schema', schema, '--host', host, '--database', database, '-u', user)
    # print(output.decode('UTF-8'))
    # return output_path


def get_input_args():
    '''
    Creates parser for command line args
    @return: args A namespace of the command line args
    '''

    parser = ArgumentParser(description='Script to get best or worst Students, Districts and Schools')
    parser.add_argument('-c', '--create', action='store_true', help='create a new schema')
    parser.add_argument('-l', '--landing-zone', action='store_true', help='flag generate landing zone file format')
    parser.add_argument('-b', '--best-worst', action='store_true', help='flag to create csv files that show the best and worst performers in the data')
    parser.add_argument('-s', '--schema', required=True, help='the name of the schema to use')
    parser.add_argument('-d', '--database', default='edware', help='the name of the database to connect to. Default: "edware"')
    parser.add_argument('-u', '--username', default='edware', help='the username for the database')
    parser.add_argument('-p', '--passwd', default='edware', help='the password to use for the database')
    parser.add_argument('--pld-off', action='store_true', help='Whether to not apply the performance level adjustments')
    parser.add_argument('--host', default='localhost', help='the host to connect to. Default: "localhost"')
    parser.add_argument('--port', default=5432, help='the port number')
    parser.add_argument('--data-gen-config-file', default='DataGeneration.src.dg_types',
                        help='a configuration file to use for data generation default: "datageneration.src.dg_types"')
    parser.add_argument('--generated-csv-path', default=None,
                        help='if the csv files have already been generated specify the path here, No new files will be generated')

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
    main(input_args.schema, input_args.database, input_args.host, input_args.username, input_args.passwd, input_args.port, input_args.create,
         input_args.landing_zone, input_args.best_worst, input_args.data_gen_config_file, pld_off=input_args.pld_off, generated_path=input_args.generated_csv_path)
