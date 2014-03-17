'''
Created on Mar 1, 2013

@author: dip
'''
from edschema.database.generic_connector import setup_db_connection_from_ini
import os
from edschema.database.data_importer import import_csv_dir
import argparse
import configparser
from edschema.database.connector import DBConnection
from edschema.metadata.ed_metadata import generate_ed_metadata
from edcore.database import get_data_source_names
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection
from sqlalchemy import update


def main(config_file, resource_dir, tenant_to_update, state_code):
    '''
    Imports data from csv
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    initialize_db(EdCoreDBConnection, config['app:main'])
    for tenant in get_data_source_names():
        delete_data(tenant)
        import_csv_dir(resource_dir, tenant)
        if tenant_to_update in tenant:
            update_state_code(tenant, state_code)


def delete_data(name):
    '''
    Delete all the data in all the tabls
    '''
    with DBConnection(name) as connection:
        metadata = connection.get_metadata()
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())


def update_state_code(tenant, state_code):
    '''
    Update state_code in all the tables for a tenant
    '''
    with DBConnection(tenant) as connection:
        dim_inst_hier = connection.get_table("dim_inst_hier")
        dim_section = connection.get_table("dim_section")
        custom_metadata = connection.get_table("custom_metadata")
        fact_asmt = connection.get_table("fact_asmt_outcome")
        dim_student = connection.get_table("dim_student")
        fact_student_reg = connection.get_table("student_reg")
        tables = [dim_inst_hier, dim_section, custom_metadata, fact_asmt, dim_student, fact_student_reg]
        for table in tables:
            stmt = update(table).values(state_code=state_code)
            connection.execute(stmt)
        state_name_stmt = update(dim_inst_hier).values(state_name='California')
        connection.execute(state_name_stmt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import csv')
    parser.add_argument('-c', '--config', help='Set the path to ini file')
    parser.add_argument('-r', '--resource', help='Set path to resource directory containing csv')
    parser.add_argument('-t', '--tenant', help='Update stateCode for tenant')
    parser.add_argument('-s', '--stateCode', help='StateCode to update with')
    args = parser.parse_args()

    __config = args.config
    __resource = args.resource
    __tenant = args.tenant
    __state_code = args.stateCode

    parent_dir = os.path.abspath(os.path.join('..', os.path.dirname(__file__)))

    if __config is None:
        __config = os.path.join(os.path.join(parent_dir, 'smarter'), 'test.ini')

    if os.path.exists(__config) is False:
        print('Error: config file does not exist')
        exit(-1)

    if __resource is None:
        __resource = os.path.join(os.path.join(os.path.join(os.path.join(parent_dir, 'edschema'), 'edschema', 'database'), 'tests'), 'resources')

    if os.path.exists(__resource) is False:
        print('Error: resources directory does not exist')
        exit(-1)

    if __tenant is None:
        __tenant = 'dog'

    if __state_code is None:
        __state_code = 'CA'

    main(__config, __resource, __tenant, __state_code)
