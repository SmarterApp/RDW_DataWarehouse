-- profile
select 'Grade'     as report_comparison_type
     , 2               as report_comparison_type_sid
     , 'School'            as is_report_level
     , 4              as is_report_level_sid
     , null::char                        as is_refpoint_level
     , null::char                         as refpoint_level_inst_name
     , null::char                         as refpoint_level_inst_sid
     , null::char                         as refpoint_level_inst_code
       
     , null::char                         as state_sid
     , state_code                   as state_code
     , state_name                   as state_name
     , state_abbrev                 as state_abbrev
     , account_code                 as account_code
     , account_name                 as account_name
     , account_abbrev               as account_abbrev
     , 3          as school_group_type_sid
     , 'Districts'     as school_group_type_name
     , null::char                         as school_group_inst_sid
     , school_group_inst_code       as school_group_inst_code
     , school_group_inst_name       as school_group_inst_name
     , school_group_inst_abbrev     as school_group_inst_abbrev
     , school_loc_code              as school_loc_code
       
     , FIRST_VALUE(school_name) over (partition by school_loc_code order by academic_year_code::integer desc)
                                    as school_name
     , school_abbrev                as school_abbrev
     , null::char                         as subject_sid
     , subject_code                 as subject_code
     , subject_name                 as subject_name
     , subject_abbrev               as subject_abbrev
     , null::char                         as course_sid
     , course_code                  as course_code
     , course_name                  as course_name
     , course_abbrev                as course_abbrev
     
     , staff_sid                    as staff_code             , staff_sid                    as staff_sid
     , staff_first_name             as staff_first_name
     , staff_last_name              as staff_last_name
     , staff_last_name || ', ' || nvl(staff_first_name, '')  as staff_full_name 
     , section_sid                  as section_sid
     , section_sid                  as section_code
     , section_name                 as section_name
     , section_abbrev               as section_abbrev
     , null::char                         as term_sid
     , null::char                         as term_code
     , null::char                         as term_name
     , null::char                         as term_abbrev
     , student_last_name            as student_last_name
     , student_first_name           as student_first_name
     , student_last_name || ', ' || student_first_name  as student_full_name
     , student_sid                  as student_sid
     , student_code                 as student_code
     , null::char                         as dim_student_key 
     , attribute_category_name      as attribute_category_label
     , attribute_category_code      as attribute_category_code
     , null::char                         as attribute_category_sid
     , null::char                         as attribute_row_label
     , attribute_value_code         as attribute_row_code
     , attribute_value_label         as attribute_row_label
     , null::char                         as attribute_row_sid
     , null::char                         as grade_sid
     , grade_code                   as grade_code
     , grade_order                  as grade_order
     , grade_name                   as grade_name
     , null::char                         as assmt_sid
     , assmt_code                   as assmt_code
     , assmt_name                   as assmt_name
     , assmt_abbrev                 as assmt_abbrev
     , assmt_family_code            as assmt_family_code
       
     , null::char                         as group_type_cid
     , null::char                         as group_type_cname
     , null::char                         as group_sid
     , group_code                   as group_code
     , group_name                   as group_name
     , group_abbrev                 as group_abbrev
     , null::char                         as subgroup_sid
     , subgroup_code                as subgroup_code
     , subgroup_name                as subgroup_name
     , subgroup_abbrev              as subgroup_abbrev
     , subgroup_rank                as subgroup_rank
     , 1             as performance_meas_type_sid
     , 'Levels'        as performance_meas_type_name
     , 'Levels'        as performance_meas_type_abbrev
     , academic_year_code           as academic_year_code
     , null::char                         as academic_year_sid
     , academic_year_name           as academic_year_name
     , academic_year_abbrev         as academic_year_abbrev
     , period_order                 as period_order
     , period_sid                   as period_sid
     , period_name                  as period_name
     , period_abbrev                as period_abbrev
     , 3                            as pii_row_flag
     , 2                            as allow_drilldown_flag
     , level_1_count                as level_1_retval
       
     , level_1_label as level_1_label
     , level_2_count                as level_2_retval
     , level_2_label as level_2_label
     , level_3_count                as level_3_retval
     , level_3_label as level_3_label
     , level_4_count                as level_4_retval
     , level_4_label as level_4_label
     , level_5_count                as level_5_retval
     , level_5_label as level_5_label
     , level_1_code
     , level_2_code
     , level_3_code
     , level_4_code
     , level_5_code
     , sum_measure_count            as sum_of_count
          , null::char                         as level_bucket
             , null::char                         as score_retval
         , null::char                         as ranks
     , null::char                         as operating_sortby_val
     
     , sum(sum_measure_count)over()     as sum_of_count_aggr
         
     , sum_measure_count                as aggregation_size
     , academic_year_code               as year
         , entity_num
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name

  from 
  


(
    select account_code
         , account_name
         , account_abbrev
         , state_name
         , state_abbrev
         , state_code
         , school_group_inst_code
         , school_group_inst_name
         , school_group_inst_abbrev
         , school_loc_code
         , school_name
         , school_abbrev
         , grade_code
         , grade_order
         , grade_name
         , subject_code
         , subject_name
         , subject_abbrev
         , course_code
         , course_name
         , course_abbrev
         , section_sid
         , section_name
         , section_abbrev
         , staff_sid
         , staff_first_name
         , staff_last_name
         , attribute_category_code
         , attribute_category_name
         , attribute_value_code
         , attribute_value_label
         , student_last_name
         , student_first_name
         , student_sid
         , student_code
         , school_loc_code_curr
         , assmt_code
         , assmt_name
         , assmt_abbrev
         , assmt_family_code
         , group_code
         , group_name
         , group_abbrev
         , subgroup_code
         , subgroup_name
         , subgroup_abbrev
         , subgroup_rank
         , academic_year_code
         , academic_year_name
         , academic_year_abbrev
         , period_sid
         , period_order
         , period_name
         , period_abbrev
                , sum(case when level_order = 1 then measure_count else 0 end) as level_1_count
         , sum(case when level_order = 2 then measure_count else 0 end) as level_2_count
         , sum(case when level_order = 3 then measure_count else 0 end) as level_3_count
         , sum(case when level_order = 4 then measure_count else 0 end) as level_4_count
         , sum(case when level_order = 5 then measure_count else 0 end) as level_5_count
         , max(case when level_order = 1 then level_label else null end) as level_1_label
         , max(case when level_order = 2 then level_label else null end) as level_2_label
         , max(case when level_order = 3 then level_label else null end) as level_3_label
         , max(case when level_order = 4 then level_label else null end) as level_4_label
         , max(case when level_order = 5 then level_label else null end) as level_5_label
         , max(case when level_order = 1 then level_code else null end) as level_1_code
         , max(case when level_order = 2 then level_code else null end) as level_2_code
         , max(case when level_order = 3 then level_code else null end) as level_3_code
         , max(case when level_order = 4 then level_code else null end) as level_4_code
         , max(case when level_order = 5 then level_code else null end) as level_5_code
                , sum(measure_score) as measure_score
         , sum(measure_score * measure_count)  as sum_measure_score
         , sum(measure_count) as sum_measure_count
         
         , dense_rank()over(
            order by account_code
                   , school_group_inst_code
                   , school_loc_code
                   , grade_code
                   , subject_code
                   , course_code
                   , staff_sid
                   , section_sid
                   , student_sid
                   , attribute_category_code
                   , attribute_value_code) entity_num
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name

      from 
      

(select  account_code,
        account_name,
        account_abbrev,
        state_name,
        state_abbrev,
        state_code,
        school_group_inst_code,
        school_group_inst_name,
        school_group_inst_abbrev,
        school_loc_code,
        school_name,
        school_abbrev,
        grade_code,
        grade_order,
        grade_name,
        subject_code,
        subject_name,
        subject_abbrev,
        course_code,
        course_name,
        course_abbrev,
        staff_sid,
        staff_last_name,
        staff_first_name,
        section_sid,
        section_name,
        section_abbrev,
        attribute_category_code,
        attribute_category_name,
        attribute_value_code,
        attribute_value_label,
        student_first_name,
        student_last_name,
        student_sid,
        student_code,
        school_loc_code_curr,
        assmt_code,
        assmt_name,
        assmt_abbrev,
        assmt_family_code,
        group_code,
        group_name,
        group_abbrev,
        subgroup_rank,
        subgroup_code,
        subgroup_name,
        subgroup_abbrev,
        max(performance_level_flag) as performance_level_flag,
        academic_year_code,
        academic_year_name,
        academic_year_abbrev,
        period_sid,
        period_order,
        period_name,
        period_abbrev,
                      
              level_order           as level_order,
              level_name            as level_label,
              level_code            as level_code,
              null::numeric                     as measure_score,
                              count(1)                  as measure_count,
         assmt_grade_code,
         assmt_grade_order,
         assmt_grade_name
from
(
    select
       di.account_sid as account_code
     , di.account_name as account_name
     , di.account_sid as account_abbrev
         , case when min(di.state_sid) over(partition by di.account_sid) <> max(di.state_sid) over(partition by di.account_sid) then 'Multiple States' else di.state_name end as state_name
         , case when min(di.state_sid) over(partition by di.account_sid) <> max(di.state_sid) over(partition by di.account_sid) then 'Multi States' else di.state_code end as state_abbrev
         , case when min(di.state_sid) over(partition by di.account_sid) <> max(di.state_sid) over(partition by di.account_sid) then '-1' else di.state_sid end as state_code

                     , di.district_sid          as school_group_inst_code
         , di.district_name          as school_group_inst_name
         , di.district_name        as school_group_inst_abbrev
                            , di.school_sid        as school_loc_code
         , di.school_name             as school_name
         , di.school_name           as school_abbrev
                       , dg.grade_level_sid          as grade_code
         , dg.grade_level_order           as grade_order  
         , dg.grade_level_name  as grade_name
                        , null::char                      as subject_code
         , null::char                      as subject_name
         , null::char                      as subject_abbrev
         , null::char                      as course_code
         , null::char                      as course_name
         , null::char                      as course_abbrev
                         , null::char                 as staff_sid
         , null::char                 as staff_last_name
         , null::char                 as staff_first_name
                       , null::char                      as section_sid
         , null::char                      as section_name
         , null::char                      as section_abbrev
                     , null::char                      as attribute_category_code
         , null::char                      as attribute_category_name
         , null::char                     as attribute_value_code
         , null::char                     as attribute_value_label
                     , null::char                     as student_first_name
         , null::char                      as student_last_name
         , null::char                      as student_sid
         , null::char                      as student_code
         , null::char                      as school_loc_code_curr
                , fao.assmt_code           as assmt_code 
         , fao.assmt_name as assmt_name
         , fao.assmt_name as assmt_abbrev
         , fao.assmt_version_code    as assmt_family_code
         , fao.daot_hier_level_code           as group_code
         , fao.daot_hier_level_name           as group_name
         , fao.daot_hier_level_name         as group_abbrev         
         , fao.daot_hier_level_rank         as subgroup_rank
         , case 
             when daot_hier_level = 1 then daot_hier_level_1_code 
             when daot_hier_level = 2 then daot_hier_level_2_code 
             when daot_hier_level = 3 then daot_hier_level_3_code 
             when daot_hier_level = 4 then daot_hier_level_4_code 
             when daot_hier_level = 5 then daot_hier_level_5_code 
           end
             as subgroup_code 
         , case 
             when daot_hier_level = 1 then daot_hier_level_1_abbrev 
             when daot_hier_level = 2 then daot_hier_level_2_abbrev 
             when daot_hier_level = 3 then daot_hier_level_3_abbrev 
             when daot_hier_level = 4 then daot_hier_level_4_abbrev 
             when daot_hier_level = 5 then daot_hier_level_5_abbrev 
           end
             as subgroup_name  
         , case 
             when daot_hier_level = 1 then daot_hier_level_1_abbrev 
             when daot_hier_level = 2 then daot_hier_level_2_abbrev 
             when daot_hier_level = 3 then daot_hier_level_3_abbrev 
             when daot_hier_level = 4 then daot_hier_level_4_abbrev 
             when daot_hier_level = 5 then daot_hier_level_5_abbrev 
           end
             as subgroup_abbrev 
         , fao.performance_level_flag
         , dp.academic_year_code     as academic_year_code
         , dp.academic_year_name     as academic_year_name
         , dp.academic_year_abbrev   as academic_year_abbrev
         , dp.period_code || '_' || dp.academic_year_code   as period_sid -- really this is period_sid
         , dp.period_order           as period_order
         , dp.academic_year_abbrev || ' ' || dp.period_abbrev as period_name  
         , dp.period_abbrev as period_abbrev
   

                       ,dpl.level_order           
           , dpl.measure_specific_level_name as level_name       
             , dpl.general_level_code as level_code
                        , count(*) over (partition by dstu.eternal_student_sid,
                                                    di.school_sid
                                                ) std_total_rows
                 , null::char                         as assmt_grade_code
         , null::numeric                      as assmt_grade_order
         , null::char                         as assmt_grade_name
              from    
      
    

(
    select dim_student_key
         , eternal_student_sid   
         , year_sid
         , dim_assmt_period_key
         , dim_assmt_grade_key
         , assmt_code
         , assmt_name
         , case when assmt_code = '706s' or assmt_code = '706' then 'TRC All Versions' else assmt_version_code end assmt_version_code
         , daot_hier_level
         , daot_hier_level_code
         , daot_hier_level_name          
         , daot_hier_level_rank
         , daot.daot_hier_level_1_code 
         , daot.daot_hier_level_1_name
         , daot.daot_hier_level_1_abbrev     
         , daot.daot_hier_level_2_code 
         , daot.daot_hier_level_2_name
         , daot.daot_hier_level_2_abbrev
         , daot.daot_hier_level_3_code 
         , daot.daot_hier_level_3_name
         , daot.daot_hier_level_3_abbrev
         , daot.daot_hier_level_4_code 
         , daot.daot_hier_level_4_name
         , daot.daot_hier_level_4_abbrev
         , daot.daot_hier_level_5_code 
         , daot.daot_hier_level_5_name
         , daot.daot_hier_level_5_abbrev
         , dim_perf_level_key
         , (case when performance_level_flag then 1 else 0 end) performance_level_flag
      from dw.fact_assmt_outcome fao
      join dw.dim_assmt_outcome_type daot
           on fao.dim_assmt_outcome_type_key  = daot.dim_assmt_outcome_type_key
          and daot.daot_hier_level_code    in ('2')
          and daot.assmt_code         in ('7')
          and case
                when daot.assmt_code = '706' then true
                when daot.assmt_code = '706s' then true
                else daot.assmt_version_code in ('1')
              end
          and  case 
                 when daot.daot_hier_level = 1 then daot.daot_hier_level_1_code 
                 when daot.daot_hier_level = 2 then daot.daot_hier_level_2_code 
                 when daot.daot_hier_level = 3 then daot.daot_hier_level_3_code 
                 when daot.daot_hier_level = 4 then daot.daot_hier_level_4_code 
                 when daot.daot_hier_level = 5 then daot.daot_hier_level_5_code 
               end in ('INSTREC')
     where fao.assmt_instance_rank=1 -- avoid duplicate assmt results in the same period
       and fao.year_sid in ('8')
       and daot.daot_measure_type_code = 'BM_AM'
) 

  

fao
      join dw.fact_enroll fe on 
                                                                     fao.dim_student_key = fe.dim_student_key 
                                                                                                   and fe.is_reporting_classe 
                                            join dw.dim_institution           di      on fe.dim_institution_key      = di.dim_institution_key
                                                                                                                    and not di.demo_flag
                                                                                                                      and ( di.school_sid in ('79394925', '79394423', '79395100', '79395771', '79394101', '79394310', '79395205', '79394622', '15770391', '79395476', '79394066', '79394220', '79395057', '137672224', '79393989', '79394822', '79394491', '79394656', '79396033', '79394353', '79394891', '79395979', '15770388', '15770384', '79394856')
                                                                                                                                )
                                                                                                                                                                                                                                               and di.district_sid
                                                                                                                               in ('15753404')
                                                                                                                        and di.account_sid = '15753406'
                                             join dw.dim_period                dp      on     fao.dim_assmt_period_key        = dp.dim_period_key
                                                            and dp.period_code || '_' || dp.academic_year_code    in ('32_8')
           join dw.dim_perf_level            dpl     on     fao.dim_perf_level_key          = dpl.dim_perf_level_key and                                                            
                                                                                                                         dpl.level_order in ('1', '2', '3')                                                             
                                                                     join dw.dim_grade                 dg      on     fe.dim_grade_key   = dg.dim_grade_key
                                                            and dg.grade_level_sid in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
           join dw.dim_student               dstu    on     fe.dim_student_key             = dstu.dim_student_key
                                                    and not dstu.demo_flag
                                                                                                                                                                                                                                                    ) main
    group by
                account_code,
        account_name,
        account_abbrev,
        state_name,
        state_abbrev,
        state_code,
        school_group_inst_code,
        school_group_inst_name,
        school_group_inst_abbrev,
        school_loc_code,
        school_name,
        school_abbrev,
        grade_code,
        grade_order,
        grade_name,
        subject_code,
        subject_name,
        subject_abbrev,
        course_code,
        course_name,
        course_abbrev,
        staff_sid,
        staff_last_name,
        staff_first_name,
        section_sid,
        section_name,
        section_abbrev,
        attribute_category_code,
        attribute_category_name,
        attribute_value_code,
        attribute_value_label,
        student_first_name,
        student_last_name,
        student_sid,
        student_code,
        school_loc_code_curr,
        assmt_code,
        assmt_name,
        assmt_abbrev,
        assmt_family_code,
        group_code,
        group_name,
        group_abbrev,
        subgroup_rank,
        subgroup_code,
        subgroup_name,
        subgroup_abbrev,
        academic_year_code,
        academic_year_name,
        academic_year_abbrev,
        period_sid,
        period_order,
        period_name,
        period_abbrev,
        level_order,
        level_name,
        level_code,
        assmt_grade_code,
        assmt_grade_order,
        assmt_grade_name
       ) aggregated_measures
       


     group by
           account_code
         , account_name
         , account_abbrev
         , state_name
         , state_abbrev
         , state_code
         , school_group_inst_code
         , school_group_inst_name
         , school_group_inst_abbrev
         , school_loc_code
         , school_name
         , school_abbrev
         , grade_code
         , grade_order
         , grade_name
         , subject_code
         , subject_name
         , subject_abbrev
         , course_code
         , course_name
         , course_abbrev
         , section_sid
         , section_name
         , section_abbrev
         , staff_sid
         , staff_first_name
         , staff_last_name
         , attribute_category_code
         , attribute_category_name
         , attribute_value_code
         , attribute_value_label
         , student_last_name
         , student_first_name
         , student_sid
         , student_code
         , school_loc_code_curr
         , assmt_code
         , assmt_name
         , assmt_abbrev
         , assmt_family_code
         , group_code
         , group_name
         , group_abbrev
         , subgroup_code
         , subgroup_name
         , subgroup_abbrev
         , subgroup_rank
         , academic_year_code
         , academic_year_name
         , academic_year_abbrev
         , period_sid
         , period_order
         , period_name
         , period_abbrev
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name
       )
       
      
  
  aggregated_measures_pivoted
 where entity_num < 50002
