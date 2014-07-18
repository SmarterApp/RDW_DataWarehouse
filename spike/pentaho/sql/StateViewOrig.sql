select
dim_inst_hier.district_name,
max(fact_asmt_outcome.district_id),
dim_asmt.asmt_subject,
count(case when fact_asmt_outcome.asmt_perf_lvl=1 then fact_asmt_outcome.student_id end) as lvl1,
count(case when fact_asmt_outcome.asmt_perf_lvl=2 then fact_asmt_outcome.student_id end) as lvl2,
count(case when fact_asmt_outcome.asmt_perf_lvl=3 then fact_asmt_outcome.student_id end) as lvl3,
count(case when fact_asmt_outcome.asmt_perf_lvl=4 then fact_asmt_outcome.student_id end) as lvl4,
count(case when fact_asmt_outcome.asmt_perf_lvl=5 then fact_asmt_outcome.student_id end) as lvl5,
count(fact_asmt_outcome.student_id) as total
from fact_asmt_outcome
inner join dim_asmt on dim_asmt.asmt_rec_id=fact_asmt_outcome.asmt_rec_id and dim_asmt.asmt_type='SUMMATIVE' and dim_asmt.most_recent=true and fact_asmt_outcome.most_recent=true
inner join dim_inst_hier on fact_asmt_outcome.inst_hier_rec_id=fact_asmt_outcome.inst_hier_rec_id and dim_inst_hier.most_recent=true
where fact_asmt_outcome.state_code='NY'
group by dim_inst_hier.district_name,dim_asmt.asmt_subject
order by dim_inst_hier.district_name,dim_asmt.asmt_subject;
