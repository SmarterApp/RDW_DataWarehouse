SELECT fact_asmt_outcome.student_id,
       dim_student.first_name                         AS
       student_first_name,
       dim_student.middle_name                        AS
       student_middle_name,
       dim_student.last_name                          AS
       student_last_name,
       dim_student.grade                              AS
       grade,
       dim_student.district_id                        AS
       district_id,
       dim_student.school_id                          AS
       school_id,
       dim_student.state_code                         AS
       state_code,
       dim_asmt.asmt_subject                          AS
       asmt_subject,
       dim_asmt.asmt_period                           AS
       asmt_period,
       dim_asmt.asmt_type                             AS
       asmt_type,
       dim_asmt.asmt_score_min                        AS
       asmt_score_min,
       dim_asmt.asmt_score_max                        AS
       asmt_score_max,
       dim_asmt.asmt_perf_lvl_name_1                  AS
       asmt_cut_point_name_1,
       dim_asmt.asmt_perf_lvl_name_2                  AS
       asmt_cut_point_name_2,
       dim_asmt.asmt_perf_lvl_name_3                  AS
       asmt_cut_point_name_3,
       dim_asmt.asmt_perf_lvl_name_4                  AS
       asmt_cut_point_name_4,
       dim_asmt.asmt_perf_lvl_name_5                  AS
       asmt_cut_point_name_5,
       dim_asmt.asmt_cut_point_1                      AS
       asmt_cut_point_1,
       dim_asmt.asmt_cut_point_2                      AS
       asmt_cut_point_2,
       dim_asmt.asmt_cut_point_3                      AS
       asmt_cut_point_3,
       dim_asmt.asmt_cut_point_4                      AS
       asmt_cut_point_4,
       fact_asmt_outcome.asmt_grade                   AS
       asmt_grade,
       fact_asmt_outcome.asmt_score                   AS
       asmt_score,
       fact_asmt_outcome.asmt_score_range_min         AS
       asmt_score_range_min,
       fact_asmt_outcome.asmt_score_range_max         AS
       asmt_score_range_max,
       fact_asmt_outcome.date_taken_day               AS
       date_taken_day,
       fact_asmt_outcome.date_taken_month             AS
       date_taken_month,
       fact_asmt_outcome.date_taken_year              AS
       date_taken_year,
       fact_asmt_outcome.asmt_perf_lvl                AS
       asmt_perf_lvl,
       dim_asmt.asmt_claim_1_name                     AS
       asmt_claim_1_name,
       dim_asmt.asmt_claim_2_name                     AS
       asmt_claim_2_name,
       dim_asmt.asmt_claim_3_name                     AS
       asmt_claim_3_name,
       dim_asmt.asmt_claim_4_name                     AS
       asmt_claim_4_name,
       dim_asmt.asmt_claim_1_score_min                AS
       asmt_claim_1_score_min,
       dim_asmt.asmt_claim_2_score_min                AS
       asmt_claim_2_score_min,
       dim_asmt.asmt_claim_3_score_min                AS
       asmt_claim_3_score_min,
       dim_asmt.asmt_claim_4_score_min                AS
       asmt_claim_4_score_min,
       dim_asmt.asmt_claim_1_score_max                AS
       asmt_claim_1_score_max,
       dim_asmt.asmt_claim_2_score_max                AS
       asmt_claim_2_score_max,
       dim_asmt.asmt_claim_3_score_max                AS
       asmt_claim_3_score_max,
       dim_asmt.asmt_claim_4_score_max                AS
       asmt_claim_4_score_max,
       fact_asmt_outcome.asmt_claim_1_score           AS
       asmt_claim_1_score,
       fact_asmt_outcome.asmt_claim_2_score           AS
       asmt_claim_2_score,
       fact_asmt_outcome.asmt_claim_3_score           AS
       asmt_claim_3_score,
       fact_asmt_outcome.asmt_claim_4_score           AS
       asmt_claim_4_score,
       fact_asmt_outcome.asmt_claim_1_score_range_min AS
       asmt_claim_1_score_range_min,
       fact_asmt_outcome.asmt_claim_2_score_range_min AS
       asmt_claim_2_score_range_min,
       fact_asmt_outcome.asmt_claim_3_score_range_min AS
       asmt_claim_3_score_range_min,
       fact_asmt_outcome.asmt_claim_4_score_range_min AS
       asmt_claim_4_score_range_min,
       fact_asmt_outcome.asmt_claim_1_score_range_max AS
       asmt_claim_1_score_range_max,
       fact_asmt_outcome.asmt_claim_2_score_range_max AS
       asmt_claim_2_score_range_max,
       fact_asmt_outcome.asmt_claim_3_score_range_max AS
       asmt_claim_3_score_range_max,
       fact_asmt_outcome.asmt_claim_4_score_range_max AS
       asmt_claim_4_score_range_max,
       dim_staff.first_name                           AS
       teacher_first_name,
       dim_staff.middle_name                          AS
       teacher_middle_name,
       dim_staff.last_name                            AS
       teacher_last_name
FROM   fact_asmt_outcome
       JOIN dim_student
         ON fact_asmt_outcome.student_id =
                 dim_student.student_id
            AND fact_asmt_outcome.section_guid =
                dim_student.section_guid
       JOIN dim_staff
         ON fact_asmt_outcome.teacher_guid =
                 dim_staff.staff_guid
            AND fact_asmt_outcome.section_guid =
                dim_staff.section_guid
            AND dim_staff.most_recent
       JOIN dim_asmt
         ON dim_asmt.asmt_rec_id =
                 fact_asmt_outcome.asmt_rec_id
            AND dim_asmt.most_recent
            AND dim_asmt.asmt_type = 'SUMMATIVE'
WHERE  fact_asmt_outcome.most_recent
       AND fact_asmt_outcome.status = 'C'
       AND fact_asmt_outcome.student_id = 'aeed1057-82ad-46c8-bf24-b0dffc171669'
ORDER  BY dim_asmt.asmt_subject DESC
