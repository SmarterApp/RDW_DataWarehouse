--rpt_fao_load.sql
--FAIL
-- too big for my laptop...

SELECT now() AS _job_start_;
/*
select now() as load_start_12;
DELETE FROM edware_lz.fact_assmt_outcome;
COPY 157626781 OFFSET 2 RECORDS
INTO edware_lz.fact_assmt_outcome
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_12;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome;

0	10508452
1	21016905
2	31525357
3	42033809
4	52542261
5	63050713
6	73559165
7	84067617
8	94576069
9	105084521
10	115592973
11	126101425
12	136609877
13	147118329
14	157626781
*/

DROP TABLE edware_lz.fact_assmt_outcome_0;
CREATE TABLE edware_lz.fact_assmt_outcome_0
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_0;
DELETE FROM edware_lz.fact_assmt_outcome_0;
COPY 10508452 OFFSET 2 RECORDS
INTO edware_lz.fact_assmt_outcome_0
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_0;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_0;

DROP TABLE edware_lz.fact_assmt_outcome_1;
CREATE TABLE edware_lz.fact_assmt_outcome_1
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_1;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 21016905 OFFSET 10508452 RECORDS
INTO edware_lz.fact_assmt_outcome_1
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_1;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_1;

DROP TABLE edware_lz.fact_assmt_outcome_2;
CREATE TABLE edware_lz.fact_assmt_outcome_2
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_2;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 31525357 OFFSET 21016905 RECORDS
INTO edware_lz.fact_assmt_outcome_2
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_2;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_2;

DROP TABLE edware_lz.fact_assmt_outcome_2;
CREATE TABLE edware_lz.fact_assmt_outcome_3
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_3;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 42033809 OFFSET 31525357 RECORDS
INTO edware_lz.fact_assmt_outcome_3
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_3;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_3;

DROP TABLE edware_lz.fact_assmt_outcome_4;
CREATE TABLE edware_lz.fact_assmt_outcome_4
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_4;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 52542261 OFFSET 42033809 RECORDS
INTO edware_lz.fact_assmt_outcome_4
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_4;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome;

DROP TABLE edware_lz.fact_assmt_outcome_5;
CREATE TABLE edware_lz.fact_assmt_outcome_5
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_5;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 63050713 OFFSET 52542261 RECORDS
INTO edware_lz.fact_assmt_outcome_5
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_5;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_5;

DROP TABLE edware_lz.fact_assmt_outcome_6;
CREATE TABLE edware_lz.fact_assmt_outcome_6
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_6;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 73559165 OFFSET 63050713 RECORDS
INTO edware_lz.fact_assmt_outcome_6
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_6;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome;

DROP TABLE edware_lz.fact_assmt_outcome_7;
CREATE TABLE edware_lz.fact_assmt_outcome_7
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_7;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 84067617 OFFSET 73559165 RECORDS
INTO edware_lz.fact_assmt_outcome_7
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_7;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome;

DROP TABLE edware_lz.fact_assmt_outcome_8;
CREATE TABLE edware_lz.fact_assmt_outcome_8
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_8;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 94576069 OFFSET 84067617 RECORDS
INTO edware_lz.fact_assmt_outcome_8
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_8;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_8;

DROP TABLE edware_lz.fact_assmt_outcome_9;
CREATE TABLE edware_lz.fact_assmt_outcome_9
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_9;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 105084521 OFFSET 94576069 RECORDS
INTO edware_lz.fact_assmt_outcome_9
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_9;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_9;

DROP TABLE edware_lz.fact_assmt_outcome_10;
CREATE TABLE edware_lz.fact_assmt_outcome_10
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_10;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 115592973 OFFSET 105084521 RECORDS
INTO edware_lz.fact_assmt_outcome_10
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_10;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_10;

DROP TABLE edware_lz.fact_assmt_outcome_11;
CREATE TABLE edware_lz.fact_assmt_outcome_11
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_11;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 126101425 OFFSET 115592973 RECORDS
INTO edware_lz.fact_assmt_outcome_11
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_11;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_11;

DROP TABLE edware_lz.fact_assmt_outcome_12;
CREATE TABLE edware_lz.fact_assmt_outcome_12
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_12;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 126101425 OFFSET 115592973 RECORDS
INTO edware_lz.fact_assmt_outcome_12
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_12;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_12;

DROP TABLE edware_lz.fact_assmt_outcome_13;
CREATE TABLE edware_lz.fact_assmt_outcome_13
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_13;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 136609877 OFFSET 126101425 RECORDS
INTO edware_lz.fact_assmt_outcome_13
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_13;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_13;

DROP TABLE edware_lz.fact_assmt_outcome_14;
CREATE TABLE edware_lz.fact_assmt_outcome_14
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_14;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 147118329 OFFSET 136609877 RECORDS
INTO edware_lz.fact_assmt_outcome_14
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_14;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_14;

DROP TABLE edware_lz.fact_assmt_outcome_15;
CREATE TABLE edware_lz.fact_assmt_outcome_15
AS SELECT * FROM edware_lz.fact_assmt_outcome
WHERE 1 = 2;

select now() as load_start_15;
-- DELETE FROM edware_lz.fact_assmt_outcome;
COPY 157626781 OFFSET 147118329 RECORDS
INTO edware_lz.fact_assmt_outcome_15
FROM '/home/edware/workspace/spike/monetdb/edware/data/fact_assmt_outcome.csv'
;
select now() as load_end_15;
SELECT COUNT(*) FROM edware_lz.fact_assmt_outcome_15;

SELECT 'loading edware_lz.fao_0 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_0
;

SELECT 'loading edware_lz.fao_1 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_1
;

SELECT 'loading edware_lz.fao_1 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_2
;

SELECT 'loading edware_lz.fao_2 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_2
;

SELECT 'loading edware_lz.fao_3 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_3
;

SELECT 'loading edware_lz.fao_4 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_4
;

SELECT 'loading edware_lz.fao_5 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_5
;

SELECT 'loading edware_lz.fao_6 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_6
;

SELECT 'loading edware_lz.fao_7 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_7
;

SELECT 'loading edware_lz.fao_8 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_8
;

SELECT 'loading edware_lz.fao_9 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_9
;

SELECT 'loading edware_lz.fao_10 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_10
;

SELECT 'loading edware_lz.fao_12 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_12
;

SELECT 'loading edware_lz.fao_13 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_13
;

SELECT 'loading edware_lz.fao_14 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_14
;

SELECT 'loading edware_lz.fao_15 partition into edware.fao' AS _ECHO_;

INSERT INTO edware.fact_assmt_outcome
(
    fact_assmt_outcome_key
,   part_key 
,   active_flag
,   dim_student_key
,   eternal_student_sid
,   year_sid
,   dim_assmt_staff_key
,   dim_assmt_outcome_type_key
,   dim_assmt_period_key
,   dim_assmt_grade_key
,   dim_assmt_time_key
,   dim_assmt_sync_time_key
,   dim_perf_level_key
,   dim_custom_perf_level_key
,   dim_assmt_institution_key
,   dim_curr_institution_key
,   dim_eoy_institution_key
,   dim_curr_enroll_attr_key
,   dim_eoy_enroll_attr_key
,   dim_eoy_student_grade_key
,   dim_curr_student_grade_key
,   dim_eoy_section_group_key
,   dim_curr_section_group_key
,   dim_offic_section_key
,   dim_curr_offic_section_key
,   outcome_int
,   outcome_string
,   outcome_float
,   assmt_date
,   sync_date
,   assmt_instance_sid
,   assmt_instance_rank
,   create_date
,   mod_date 
,   assmt_custom_id_code 
,   assmt_custom_id_name
)
SELECT
    CAST(fact_assmt_outcome_key AS int),
    CAST(part_key AS int),
    CAST(active_flag AS boolean),
    CAST(dim_student_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(year_sid AS int),
    CAST(dim_assmt_staff_key AS int),
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(dim_assmt_period_key AS int),
    CAST(dim_assmt_grade_key AS int),
    CAST(dim_assmt_time_key AS int),
    CAST(dim_assmt_sync_time_key AS int),
    CAST(dim_perf_level_key AS int),
    CAST(dim_custom_perf_level_key AS int),
    CAST(dim_assmt_institution_key AS int),
    CAST(dim_curr_institution_key AS int),
    CAST(dim_eoy_institution_key AS int),
    CAST(dim_curr_enroll_attr_key AS int),
    CAST(dim_eoy_enroll_attr_key AS int),
    CAST(dim_eoy_student_grade_key AS int),
    CAST(dim_curr_student_grade_key AS int),
    CAST(dim_eoy_section_group_key AS int),
    CAST(dim_curr_section_group_key AS int),
    CAST(dim_offic_section_key AS int),
    CAST(dim_curr_offic_section_key AS int),
    CAST(outcome_int AS int),
    CAST(outcome_string AS varchar(255)),
    CAST(outcome_float AS float),
    CAST(assmt_date AS timestamp),
    CAST(sync_date AS timestamp),
    CAST(assmt_instance_sid AS int),
    CAST(assmt_instance_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(assmt_custom_id_code AS varchar(255)),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.fact_assmt_outcome_15
;

SELECT count(*) AS _final_fao_load_count_
FROM edware.fact_assmt_outcome;

SELECT now() AS _job_end_;