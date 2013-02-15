'''
Created on Feb 15, 2013

@author: Smitha Pitla
'''
from sqlalchemy import create_engine
import sys
engine = create_engine('postgresql+psycopg2://postgres:postgres@monetdb1.poc.dum.edwdc.net:5432/edware')
#year=sys.argv[1]
#state=sys.argv[2]
#query="select dist.district_name, count(fact.student_id), case when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1 when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2 when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3 when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4 end as performance_level from edware_star_20130212_fixture_3.dim_asmt asmt, edware_star_20130212_fixture_3.dim_district dist, edware_star_20130212_fixture_3.fact_asmt_outcome fact,edware_star_20130212_fixture_3.dim_student stu where asmt.asmt_id = fact.asmt_id and dist.district_id = fact.district_id and stu.student_id = fact.student_id and fact.date_taken_year=:year and fact.state_id =:state group by dist.district_name, performance_level "
def compare_populations(self):
    query="select dist.district_name, count(fact.student_id), case when fact.asmt_score <= asmt.asmt_cut_point_1 then asmt.asmt_perf_lvl_name_1 when fact.asmt_score > asmt.asmt_cut_point_1 and fact.asmt_score <= asmt.asmt_cut_point_2 then asmt.asmt_perf_lvl_name_2 when fact.asmt_score > asmt.asmt_cut_point_2 and fact.asmt_score <= asmt.asmt_cut_point_3 then asmt.asmt_perf_lvl_name_3 when fact.asmt_score > asmt.asmt_cut_point_3  then asmt.asmt_perf_lvl_name_4 end as performance_level from edware_star_20130212_fixture_3.dim_asmt asmt, edware_star_20130212_fixture_3.dim_district dist, edware_star_20130212_fixture_3.fact_asmt_outcome fact,edware_star_20130212_fixture_3.dim_student stu where asmt.asmt_id = fact.asmt_id and dist.district_id = fact.district_id and stu.student_id = fact.student_id and fact.date_taken_year='2012' and fact.state_id ='DE' group by dist.district_name, performance_level "
    #print(state)
    #resultset = engine.execute(query,{'state':state, 'year':year})
    resultset = engine.execute(query)
    results = resultset.fetchall()
    print(results)
        
