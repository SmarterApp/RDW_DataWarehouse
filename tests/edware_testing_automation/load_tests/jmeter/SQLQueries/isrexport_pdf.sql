SELECT DISTINCT ON (dim_student.student_guid) dim_student.student_guid, dim_student.last_name, fact_asmt_outcome_vw.asmt_type, 
fact_asmt_outcome_vw.state_code,  dim_asmt.effective_date, fact_asmt_outcome_vw.asmt_rec_id, fact_asmt_outcome_vw.asmt_guid, fact_asmt_outcome_vw.asmt_rec_id
FROM edware_pa_1_0.dim_student INNER JOIN edware_pa_1_0.fact_asmt_outcome_vw
ON edware_pa_1_0.dim_student.student_guid = edware_pa_1_0.fact_asmt_outcome_vw.student_guid INNER JOIN edware_pa_1_0.dim_asmt 
ON edware_pa_1_0.fact_asmt_outcome_vw.asmt_rec_id = edware_pa_1_0.dim_asmt.asmt_rec_id
WHERE edware_pa_1_0.fact_asmt_outcome_vw.asmt_type = 'SUMMATIVE' and edware_pa_1_0.fact_asmt_outcome_vw.batch_guid = '7c99bcf2-22dc-4103-b216-d1a46a6c0ad2'
ORDER BY dim_student.student_guid,
fact_asmt_outcome_vw.asmt_type, dim_student.last_name, fact_asmt_outcome_vw.state_code, 
fact_asmt_outcome_vw.asmt_rec_id, dim_asmt.effective_date, 
fact_asmt_outcome_vw.asmt_guid, fact_asmt_outcome_vw.asmt_rec_id
LIMIT 100;