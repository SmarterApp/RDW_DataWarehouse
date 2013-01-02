profile select 'Institution'     as report_comparison_type
     , 1               as report_comparison_type_sid
     , 'Account'            as is_report_level
     , 6              as is_report_level_sid
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
     , 4          as school_group_type_sid
     , 'Programs'     as school_group_type_name
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
       -1 as account_code
     , 'Program' as account_name
     , 'SPA' as account_abbrev
         , case when min(di.state_sid) over(partition by di.account_sid) <> max(di.state_sid) over(partition by di.account_sid) then 'Multiple States' else di.state_name end as state_name
         , case when min(di.state_sid) over(partition by di.account_sid) <> max(di.state_sid) over(partition by di.account_sid) then 'Multi States' else di.state_code end as state_abbrev
         , case when min(di.state_sid) over(partition by di.account_sid) <> max(di.state_sid) over(partition by di.account_sid) then '-1' else di.state_sid end as state_code

                     , dig.inst_group_code            as school_group_inst_code
         , dig.inst_group_name            as school_group_inst_name
         , dig.inst_group_name          as school_group_inst_abbrev
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
                                                                                                                      and ( di.school_sid in ('20438101', '20459216', '43469025', '43706095', '20431661', '43708597', '496944141', '43467662', '43467712', '20507132', '20492789', '43470153', '43708598', '43467688', '20456901', '20487573', '206265284', '43499661', '43489530', '28778011', '362364866', '43469429', '43704940', '43470899', '43701878', '20454039', '48372589', '20485833', '362368302', '43467969', '20512354', '23763112', '28777731', '43705456', '43704151', '20456385', '43708243', '206261316', '20508015', '43469049', '362386476', '20465963', '43467608', '43705059', '20497572', '43470484', '43704748', '20488364', '20508235', '20481663', '130678856', '20507941', '43702902', '91676218', '43498394', '43489679', '43470947', '43489774', '43473330', '43708324', '43467861', '43704700', '43499711', '43706348', '43470129', '43703410', '47932844', '43706913', '20441339', '43470859', '43708720', '43704796', '20492159', '20441969', '43703580', '43703241', '43705503', '43707209', '43468082', '29457557', '20425933', '43707346', '43468433', '43704508', '43705131', '43498419', '43705717', '43704034', '43470703', '20495621', '20431307', '43703628', '43469957', '43489731', '43468238', '43473403', '43703434', '20512799', '43702539', '20495145', '43708539', '43702047', '43708793', '20495902', '43470923', '43499449', '20458966', '43473453', '43706404', '20496031', '43703963', '43708217', '20487147', '43470316', '20465448', '362369232', '43706774', '20461597', '20481295', '20493073', '43469073', '20492460', '43469276', '43703363', '43706278', '43707920', '43469186', '43499511', '43703604', '20438682', '43707895', '43468289', '43706822', '20461253', '43468313', '20493420', '20486245', '20438337', '20497414', '43707095', '43473652', '43498444', '43704844', '43498359', '362364870', '43470737', '43707806', '43499613', '43705646', '45929337', '43473489', '43706071', '43700948', '43709048', '43703655', '23225020', '43706224', '43469596', '43707710', '43514330', '20432692', '29457364', '43708767', '43489076', '20506072', '43705749', '20508641', '43705796', '43705914', '130677887', '20436203', '43468361', '43468209', '20488258', '43467811', '43702823', '43704484', '43705551', '20440934', '491856434', '20440760', '20506627', '43705598', '20454818', '43705527', '43702702', '43467534', '43470005', '43469933', '43704868', '43469001', '43706726', '152732072', '43704388', '43705107', '20490700', '20438798', '43499810', '43468337', '20506356', '43704293', '20434180', '43705975', '43499637', '43708573', '20485394', '20438546', '43514303', '20425541', '43707371', '43703029', '43705843', '43703505', '43707280', '29456636', '43470532', '43704676', '28777891', '43703774', '43701534', '20497546', '43703529', '43706501', '43467634', '20488485', '362366296', '43467760', '43470679', '43468481', '43704175', '43701230', '43705233', '20488602', '43470835', '29457854', '43706847', '43706750', '23225037', '43707567', '43498335', '43704081', '20465734', '43703481', '217670146', '43470809', '29457409', '20464708', '43706635', '43708696', '43488078', '43706023', '43499834', '20494691', '20477175', '43706474', '362364872', '20455010', '43704652', '43489837', '43473609', '20488222', '43704317', '43704628', '43468138', '43707734', '43468265', '43704412', '43489274', '43470655', '43469622', '43467583', '20487358', '20497598', '20488603', '43488981', '217671322', '20510504', '20496146', '483338772', '43470628', '43707500', '43705370', '20487526', '43703750', '43470177', '29456622', '20514298', '43469909', '43470292', '20512468', '20508854', '43469811', '43469162', '43498418', '20497494', '43469783', '43706607', '20426059', '43708648', '43699324', '43704437', '43513997', '20494786', '43704724', '43489336', '43468385', '20509885', '20462312', '43705180', '20437592', '43489298', '43470436', '43468887', '43470630', '43703939', '20478326', '43468558', '43706047', '43490105', '29456623', '20435729', '43469659', '43498516', '43708193', '43704010', '43499910', '43473560', '43470508', '43488957', '20515406', '43704892', '43707121', '43706961', '43468000', '43499773', '43708376', '43699776', '20496175', '43704772', '43706987', '43489434', '43468409', '43707169', '43703868', '43706376', '43470785', '20462075', '43706582', '43469709', '43498468', '43707686', '43489161', '28777217', '28777630', '20510183', '20441105', '43470388', '362364868', '43499934', '43707396', '20489574', '43706249', '43467558', '43706872', '43468457', '29457123', '43473340', '43470971', '20484096', '20515000', '43470029', '43470364', '43704999', '20497522', '43470580', '43706121', '20514001', '20438426', '43701714', '20511516', '43705397', '20482222', '362386478', '494433999', '20435957', '43470604', '43706149', '43707758', '43470092', '43468939', '20455131', '43488005', '43708012', '43703679', '20493791', '43470761', '20478302', '43489185', '43703148', '29457032', '43469733', '43707948', '43473585', '43703915', '43702209', '43514227', '43467885', '43468529', '43705693', '20509130', '20466829', '43708060', '43499422', '43703316', '43708036', '20490777', '20570782', '43489008', '43706437', '43703556', '20495078', '43705083', '43468582', '20454497', '20456689', '43470340', '483337258', '20467257', '20441265', '43708510', '20487967', '43700596', '43700760', '43704532', '20495237', '20435623', '28777424', '20497469', '43468505', '20467109', '20432394', '43706937', '43703821', '43469405', '43704364', '43469848', '43473372', '43470833', '20511931', '29456545', '43467485', '43703703', '43705622', '43468977', '43467909', '43704580', '43470631', '43704604', '20467455', '28778041', '43704246', '43707524', '43706179', '43469885', '43468113', '43704556')
                                                                                                                                )
                                                                                                                                                                                  join   dw.map_inst_group_inst migi on di.dim_institution_key = migi.dim_institution_key
join   dw.dim_inst_group dig on migi.dim_inst_group_key = dig.dim_inst_group_key
                            and dig.inst_group_type_code = '33' and dig.inst_group_code
                                                                                                                               in ('174897917', '244554048', '370401232', '373872746', '422209414', '425072528', '425099104', '425125894', '425133992', '425161932', '425193016', '425224358', '425233856', '425254226', '425254346', '425254574', '425325990', '425341672', '425356978', '425363860', '444979174', '444990860', '505443662', '505448392', '506381982', '508945973', '508949953', '508952381', '508958390', '508962804', '508967441', '508967452', '508968361', '508968598', '508968952', '508969350', '508969845', '508970831', '508971128', '508972085', '508972619', '508973311', '508973784', '508974018', '508974522', '508974992', '508975076', '508975353', '508975589', '508976292', '508976465', '508996250', '509006948', '509007992', '509009309', '509009842', '509010248', '509010924', '509011694', '509011952', '509012072', '509012136', '509012215', '509012373', '509121112', '509124308', '509148664', '509149371', '509150603', '509151593', '509152601', '509153403', '509154896', '509160398', '509160961', '509162581', '509163661', '509164769', '509165805', '509166960', '509168034', '509169493', '509170142', '527732702')
                                                                                                   join dw.dim_period                dp      on     fao.dim_assmt_period_key        = dp.dim_period_key
                                                            and dp.period_code || '_' || dp.academic_year_code    in ('31_8')
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
