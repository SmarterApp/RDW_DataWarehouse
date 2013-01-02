--explain_rudd_q4_pg.sql
select now() as _q4_start_;
explain verbose select
       di.account_sid::varchar                              as _account_code
     , di.account_name                                      as _account_name
     , di.district_sid::varchar                             as school_group_code
     , di.district_name                                     as school_group_name
     , null                                                 as school_code
     , null                                                 as school_sid
     , null                                                 as school_name
     , null                                                 as grade_code
     , null                                                 as grade_name
     , null                                                 as grade_order
     , null                                                 as teacher_code
     , null                                                 as teacher_last_name
     , null                                                 as teacher_first_name
     , null                                                 as teacher_name
     , null                                                 as section_code
     , null                                                 as section_name
     , null                                                 as grain_attribute_value_code
     , null                                                 as grain_attribute_value_name
     , null                                                 as student_code
     , null                                                 as student_sid
     , null                                                 as student_last_name
     , null                                                 as student_first_name
     , null                                                 as student_name
     , null                                                 as school_code_curr
     , fao.academic_year_code                               as year_code
     , fao.academic_year_name                               as year_name
     , fao.academic_year_order                              as year_order
     , fao.period_code || '_' || fao.academic_year_code     as period_code
     , fao.period_abbrev                                    as period_name
     , fao.period_order                                     as period_order
     , dpl.general_level_code                               as perf_level_code
     , dpl.measure_specific_level_name                      as perf_level_name
     , dpl.level_order                                      as perf_level_order
     --coalesce(field, 'Empty')
     , avg(fao.score)                                       as score
     , count(1)                                             as student_count
  from (
        select dim_student_key
             , eternal_student_sid
             , academic_year_code
             , academic_year_name
             , academic_year_abbrev
             , academic_year_order
             , period_code
             , period_name
             , period_abbrev
             , period_order
             , dim_perf_level_key
             , performance_level_flag
             , score
          from (
                -- Flatten FAO/DAOT/DP
                select fao.dim_student_key         as dim_student_key
                     , fao.eternal_student_sid     as eternal_student_sid
                     , dp.academic_year_code       as academic_year_code
                     , dp.academic_year_name       as academic_year_name
                     , dp.academic_year_abbrev     as academic_year_abbrev
                     , academic_year_code::integer as academic_year_order
                     , dp.period_code              as period_code
                     , dp.period_name              as period_name
                     , dp.period_abbrev            as period_abbrev
                     , dp.period_order             as period_order
                     , fao.dim_perf_level_key      as dim_perf_level_key
                     , daot.performance_level_flag as performance_level_flag
                     , null::bigint                as score
                     , count(1) over (partition by fao.eternal_student_sid
                                     )             as assessed_in_all_periods_count
                  from edware.fact_assmt_outcome     fao
                  join edware.dim_assmt_outcome_type daot on fao.dim_assmt_outcome_type_key = daot.dim_assmt_outcome_type_key
                  join edware.dim_period             dp   on fao.dim_assmt_period_key       = dp.dim_period_key
                 where fao.assmt_instance_rank        =  1
                   and fao.year_sid                   in ('9')
                   and daot.assmt_code                in ('7')
                   and case
                         when daot.assmt_code         =  '706' then true
                         when daot.assmt_code         =  '706s' then true
                         else daot.assmt_version_code in ('1', '1', '1', '1', '1')
                       end
                   and daot.daot_measure_type_code    in ('BM_AM')
                   and daot.daot_hier_level_code      in ('2')
                   and case daot.daot_hier_level
                         when 1 then daot.daot_hier_level_1_code
                         when 2 then daot.daot_hier_level_2_code
                         when 3 then daot.daot_hier_level_3_code
                         when 4 then daot.daot_hier_level_4_code
                         when 5 then daot.daot_hier_level_5_code
                       end                            in ('INSTREC')
                   and dp.period_code || '_' || dp.academic_year_code in ('32_9', '31_9')
               ) fao
        )                     fao
  join edware.fact_enroll         fe       on
                                          fao.dim_student_key      = fe.dim_student_key
  join edware.dim_institution     di       on fe.dim_institution_key   = di.dim_institution_key
  join edware.dim_perf_level      dpl      on fao.dim_perf_level_key   = dpl.dim_perf_level_key
  join edware.dim_grade           dg       on fe.dim_grade_key         = dg.dim_grade_key
  join edware.dim_student         dstu     on fe.dim_student_key       = dstu.dim_student_key
 where not di.demo_flag
   and fe.is_reporting_classe
   and di.account_sid                                 =  '15753406'
   and di.district_sid                                in ('15753404')
   and performance_level_flag = true
   and not dstu.demo_flag
 group by _account_code
        , _account_name
        , school_group_code
        , school_group_name
        , year_code
        , year_name
        , period_code
        , fao.academic_year_abbrev
        , year_order
        , fao.period_abbrev
        , period_name
        , period_order
        , perf_level_code
        , perf_level_name
        , perf_level_order
 order by 1
        , _account_name
        , grade_order
        , school_group_name
        , year_order desc
        , period_order desc
        , perf_level_order
;
select now() as _q4_finish_;
