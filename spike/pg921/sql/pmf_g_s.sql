profile select * from (
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
     , null::char            as assmt_family_code
       
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
     , sum_measure_count            as sum_of_count
     , level_order     
     , level_code
     , level_label
          , null::char                         as level_bucket
          , null::char                         as score_retval
     , null::char                         as ranks
     , null::char                         as operating_sortby_val
     
     , sum(sum_measure_count)over()     as sum_of_count_aggr
         
     , sum_measure_count                as aggregation_size
     , academic_year_code               as year
         , display_date                     as as_of_date
     , to_char(as_of_date, 'mm/dd/yyyy') as calendar_date
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
  


(
    select
        account_code
        ,account_name
        ,account_abbrev
        ,state_name
        ,state_abbrev
        ,state_code
        ,school_group_inst_code
        ,school_group_inst_name
        ,school_group_inst_abbrev
        ,school_loc_code
        ,school_name
        ,school_abbrev
        ,grade_code
        ,grade_order  
        ,grade_name
        ,subject_code
        ,subject_name
        ,subject_abbrev
        ,course_code
        ,course_name
        ,course_abbrev
        ,staff_sid
        ,staff_last_name
        ,staff_first_name
        ,section_sid
        ,section_name
        ,section_abbrev
        ,attribute_category_code
        ,attribute_category_name
        ,attribute_value_code
        ,attribute_value_label
        ,student_first_name
        ,student_last_name
        ,student_sid
        ,student_code
        ,school_loc_code_curr
        ,assmt_code 
        ,assmt_name
        ,assmt_abbrev
        ,group_code
        ,group_name
        ,group_abbrev         
        ,subgroup_rank
        ,subgroup_code 
        ,subgroup_name 
        ,subgroup_abbrev 
        ,academic_year_code
        ,academic_year_name
        ,academic_year_abbrev
        ,period_sid 
        ,period_order
        ,period_name  
        ,period_abbrev
        ,level_order
        ,level_code
        ,level_label
        ,display_date
        ,as_of_date
         , max(performance_level_flag) as performance_level_flag
         , count(1)                  as sum_measure_count
         , count(case when max_pm_date is not null and  case when level_order=1 then 2 = -1 or as_of_date - max_pm_date < 2 * 7
                                                                    when level_order=2 then 4 = -1 or as_of_date - max_pm_date < 4 * 7
                                                                    when level_order=3 then 0 = -1 or as_of_date - max_pm_date < 0 * 7
                                                                    when level_order=4 then -2 = -1 or as_of_date - max_pm_date < -2 * 7
                                                                    when level_order=5 then -2 = -1 or as_of_date - max_pm_date < -2 * 7
                                                                    end
                 then 1 else null end) as level_1_count            
         , count(case when max_pm_date is not null and  case when level_order=1 then 2 <> -1 and as_of_date - max_pm_date >= 2 * 7
                                                                    when level_order=2 then 4 <> -1 and as_of_date - max_pm_date >= 4 * 7
                                                                    when level_order=3 then 0 <> -1 and as_of_date - max_pm_date >= 0 * 7
                                                                    when level_order=4 then -2 <> -1 and as_of_date - max_pm_date >= -2 * 7
                                                                    when level_order=5 then -2 <> -1 and as_of_date - max_pm_date >= -2 * 7
                                                                    end
                 then 1 else null end) as level_2_count
         , count(case when max_pm_date is null then 1 else null end) as level_3_count
         , 0 as level_4_count
         , 0 as level_5_count         
         , 'At Rate' as level_1_label
         , 'Below Rate' as level_2_label
         , 'None' as level_3_label
         , null::char as level_4_label
         , null::char as level_5_label
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name
      from    
(
select        di.account_sid as account_code
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
                , bm.assmt_code           as assmt_code 
         , bm.assmt_name as assmt_name
         , bm.assmt_name as assmt_abbrev
         , bm.daot_hier_level_code           as group_code
         , bm.daot_hier_level_name           as group_name
         , bm.daot_hier_level_name         as group_abbrev         
         , bm.daot_hier_level_rank         as subgroup_rank
         , case 
             when daot_hier_level = 1 then daot_hier_level_1_code 
             when daot_hier_level = 2 then daot_hier_level_2_code 
             when daot_hier_level = 3 then daot_hier_level_3_code 
             when daot_hier_level = 4 then daot_hier_level_4_code 
             when daot_hier_level = 5 then daot_hier_level_5_code 
           end
             as subgroup_code 
         , null -- so don't group Dibles 6.0 and D-Next separately
             as subgroup_name  
         , null
             as subgroup_abbrev 
         , performance_level_flag as performance_level_flag
         , dp.academic_year_code     as academic_year_code
         , dp.academic_year_name     as academic_year_name
         , dp.academic_year_abbrev   as academic_year_abbrev
         , dp.period_code || '_' || dp.academic_year_code   as period_sid -- really this is period_sid
         , dp.period_order           as period_order
         , dp.academic_year_abbrev || ' ' || dp.period_abbrev as period_name  
         , dp.period_abbrev as period_abbrev
         , dpl.level_order           as level_order
         , dpl.general_level_code          as level_code
         , case when bm.assmt_code = '7' then 
          --dpl.measure_type_specific_level_name
            case when dpl.level_order = 1 then 'Intensive'
            when dpl.level_order = 2 then 'Strategic'
            when dpl.level_order = 3 then 'Benchmark' end
         else dpl.measure_specific_level_name end           as level_label
          
         , dates.as_of_date    
         , dates.display_date
         , pm.calendar_date max_pm_date
,ROW_NUMBER() OVER (PARTITION BY dates.as_of_date, 
fe.dim_student_key
                                      ORDER BY pm.calendar_date DESC ) pm_date_rank
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
         , 1 performance_level_flag
         , calendar_date
      from dw.fact_assmt_outcome fao
      join dw.dim_assmt_outcome_type daot
           on fao.dim_assmt_outcome_type_key  = daot.dim_assmt_outcome_type_key
          
          and daot.assmt_code         in ('7')
                  and  case 
                 when daot.daot_hier_level = 1 then daot.daot_hier_level_1_code 
                 when daot.daot_hier_level = 2 then daot.daot_hier_level_2_code 
                 when daot.daot_hier_level = 3 then daot.daot_hier_level_3_code 
                 when daot.daot_hier_level = 4 then daot.daot_hier_level_4_code 
                 when daot.daot_hier_level = 5 then daot.daot_hier_level_5_code 
               end in ('INSTREC')
      join dw.dim_time dt on fao.dim_assmt_time_key = dt.dim_time_key
     where
       fao.assmt_instance_rank=1 -- avoid duplicate assmt results in the same period
       and daot.daot_hier_level_code    in ('2')       
          and  case 
                 when daot.daot_hier_level = 1 then daot.daot_hier_level_1_code 
                 when daot.daot_hier_level = 2 then daot.daot_hier_level_2_code 
                 when daot.daot_hier_level = 3 then daot.daot_hier_level_3_code 
                 when daot.daot_hier_level = 4 then daot.daot_hier_level_4_code 
                 when daot.daot_hier_level = 5 then daot.daot_hier_level_5_code 
               end in ('INSTREC')
       and fao.year_sid in ('8')
       and daot.daot_measure_type_code = 'BM_AM'
       and daot.performance_level_flag
) bm

           join dw.dim_perf_level            dpl     on     bm.dim_perf_level_key          = dpl.dim_perf_level_key and                                                            
                                                                                                                           dpl.level_order in ('1', '2')                                                                  
                                                                       join dw.dim_period                dp      on     bm.dim_assmt_period_key        = dp.dim_period_key
                                                            and dp.period_code || '_' || dp.academic_year_code    in ('33_8')   
join dw.fact_enroll fe                           on bm.eternal_student_sid = fe.eternal_student_sid                                 
                                                   and bm.year_sid = fe.year_sid
                                                                                                      and fe.is_reporting_classe 
                                                              join dw.dim_institution           di      on fe.dim_institution_key      = di.dim_institution_key
                                                                                                                    and not di.demo_flag
                                                                                                                      and ( di.school_sid in ('79395402', '79394925', '79394423', '79395100', '79395771', '79394101', '79394310', '79395205', '79394622', '15770391', '79395476', '79396107', '79394066', '79394220', '79395057', '137672224', '79393989', '79394822', '79394491', '79394656', '79396145', '79396033', '79394353', '79394891', '79395979')
                                                                                                                                )
                                                                                                                                                                                                                                               and di.district_sid
                                                                                                                               in ('15753404')
                                                                                                                        and di.account_sid = '15753406'
                                  
join dw.dim_grade                 dg      on     fe.dim_grade_key   = dg.dim_grade_key
                                        and dg.grade_level_sid in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
join dw.dim_student               dstu    on     fe.dim_student_key             = dstu.dim_student_key
                                                    and not dstu.demo_flag
                                                                                                                                                                                                                        
cross join (select calendar_date as as_of_date, case when calendar_date = current_date then 'Now*' else to_char(calendar_date, 'mm/dd/yyyy') end as display_date  from dw.dim_time where calendar_date in ('08/31/2010')) dates
left join
(
select dim_student_key
         , eternal_student_sid   
         , dim_assmt_period_key 
         , calendar_date
      from dw.fact_assmt_outcome fao
      join dw.dim_assmt_outcome_type daot
           on fao.dim_assmt_outcome_type_key  = daot.dim_assmt_outcome_type_key
          and daot.assmt_code         in ('7')
      join dw.dim_time dt on fao.dim_assmt_time_key = dt.dim_time_key
     where fao.year_sid in ('8')
       and daot.daot_measure_type_code = 'PM_DI'
     group by dim_student_key
         , eternal_student_sid, dim_assmt_period_key, calendar_date
) pm
on bm.eternal_student_sid = pm.eternal_student_sid
and bm.dim_assmt_period_key = pm.dim_assmt_period_key
and dates.as_of_date >= pm.calendar_date
                    
           join dw.dim_time dt1 on fe.dim_inst_admit_time_key = dt1.dim_time_key
                               and dt1.calendar_date <= dates.as_of_date
           join dw.dim_time dt2 on fe.dim_inst_disc_time_key = dt2.dim_time_key
                               and dt2.calendar_date > dates.as_of_date


      
           
                                where bm.calendar_date <= dates.as_of_date) bm_pm
    where bm_pm.pm_date_rank=1
    group by
        account_code
        ,account_name
        ,account_abbrev
        ,state_name
        ,state_abbrev
        ,state_code
        ,school_group_inst_code
        ,school_group_inst_name
        ,school_group_inst_abbrev
        ,school_loc_code
        ,school_name
        ,school_abbrev
        ,grade_code
        ,grade_order  
        ,grade_name
        ,subject_code
        ,subject_name
        ,subject_abbrev
        ,course_code
        ,course_name
        ,course_abbrev
        ,staff_sid
        ,staff_last_name
        ,staff_first_name
        ,section_sid
        ,section_name
        ,section_abbrev
        ,attribute_category_code
        ,attribute_category_name
        ,attribute_value_code
        ,attribute_value_label
        ,student_first_name
        ,student_last_name
        ,student_sid
        ,student_code
        ,school_loc_code_curr
        ,assmt_code 
        ,assmt_name
        ,assmt_abbrev
        ,group_code
        ,group_name
        ,group_abbrev         
        ,subgroup_rank
        ,subgroup_code 
        ,subgroup_name 
        ,subgroup_abbrev 
        ,academic_year_code
        ,academic_year_name
        ,academic_year_abbrev
        ,period_sid 
        ,period_order
        ,period_name  
        ,period_abbrev
        ,level_order
        ,level_code
        ,level_label
         , assmt_grade_code
         , assmt_grade_order
          , assmt_grade_name
        ,as_of_date
        ,display_date
       ) aggregated_measures
       

) with_entity_num

 where entity_num < 50002
