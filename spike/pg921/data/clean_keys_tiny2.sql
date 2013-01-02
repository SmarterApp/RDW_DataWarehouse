--clean_keys_tiny2.sql
set search_path = edware;

select now() as _ck_start_;

drop table edware.fact_enroll_clean;
create table edware.fact_enroll_clean as
select fe.* from edware.fact_enroll fe
join edware.dim_student dstu using (dim_student_key)
join edware.dim_section dsec using (dim_section_key)
--where 1=2
;

ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fact_enroll_clean_pkey PRIMARY KEY (fact_enroll_key); 
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fact_enroll_clean_nkey UNIQUE (student_sid, section_sid); 

drop table edware.fact_assmt_outcome_clean;
create table edware.fact_assmt_outcome_clean as
select fao.* from edware.fact_assmt_outcome fao
join edware.dim_student dstu using (dim_student_key)
join edware.dim_assmt_outcome_type daot using (dim_assmt_outcome_type_key)
join edware.dim_period dp on (fao.dim_assmt_period_key = dp.dim_period_key)
--where 1=2
;

ALTER TABLE edware.fact_assmt_outcome_clean
ADD CONSTRAINT fact_assmt_outcome_clean_pkey
PRIMARY KEY (fact_assmt_outcome_key); 

ALTER TABLE edware.fact_assmt_outcome_clean
ADD CONSTRAINT fact_assmt_outcome_clean_nkey
UNIQUE (dim_student_key, dim_assmt_outcome_type_key, dim_assmt_period_key, dim_assmt_grade_key, assmt_instance_sid); 

ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_institution_fk FOREIGN KEY (dim_institution_key) references edware.dim_institution (dim_institution_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_student_fk FOREIGN KEY (dim_student_key) references edware.dim_student (dim_student_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_grade_fk FOREIGN KEY (dim_grade_key) references edware.dim_grade (dim_grade_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_section_fk FOREIGN KEY (dim_section_key) references edware.dim_section (dim_section_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_teacher_staff_fk FOREIGN KEY (dim_teacher_staff_key) references edware.dim_staff (dim_staff_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_enroll_attr_fk FOREIGN KEY (dim_enroll_attr_key) references edware.dim_enroll_attr (dim_enroll_attr_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_inst_admit_time_fk FOREIGN KEY (dim_inst_admit_time_key) references edware.dim_time (dim_time_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_inst_disc_time_fk FOREIGN KEY (dim_inst_disc_time_key) references edware.dim_time (dim_time_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_sect_admit_time_fk FOREIGN KEY (dim_sect_admit_time_key) references edware.dim_time (dim_time_key);
ALTER TABLE edware.fact_enroll_clean ADD CONSTRAINT fec_dim_sect_disc_time_fk FOREIGN KEY (dim_sect_disc_time_key) references edware.dim_time (dim_time_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_student_fk FOREIGN KEY (dim_student_key) references edware.dim_student (dim_student_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_staff_fk FOREIGN KEY (dim_assmt_staff_key) references edware.dim_staff (dim_staff_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_outcome_type_fk FOREIGN KEY (dim_assmt_outcome_type_key) references edware.dim_assmt_outcome_type (dim_assmt_outcome_type_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_period_fk FOREIGN KEY (dim_assmt_period_key) references edware.dim_period (dim_period_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_grade_fk FOREIGN KEY (dim_assmt_grade_key) references edware.dim_grade (dim_grade_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_time_fk FOREIGN KEY (dim_assmt_time_key) references edware.dim_time (dim_time_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_sync_time_fk FOREIGN KEY (dim_assmt_sync_time_key) references edware.dim_time (dim_time_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_perf_level_fk FOREIGN KEY (dim_perf_level_key) references edware.dim_perf_level (dim_perf_level_key);
ALTER TABLE edware.fact_assmt_outcome_clean  ADD CONSTRAINT faoc_dim_assmt_institution_fk FOREIGN KEY (dim_assmt_institution_key) references edware.dim_institution (dim_institution_key);

/*
create index idx_fec_dim_institution_key on edware.fact_enroll_clean(dim_institution_key);
create index idx_fec_dim_student_key on edware.fact_enroll_clean(dim_student_key);
create index idx_fec_dim_grade_key on edware.fact_enroll_clean(dim_grade_key);
create index idx_fec_dim_section_key on edware.fact_enroll_clean(dim_section_key);
create index idx_fec_dim_term_key on edware.fact_enroll_clean(dim_term_key);
create index idx_fec_dim_teacher_staff_key on edware.fact_enroll_clean(dim_teacher_staff_key);
create index idx_fec_dim_enroll_attr_key on edware.fact_enroll_clean(dim_enroll_attr_key);
create index idx_fec_dim_inst_admit_time_key on edware.fact_enroll_clean(dim_inst_admit_time_key);
create index idx_fec_dim_inst_disc_time_key on edware.fact_enroll_clean(dim_inst_disc_time_key);
create index idx_fec_dim_sect_admit_time_key on edware.fact_enroll_clean(dim_sect_admit_time_key);
create index idx_fec_dim_sect_disc_time_key on edware.fact_enroll_clean(dim_sect_disc_time_key);


create index idx_faoc_dim_student_key on edware.fact_assmt_outcome_clean(dim_student_key);
create index idx_faoc_dim_assmt_outcome_type_key on edware.fact_assmt_outcome_clean(dim_assmt_outcome_type_key);
create index idx_faoc_dim_assmt_period_key on edware.fact_assmt_outcome_clean(dim_assmt_period_key);
*/

select now() as _ck_end_;
