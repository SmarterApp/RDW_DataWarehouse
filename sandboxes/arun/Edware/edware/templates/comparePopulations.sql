	select
	% if segment_by=="student":
		student_t.student_key,
		student_t.eternal_student_id as student_code,
		student_t.last_name || ', ' ||student_t.first_name as student_name,
		fact.assessment_score,	
		1 as student_count,		
	% else:
		null as student_key,
		null as student_code,
		null as student_name,
		round(cast (avg(fact.assessment_score) as numeric),2) :: float as assessment_score,
		count(1) as student_count,
	% endif
	% if (segment_by=="student" or segment_by=="teacher"):
		teacher_t.teacher_key as teacher_code,	
		teacher_t.last_name || ', ' || teacher_t.first_name as teacher_name,
	% else:
		null as teacher_code,	
		null as teacher_name,
	% endif
	% if (segment_by=="student" or segment_by=="teacher" or segment_by=="school"):	
		school_t.school_key as school_code,	
		school_t.name as school_name,
	% else:
		null as school_code,	
		null as school_name,
	% endif
	school_grp_t.group_of_school_key as school_group_code,	
	school_grp_t.name as school_group_name,
	time_t.id as period_code,
	% if (segment_by=="student" or grade_divider=="true"):
		grade_t.grade_key as grade_order,
		grade_t.name as grade_name,
	% else:
		null as grade_order,
		null as grade_name,
	% endif	
	assessment_t.subject_name as subject_name,
	assessment_t.time_period as period_name,
	assessment_t.year_range,
	state_grp_t.name as state_group_name,
	state_t.name as state_name,
	case 
	 when fact.assessment_score < 50 then 'Below Benchmark'
	 when fact.assessment_score >= 50 and fact.assessment_score < 60 then 'Benchmark'
	 else 'Above Benchmark'
	end as performance_level 
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
	fact.student_id=student_t.student_key
	and time_t.id=fact.time_id
	and teacher_t.teacher_key=fact.teacher_id
	and state_t.state_key=fact.state_id
	and school_t.school_key=fact.school_id
	and school_grp_t.group_of_school_key=fact.group_of_school_id
	and state_grp_t.group_of_state_key=fact.group_of_state_id
	and grade_t.grade_key=fact.grade_id
	and assessment_t.assessment_key=fact.assessment_id
	--student id filter
	% if student_id:
	and student_t.student_key = ${student_id}
	% endif
	--grade filter if not all -- grade_t.code in () and
	% if (grades and grades[0] != 'ALL'):
	and grade_t.code in ${grades}
	% endif
	-- time filter if not all -- assessment_t.year_range in () and
	% if (year_range and year_range[0] != 'ALL'):
	and assessment_t.year_range in ${year_range}
	% endif
	-- district filter if not null -- school_grp_t.group_of_school_key in () and
	% if (district_filter and district_filter[0] != 'ALL'):
	and school_grp_t.group_of_school_key in ${district_filter}
	% endif
	-- period filter if not all --  assessment_t.time_period in () and
	% if (time_period and time_period[0] != 'ALL'):
	and assessment_t.time_period in ${time_period}
	% endif
	-- school filter if not all - school_t.school_key in () and
	% if (school_filter and school_filter[0] != 'ALL'):
	and school_t.school_key in ${school_filter}
	% endif
	-- teacher filter if not all -- 
	% if (teacher_filter and teacher_filter[0] != 'ALL'):
	and teacher_t.teacher_key in ${teacher_filter}
	% endif
	% if (subject_code and subject_code[0] != 'ALL'):
	and assessment_t.subject_code in ${subject_code}
	% endif
	% if segment_by !="student":
	group by
		% if segment_by =="teacher":
			teacher_t.teacher_key,	
			teacher_t.last_name,		
		% endif
		% if (segment_by=="teacher" or segment_by=="school"):		
				school_t.school_key,	
				school_t.name,
		% endif
		school_grp_t.group_of_school_key,	
		school_grp_t.name,
		time_t.id,
		% if (segment_by=="student" or grade_divider=="true"):		
			grade_t.grade_key,	
			grade_t.name,
		% endif			
		assessment_t.subject_name,
		assessment_t.time_period,
		assessment_t.year_range,
		state_grp_t.name,
		state_t.name,
		case 
	 		when fact.assessment_score < 50 then 'Below Benchmark'
	 		when fact.assessment_score >= 50 and fact.assessment_score < 60 then 'Benchmark'
	 		else 'Above Benchmark'
		end		
	% endif
	-- performance level if not all -- no column in schema
	-- student demographics -- no column in schema
	order by 
	school_grp_t.name,
	% if (segment_by=="student" or segment_by=="teacher"):	
	teacher_t.last_name, 
	% endif
	% if (segment_by=="student"):	
	student_t.last_name, 
	% endif
	grade_order, 
	assessment_t.year_range,
	assessment_t.time_period,
	assessment_t.subject_name
	