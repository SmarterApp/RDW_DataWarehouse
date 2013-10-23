SELECT 
 dim_inst_hier.district_name AS district_name,
 dim_inst_hier.district_guid AS district_guid,
 dim_asmt.asmt_subject AS asmt_subject,
 --dim_asmt.asmt_custom_metadata AS asmt_custom_metadata,
 count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 1 THEN fact_asmt_outcome.student_guid END) AS level1,
 count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 2 THEN fact_asmt_outcome.student_guid END) AS level2,
 count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 3 THEN fact_asmt_outcome.student_guid END) AS level3,
 count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 4 THEN fact_asmt_outcome.student_guid END) AS level4,
 count(CASE WHEN fact_asmt_outcome.asmt_perf_lvl = 5 THEN fact_asmt_outcome.student_guid END) AS level5,
 count(fact_asmt_outcome.student_guid) AS total,
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
JOIN dim_inst_hier ON dim_inst_hier.inst_hier_rec_id = fact_asmt_outcome.inst_hier_rec_id
 AND dim_inst_hier.most_recent = true
WHERE fact_asmt_outcome.state_code = 'NY'
GROUP BY dim_inst_hier.district_name, dim_inst_hier.district_guid, dim_asmt.asmt_subject--, dim_asmt.asmt_custom_metadata
ORDER BY dim_inst_hier.district_name, dim_asmt.asmt_subject DESC