select 
student_t.student_key,
student_t.eternal_student_id as student_code,
student_t.last_name || ', ' ||student_t.first_name as student_name,
grade_t.name as grade_name,
assessment_t.subject_name as subject_name,
assessment_t.time_period as period_name,
assessment_t.year_range,
fact.assessment_score,
'50-59' as benchmark,
case 
 when fact.assessment_score < 50 then 'Below Benchmark'
 when fact.assessment_score >= 50 and fact.assessment_score < 60 then 'Benchmark'
 else 'Above Benchmark'
end as performance_level, 
state_t.name as state_name,
teacher_t.last_name || ', ' || teacher_t.first_name as teacher_name,
school_t.name as school_name,
school_grp_t.name as school_group_name,
state_grp_t.name as state_group_name,
school_grp_t.group_of_school_key as school_group_code,
school_t.school_key as school_code,
teacher_t.teacher_key as teacher_code,
student_t.eternal_student_id as student_code,
time_t.id as period_code,
1 as student_count,
grade_t.grade_key as grade_order
from 
fact_assessment_result fact,
dim_time time_t,
dim_teacher teacher_t,
dim_state state_t,
dim_school school_t,
dim_group_of_school school_grp_t,
dim_group_of_state state_grp_t,
dim_grade grade_t,
dim_assessment assessment_t,
dim_student student_t
where 
student_t.student_key=6201
and fact.student_id=student_t.student_key
and time_t.id=fact.time_id
and teacher_t.teacher_key=fact.teacher_id
and state_t.state_key=fact.state_id
and school_t.school_key=fact.school_id
and school_grp_t.group_of_school_key=fact.group_of_school_id
and state_grp_t.group_of_state_key=fact.group_of_state_id
and grade_t.grade_key=fact.grade_id
and assessment_t.assessment_key=fact.assessment_id
--grade filter if not all -- grade_t.code in () and
% if (grades[0] != 'ALL'):
and grade_t.code in ${grades}
% endif
-- time filter if not all -- assessment_t.year_range in () and
% if year_range[0] != 'ALL':
and assessment_t.year_range in ${year_range}
% endif
-- district filter if not null -- school_grp_t.group_of_school_key in () and
% if district_filter:
and school_grp_t.group_of_school_key in ${district}
% endif
-- period filter if not all --  assessment_t.time_period in () and
% if time_period[0] != 'ALL':
and assessment_t.time_period in ${time_period}
% endif
-- school filter if not all - school_t.school_key in () and
% if school_filter[0] != 'ALL':
and school_t.school_key in ${school_filter}
% endif
-- teacher filter if not all -- 
% if teacher_filter[0] != 'ALL':
and teacher_t.teacher_key in ${teacher_filter}
% endif
-- performance level if not all -- no column in schema
-- student demographics -- no column in schema
order by school_grp_t.name, teacher_t.last_name, student_t.last_name, grade_order, assessment_t.subject_name, assessment_t.year_range