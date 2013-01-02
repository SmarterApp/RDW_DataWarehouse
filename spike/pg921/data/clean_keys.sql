--clean_keys.sql
set search_path = edware;

select now() as _ck_start_;

delete from edware.fact_enroll
where dim_student_key not in
(
    select dim_student_key
    from edware.dim_student
    group by 1
--    limit 10
)
;

select now() as _ck_start_;

delete from edware.fact_assmt_outcome
where dim_student_key not in
(
    select dim_student_key
    from edware.dim_student
    group by 1
--    limit 10
)
;

select now() as _ck_end_;

delete from edware.fact_enroll
where dim_grade_key not in
(
    select dim_grade_key
    from edware.dim_grade
    group by 1
--    limit 10
)
;

delete from edware.fact_enroll
where dim_section_key not in
(
    select dim_section_key
    from edware.dim_section
    group by 1
--    limit 10
)
;

delete from edware.fact_enroll
where dim_teacher_staff_key not in
(
    select dim_teacher_staff_key
    from edware.dim_teacher_staff
    group by 1
--    limit 10
)
;

delete from edware.fact_enroll
where dim_teacher_staff_key not in
(
    select dim_enroll_attr_key
    from edware.dim_enroll_attr
    group by 1
--    limit 10
)
;

delete from edware.fact_enroll
where dim_inst_admit_time_key not in
(
    select dim_inst_admit_time_key
    from edware.dim_inst_admit_time
    group by 1
--    limit 10
)
;


delete from edware.fact_enroll
where dim_inst_disc_time_key not in
(
    select dim_inst_disc_time_key
    from edware.dim_inst_disc_time
    group by 1
--    limit 10
)
;

delete from edware.fact_enroll
where dim_sect_admit_time_key not in
(
    select dim_sect_admit_time_key
    from edware.dim_sect_admit_time
    group by 1
--    limit 10
)
;

delete from edware.fact_enroll
where dim_sect_disc_time_key not in
(
    select dim_sect_disc_time_key
    from edware.dim_sect_disc_time
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_student_key not in
(
    select dim_student_key
    from edware.dim_student
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_staff_key not in
(
    select dim_staff_key
    from edware.dim_staff
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_assmt_outcome_type_key not in
(
    select dim_assmt_outcome_type_key
    from edware.dim_assmt_outcome_type
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_period_key not in
(
    select dim_period_key
    from edware.dim_period
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_assmt_grade_key not in
(
    select dim_grade_key
    from edware.dim_grade
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_assmt_grade_key not in
(
    select dim_time_key
    from edware.dim_time
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_assmt_sync_time_key not in
(
    select dim_time_key
    from edware.dim_time
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_perf_level_key not in
(
    select dim_perf_level_key
    from edware.dim_perf_level
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_assmt_institution_key not in
(
    select dim_assmt_institution_key
    from edware.dim_assmt_institution
    group by 1
--    limit 10
)
;


