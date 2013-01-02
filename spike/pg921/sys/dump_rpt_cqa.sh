#!/bin/bash
# dump_rpt_cqa.sh
# The Tables to Dump
#edware=# \d
#                  List of relations
# Schema |          Name           | Type  |  Owner   
#--------+-------------------------+-------+----------
# edware | dim_assmt_outcome_type  | table | postgres
# edware | dim_assmt_subject       | table | postgres
# edware | dim_enroll_attr         | table | postgres
# edware | dim_grade               | table | postgres
# edware | dim_inst_group          | table | postgres
# edware | dim_institution         | table | postgres
# edware | dim_perf_level          | table | postgres
# edware | dim_period              | table | postgres
# edware | dim_section             | table | postgres
# edware | dim_section_group       | table | postgres
# edware | dim_staff               | table | postgres
# edware | dim_staff_group         | table | postgres
# edware | dim_student             | table | postgres
# edware | dim_subject             | table | postgres
# edware | dim_term                | table | postgres
# edware | dim_time                | table | postgres
# edware | etl_date                | table | postgres
# edware | executionlog            | table | postgres
# edware | fact_assmt_outcome      | table | postgres
# edware | fact_enroll             | table | postgres
# edware | map_assmt_subj_subj     | table | postgres
# edware | map_inst_group_inst     | table | postgres
# edware | map_sect_group_sect     | table | postgres
# edware | map_staff_group_sect    | table | postgres
# edware | map_staff_group_staff   | table | postgres
# edware | mv_academic_year_period | table | postgres
# edware | mv_amp_user_assmt       | table | postgres
# edware | mv_amp_user_inst        | table | postgres
# edware | mv_amp_user_program     | table | postgres
# edware | pm_periods              | table | postgres
#(30 rows)

rm -f /opt/spike1/edware/files/rpt/*.csv

vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_assmt_outcome_type;" -o/opt/spike1/edware/files/rpt/dim_assmt_outcome_type.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_assmt_subject;" -o/opt/spike1/edware/files/rpt/dim_assmt_subject.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_enroll_attr;" -o/opt/spike1/edware/files/rpt/dim_enroll_attr.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_grade;" -o/opt/spike1/edware/files/rpt/dim_grade.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_inst_group;" -o/opt/spike1/edware/files/rpt/dim_inst_group.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_institution;" -o/opt/spike1/edware/files/rpt/dim_institution.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_perf_level;" -o/opt/spike1/edware/files/rpt/dim_perf_level.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_period;" -o/opt/spike1/edware/files/rpt/dim_period.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_section;" -o/opt/spike1/edware/files/rpt/dim_section.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_section_group;" -o/opt/spike1/edware/files/rpt/dim_section_group.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_staff;" -o/opt/spike1/edware/files/rpt/dim_staff.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_student;" -o/opt/spike1/edware/files/rpt/dim_student.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_subject;" -o/opt/spike1/edware/files/rpt/dim_subject.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_term;" -o/opt/spike1/edware/files/rpt/dim_term.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.dim_time;" -o/opt/spike1/edware/files/rpt/dim_time.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.etl_date;" -o/opt/spike1/edware/files/rpt/etl_date.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.executionlog;" -o/opt/spike1/edware/files/rpt/executionlog.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.fact_assmt_outcome;" -o/opt/spike1/edware/files/rpt/fact_assmt_outcome.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.fact_enroll;" -o/opt/spike1/edware/files/rpt/fact_enroll.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.map_assmt_subj_subj;" -o/opt/spike1/edware/files/rpt/map_assmt_subj_subj.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.map_inst_group_inst;" -o/opt/spike1/edware/files/rpt/map_inst_group_inst.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.map_sect_group_sect;" -o/opt/spike1/edware/files/rpt/map_sect_group_sect.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.map_staff_group_sect;" -o/opt/spike1/edware/files/rpt/map_staff_group_sect.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.map_staff_group_staff;" -o/opt/spike1/edware/files/rpt/map_staff_group_staff.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.mv_academic_year_period;" -o/opt/spike1/edware/files/rpt/mv_academic_year_period.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.mv_amp_user_assmt;" -o/opt/spike1/edware/files/rpt/mv_amp_user_assmt.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.mv_amp_user_inst;" -o/opt/spike1/edware/files/rpt/mv_amp_user_inst.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.mv_amp_user_program;" -o/opt/spike1/edware/files/rpt/mv_amp_user_program.csv
vsql -Udevel_ro -hservice-vertica-futureqa.mc.wgenhq.net -A -F'|' -c"select * from dw.pm_periods;" -o/opt/spike1/edware/files/rpt/pm_periods.csv

wc -l /opt/spike1/edware/files/rpt/*.csv

tar cvfz rpt_cqa_20121018.tar.gz *.csv

