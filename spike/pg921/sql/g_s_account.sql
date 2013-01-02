profile select *
                              from 
  


( 
select     'Institution'     as report_comparison_type
         , 1               as report_comparison_type_sid
         , 'Account'            as is_report_level
         , 6              as is_report_level_sid
         , null                         as is_refpoint_level
         , null                         as refpoint_level_inst_name
         , null                         as refpoint_level_inst_sid
         , null                         as refpoint_level_inst_code
         , null                         as state_sid
         , state_code
         , state_name
         , state_abbrev
         , account_code
         , account_name
         , account_abbrev
         , 3          as school_group_type_sid
         , 'Districts'     as school_group_type_name
         , null                         as school_group_inst_sid
         , school_group_inst_code
         , school_group_inst_name
         , school_group_inst_abbrev
         , null                         as school_sid
         , school_loc_code
           
         , FIRST_VALUE(school_name) over (partition by school_loc_code ORDER BY academic_year_code::integer DESC)
                                        as school_name
         , school_abbrev
         
         , staff_sid                    as staff_code                    , staff_sid                    as staff_sid
         , staff_first_name
         , staff_last_name
     , staff_last_name || ', ' || nvl(staff_first_name, '')  as staff_full_name 
         , null                         as grade_sid
         , grade_code
         , grade_order
         , grade_name
         , null                         as subject_sid
         , subject_code
         , subject_name
         , subject_abbrev
         , null                         as course_sid
         , course_code
         , course_name
         , course_abbrev
         , section_sid                  as section_code
         , section_sid
         , section_name
         , section_abbrev
         , null                         as term_sid
         , null                         as term_code
         , null                         as term_name
         , null                         as term_abbrev
         , student_first_name
         , student_last_name
     , student_last_name || ', ' || student_first_name  as student_full_name
         , student_sid
         , student_code
         , null                         as dim_student_key 
         , null                         as applicable_schools
         , null                         as applicable_subjects
         , null                         as applicable_courses
         , attribute_category_name      as attribute_category_label
         , attribute_category_code      as attribute_category_code
         , null                         as attribute_category_sid
         , attribute_value_label        as attribute_row_label
         , attribute_value_code         as attribute_row_code
         , null                         as attribute_row_sid
         , null                         as assmt_sid
         , assmt_code
         , assmt_name
         , assmt_abbrev
         , assmt_family_code
         , null                         as group_type_cid
         , null                         as group_type_cname
         , null                         as group_sid
         , group_code
         , group_name
         , group_abbrev
         , null                         as group_seq
         , null                         as subgroup_sid
         , subgroup_code
         , subgroup_name
         , subgroup_abbrev
         , subgroup_rank
         , null                         as subgroup_seq
         , null                         as academic_year_sid
         , academic_year_code
         , academic_year_name
         , academic_year_abbrev
         , period_sid
         , period_order
         , period_name
         , period_abbrev
         , null                         as unified_period_label
         , null                         as unified_period_sid
         , null                         as applicable_periods
         , null                         as ranks
         , 1                            as pagenum
         , null                         as unified_series_label
         , has_series_level
         , series_level_order
         , series_level_displaylabel
         , 3                            as pii_row_flag
         , 2                            as allow_drilldown_flag
                                     , sum_raw_score
         , sum_scale_score
         , sum_percent_correct
         , sum_num_correct
         , measure_count as total_students
         , measure_count as return_val
         , sum(measure_count)
                over(partition by 
                     account_code
                   , school_group_inst_code
                   , school_loc_code
                   , grade_code
                   , subject_code
                   , course_code
                   , staff_sid
                   , section_sid
                   , attribute_category_code
                   , attribute_value_code
                   , student_sid
                   , assmt_code
                   , group_code
                   , subgroup_code
                   , academic_year_code
                   , period_sid) as sum_of_count
             
         , sum(measure_count)
                over(partition by 
                     account_code
                   , school_group_inst_code
                   , school_loc_code
                   , grade_code
                   , subject_code
                   , course_code
                   , staff_sid
                   , section_sid
                   , attribute_category_code
                   , attribute_value_code
                   , student_sid
                   , assmt_code
                   , group_code
                   , subgroup_code
                   , academic_year_code
                   , period_sid)            as aggregation_size
         , academic_year_code               as year
             
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
         , account_name
         , account_abbrev
         , state_code
         , state_name
         , state_abbrev
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
         , staff_sid 
         , staff_last_name
         , staff_first_name
         , section_sid
         , section_name
         , section_abbrev
         , attribute_category_code
         , attribute_category_name
         , attribute_value_code
         , attribute_value_label
              , null::char as student_first_name
         , null::char as student_last_name
         , null::char as student_sid  
         , null::char as student_code
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
         , dpl.level_order as series_level_order
         , dpl.measure_specific_level_name  as series_level_displaylabel
         , has_series_level
         , sum(raw_score) as sum_raw_score
         , sum(scale_score) as sum_scale_score
         , sum(num_correct) as sum_num_correct
         , sum(percent_correct) as sum_percent_correct
         , count(1) as measure_count
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name
from 


(select 
           account_code
         , account_name
         , account_abbrev         
         , state_code
         , state_name
         , state_abbrev
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
         , staff_sid 
         , staff_last_name
         , staff_first_name
         , section_sid
         , section_name
         , section_abbrev
         , attribute_category_code
         , attribute_category_name
         , attribute_value_code
         , attribute_value_label
         , student_first_name
         , student_last_name
         , student_sid
              , student_code
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
         , max(raw_score) as raw_score
         , max(scale_score) as scale_score
         , max(num_correct) as num_correct
         , max(percent_correct) as percent_correct
         , max(dim_perf_level_key) as perf_level_key
         , max(case when has_series_level then 1 else 0 end) as has_series_level
         , count(*) over (partition by student_sid,
                                                                            school_loc_code
                                                                        ) std_total_rows
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name
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
                       , null::char                      as grade_code
         , null::char                      as grade_order
         , null::char                      as grade_name
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
              , dstu.first_name           as student_first_name
         , dstu.last_name            as student_last_name
         , dstu.eternal_student_sid          as student_sid
         , dstu.student_sid                      as student_code
    --     , dim_assmt_grade_key, dim_assmt_institution_key 
              , daot.assmt_code           as assmt_code
         , daot.assmt_name as assmt_name
         , daot.assmt_name as assmt_abbrev
         , case when daot.assmt_code = '706s' or daot.assmt_code = '706' then 'TRC All Versions' else assmt_version_code end    as assmt_family_code
         , daot.daot_hier_level_code           as group_code
         , daot.daot_hier_level_name           as group_name
         , daot.daot_hier_level_name         as group_abbrev
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
         , daot.daot_hier_level_rank as subgroup_rank
         , dp.academic_year_code     as academic_year_code
         , dp.academic_year_name     as academic_year_name
         , dp.academic_year_abbrev   as academic_year_abbrev
         , dp.period_code || '_' || dp.academic_year_code   as period_sid -- really this is period_sid
         , dp.period_order           as period_order
         , dp.academic_year_abbrev || ' ' || dp.period_abbrev as period_name 
         , dp.period_abbrev as period_abbrev
         , daot.performance_level_flag  as has_series_level
         , dpl.dim_perf_level_key 
         , case when daot.outcome_int_code = 'RAWSCORE' 
                    then fao.outcome_int
                    else null::numeric end as raw_score
         , case when daot.outcome_int_code = 'SCORE' 
                    then fao.outcome_int
                    else null::numeric end as scale_score
         , null::numeric  as num_correct  -- TODO: we don't have num correct data yet
         , null::numeric  as percent_correct -- TODO: we don't have num correct data yet
                 , null::char                         as assmt_grade_code
         , null::numeric                      as assmt_grade_order
         , null::char                         as assmt_grade_name
              from      dw.fact_assmt_outcome        fao
      join dw.fact_enroll fe on 
                                                                     fao.dim_student_key = fe.dim_student_key 
                                                                                                   and fe.is_reporting_classe
                                                                  and fao.year_sid in ('8')
           join dw.dim_institution           di      on  fe.dim_institution_key      = di.dim_institution_key
                                                                                                                    and not di.demo_flag
                                                                                                                      and ( di.school_sid in ('79395402', '79394925', '79394423', '79395100', '79395771', '79394101', '79394310', '79395205', '79394622', '15770391', '79395476', '79396107', '79394066', '79394220', '79395057', '137672224', '79393989', '79394822', '79394491', '79394656', '79396145', '79396033', '79394353', '79394891', '79395979', '15770388', '15770384', '79394856', '79395882', '79394726', '79394525', '15770390', '79395839', '15770386', '79394148', '79394691', '79394960', '15770387', '79394457', '15770385', '79394389', '91032670', '79394761', '79394254', '79395534', '15770389', '79396192', '79394567', '79393953')
                                                                                                                                )
                                                                                                                                                                                                                                               and di.district_sid
                                                                                                                               in ('15753404')
                                                                                                          and di.account_sid = '15753406'
                                       join dw.dim_assmt_outcome_type    daot    on     fao.dim_assmt_outcome_type_key  = daot.dim_assmt_outcome_type_key
                                                            and daot.assmt_code in ('7')
                                                                                                                                  and case
                                                                            when daot.assmt_code = '706' then true
                                                                            when daot.assmt_code = '706s' then true
                                                                            else daot.assmt_version_code in ('1')
                                                                          end
                                                                                                                                                                                    and daot.daot_hier_level_code                in ('2')
                                                                                                                        and 
                                                               case 
                                                                 when daot.daot_hier_level = 1 then daot.daot_hier_level_1_code 
                                                                 when daot.daot_hier_level = 2 then daot.daot_hier_level_2_code 
                                                                 when daot.daot_hier_level = 3 then daot.daot_hier_level_3_code 
                                                                 when daot.daot_hier_level = 4 then daot.daot_hier_level_4_code 
                                                                 when daot.daot_hier_level = 5 then daot.daot_hier_level_5_code 
                                                               end
                                                                 in ('INSTREC')
                                                                                                                        and daot.daot_measure_type_code = 'BM_AM'
           join dw.dim_period                dp      on     fao.dim_assmt_period_key        = dp.dim_period_key
                                                            and dp.period_code || '_' || dp.academic_year_code    in ('31_8', '32_8', '33_8')
           join dw.dim_perf_level            dpl     on     dpl.dim_perf_level_key = fao.dim_perf_level_key
                                                              and daot.performance_level_flag and dpl.level_order > 0 and dpl.level_order < 6
                                                              join dw.dim_grade                 dg      on     fe.dim_grade_key   = dg.dim_grade_key              
                                                          and dg.grade_level_sid in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
           join dw.dim_student               dstu    on     fe.dim_student_key             = dstu.dim_student_key
                                                    and not dstu.demo_flag
                                                                                                                                                                                                                                                                                                   
       where fao.assmt_instance_rank         = 1
)


measures
group by
           account_code
         , account_name
         , account_abbrev
         , state_code
         , state_name
         , state_abbrev
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
         , staff_sid 
         , staff_last_name
         , staff_first_name
         , section_sid
         , section_name
         , section_abbrev
         , attribute_category_code
         , attribute_category_name
         , attribute_value_code
         , attribute_value_label
         , student_first_name
         , student_last_name
         , student_sid
              , student_code
      --   , dim_assmt_grade_key, dim_assmt_institution_key // count out of grade/transfer separately?
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


flat_measures
 join dw.dim_perf_level dpl on dpl.dim_perf_level_key = perf_level_key
    group by
           account_code
         , account_name
         , account_abbrev
         , state_code
         , state_name
         , state_abbrev
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
         , staff_sid 
         , staff_last_name
         , staff_first_name
         , section_sid
         , section_name
         , section_abbrev
         , attribute_category_code
         , attribute_category_name
         , attribute_value_code
         , attribute_value_label
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
         , dpl.level_order
         , dpl.measure_specific_level_name
         , has_series_level
         , assmt_grade_code
         , assmt_grade_order
         , assmt_grade_name
)


aggregated_measures
)


  
  agg_measures_ranked_sums
 where entity_num < 266666
