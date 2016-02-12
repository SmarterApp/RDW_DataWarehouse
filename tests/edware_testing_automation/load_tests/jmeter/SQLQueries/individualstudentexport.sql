select distinct(f.student_guid), f.state_code, f.asmt_type,a.effective_date,s.last_name 
from (select student_guid, state_code, asmt_type,asmt_rec_id from edware_es_1_10.fact_asmt_outcome_vw limit 200 offset 909999) f 
join edware_es_1_10.dim_asmt a on f.asmt_type=a.asmt_type and f.asmt_rec_id=a.asmt_rec_id 
join edware_es_1_10.dim_student s on s.student_guid=f.student_guid limit 100;