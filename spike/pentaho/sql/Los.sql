SELECT dim_student.student_id AS student_id,
dim_student.first_name AS student_first_name, dim_student.middle_name AS student_middle_name,
dim_student.last_name AS student_last_name, fact_asmt_outcome.enrl_grade AS enrollment_grade,
dim_staff.first_name AS teacher_first_name, dim_staff.middle_name AS teacher_middle_name,
dim_staff.last_name AS teacher_last_name, fact_asmt_outcome.asmt_grade AS asmt_grade,
dim_asmt.asmt_subject AS asmt_subject, fact_asmt_outcome.asmt_score AS asmt_score,
fact_asmt_outcome.asmt_score_range_min AS asmt_score_range_min,
fact_asmt_outcome.asmt_score_range_max AS asmt_score_range_max,
fact_asmt_outcome.asmt_perf_lvl AS asmt_perf_lvl,
dim_asmt.asmt_claim_1_name AS asmt_claim_1_name,
dim_asmt.asmt_claim_2_name AS asmt_claim_2_name,
dim_asmt.asmt_claim_3_name AS asmt_claim_3_name,
dim_asmt.asmt_claim_4_name AS asmt_claim_4_name,
fact_asmt_outcome.asmt_claim_1_score AS asmt_claim_1_score,
fact_asmt_outcome.asmt_claim_2_score AS asmt_claim_2_score,
fact_asmt_outcome.asmt_claim_3_score AS asmt_claim_3_score,
fact_asmt_outcome.asmt_claim_4_score AS asmt_claim_4_score,
fact_asmt_outcome.asmt_claim_1_score_range_min AS asmt_claim_1_score_range_min,
fact_asmt_outcome.asmt_claim_2_score_range_min AS asmt_claim_2_score_range_min,
fact_asmt_outcome.asmt_claim_3_score_range_min AS asmt_claim_3_score_range_min,
fact_asmt_outcome.asmt_claim_4_score_range_min AS asmt_claim_4_score_range_min,
fact_asmt_outcome.asmt_claim_1_score_range_max AS asmt_claim_1_score_range_max,
fact_asmt_outcome.asmt_claim_2_score_range_max AS asmt_claim_2_score_range_max,
fact_asmt_outcome.asmt_claim_3_score_range_max AS asmt_claim_3_score_range_max,
fact_asmt_outcome.asmt_claim_4_score_range_max AS asmt_claim_4_score_range_max
FROM fact_asmt_outcome
JOIN dim_student ON dim_student.student_id = fact_asmt_outcome.student_id
AND dim_student.most_recent
AND dim_student.section_guid = fact_asmt_outcome.section_guid
JOIN dim_asmt
ON dim_asmt.asmt_rec_id = fact_asmt_outcome.asmt_rec_id
AND dim_asmt.asmt_type = 'SUMMATIVE'
JOIN dim_staff
ON dim_staff.staff_guid = fact_asmt_outcome.teacher_guid
AND dim_staff.most_recent
AND dim_staff.section_guid = fact_asmt_outcome.section_guid
WHERE fact_asmt_outcome.school_id in ('248')
AND fact_asmt_outcome.asmt_grade in ('11')
AND fact_asmt_outcome.district_id in ('228')
AND fact_asmt_outcome.most_recent AND fact_asmt_outcome.status = 'C'
ORDER BY dim_student.last_name, dim_student.first_name
