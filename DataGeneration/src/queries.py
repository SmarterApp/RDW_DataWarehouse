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


query_stat1 = "select count(distinct dist_name) AS dist_num from school_raw_stat where length(state_name) > 0 and state_name = '"
query_stat2 = "' group by state_name"

query_stat3 = "select count(*) AS scho_num from school_raw_stat where state_name = '"
query_stat4 = "' group by state_name"

query_stat5 = "select num_of_stu from school_raw_stat where state_name='"
query_stat6 = "' order by dist_name, school_name"

query_stat7 = "select stu_teacher_rario from school_raw_stat where state_name= '"
query_stat8 = "' order by dist_name, school_name"

query_stat9 = "select SUM(num_of_stu) AS stu_num from school_raw_stat where state_name = '"
query_stat10 = "' group by state_name order by state_name"

query_stat11 = "select SUM(num_of_teacher) AS tea_num from school_raw_stat where state_name = '"
query_stat12 = "' group by state_name order by state_name"

query_stat13 = "select count(*) from school_raw_stat where state_name = '"
query_stat14 = "' and school_level = '"
query_stat15 = "' group by state_name"
