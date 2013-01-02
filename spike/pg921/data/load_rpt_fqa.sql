-- COPY [ int_val [ OFFSET int_val ] RECORDS ] INTO table_name
--      FROM ( file_name ',' ... | STDIN )
--      [ [USING] DELIMITERS field_separator [',' record_separator [ ',' string_quote ]]] [ NULL AS null_string ] [LOCKED]
-- COPY n OFFSET m RECORDS INTO table FROM 'file';
-- 

COPY 17173 OFFSET 0 RECORDS
INTO edware.dim_assmt_outcome_type
FROM '/home/edware/workspace/spike/monetdb/edware/data/dim_assmt_outcome_type.csv';

TABLE  edware.dim_assmt_subject
TABLE  edware.dim_enroll_attr
TABLE  edware.dim_grade
TABLE  edware.dim_inst_group
TABLE  edware.dim_institution
TABLE  edware.dim_perf_level
TABLE  edware.dim_period
TABLE  edware.dim_section
TABLE  edware.dim_section_group
TABLE  edware.dim_staff
TABLE  edware.dim_staff_group
TABLE  edware.dim_student
TABLE  edware.dim_subject
TABLE  edware.dim_term
TABLE  edware.dim_time
TABLE  edware.etl_date
TABLE  edware.executionlog
TABLE  edware.fact_assmt_outcome
TABLE  edware.fact_enroll
TABLE  edware.map_assmt_subj_subj
TABLE  edware.map_inst_group_inst
TABLE  edware.map_sect_group_sect
TABLE  edware.map_staff_group_sect
TABLE  edware.map_staff_group_staff
TABLE  edware.mv_academic_year_period
TABLE  edware.mv_amp_user_assmt
TABLE  edware.mv_amp_user_inst
TABLE  edware.mv_amp_user_program
TABLE  edware.pm_periods

