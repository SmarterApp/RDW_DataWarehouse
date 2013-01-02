-- fao_not_in_dim_student.sql

delete from edware.fact_enroll
where dim_student_key not in
    (
        select dim_student_key
        from edware.dim_student
    )
;

COPY
(select dim_student_key as _fao_not_in_dim_student_key_
from edware.fact_enroll
where dim_student_key not in
    (
        select dim_student_key
        from edware.dim_student
    )
-- and 1 = 2
) TO '/var/lib/pgsql/workspace/spike/pg921/edware/data/fao_not_in_dim_student.csv'
;


select count(dim_student_key) as _fao_not_in_dim_student_key_cnt_
from edware.fact_enroll
where dim_student_key not in
    (
        select dim_student_key
        from edware.dim_student
    )
;