'''
Created on Feb 15, 2013

@author: Smitha Pitla
'''
from sqlalchemy import create_engine
import sys
engine = create_engine('postgresql+psycopg2://postgres:postgres@monetdb1.poc.dum.edwdc.net:5432/edware')


def districts_in_a_state(state_id, asmt_type, asmt_subject):
    query="""
    select dist.district_name, count(fact.student_id), 
    case when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1 
    when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2 
    when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3 
    when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4 
    end 
    as performance_level 
    from 
    edware_star_20130212_fixture_3.dim_asmt asmt, 
    edware_star_20130212_fixture_3.dim_district dist, 
    edware_star_20130212_fixture_3.fact_asmt_outcome fact, 
    edware_star_20130212_fixture_3.dim_student stu 
    where asmt.asmt_id = fact.asmt_id 
    and dist.district_id = fact.district_id 
    and stu.student_id = fact.student_id 
    and fact.date_taken_year='2012' 
    and fact.state_id = '{state_id}'
    and asmt.asmt_type = '{asmt_type}'
    and asmt.asmt_subject = '{asmt_subject}' 
    group by dist.district_name, performance_level 
    """.format(state_id=state_id, asmt_type=asmt_type, asmt_subject=asmt_subject)
    
    #print(state)
    #resultset = engine.execute(query,{'state':state, 'year':year})
    resultset = engine.execute(query)
    results = resultset.fetchall()
    #print(results)
    return results

def state_statistics(state_id):
    district_count_query = '''
    select count(*)
    from edware_star_20130212_fixture_3.dim_district district
    where district.state_id = '{state_id}'
    '''.format(state_id=state_id)

    student_count_query = '''
    select count(*)
    from edware_star_20130212_fixture_3.dim_student student
    where student.state_id = '{state_id}'
    '''.format(state_id=state_id)

    total_students_query = '''
    select count(*)
    from edware_star_20130212_fixture_3.dim_student
    '''

    total_dist_query = '''
    select count(*)
    from edware_star_20130212_fixture_3.dim_district
    '''

    total_schools_query = '''
    select count(*)
    from edware_star_20130212_fixture_3.dim_school
    '''

    start_time = time.time()
    school_count_set = engine.execute(district_count_query)
    stu_count_set = engine.execute(student_count_query)
    tot_stu_set = engine.execute(total_students_query)
    tot_dist_set = engine.execute(total_dist_query)
    tot_sch_set = engine.execute(total_schools_query)
    query_time = time.time() - start_time

    print('************* Benchmarks for State %d *************' '% state_id')
    print('Total Districts:\t%6d' % tot_dist_set.fetchall()[0][0])
    print('Total Schools:\t\t%6d' % tot_sch_set.fetchall()[0][0])
    print('Total Students:\t\t%6d' % tot_stu_set.fetchall()[0][0])
    print('Schools in district:\t%6d' % school_count_set.fetchall()[0][0])
    print('Students in district:\t%6d' % stu_count_set.fetchall()[0][0])
    print('Time to run counts:\t%6.3fs' % query_time)
    print('**** Benchmarks for Queries ****')

    start_time1 = time.time()
    res1 = districts_in_a_state(state_id, 'SUMMATIVE', 'ELA')
    query_time = time.time() - start_time1
    print('Summative-ELA:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    res2 = districts_in_a_state(state_id, 'INTERIM', 'ELA')
    query_time = time.time() - start_time1
    print('Interim-ELA:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    res3 = districts_in_a_state(state_id, 'SUMMATIVE', 'Math')
    query_time = time.time() - start_time1
    print('Summative-Math:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    res4 = districts_in_a_state(state_id, 'INTERIM', 'Math')
    query_time = time.time() - start_time1
    print('Summative-Math:\t\t%6.2fs' % query_time)


if __name__ == '__main__':
    import time
    stime = time.time()
    res = districts_in_a_state('DE', 'SUMMATIVE', 'ELA')
    duration = time.time() - stime
    res.sort(key=lambda tup: tup[0])
    state_statistics('DE')
    #state_statistics(127)
    #state_statistics(143)
        
