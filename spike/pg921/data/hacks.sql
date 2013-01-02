create table edware_lz.foo(bar varchar(3));
insert into edware_lz.foo values('baz');
select * from edware_lz.foo

select now() as _bm_start_;

select assmt_code, assmt_name, count(0)
from edware.dim_assmt_outcome_type
group by assmt_code, assmt_name;

select now() as _bm_end_;


select dim_student_key as _fao_not_in_dim_student_key_
from edware.fact_enroll
where dim_student_key not in
(
    select dim_student_key
    from edware.dim_student
)
;


select distinct
       daot.daot_hier_level_code        as code
     , daot.daot_hier_level_name        as name
     , max(daot.daot_measure_type_rank) as rank
  from edware.dim_assmt_outcome_type daot
 where daot.assmt_code in ('7')
   and case
         when daot.assmt_code = '706' then true
         when daot.assmt_code = '706s' then true
         else daot.assmt_version_code in ('1', '1', '1', '1', '1')
       end
   and daot.daot_measure_type_code in ('BM_AM')
 group by code, name
 order by rank asc
 
 select avg(length(first_name || middle_name || last_name)) as avg_name_len
 from dim_student
 group by first_name, middle_name, last_name
 ;