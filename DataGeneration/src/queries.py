# get all states
query0 = "select state_name, state_code, count(distinct dist_name) AS dist_num from school_raw_stat where length(state_name) > 0 group by state_name, state_code order by state_name"
# query1 = "select distinct state_name from school_stat where length(state_name) > 0 order by state_name"
query2_first = "select count(*) from school_raw_stat where state_name='"
query2_second = "' group by dist_name order by dist_name"
query3_first = "select dist_name, school_name,num_of_stu from school_raw_stat where state_name='"
query3_second = "' order by dist_name, school_name"
query4_first = "select dist_name, school_level, count(*) from school_raw_stat where state_name='"
query4_second = "' group by dist_name, school_level order by dist_name"
query5_first = "select dist_name, school_name,num_of_teacher from school_raw_stat where state_name='"
query5_second = "' order by dist_name, school_name"

query6_first = "select dist_name, school_name,stu_teacher_rario from school_raw_stat where state_name= '"
query6_second = "' order by dist_name, school_name"
