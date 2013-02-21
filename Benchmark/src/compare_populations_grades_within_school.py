'''
Created on Feb 15, 2013

@author: Smitha Pitla
'''
from sqlalchemy import create_engine
import sys
engine = create_engine('postgresql+psycopg2://postgres:postgres@monetdb1.poc.dum.edwdc.net:5432/edware')
#district=sys.argv[1]


def grades_in_a_school(school_id, asmt_type, asmt_subject, engine):
    query = """
    select fact.asmt_grade_id, count(fact.student_id),
    case
    when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1
    when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2
    when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3
    when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4
    end
    as performance_level
    from
    edware_star_20130212_fixture_3.dim_asmt asmt,
    edware_star_20130212_fixture_3.dim_school school,
    edware_star_20130212_fixture_3.fact_asmt_outcome fact,
    edware_star_20130212_fixture_3.dim_student stu
    where asmt.asmt_id = fact.asmt_id
    and school.school_id = fact.school_id
    and stu.student_id = fact.student_id
    and fact.date_taken_year='2012'
    and fact.school_id = {school_id}
    and asmt.asmt_type = '{asmt_type}'
    and asmt.asmt_subject = '{asmt_subject}'
    group by fact.asmt_grade_id, performance_level
    """.format(school_id=school_id, asmt_type=asmt_type, asmt_subject=asmt_subject)
    #print(district)
    resultset = engine.execute(query)
    results = resultset.fetchall()
    #print(results)
    return results


def school_statistics(school_id):

    student_count_query = '''
    select count(*)
    from edware_star_20130212_fixture_3.dim_student student
    where student.school_id = {school_id}
    '''.format(school_id=school_id)

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
    stu_count_set = engine.execute(student_count_query)
    tot_stu_set = engine.execute(total_students_query)
    tot_dist_set = engine.execute(total_dist_query)
    tot_sch_set = engine.execute(total_schools_query)
    query_time = time.time() - start_time

    print('************* Benchmarks for School %d *************' % school_id)
    print('Total Districts:\t%6d' % tot_dist_set.fetchall()[0][0])
    print('Total Schools:\t\t%6d' % tot_sch_set.fetchall()[0][0])
    print('Total Students:\t\t%6d' % tot_stu_set.fetchall()[0][0])
    print('Students in district:\t%6d' % stu_count_set.fetchall()[0][0])
    print('Time to run counts:\t%6.3fs' % query_time)
    print('**** Benchmarks for Queries ****')

    start_time1 = time.time()
    grades_in_a_school(school_id, 'SUMMATIVE', 'ELA')
    query_time = time.time() - start_time1
    print('Summative-ELA:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    grades_in_a_school(school_id, 'INTERIM', 'ELA')
    query_time = time.time() - start_time1
    print('Interim-ELA:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    grades_in_a_school(school_id, 'SUMMATIVE', 'Math')
    query_time = time.time() - start_time1
    print('Summative-Math:\t\t%6.2fs' % query_time)

    start_time1 = time.time()
    grades_in_a_school(school_id, 'INTERIM', 'Math')
    query_time = time.time() - start_time1
    print('Interim-Math:\t\t%6.2fs' % query_time)


if __name__ == '__main__':
    import time

    school_statistics(167)
    school_statistics(169)
    school_statistics(171)
    school_statistics(173)

    stime = time.time()
    result = grades_in_a_school(167, 'SUMMATIVE', 'ELA')
    duration = time.time() - stime
    result.sort(key=lambda tup: tup[0])

    for res in result:
        print(res)
