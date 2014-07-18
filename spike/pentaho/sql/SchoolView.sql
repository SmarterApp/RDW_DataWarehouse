SELECT
   'Grade ' || fact_asmt_outcome.asmt_grade AS asmt_grade_name,
   fact_asmt_outcome.asmt_grade AS asmt_grade,
   dim_asmt.asmt_subject AS asmt_subject,
   count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 1 THEN fact_asmt_outcome.student_id END) AS level1,
   count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 2 THEN fact_asmt_outcome.student_id END) AS level2,
   count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 3 THEN fact_asmt_outcome.student_id END) AS level3,
   count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 4 THEN fact_asmt_outcome.student_id END) AS level4,
   count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 5 THEN fact_asmt_outcome.student_id END) AS level5,
   count(fact_asmt_outcome.student_id) AS total,
   max(CAST(
      CASE WHEN (dim_asmt.asmt_perf_lvl_name_5 IS NOT NULL) THEN '1'
                WHEN (dim_asmt.asmt_perf_lvl_name_4 IS NOT NULL) THEN '2'
                WHEN (dim_asmt.asmt_perf_lvl_name_3 IS NOT NULL) THEN '3'
                WHEN (dim_asmt.asmt_perf_lvl_name_2 IS NOT NULL) THEN '4'
                WHEN (dim_asmt.asmt_perf_lvl_name_1 IS NOT NULL) THEN '5'
                ELSE '0' END AS INTEGER)) AS display_level
FROM fact_asmt_outcome
JOIN dim_asmt ON dim_asmt.asmt_rec_id = fact_asmt_outcome.asmt_rec_id
 AND dim_asmt.asmt_type = 'SUMMATIVE'
 AND dim_asmt.most_recent = true
 AND fact_asmt_outcome.most_recent = true
WHERE fact_asmt_outcome.state_code = 'NY' AND fact_asmt_outcome.district_id in ('228', '229')
AND fact_asmt_outcome.school_id in ('242', '245', '248')
GROUP BY fact_asmt_outcome.asmt_grade, dim_asmt.asmt_subject
ORDER BY fact_asmt_outcome.asmt_grade, dim_asmt.asmt_subject DESC
