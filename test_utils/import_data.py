'''
Created on Mar 1, 2013

@author: dip
'''
from database.generic_connector import setup_connection_from_ini
import os
from database.data_importer import import_csv_dir
import argparse
import configparser
from database.connector import DBConnection


def main(config_file, resource_dir):
    '''
    Imports data from csv
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    setup_connection_from_ini(config['app:main'], 'edware.db.main.')

    delete_data()
    import_csv_dir(resource_dir)


def delete_data():
    '''
    Delete all the data in all the tabls
    '''
    with DBConnection() as connection:
        metadata = connection.get_metadata()
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import csv')
    parser.add_argument('-config', help='Set the path to ini file')
    parser.add_argument('--resource', help='Set path to resource directory containing csv')
    args = parser.parse_args()

    __config = args.config
    __resource = args.resource

    if __config is None:
        print('Please specify path to ini file')
        exit(-1)

    if os.path.exists(__config) is False:
        print('Error: config file does not exist')
        exit(-1)

    if __resource is None:
        here = os.path.abspath(os.path.dirname(__file__))
        __resource = os.path.join(os.path.join(here, 'resources'))

    if os.path.exists(__resource) is False:
        print('Error: resources directory does not exist')
        exit(-1)

    main(__config, __resource)
