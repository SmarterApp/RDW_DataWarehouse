
# schema name
SCHEMA = 'data_generation_config'

# query0: select all states in table school_raw_stat
query0 = "select state_name, state_code, count(distinct dist_name) AS dist_num from " + SCHEMA + ".school_raw_stat where length(state_name) > 0 group by state_name, state_code order by state_name"

# query2_first and query2_second: select number of schools in each district of a state
query2_first = "select count(*) from " + SCHEMA + ".school_raw_stat where state_name='"
query2_second = "' group by dist_name order by dist_name"

# query_stat1 and query_stat2: select total number of districts of a state
query_stat1 = "select count(distinct dist_name) AS dist_num from " + SCHEMA + ".school_raw_stat where length(state_name) > 0 and state_name = '"
query_stat2 = "' group by state_name"

# query_stat3 and query_stat4: select total number of schools of a state
query_stat3 = "select count(*) AS scho_num from " + SCHEMA + ".school_raw_stat where state_name = '"
query_stat4 = "' group by state_name"

# query_stat5 and query_stat6: select number of students in each school of a state
query_stat5 = "select num_of_stu from " + SCHEMA + ".school_raw_stat where state_name='"
query_stat6 = "' order by dist_name, school_name"

# query_stat7 and query_stat8: select student_teacher_ratio in each school of a state
query_stat7 = "select stu_teacher_rario from " + SCHEMA + ".school_raw_stat where state_name= '"
query_stat8 = "' order by dist_name, school_name"

# query_stat9 and query_stat10: select total number of students of a state
query_stat9 = "select SUM(num_of_stu) AS stu_num from " + SCHEMA + ".school_raw_stat where state_name = '"
query_stat10 = "' group by state_name order by state_name"

# query_stat11 and query_stat12: select total number of teachers of a state
query_stat11 = "select SUM(num_of_teacher) AS tea_num from " + SCHEMA + ".school_raw_stat where state_name = '"
query_stat12 = "' group by state_name order by state_name"

# query_stat13, query_stat14 and query_stat15: select school percentages of four types of school in a state
query_stat13 = "select count(*) from " + SCHEMA + ".school_raw_stat where state_name = '"
query_stat14 = "' and school_level = '"
query_stat15 = "' group by state_name"
