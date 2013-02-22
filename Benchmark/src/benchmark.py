'''
Created on Feb 21, 2013

@author: swimberly
'''

import random

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
    district_num -- the number of districts to run benchmarks on
    state_num -- the number of states to run benchmarks on
    school_num -- the number of schools to run benchmarks on
    '''

    states = get_state_id_list_by_size(metadata, connection)
    districts = get_district_id_list_by_size(metadata, connection)
    schools = get_school_list_by_size(metadata, connection)

    run_statistics(metadata, connection, schema, state_statistics, state_num, states)
    run_statistics(metadata, connection, schema, district_statistics, district_num, districts)
    run_statistics(metadata, connection, schema, school_statistics, school_num, schools)


def run_statistics(metadata, connection, schema, statistics_method, count_num, object_list):
    '''
    '''
    if count_num >= len(object_list):
        for obj in object_list:
            statistics_method(obj[0], connection, schema)
    else:
        for i in range(count_num):
            index = random.randint(0, len(object_list) - 1)
            statistics_method(object_list.pop(index)[0], connection, schema)


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
    for t in metadata.sorted_tables:
        if t.name == 'dim_state':
            dim_state = t
        elif t.name == 'dim_district':
            dim_district = t

    if dim_state is None or dim_district is None:
        raise AttributeError('metadata table list missing a desired table')

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

    for t in metadata.sorted_tables:
        if t.name == 'dim_school':
            dim_school = t
        elif t.name == 'dim_student':
            dim_student = t

    if dim_school is None or dim_student is None:
        raise AttributeError('metadata table list missing a desired table')

    school_select = select([dim_school.c.school_id, func.count(dim_student.c.student_id)], dim_student.c.school_id == dim_school.c.school_id)
    school_select = school_select.group_by(dim_school.c.school_id).order_by(func.count(dim_student.c.student_id))

    if district_id:
        school_select = school_select.where(dim_school.c.district_id == district_id)
    elif state_id:
        school_select = school_select.where(dim_school.c.state_id == state_id)

    district_list = connection.execute(school_select).fetchall()
    return district_list


if __name__ == '__main__':

    engine = create_engine('postgresql+psycopg2://postgres:edware2013@edwdbsrv2.poc.dum.edwdc.net:5432/edware')
    db_connection = engine.connect()
    schema_name = 'edware_star_20130215_2'
    metadata = MetaData()
    metadata.reflect(engine, schema_name)

    res1 = get_district_id_list_by_size(metadata, db_connection)

    for r in res1:
        print(r)
    print(len(res1))

    for r in get_state_id_list_by_size(metadata, db_connection):
        print(r)

    for r in get_school_list_by_size(metadata, db_connection):
        print(r)

    run_benchmarks(metadata, db_connection, schema_name, 1, 1, 1)
