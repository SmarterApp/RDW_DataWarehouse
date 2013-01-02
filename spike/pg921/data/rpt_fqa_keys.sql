-- unique keys
--PASS
ALTER TABLE edware.dim_staff ADD CONSTRAINT dim_staff_nkey UNIQUE (staff_sid); 
--PASS
ALTER TABLE edware.dim_section ADD CONSTRAINT dim_section_nkey UNIQUE (section_sid);
--PASS
ALTER TABLE edware.dim_enroll_attr ADD CONSTRAINT dim_enroll_attr_nkey UNIQUE (ethnicity_code, sped_environ_code, disability_status_code, specific_disability_code, s504_status_code, econ_disadvantage_code, meal_status_code, title_1_status_code, migrant_status_code, english_prof_code, ell_status_code, home_lang_code, alt_assmt_code, housing_status_code, is_classed_code); 
--PASS
ALTER TABLE edware.dim_period ADD CONSTRAINT dim_period_nkey UNIQUE (assmt_code, academic_year_code, period_code); 
--PASS
ALTER TABLE edware.dim_perf_level ADD CONSTRAINT dim_perf_level_nkey UNIQUE (measure_specific_level_code, level_type_code, account_sid); 
--PASS
ALTER TABLE edware.dim_grade ADD CONSTRAINT dim_grade_nkey UNIQUE (grade_level_sid);
--PASS
ALTER TABLE edware.dim_time ADD CONSTRAINT dim_time_nkey UNIQUE (calendar_date);
--PASS
ALTER TABLE edware.dim_institution ADD CONSTRAINT dim_institution_nkey UNIQUE (school_year_sid);
--PASS
ALTER TABLE edware.dim_inst_group ADD CONSTRAINT dim_inst_group_nkey UNIQUE (inst_group_code, inst_group_type_code);
--PASS
ALTER TABLE edware.dim_student ADD CONSTRAINT dim_student_nkey UNIQUE (student_sid);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fact_enroll_nkey UNIQUE (student_sid, section_sid);
--PASS
ALTER TABLE edware.dim_assmt_outcome_type ADD CONSTRAINT dim_assmt_outcome_type_nkey UNIQUE (assmt_code, assmt_version_code, daot_measure_type_code, daot_hier_level_1_code, daot_hier_level_2_code, daot_hier_level_3_code, daot_hier_level_4_code, daot_hier_level_5_code, outcome_int_code, outcome_float_code, outcome_string_code, performance_level_type_code, assmt_course_code);
/*
sql>ALTER TABLE edware.dim_assmt_outcome_type ADD CONSTRAINT dim_assmt_outcome_type_nkey UNIQUE (assmt_code, assmt_version_code, daot_measure_type_code, daot_hier_level_1_code, daot_hier_level_2_code, daot_hier_level_3_code, daot_hier_level_4_code, daot_hier_level_5_code, outcome_int_code, outcome_float_code, outcome_string_code, performance_level_type_code, assmt_course_code);
UPDATE: UNIQUE constraint 'dim_assmt_outcome_type.dim_assmt_outcome_type_nkey' violated
*/
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fact_assmt_outcome_nkey UNIQUE (dim_student_key, dim_assmt_outcome_type_key, dim_assmt_period_key, dim_assmt_grade_key, assmt_instance_sid); 


--foreign keys
--PASS
ALTER TABLE edware.map_sect_group_sect ADD CONSTRAINT msgs_dim_section_group_fk FOREIGN KEY (dim_section_group_key) references edware.dim_section_group (dim_section_group_key);
--PASS
ALTER TABLE edware.map_sect_group_sect ADD CONSTRAINT msgs_dim_section_fk FOREIGN KEY (dim_section_key) references edware.dim_section (dim_section_key);
--PASS
ALTER TABLE edware.map_staff_group_sect ADD CONSTRAINT msgs_dim_staff_group_fk FOREIGN KEY (dim_staff_group_key) references edware.dim_staff_group (dim_staff_group_key);
--PASS
ALTER TABLE edware.map_staff_group_staff ADD CONSTRAINT msgs_dim_staff_fk FOREIGN KEY (dim_staff_key) references edware.dim_staff (dim_staff_key);
--PASS
ALTER TABLE edware.map_assmt_subj_subj ADD CONSTRAINT ass_dim_assmt_subject_fk FOREIGN KEY (dim_assmt_subject_key) references edware.dim_assmt_subject (dim_assmt_subject_key);
--PASS
ALTER TABLE edware.map_assmt_subj_subj ADD CONSTRAINT ass_dim_subject_fk FOREIGN KEY (dim_subject_key) references edware.dim_subject (dim_subject_key);
--PASS
ALTER TABLE edware.map_inst_group_inst ADD CONSTRAINT migi_dim_inst_group_fk FOREIGN KEY (dim_inst_group_key) references edware.dim_inst_group (dim_inst_group_key);
--PASS
ALTER TABLE edware.map_inst_group_inst ADD CONSTRAINT migi_institution_fk FOREIGN KEY (dim_institution_key) references edware.dim_institution (dim_institution_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_institution_fk FOREIGN KEY (dim_institution_key) references edware.dim_institution (dim_institution_key);
--FAIL
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_student_fk FOREIGN KEY (dim_student_key) references edware.dim_student (dim_student_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_grade_fk FOREIGN KEY (dim_grade_key) references edware.dim_grade (dim_grade_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_section_fk FOREIGN KEY (dim_section_key) references edware.dim_section (dim_section_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_teacher_staff_fk FOREIGN KEY (dim_teacher_staff_key) references edware.dim_staff (dim_staff_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_enroll_attr_fk FOREIGN KEY (dim_enroll_attr_key) references edware.dim_enroll_attr (dim_enroll_attr_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_inst_admit_time_fk FOREIGN KEY (dim_inst_admit_time_key) references edware.dim_time (dim_time_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_inst_disc_time_fk FOREIGN KEY (dim_inst_disc_time_key) references edware.dim_time (dim_time_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_sect_admit_time_fk FOREIGN KEY (dim_sect_admit_time_key) references edware.dim_time (dim_time_key);
--PASS
ALTER TABLE edware.fact_enroll ADD CONSTRAINT fe_dim_sect_disc_time_fk FOREIGN KEY (dim_sect_disc_time_key) references edware.dim_time (dim_time_key);
--FAIL
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_student_fk FOREIGN KEY (dim_student_key) references edware.dim_student (dim_student_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_staff_fk FOREIGN KEY (dim_assmt_staff_key) references edware.dim_staff (dim_staff_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_outcome_type_fk FOREIGN KEY (dim_assmt_outcome_type_key) references edware.dim_assmt_outcome_type (dim_assmt_outcome_type_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_period_fk FOREIGN KEY (dim_assmt_period_key) references edware.dim_period (dim_period_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_grade_fk FOREIGN KEY (dim_assmt_grade_key) references edware.dim_grade (dim_grade_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_time_fk FOREIGN KEY (dim_assmt_time_key) references edware.dim_time (dim_time_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_sync_time_fk FOREIGN KEY (dim_assmt_sync_time_key) references edware.dim_time (dim_time_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_perf_level_fk FOREIGN KEY (dim_perf_level_key) references edware.dim_perf_level (dim_perf_level_key);
--PASS
ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fao_dim_assmt_institution_fk FOREIGN KEY (dim_assmt_institution_key) references edware.dim_institution (dim_institution_key);
