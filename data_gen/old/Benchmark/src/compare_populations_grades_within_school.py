'''
Created on Feb 15, 2013

@author: Smitha Pitla, swimberly

Grades withing a school query & benchmarks

Public interface:
school_statistics(state_code, connection, schema_name)
grades_in_a_school(state_code, asmt_type, asmt_subject, connection, schema_name)

Descriptions:
'school_statistics()' prints statistics for how long it takes for the query to return
for each of the different types of queries:
Summative-ELA, Summative-Math, Interim-ELA, Interim-Math

'grades_in_a_school()': returns the result of running the query on the
given parameters
'''

import time


def school_statistics(school_id, connection, schema_name):
    '''
    Runs queries that print out the statistics and benchmarks for a school
    @param school_id: an id for a school from the database
    @param connection: the db connection created by a sqlAlchemy connection() statement
    @param schema_name: the name of the schema to use in the queries
    @return:
    result_dict -- A dictionary of results. The dictionary will have two items: 'stats' and 'benchmarks'
    'stats' is a dictionary of two items a float and a list of dicts 'query_time' and 'data' respectively.
    'data' is a list of query results in a dict with keys: name and value
    'descriptor' is the string 'School' to help identify the result
    'id' is the id that was used for the query
    'benchmarks' is a dictionary of 'total_time', 'total_rows' and 'data'. 'data' is a list of dictionaries.
    Each dictionary in 'data' has keys: 'type', 'query_time' and 'result'
    '''

    result_dict = {}

    student_count_query = '''
    select count(*)
    from {schema}.dim_student student
    where student.school_id = '{school_id}'
    '''.format(school_id=school_id, schema=schema_name)

    # Execute queries
    start_time = time.time()
    stu_count_set = connection.execute(student_count_query).fetchall()[0][0]

    query_time = time.time() - start_time

    result_dict['stats'] = {'query_time': query_time, 'data': []}

    result_dict['descriptor'] = 'School'
    result_dict['id'] = school_id

    result_dict['stats']['data'].append({'name': 'Students in School', 'value': stu_count_set})

    result_dict['benchmarks'] = {'total_time': 0, 'total_rows': 0, 'data': []}

    start_time1 = time.time()
    res = grades_in_a_school(school_id, 'SUMMATIVE', 'ELA', connection, schema_name)
    query_time = time.time() - start_time1
    result_dict['benchmarks']['data'].append({'type': 'Summative-ELA', 'query_time': query_time, 'result': res})
    result_dict['benchmarks']['total_time'] += query_time
    result_dict['benchmarks']['total_rows'] += len(res)

    start_time1 = time.time()
    res = grades_in_a_school(school_id, 'INTERIM', 'ELA', connection, schema_name)
    query_time = time.time() - start_time1
    result_dict['benchmarks']['data'].append({'type': 'Interim-ELA', 'query_time': query_time, 'result': res})
    result_dict['benchmarks']['total_time'] += query_time
    result_dict['benchmarks']['total_rows'] += len(res)

    start_time1 = time.time()
    res = grades_in_a_school(school_id, 'SUMMATIVE', 'Math', connection, schema_name)
    query_time = time.time() - start_time1
    result_dict['benchmarks']['data'].append({'type': 'Summative-Math', 'query_time': query_time, 'result': res})
    result_dict['benchmarks']['total_time'] += query_time
    result_dict['benchmarks']['total_rows'] += len(res)

    start_time1 = time.time()
    res = grades_in_a_school(school_id, 'INTERIM', 'Math', connection, schema_name)
    query_time = time.time() - start_time1
    result_dict['benchmarks']['data'].append({'type': 'Interim-Math', 'query_time': query_time, 'result': res})
    result_dict['benchmarks']['total_time'] += query_time
    result_dict['benchmarks']['total_rows'] += len(res)

    return result_dict


def grades_in_a_school(school_id, asmt_type, asmt_subject, connection, schema_name):
    '''
    Run a query for assessment performance for grades within a school.
    @param school_id: the id of the school that you want to use in the query (ie. 'DE' for deleware)
    @param asmt_type: the type of assessment to use in the query ('SUMMATIVE' or 'INTERIM')
    @param asmt_subject: the subject of assessment to use in the query ('ELA' or 'Math')
    @param connection: the db connection created by a sqlAlchemy connect() statement
    @param schema_name: the name of the schema to use in the queries
    @return: result -- a list of tuples (grade, count, performance level)
    '''

    query = """
    select fact.asmt_grade, count(fact.student_id),
    case
    when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1
    when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2
    when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3
    when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4
    end
    as performance_level
    from
    {schema}.dim_asmt asmt,
    {schema}.dim_inst_hier inst,
    {schema}.fact_asmt_outcome fact,
    {schema}.dim_student stu
    where asmt.asmt_id = fact.asmt_id
    and inst.school_id = fact.school_id
    and stu.student_id = fact.student_id
    and fact.date_taken_year='2012'
    and fact.school_id = '{school_id}'
    and asmt.asmt_type = '{asmt_type}'
    and asmt.asmt_subject = '{asmt_subject}'
    group by fact.asmt_grade, performance_level
    """.format(school_id=school_id, asmt_type=asmt_type, asmt_subject=asmt_subject, schema=schema_name)

    resultset = connection.execute(query)
    results = resultset.fetchall()

    return results


if __name__ == '__main__':

#    engine = create_engine('postgresql+psycopg2://postgres:postgres@monetdb1.poc.dum.edwdc.net:5432/edware')
#    schema_name = 'edware_star_20130212_fixture_3'
#    connection = engine.connect()
    print("This module is not runnable from the command line. For usage instructions:")
    print("python benchmark.py -h")
