--clean_keys.sql
set search_path = edware;

create index idx_fe_dim_student_key on edware.fact_enroll(dim_student_key);
create index idx_fe_dim_section_key on edware.fact_enroll(dim_section_key);

create index idx_fao_dim_student_key on edware.fact_assmt_outcome(dim_student_key);
create index idx_fao_dim_assmt_outcome_type_key on edware.fact_assmt_outcome(dim_assmt_outcome_type_key);
create index idx_fao_dim_assmt_period_key on edware.fact_assmt_outcome(dim_assmt_period_key);


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

delete from edware.fact_enroll
where dim_section_key not in
(
    select dim_section_key
    from edware.dim_section
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
where dim_assmt_outcome_type_key not in
(
    select dim_assmt_outcome_type_key
    from edware.dim_assmt_outcome_type
    group by 1
--    limit 10
)
;

delete from edware.fact_assmt_outcome
where dim_assmt_period_key not in
(
    select dim_assmt_period_key
    from edware.dim_assmt_period
    group by 1
--    limit 10
)
;

select now() as _ck_end_;
