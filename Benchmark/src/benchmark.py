'''
benchmark.py
a command line tool to run benchmarks on the postgresql db
usage instructions: python benchmark.py -h

Runs benchmarks for the following types of comparing populations reports


main method at bottom of file

Created on Feb 21, 2013

@author: swimberly
'''

from datetime import date
import argparse
import locale

from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import select, func

from compare_populations_districts_within_state import state_statistics
from compare_populations_schools_within_district import district_statistics
from compare_populations_grades_within_school import school_statistics


def run_benchmarks(metadata, connection, schema, is_verbose, district_num=1, state_num=1, school_num=1, as_csv=False):
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

    # check for is_verbose.
    # If is_verbose is not true but the number of queries to run for any of the objects is greater than 1
    # set is_verbose to true
    if not is_verbose:
        if not (district_num == state_num == school_num == 1):
            is_verbose = True

    # get lists of items sorted ascending by size
    states = get_state_id_list_by_size(metadata, connection)
    districts = get_district_id_list_by_size(metadata, connection)
    schools = get_school_list_by_size(metadata, connection)

    db_stats = get_database_statistics(metadata, connection, schema)

    # print out the database stats if verbose mode is on
    if is_verbose:
        print_db_stats(db_stats)

    state_results = run_statistics(metadata, connection, schema, state_statistics, state_num, states, is_verbose)
    district_results = run_statistics(metadata, connection, schema, district_statistics, district_num, districts, is_verbose)
    school_results = run_statistics(metadata, connection, schema, school_statistics, school_num, schools, is_verbose)

    if len(state_results) == len(district_results) == len(school_results) == 1:
        total_time = state_results[0]['benchmarks']['total_time']
        total_time += district_results[0]['benchmarks']['total_time']
        total_time += school_results[0]['benchmarks']['total_time']

        print_short_result(total_time, db_stats, state_results[0], district_results[0], school_results[0], as_csv)


def run_statistics(metadata, connection, schema, statistics_method, count_num, object_list, is_verbose):
    '''
    Helper method to call the statistic methods for each of the different types of queries
    INPUT:
    metadata -- A SQLAlchemy metadata object that reflects the database
    connection -- A connection to the db
    schema -- the name of the schema to run queries on
    statistics_method -- the statistics method that will do the benchmarks to call for the given data
    count_num -- the number of times to run the benchmark
    object_list -- a list of tuples that include the id of the object to query, where an objece is a state, school or district
    RETURNS: res_list -- a list of the results received during the queries.
    '''

    res_list = []
    # if count is greater the len. run stats for all items in object_list
    # otherwise for the x largest where x is count_num
    if count_num >= len(object_list):
        for obj in object_list:
            res = statistics_method(obj[0], connection, schema)
            res_list.append(res)
            if is_verbose:
                print_results(res)
    else:
        for i in range(count_num):
            obj_id = object_list[i][0]
            res = statistics_method(obj_id, connection, schema)
            res_list.append(res)
            if is_verbose:
                print_results(res)

    return res_list


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


def get_database_statistics(metadata, connection, schema):
    '''
    Get statistics for the database, including:
    number of states, number of schools, number of students, number of districts
    INPUT:
    metadata -- SQLAlchemy metadata object
    connection -- SQLAlchemy connection object. A connection to the db
    schema -- the name of the schema to use in the queries
    RETURNS:
    result -- a dict of counts
    '''

    dim_state = metadata.tables.get('%s.dim_state' % schema)
    dim_district = metadata.tables.get('%s.dim_district' % schema)
    dim_school = metadata.tables.get('%s.dim_school' % schema)
    dim_student = metadata.tables.get('%s.dim_student' % schema)

    if dim_state is None or dim_district is None or dim_school is None or dim_student is None:
        raise AttributeError('metadata table list missing a desired table')

    state_count_select = select([func.count(dim_state.c.state_id)])
    districts_count_select = select([func.count(dim_district.c.district_id)])
    school_count_select = select([func.count(dim_school.c.school_id)])
    student_count_select = select([func.count(dim_student.c.student_id)])

    state_count = connection.execute(state_count_select).fetchall()[0][0]
    district_count = connection.execute(districts_count_select).fetchall()[0][0]
    school_count = connection.execute(school_count_select).fetchall()[0][0]
    student_count = connection.execute(student_count_select).fetchall()[0][0]

    result = {
        'state_count': state_count,
        'district_count': district_count,
        'school_count': school_count,
        'student_count': student_count,
    }

    return result


def print_db_stats(db_stats):
    '''
    format and print results gather in the get_database_statistics method
    INPUT:
    db_stats -- dictionary returned by get_database_statistics
    '''
    print('******** Data Base Stats ********')
    print('State Count:    ', db_stats['state_count'])
    print('District Count: ', db_stats['district_count'])
    print('School Count:   ', db_stats['school_count'])
    print('Student Count:  ', db_stats['student_count'])
    print('\n')


def print_short_result(total_time, db_stats, state_res_dict, district_res_dict, school_res_dict, as_csv=False):
    '''
    Formats and prints a one line summary of the benchmark that can be easily stored
    in a database or table. Includes a header. Will print either formatted as csv or as tab separated
    INPUT:
    total_time -- float, the amount of time it took to run all queries
    db_stats -- dictionary of database stats returned by get_database_statistics
    state_res_dict -- the result dictionary for a state
    district_res_dict -- the result dictionary for a district
    school_res_dict -- the result dictionary for a district
    as_csv -- boolean, format as a csv with commas or not.
    RETURNS:
    '''

    state_bench = state_res_dict['benchmarks']
    district_bench = district_res_dict['benchmarks']
    school_bench = school_res_dict['benchmarks']

    # Small output headers
    headings = [
        'Date', 'Total Time', 'State DB Count', 'State', 'State Time', 'State Result Count',
        'District DB Count', 'District ID', 'District Time', 'District Result Count',
        'School DB Count', 'School ID', 'School Time', 'School Result Count',
    ]

    # Small output data, Convert all data to string object (and format if necessary)
    data = [
        str(date.today()), '%.2fs' % total_time, str(db_stats['state_count']), state_res_dict['id'],
        '%.2fs' % state_bench['total_time'], str(state_bench['total_rows']), str(db_stats['district_count']),
        str(district_res_dict['id']), '%.2fs' % district_bench['total_time'],
        str(district_bench['total_rows']), str(db_stats['school_count']), str(school_res_dict['id']),
        '%.2fs' % school_bench['total_time'], str(school_bench['total_rows'])
    ]

    head_string = ''
    data_string = ''

    # loop through headings and construct the output string, Either as tab separated or comma separated
    for i in range(len(headings)):
        if as_csv:
            head_string += (headings[i] + ',')
        else:
            width = max(len(headings[i]), len(data[i]))
            head_string += '{0:>{1}}'.format(headings[i], width + 2)

    # remove trailing comma (if present)
    head_string = head_string.rstrip(',')
    print(head_string)

    # loop through data and construct the output string, Either as tab separated or comma separated
    for i in range(len(headings)):
        if as_csv:
            data_string += (data[i] + ',')
        else:
            width = max(len(headings[i]), len(data[i]))
            data_string += '{0:>{1}}'.format(data[i], width + 2)

    # remove trailing comma (if present)
    data_string = data_string.rstrip(',')
    print(data_string)


def print_results(result_dict):
    '''
    prints the result dictionary returned by one of the statistic methods
    INPUT:
    result_dict -- dict with two items
    is_verbose -- boolean flag for whether to print query results
    RETURNS: None
    '''

    num_offset = 10
    string_space = 7
    float_places = 3
    db_stats = result_dict['stats']
    benchmarks = result_dict['benchmarks']
    description = result_dict['descriptor'] + ' ' + str(result_dict['id'])

    print('************* Benchmarks for %s *************' % description)

    #Get length of longest string, use to help with output formatting, so that columns line-up
    max_str_len = len(max((x['name'] for x in db_stats['data']), key=len))

    #loop through statistics gathered and print each one out, Use local to format number with commas
    for stat in db_stats['data']:
        string = '{0:{1}}{2:>{3}}'.format(stat['name'] + ':', max_str_len + string_space, locale.format("%d", stat['value'], grouping=True), num_offset)
        print(string)

    #print out amount of time used to gather overall counts
    print('{0:{1}}{2:{3}.{4}f}s'.format('Time to run counts:', max_str_len + string_space, db_stats['query_time'], num_offset, float_places))
    print('**** Benchmarks for Queries ****')

    #Get Length of longest string and use to format output
    max_str_len = max(max_str_len, len(max((x['type'] for x in benchmarks['data']), key=len)))

    # Loop through benchmark results and print
    for mark in benchmarks['data']:
        string = '{0:{1}}{2:{3}.{4}f}s'.format(mark['type'], max_str_len + string_space, mark['query_time'], num_offset, float_places)
        print(string)

    print()


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
    parser.add_argument('--state_count', help='number of states to run benchmarks on. Benchmarks run on the n largest. Default: 1', default=1)
    parser.add_argument('--district_count', help='number of districts to run benchmarks on. Benchmarks run on the n largest. Default: 1', default=1)
    parser.add_argument('--school_count', help='number of schools to run benchmarks on. Benchmarks run on the n largest. Default: 1', default=1)
    parser.add_argument('--state', help='State code you wish to run benchmarks for')
    parser.add_argument('--district', help='District ID you wish to run benchmarks for')
    parser.add_argument('--school', help='District ID you wish to run benchmarks for')
    parser.add_argument('-v', '--verbose', action='store_true', help='print out query results.')
    parser.add_argument('-c', '--csv', action='store_true', help='whether or not to print short output as csv')

    args = parser.parse_args()
    return vars(args)


def main():
    '''
    Entry point main method
    '''

    # set locale, for string formatting
    locale.setlocale(locale.LC_ALL, 'en_US')

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
    run_benchmarks(metadata, db_connection, input_args['schema'], input_args['verbose'], input_args['district_count'],
                   input_args['state_count'], input_args['school_count'], input_args['csv'])
    print()
    print("Benchmarking Complete")

    #Close db connection
    db_connection.close()

if __name__ == '__main__':
    main()
