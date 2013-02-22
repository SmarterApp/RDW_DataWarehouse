'''
Created on Feb 15, 2013

@author: Smitha Pitla, swimberly

Districts withing a state query

Public interface:
state_statistics(state_id, connection, schema_name)
districts_in_a_state(state_id, asmt_type, asmt_subject, connection, schema_name)

Descriptions:
'state_statistics()' prints statistics for how long it takes for the query to return
for each of the different types of queries:
Summative-ELA, Summative-Math, Interim-ELA, Interim-Math

'districts_in_a_state()': returns the result of running the query on the
given parameters
'''

import time

from sqlalchemy import create_engine


def state_statistics(state_id, connection, schema_name):
    '''
    Runs queries that print out the statistics and benchmarks for a state
    INPUT:
    state_id -- an id for a state from the database
    connection -- the db connection created by a sqlAlchemy connect() statement
    schema_name -- the name of the schema to use in the queries
    '''

    if state_id is None or connection is None:
        raise ValueError('Bad Params for state_id or connection')

    district_count_query = '''
    select count(*)
    from {schema}.dim_district district
    where district.state_id = '{state_id}'
    '''.format(state_id=state_id, schema=schema_name)

    student_count_query = '''
    select count(*)
    from {schema}.dim_student student
    where student.state_id = '{state_id}'
    '''.format(state_id=state_id, schema=schema_name)

    total_students_query = '''
    select count(*)
    from {schema}.dim_student
    '''.format(schema=schema_name)

    total_dist_query = '''
    select count(*)
    from {schema}.dim_district
    '''.format(schema=schema_name)

    total_schools_query = '''
    select count(*)
    from {schema}.dim_school
    '''.format(schema=schema_name)

    start_time = time.time()
    school_count_set = connection.execute(district_count_query)
    stu_count_set = connection.execute(student_count_query)
    tot_stu_set = connection.execute(total_students_query)
    tot_dist_set = connection.execute(total_dist_query)
    tot_sch_set = connection.execute(total_schools_query)
    query_time = time.time() - start_time

    print('************* Benchmarks for State %s *************' % state_id)
    print('Total Districts:\t%6d' % tot_dist_set.fetchall()[0][0])
    print('Total Schools:\t\t%6d' % tot_sch_set.fetchall()[0][0])
    print('Total Students:\t\t%6d' % tot_stu_set.fetchall()[0][0])
    print('Schools in district:\t%6d' % school_count_set.fetchall()[0][0])
    print('Students in district:\t%6d' % stu_count_set.fetchall()[0][0])
    print('Time to run counts:\t%6.3fs' % query_time)
    print('**** Benchmarks for Queries ****')

    start_time1 = time.time()
    districts_in_a_state(state_id, 'SUMMATIVE', 'ELA', connection, schema_name)
    query_time = time.time() - start_time1
    print('Summative-ELA:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    districts_in_a_state(state_id, 'INTERIM', 'ELA', connection, schema_name)
    query_time = time.time() - start_time1
    print('Interim-ELA:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    districts_in_a_state(state_id, 'SUMMATIVE', 'Math', connection, schema_name)
    query_time = time.time() - start_time1
    print('Summative-Math:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    districts_in_a_state(state_id, 'INTERIM', 'Math', connection, schema_name)
    query_time = time.time() - start_time1
    print('Interim-Math:\t\t%6.2fs' % query_time)


def districts_in_a_state(state_id, asmt_type, asmt_subject, connection, schema_name):
    '''
    Run a query for assessment performance for districts within a state.
    INPUT:
    state_id -- the id of the state that you want to use in the query (ie. 'DE' for deleware)
    asmt_type -- the type of assessment to use in the query ('SUMMATIVE' or 'INTERIM')
    asmt_subject -- the subject of assessment to use in the query ('ELA' or 'Math')
    connection -- the db connection created by a sqlAlchemy connect() statement
    schema_name -- the name of the schema to use in the queries
    RETURNS: result -- a list of tuples (district, count, performance level)
    '''

    query = """
    select dist.district_name, count(fact.student_id),
    case when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1
    when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2
    when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3
    when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4
    end
    as performance_level
    from
    {schema}.dim_asmt asmt,
    {schema}.dim_district dist,
    {schema}.fact_asmt_outcome fact,
    {schema}.dim_student stu
    where asmt.asmt_id = fact.asmt_id
    and dist.district_id = fact.district_id
    and stu.student_id = fact.student_id
    and fact.date_taken_year='2012'
    and fact.state_id = '{state_id}'
    and asmt.asmt_type = '{asmt_type}'
    and asmt.asmt_subject = '{asmt_subject}'
    group by dist.district_name, performance_level
    """.format(state_id=state_id, asmt_type=asmt_type, asmt_subject=asmt_subject, schema=schema_name)

    # print(state)
    # resultset = engine.execute(query,{'state':state, 'year':year})
    resultset = connection.execute(query)
    results = resultset.fetchall()
    # print(results)
    return results

if __name__ == '__main__':
    import time

    engine = create_engine('postgresql+psycopg2://postgres:postgres@monetdb1.poc.dum.edwdc.net:5432/edware')
    schema_name = 'edware_star_20130212_fixture_3'
    connection = engine.connect()

    stime = time.time()
    res = districts_in_a_state('DE', 'SUMMATIVE', 'ELA', connection, schema_name)
    duration = time.time() - stime

    res.sort(key=lambda tup: tup[0])
    state_statistics('DE', connection, schema_name)
