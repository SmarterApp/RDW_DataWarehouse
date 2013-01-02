/*
    rpt_fqa_load.sql
    COPY [ int_val [ OFFSET int_val ] RECORDS ] INTO table_name
         FROM ( file_name ',' ... | STDIN )
         [ [USING] DELIMITERS field_separator [',' record_separator [ ',' string_quote ]]] [ NULL AS null_string ] [LOCKED]
    COPY n OFFSET m RECORDS INTO table FROM 'file';
*/ 
SELECT now() AS _job_start_;

--PASS
select now() as load_start_1;
DELETE FROM edware_lz.dim_assmt_outcome_type;
COPY edware_lz.dim_assmt_outcome_type
FROM '/opt/spike1/edware/files/rpt/dim_assmt_outcome_type.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_1;

--PASS
select now() as load_start_2;
DELETE FROM edware_lz.dim_enroll_attr;
COPY edware_lz.dim_enroll_attr
FROM '/opt/spike1/edware/files/rpt/dim_enroll_attr.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_2;

--PASS
select now() as load_start_3;
DELETE FROM edware_lz.dim_grade;
COPY edware_lz.dim_grade
FROM '/opt/spike1/edware/files/rpt/dim_grade.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_3;

--PASS
select now() as load_start_4;
DELETE FROM edware_lz.dim_inst_group;
COPY edware_lz.dim_inst_group
FROM '/opt/spike1/edware/files/rpt/dim_inst_group.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_4;

--PASS
select now() as load_start_5;
DELETE FROM edware_lz.dim_institution;
COPY edware_lz.dim_institution
FROM '/opt/spike1/edware/files/rpt/dim_institution.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_5;

--PASS
select now() as load_start_6;
DELETE FROM edware_lz.dim_perf_level;
COPY edware_lz.dim_perf_level
FROM '/opt/spike1/edware/files/rpt/dim_perf_level.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_6;

--PASS                                                                                                                                           SS
select now() as load_start_7;
DELETE FROM edware_lz.dim_period;
COPY edware_lz.dim_period
FROM '/opt/spike1/edware/files/rpt/dim_period.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_7;

--PASS
select now() as load_start_8;
DELETE FROM edware_lz.dim_section;
COPY edware_lz.dim_section
FROM '/opt/spike1/edware/files/rpt/dim_section.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_8;

--PASS
select now() as load_start_9;
DELETE FROM edware_lz.dim_staff;
COPY edware_lz.dim_staff
FROM '/opt/spike1/edware/files/rpt/dim_staff_trim.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_9;

--PASS
select now() as load_start_10;
DELETE FROM edware_lz.dim_student;
COPY edware_lz.dim_student
FROM '/opt/spike1/edware/files/rpt/dim_student_trim.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_10;

--PASS
select now() as load_start_11;
DELETE FROM edware_lz.dim_time;
COPY edware_lz.dim_time
FROM '/opt/spike1/edware/files/rpt/dim_time.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_11;

--PASS
-- too big for my laptop...
select now() as load_start_12;
DELETE FROM edware_lz.fact_assmt_outcome;
COPY edware_lz.fact_assmt_outcome
FROM '/opt/spike1/edware/files/rpt/fact_assmt_outcome_trim.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_12;

--PASS
select now() as load_start_13;
DELETE FROM edware_lz.fact_enroll;
COPY edware_lz.fact_enroll
FROM '/opt/spike1/edware/files/rpt/fact_enroll_trim.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_13;

--PASS
select now() as load_start_14;
DELETE FROM edware_lz.map_inst_group_inst;
COPY edware_lz.map_inst_group_inst
FROM '/opt/spike1/edware/files/rpt/map_inst_group_inst.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_14;

--PASS
select now() as load_start_15;
DELETE FROM edware_lz.mv_academic_year_period;
COPY edware_lz.mv_academic_year_period
FROM '/opt/spike1/edware/files/rpt/mv_academic_year_period_trim.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_15;

--PASS
select now() as load_start_16;
DELETE FROM edware_lz.mv_amp_user_assmt;
COPY edware_lz.mv_amp_user_assmt
FROM '/opt/spike1/edware/files/rpt/mv_amp_user_assmt.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_16;

--PASS
select now() as load_start_17;
DELETE FROM edware_lz.mv_amp_user_inst;
COPY edware_lz.mv_amp_user_inst
FROM '/opt/spike1/edware/files/rpt/mv_amp_user_inst.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_17;

--PASS
select now() as load_start_18;
DELETE FROM edware_lz.mv_amp_user_program;
COPY edware_lz.mv_amp_user_program
FROM '/opt/spike1/edware/files/rpt/mv_amp_user_program.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_18;

--PASS
select now() as load_start_19;
DELETE FROM edware_lz.pm_periods;
COPY edware_lz.pm_periods
FROM '/opt/spike1/edware/files/rpt/pm_periods.csv'
WITH DELIMITER AS '|' CSV HEADER
;
select now() as load_end_19;

/* None of these files have data???
DELETE FROM edware_lz.dim_section_group;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.dim_section_group
FROM '/opt/spike1/edware/files/rpt/dim_section_group.csv'
;

DELETE FROM edware_lz.dim_subject;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.dim_subject
FROM '/opt/spike1/edware/files/rpt/dim_subject.csv'
;

DELETE FROM edware_lz.dim_term;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.dim_term
FROM '/opt/spike1/edware/files/rpt/dim_term.csv'
;

DELETE FROM edware_lz.map_assmt_subj_subj;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.map_assmt_subj_subj
FROM '/opt/spike1/edware/files/rpt/map_assmt_subj_subj.csv'
;

DELETE FROM edware_lz.map_sect_group_sect;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.map_sect_group_sect
FROM '/opt/spike1/edware/files/rpt/map_sect_group_sect.csv'
;

DELETE FROM edware_lz.map_staff_group_sect;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.map_staff_group_sect
FROM '/opt/spike1/edware/files/rpt/map_staff_group_sect.csv'
;

DELETE FROM edware_lz.map_staff_group_staff;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.map_staff_group_staff
FROM '/opt/spike1/edware/files/rpt/map_staff_group_staff.csv'
;

*/

/* None of the mv_* file's exist???
[edware_lz@localhost data]$ ls -l mv_*
ls: cannot access mv_*: No such file or directory

DELETE FROM edware_lz.mv_amp_user_program;
COPY 17171 OFFSET 2 RECORDS
INTO edware_lz.mv_amp_user_program
FROM '/opt/spike1/edware/files/rpt/mv_amp_user_program.csv'
;

select now() as load_start_15;
DELETE FROM edware_lz.pm_periods;
COPY 2 OFFSET 2 RECORDS
INTO edware_lz.pm_periods
FROM '/opt/spike1/edware/files/rpt/pm_periods.csv'
;
select now() as load_end_15;
SELECT COUNT(*) FROM edware_lz.pm_periods;
*/

SELECT COUNT(*) AS _dim_assmt_outcome_type_count_ FROM edware_lz.dim_assmt_outcome_type;
SELECT COUNT(*) AS _dim_enroll_attr_count_ FROM edware_lz.dim_enroll_attr;
SELECT COUNT(*) AS _dim_grade_count_ FROM edware_lz.dim_grade;
SELECT COUNT(*) AS _dim_inst_group_count_ FROM edware_lz.dim_inst_group;
SELECT COUNT(*) AS _dim_institution_count_ FROM edware_lz.dim_institution;
SELECT COUNT(*) AS _dim_perf_level_count_ FROM edware_lz.dim_perf_level;
SELECT COUNT(*) AS _dim_peroid_count_ FROM edware_lz.dim_period;
SELECT COUNT(*) AS _dim_section_count_ FROM edware_lz.dim_section;
SELECT COUNT(*) AS _dim_staff_count_ FROM edware_lz.dim_staff;
SELECT COUNT(*) AS _dim_student_count_ FROM edware_lz.dim_student;
SELECT COUNT(*) AS _dim_time_count_ FROM edware_lz.dim_time;
SELECT COUNT(*) AS _fact_assmt_outcome_count_ FROM edware_lz.fact_assmt_outcome;
SELECT COUNT(*) AS _fact_enroll_count_ FROM edware_lz.fact_enroll;
SELECT COUNT(*) AS _map_inst_group_inst_count_ FROM edware_lz.map_inst_group_inst;
SELECT COUNT(*) AS _mv_academic_year_period_count_ FROM edware_lz.mv_academic_year_period;
SELECT COUNT(*) AS _mv_amp_user_assmt_count_ FROM edware_lz.mv_amp_user_assmt;
SELECT COUNT(*) AS _mv_amp_user_inst_count_ FROM edware_lz.mv_amp_user_inst;
SELECT COUNT(*) AS _mv_amp_user_program_count_ FROM edware_lz.mv_amp_user_program;
SELECT COUNT(*) AS _pm_periods_count_ FROM edware_lz.pm_periods;

SELECT now() AS _job_end_;