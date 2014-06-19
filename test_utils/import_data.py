'''
Created on Mar 1, 2013

@author: dip
'''
from edschema.database.generic_connector import setup_db_connection_from_ini
import os
from edschema.database.data_importer import import_csv_dir, load_fact_asmt_outcome
import argparse
import configparser
from edschema.database.connector import DBConnection
from edschema.metadata.ed_metadata import generate_ed_metadata
from edcore.database import get_data_source_names
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection
from sqlalchemy import update


def main(config_file, resource_dir, tenant_to_update, state_code, state_name, update_year):
    '''
    Imports data from csv
    '''
    config = configparser.ConfigParser()
    config.read(config_file)

    initialize_db(EdCoreDBConnection, config['app:main'])
    for tenant in get_data_source_names():
        if tenant_to_update in tenant:
            delete_data(tenant)
            import_csv_dir(resource_dir, tenant)
            load_fact_asmt_outcome(tenant)
            update_state(tenant, state_code, state_name)
            if update_year:
                update_aca_year(tenant)


def delete_data(name):
    '''
    Delete all the data in all the tables
    '''
    with DBConnection(name) as connection:
        metadata = connection.get_metadata()
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())


def update_state(tenant, state_code, state_name):
    '''
    Update state_code in all the tables for a tenant
    '''
    with DBConnection(tenant) as connection:
        dim_inst_hier = connection.get_table("dim_inst_hier")
        custom_metadata = connection.get_table("custom_metadata")
        fact_asmt = connection.get_table("fact_asmt_outcome")
        fact_asmt_vw = connection.get_table("fact_asmt_outcome_vw")
        fact_student_reg = connection.get_table("student_reg")
        tables = [dim_inst_hier, custom_metadata, fact_asmt, fact_asmt_vw, fact_student_reg]
        for table in tables:
            stmt = update(table).values(state_code=state_code)
            connection.execute(stmt)


def update_aca_year(tenant):
    '''Update acadamic year'''
    with DBConnection(tenant) as connection:
        dim_asmt = connection.get_table("dim_asmt")
        dim_query = update(dim_asmt).where(dim_asmt.c.asmt_period_year == '2016').values({dim_asmt.c.asmt_period: 'Spring 2015',
                                                                                          dim_asmt.c.asmt_period_year: '2015',
                                                                                          dim_asmt.c.effective_date: '20150101',
                                                                                          dim_asmt.c.from_date: '20150101'})
        fact_asmt = connection.get_table("fact_asmt_outcome_vw")
        fact_query = update(fact_asmt).where(fact_asmt.c.asmt_year == '2016').values({fact_asmt.c.asmt_year: '2015',
                                                                                     fact_asmt.c.date_taken: '20150106',
                                                                                     fact_asmt.c.date_taken_day: '6',
                                                                                     fact_asmt.c.date_taken_month: '1',
                                                                                     fact_asmt.c.date_taken_year: '2015'})
        connection.execute(dim_query)
        connection.execute(fact_query)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import csv')
    parser.add_argument('-c', '--config', help='Set the path to ini file')
    parser.add_argument('-r', '--resource', help='Set path to resource directory containing csv')
    parser.add_argument('-t', '--tenant', help='Tenant to import data to', default='dog')
    parser.add_argument('-s', '--stateCode', help='StateCode to update the tenant with', default='CA')
    parser.add_argument('-n', '--stateName', help='State Name to update the tenant with', default='California')
    parser.add_argument('-u', '--updateYear', help='If set, updates year', action='store_true', default=False)
    args = parser.parse_args()

    __config = args.config
    __resource = args.resource
    __tenant = args.tenant
    __state_code = args.stateCode
    __state_name = args.stateName
    __update_year = args.updateYear

    parent_dir = os.path.abspath(os.path.join('..', os.path.dirname(__file__)))

    if __config is None:
        __config = os.path.join(os.path.join(parent_dir, 'smarter'), 'test.ini')

    if os.path.exists(__config) is False:
        print('Error: config file does not exist')
        exit(-1)

    if __resource is None:
        __resource = os.path.join(parent_dir, 'edschema', 'edschema', 'database', 'tests', 'resources')

    if os.path.exists(__resource) is False:
        print('Error: resources directory does not exist')
        exit(-1)

    main(__config, __resource, __tenant, __state_code, __state_name, __update_year)
