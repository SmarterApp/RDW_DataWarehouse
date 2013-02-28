'''
benchmark.py
a command line tool to run benchmarks on the postgresql db
usage instructions: python benchmark.py -h

Runs benchmarks for the following types of comparing populations reports


main method at bottom of file

Created on Feb 21, 2013

@author: swimberly
'''

import random
import argparse

from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import select, func

from compare_populations_districts_within_state import state_statistics
from compare_populations_schools_within_district import district_statistics
from compare_populations_grades_within_school import school_statistics


def run_benchmarks(metadata, connection, schema, district_num=4, state_num=1, school_num=10):
    '''
    runs the three benchmark methods which print out their results
    also runs queries to get the id's of districts and states to run
    INPUT:
    metadata -- A SQLAlchemy metadata object that reflects the database
    connection -- A connection to the db
    schema -- the name of the schema to run queries on
    district_num -- the number of districts to run benchmarks on
    state_num -- the number of states to run benchmarks on
    school_num -- the number of schools to run benchmarks on
    '''

    # get lists of items sorted ascending by size
    states = get_state_id_list_by_size(metadata, connection)
    districts = get_district_id_list_by_size(metadata, connection)
    schools = get_school_list_by_size(metadata, connection)

    run_statistics(metadata, connection, schema, state_statistics, state_num, states, 'State')
    run_statistics(metadata, connection, schema, district_statistics, district_num, districts, 'District')
    run_statistics(metadata, connection, schema, school_statistics, school_num, schools, 'School')


def run_statistics(metadata, connection, schema, statistics_method, count_num, object_list, descriptor):
    '''
    Helper method to call the statistic methods for each of the different types of queries
    INPUT:
    metadata -- A SQLAlchemy metadata object that reflects the database
    connection -- A connection to the db
    schema -- the name of the schema to run queries on
    statistics_method -- the statistics method that will do the benchmarks to call for the given data
    count_num -- the number of times to run the benchmark
    object_list -- a list of tuples that include the id of the object to query, where an objece is a state, school or district
    descriptor -- a non-plural string that describes the objects (ie. school, state, district)
    '''

    # if count is greater the len. run stats for all items in object_list
    # otherwise for the x largest where x is count_num
    if count_num >= len(object_list):
        for obj in object_list:
            res = statistics_method(obj[0], connection, schema)
            description = descriptor + ' ' + str(obj[0])
            print_results(res, description)
    else:
        for _i in range(count_num):
            obj_id = object_list.pop(0)[0]
            res = statistics_method(obj_id, connection, schema)
            description = descriptor + ' ' + str(obj_id)
            print_results(res, description)


def get_district_id_list_by_size(metadata, connection, state_id=None):
    '''
    Queries for a list of districts sorted ascending by size
    size calculated by number of schools
    INPUT:
    metadata -- SQLAlchemy metadata object
    connection -- SQLAlchemy connection object. A connection to the db
    state_id -- optional parameter to limit the query to districts within a state
    RETURNS: district_list -- a list of districts sorted by size
    '''

    dim_district = None
    dim_school = None

    # TODO: Change to use table name as key, Will require schema name be passed in
    # Loop through table list to find desired tables
    for t in metadata.sorted_tables:
        if t.name == 'dim_district':
            dim_district = t
        elif t.name == 'dim_school':
            dim_school = t

    if dim_district is None or dim_school is None:
        raise AttributeError('metadata table list missing a desired table')

    # create select object, group by dim_district, order by number of schools
    district_select = select([dim_district.c.district_id, func.count(dim_school.c.school_id)], dim_district.c.district_id == dim_school.c.district_id)
    district_select = district_select.group_by(dim_district.c.district_id).order_by(func.count(dim_school.c.school_id))

    # add where based on state id
    if state_id:
        # add where condition to match state_id
        district_select = district_select.where(state_id == dim_school.c.district_id)

    district_list = connection.execute(district_select).fetchall()
    return district_list


def get_state_id_list_by_size(metadata, connection):
    '''
    queries for a list of states sorted by size
    size calculated by number of districts
    INPUT:
    metadata -- SQLAlchemy metadata object
    connection -- SQLAlchemy connection object. A connection to the db
    RETURNS: state_list -- a list of states sorted by the size
    '''

    dim_state = None
    dim_district = None

    # TODO: Change to use table name as key, Will require schema name be passed in
    # Loop through table list to find desired tables
    for t in metadata.sorted_tables:
        if t.name == 'dim_state':
            dim_state = t
        elif t.name == 'dim_district':
            dim_district = t

    if dim_state is None or dim_district is None:
        raise AttributeError('metadata table list missing a desired table')

    # build select statement
    state_select = select([dim_state, func.count(dim_district.c.district_id)], dim_state.c.state_id == dim_district.c.state_id)
    state_select = state_select.group_by(dim_state.c.state_id).order_by(func.count(dim_district.c.district_id))

    state_list = connection.execute(state_select).fetchall()
    return state_list


def get_school_list_by_size(metadata, connection, district_id=None, state_id=None):
    '''
    Queries for a list of school ids sorted by size.
    size is based on students
    INPUT
    metadata -- SQLAlchemy metadata object
    connection -- SQLAlchemy connection object. A connection to the db
    state_id -- the id of the state to pull the schools from if district_id provided this will be ignored
    district_id -- the id of the district to pull the schools from
    RETURNS: school_list -- a list of schools sorted by size
    '''

    dim_school = None
    dim_student = None

    # TODO: Change to use table name as key, Will require schema name be passed in
    # Loop through table list to find desired tables
    for t in metadata.sorted_tables:
        if t.name == 'dim_school':
            dim_school = t
        elif t.name == 'dim_student':
            dim_student = t

    if dim_school is None or dim_student is None:
        raise AttributeError('metadata table list missing a desired table')

    # Build select statement
    school_select = select([dim_school.c.school_id, func.count(dim_student.c.student_id)], dim_student.c.school_id == dim_school.c.school_id)
    school_select = school_select.group_by(dim_school.c.school_id).order_by(func.count(dim_student.c.student_id))

    #Specify where by district id or state id if there is no district id
    if district_id:
        school_select = school_select.where(dim_school.c.district_id == district_id)
    elif state_id:
        school_select = school_select.where(dim_school.c.state_id == state_id)

    district_list = connection.execute(school_select).fetchall()
    return district_list


def print_results(result_dict, description):
    '''
    prints the result dictionary returned by one of the statistic methods
    INPUT:
    result_dict -- dict with two items
    description -- a string to describe benchmark data ('Benchmarks for {description})
    is_verbose -- boolean flag for whether to print query results
    RETURNS: None
    '''

    num_offset = 6
    string_space = 7
    float_places = 3
    db_stats = result_dict['stats']
    benchmarks = result_dict['benchmarks']

    print('************* Benchmarks for %s *************' % description)

    #Get length of longest string, use to help with output formatting, so that columns line-up
    max_str_len = len(max((x['name'] for x in db_stats['data']), key=len))

    #loop through statistics gathered and print each one out
    for stat in db_stats['data']:
        string = '{0:{1}}{2:{3}}'.format(stat['name'] + ':', max_str_len + string_space, stat['value'], num_offset)
        print(string)

    #print out amount of time used to gather overall counts
    print('{0:{1}}{2:{3}.{4}f}s'.format('Time to run counts:', max_str_len + string_space, db_stats['query_time'], num_offset, float_places))
    print('**** Benchmarks for Queries ****')

    #Get Length of longest string and use to format output
    max_str_len = max(max_str_len, len(max((x['type'] for x in benchmarks), key=len)))

    # Loop through benchmark results and print
    for mark in benchmarks:
        string = '{0:{1}}{2:{3}.{4}f}s'.format(mark['type'], max_str_len + string_space, mark['query_time'], num_offset, float_places)
        print(string)


def get_input_args():
    '''
    Creates parser for command line args
    RETURNS vars(args) -- A dict of the command line args
    '''

    parser = argparse.ArgumentParser(description='Script to run benchmarks on predefined queries')
    parser.add_argument('server', help='server path (ie. edwdbsrv2.poc.dum.edwdc.net')
    parser.add_argument('database', help='name of the database to connect to (ie. edware)')
    parser.add_argument('username', help='username for the db')
    parser.add_argument('password', help='password for the user')
    parser.add_argument('schema', help='schema to use')
    parser.add_argument('-p', '--port', type=int, help='port to connect to. Default: 5432', default=5432)
    parser.add_argument('--state_count', help='number of states to run benchmarks on. Default: 1', default=1)
    parser.add_argument('--district_count', help='number of districts to run benchmarks on. Default: 4', default=4)
    parser.add_argument('--school_count', help='number of schools to run benchmarks on. Default: 10', default=10)
    parser.add_argument('-v', '--verbose', action='store_true', help='print out query results. NOT IMPLEMENTED YET')

    args = parser.parse_args()
    return vars(args)


def main():
    '''
    Entry point main method
    '''

    #Get command line args
    input_args = get_input_args()

    # Have SQLAlchemy connect to and reflect the database
    db_string = 'postgresql+psycopg2://{username}:{password}@{server}:{port}/{database}'.format(**input_args)
    engine = create_engine(db_string)
    db_connection = engine.connect()
    metadata = MetaData()
    metadata.reflect(engine, input_args['schema'])

    # Run benchmarks
    print("Starting Benchmarks")
    print()
    run_benchmarks(metadata, db_connection, input_args['schema'], input_args['district_count'], input_args['state_count'], input_args['school_count'])
    print()
    print("Benchmarking Complete")

    #Close db connection
    db_connection.close()

if __name__ == '__main__':
    main()
