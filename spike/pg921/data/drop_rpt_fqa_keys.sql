-- unique keys
--PASS
ALTER TABLE edware.dim_staff DROP CONSTRAINT dim_staff_nkey; 
--PASS
ALTER TABLE edware.dim_section DROP CONSTRAINT dim_section_nkey;
--PASS
ALTER TABLE edware.dim_enroll_attr DROP CONSTRAINT dim_enroll_attr_nkey; 
--PASS
ALTER TABLE edware.dim_period DROP CONSTRAINT dim_period_nkey; 
--PASS
ALTER TABLE edware.dim_perf_level DROP CONSTRAINT dim_perf_level_nkey; 
--PASS
ALTER TABLE edware.dim_grade DROP CONSTRAINT dim_grade_nkey;
--PASS
ALTER TABLE edware.dim_time DROP CONSTRAINT dim_time_nkey;
--PASS
ALTER TABLE edware.dim_institution DROP CONSTRAINT dim_institution_nkey;
--PASS
ALTER TABLE edware.dim_inst_group DROP CONSTRAINT dim_inst_group_nkey;
--PASS
ALTER TABLE edware.dim_student DROP CONSTRAINT dim_student_nkey;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fact_enroll_nkey;
--PASS
ALTER TABLE edware.dim_assmt_outcome_type DROP CONSTRAINT dim_assmt_outcome_type_nkey;
/*
sql>ALTER TABLE edware.dim_assmt_outcome_type DROP CONSTRAINT dim_assmt_outcome_type_nkey UNIQUE (assmt_code, assmt_version_code, daot_measure_type_code, daot_hier_level_1_code, daot_hier_level_2_code, daot_hier_level_3_code, daot_hier_level_4_code, daot_hier_level_5_code, outcome_int_code, outcome_float_code, outcome_string_code, performance_level_type_code, assmt_course_code);
UPDATE: UNIQUE constraint 'dim_assmt_outcome_type.dim_assmt_outcome_type_nkey' violated
*/
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fact_assmt_outcome_nkey; 
--foreign keys
--PASS
ALTER TABLE edware.map_sect_group_sect DROP CONSTRAINT msgs_dim_section_group_fk ;
--PASS
ALTER TABLE edware.map_sect_group_sect DROP CONSTRAINT msgs_dim_section_fk;
--PASS
ALTER TABLE edware.map_staff_group_sect DROP CONSTRAINT msgs_dim_staff_group_fk ;
--PASS
ALTER TABLE edware.map_staff_group_staff DROP CONSTRAINT msgs_dim_staff_fk;
--PASS
ALTER TABLE edware.map_assmt_subj_subj DROP CONSTRAINT ass_dim_assmt_subject_fk;
--PASS
ALTER TABLE edware.map_assmt_subj_subj DROP CONSTRAINT ass_dim_subject_fk;
--PASS
ALTER TABLE edware.map_inst_group_inst DROP CONSTRAINT migi_dim_inst_group_fk;
--PASS
ALTER TABLE edware.map_inst_group_inst DROP CONSTRAINT migi_institution_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_institution_fk;
--FAIL
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_student_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_grade_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_section_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_teacher_staff_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_enroll_attr_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_inst_admit_time_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_inst_disc_time_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_sect_admit_time_fk;
--PASS
ALTER TABLE edware.fact_enroll DROP CONSTRAINT fe_dim_sect_disc_time_fk;
--FAIL
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_student_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_staff_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_outcome_type_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_period_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_grade_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_time_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_sync_time_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_perf_level_fk;
--PASS
ALTER TABLE edware.fact_assmt_outcome DROP CONSTRAINT fao_dim_assmt_institution_fk;
