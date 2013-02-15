'''
Created on Feb 15, 2013

@author: Smitha Pitla
'''
from sqlalchemy import create_engine
import sys
engine = create_engine('postgresql+psycopg2://postgres:postgres@monetdb1.poc.dum.edwdc.net:5432/edware')
#district=sys.argv[1]
query="select school.school_name, count(fact.student_id), case when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1 when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2 when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3 when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4 end as performance_level from edware_star_20130212_fixture_3.dim_asmt asmt, edware_star_20130212_fixture_3.dim_school school, edware_star_20130212_fixture_3.fact_asmt_outcome fact,edware_star_20130212_fixture_3.dim_student stu where asmt.asmt_id = fact.asmt_id and school.school_id = fact.school_id  and stu.student_id = fact.student_id and fact.date_taken_year='2012' and fact.district_id =124 group by school.school_name, performance_level  "
#print(district)
resultset = engine.execute(query)
results = resultset.fetchall()
print(results)