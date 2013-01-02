-- rtp_fql_elt.sql
-- Extract Tramsform and Load _lz tables in to typed edware rpt tables

--PASS no data...
DELETE FROM edware.dim_subject;
INSERT INTO edware.dim_subject
(
    dim_subject_key
,   subject_code
,   subject_name
,   is_summary_flag
,   hs_required_credits
,   custom_id_1_code
,   custom_id_1_type_code
,   custom_id_2_code
,   custom_id_2_type_code
,   custom_id_3_code
,   custom_id_3_type_code
,   custom_id_4_code
,   custom_id_4_type_code
,   custom_id_5_code
,   custom_id_5_type_code
,   dim_parent_subject_key
,   subject_level
,   subject_group_code
,   subject_group_name
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_subject_key AS int),
    CAST(subject_code AS varchar(255)),
    CAST(subject_name AS varchar(255)),
    CAST(is_summary_flag AS boolean),
    CAST(hs_required_credits AS int),
    CAST(custom_id_1_code AS varchar(255)),
    CAST(custom_id_1_type_code AS varchar(255)),
    CAST(custom_id_2_code AS varchar(255)),
    CAST(custom_id_2_type_code AS varchar(255)),
    CAST(custom_id_3_code AS varchar(255)),
    CAST(custom_id_3_type_code AS varchar(255)),
    CAST(custom_id_4_code AS varchar(255)),
    CAST(custom_id_4_type_code AS varchar(255)),
    CAST(custom_id_5_code AS varchar(255)),
    CAST(custom_id_5_type_code AS varchar(255)),
    CAST(dim_parent_subject_key AS int),
    CAST(subject_level AS int),
    CAST(subject_group_code AS varchar(255)),
    CAST(subject_group_name AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_subject
;

SELECT count(*) AS _lz_count_ from edware_lz.dim_subject;
SELECT count(*) AS _load_count_ from edware.dim_subject;

--PASS
--NULL Dates break CAST()
UPDATE edware_lz.dim_staff
SET dob = '1970-01-01'
WHERE dob = '';

--CAST() can't handle 't' || 'f'
UPDATE edware_lz.dim_staff
SET demo_flag = '0'
WHERE demo_flag = 'f';

UPDATE edware_lz.dim_staff
SET demo_flag = '1'
WHERE demo_flag = 't';

DELETE FROM edware.dim_staff;
INSERT INTO edware.dim_staff
(
    dim_staff_key
,   staff_sid
,   school_year_sid
,   amp_user_sid
,   amp_user_handle
,   first_name
,   middle_name
,   last_name
,   dob
,   phone
,   email
,   custom_id_1_code
,   custom_id_1_type_code
,   custom_id_2_code
,   custom_id_2_type_code
,   custom_id_3_code
,   custom_id_3_type_code
,   custom_id_4_code
,   custom_id_4_type_code
,   custom_id_5_code
,   custom_id_5_type_code
,   status_code
,   demo_flag 
,   spa_pii_flag
,   create_date
,   mod_date
,   part_key
,   staff_type_code
,   staff_type_name
,   staff_role_code
,   staff_role_name
,   opt_out
)
SELECT
    CAST(dim_staff_key AS int),
    CAST(staff_sid AS int),
    CAST(school_year_sid AS int),
    CAST(amp_user_sid AS int),
    CAST(amp_user_handle AS varchar(255)),
    CAST(first_name AS varchar(255)),
    CAST(middle_name AS varchar(255)),
    CAST(last_name AS varchar(255)),
    CAST(dob AS date),
    CAST(phone AS varchar(255)),
    CAST(email AS varchar(255)),
    CAST(custom_id_1_code AS varchar(255)),
    CAST(custom_id_1_type_code AS varchar(255)),
    CAST(custom_id_2_code AS varchar(255)),
    CAST(custom_id_2_type_code AS varchar(255)),
    CAST(custom_id_3_code AS varchar(255)),
    CAST(custom_id_3_type_code AS varchar(255)),
    CAST(custom_id_4_code AS varchar(255)),
    CAST(custom_id_4_type_code AS varchar(255)),
    CAST(custom_id_5_code AS varchar(255)),
    CAST(custom_id_5_type_code AS varchar(255)),
    CAST(status_code AS varchar(255)),
    CAST(demo_flag AS boolean),
    CAST(spa_pii_flag AS boolean),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(staff_type_code AS varchar(255)),
    CAST(staff_type_name AS varchar(255)),
    CAST(staff_role_code AS varchar(255)),
    CAST(staff_role_name AS varchar(255)),
    CAST(opt_out AS boolean)
FROM edware_lz.dim_staff
;

SELECT count(*) AS _lz_count_ from edware_lz.dim_staff;
SELECT count(*) AS _load_count_ from edware.dim_staff;

--PASS no data...
DELETE FROM edware.dim_staff_group;
INSERT INTO edware.dim_staff_group
(
    dim_staff_group_key
,   integerized_staff_keys
,   staff_group_name
,   staff_group_type
,   primary_staff_key
,   group_start_time
,   group_end_time
,   active_flag
,   staff_group_code
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_staff_group_key AS int),
    CAST(integerized_staff_keys AS varchar(255)),
    CAST(staff_group_name AS varchar(255)),
    CAST(staff_group_type AS varchar(255)),
    CAST(primary_staff_key AS int),
    CAST(group_start_time AS date),
    CAST(group_end_time AS date),
    CAST(active_flag AS boolean),
    CAST(staff_group_code AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_staff_group
;

SELECT count(*) AS _lz_count_ from edware_lz.dim_staff_group;
SELECT count(*) AS _load_count_ from edware.dim_staff_group;

--PASS
UPDATE edware_lz.dim_section
SET student_group_start_time = '1970-01-01'
WHERE student_group_start_time = '';

UPDATE edware_lz.dim_section
SET student_group_end_time = '1970-01-01'
WHERE student_group_start_time = '';

UPDATE edware_lz.dim_section
SET duplicate_offering_flag = '0'
WHERE duplicate_offering_flag = '';

UPDATE edware_lz.dim_section
SET duplicate_offering_flag = '0'
WHERE duplicate_offering_flag = 'f';

UPDATE edware_lz.dim_section
SET duplicate_offering_flag = '1'
WHERE duplicate_offering_flag = 't';

UPDATE edware_lz.dim_section
SET updated_flag = '0'
WHERE updated_flag = '';

UPDATE edware_lz.dim_section
SET updated_flag = '0'
WHERE updated_flag = 'f';

UPDATE edware_lz.dim_section
SET updated_flag = '1'
WHERE updated_flag = 't';

UPDATE edware_lz.dim_section
SET elective_flag = '0'
WHERE elective_flag = '';

UPDATE edware_lz.dim_section
SET elective_flag = '0'
WHERE elective_flag = 'f';

UPDATE edware_lz.dim_section
SET elective_flag = '1'
WHERE elective_flag = 't';

UPDATE edware_lz.dim_section
SET active_flag = '0'
WHERE active_flag = '';

UPDATE edware_lz.dim_section
SET active_flag = '0'
WHERE active_flag = 'f';

UPDATE edware_lz.dim_section
SET active_flag = '1'
WHERE active_flag = 't';

UPDATE edware_lz.dim_section
SET completed_flag = '0'
WHERE completed_flag = '';

UPDATE edware_lz.dim_section
SET completed_flag = '0'
WHERE completed_flag = 'f';

UPDATE edware_lz.dim_section
SET completed_flag = '1'
WHERE completed_flag = 't';

UPDATE edware_lz.dim_section
SET staff_1_is_primary = '0'
WHERE staff_1_is_primary = '';

UPDATE edware_lz.dim_section
SET staff_1_is_primary = '0'
WHERE staff_1_is_primary = 'f';

UPDATE edware_lz.dim_section
SET staff_1_is_primary = '1'
WHERE staff_1_is_primary = 't';

UPDATE edware_lz.dim_section
SET staff_2_is_primary = '0'
WHERE staff_2_is_primary = '';

UPDATE edware_lz.dim_section
SET staff_2_is_primary = '0'
WHERE staff_2_is_primary = 'f';

UPDATE edware_lz.dim_section
SET staff_2_is_primary = '1'
WHERE staff_2_is_primary = 't';

UPDATE edware_lz.dim_section
SET staff_3_is_primary = '0'
WHERE staff_3_is_primary = '';

UPDATE edware_lz.dim_section
SET staff_3_is_primary = '0'
WHERE staff_3_is_primary = 'f';

UPDATE edware_lz.dim_section
SET staff_3_is_primary = '1'
WHERE staff_3_is_primary = 't';

UPDATE edware_lz.dim_section
SET staff_4_is_primary = '0'
WHERE staff_4_is_primary = '';

UPDATE edware_lz.dim_section
SET staff_4_is_primary = '0'
WHERE staff_4_is_primary = 'f';

UPDATE edware_lz.dim_section
SET staff_4_is_primary = '1'
WHERE staff_4_is_primary = 't';

UPDATE edware_lz.dim_section
SET demo_flag = '0'
WHERE demo_flag = '';

UPDATE edware_lz.dim_section
SET demo_flag = '0'
WHERE demo_flag = 'f';

UPDATE edware_lz.dim_section
SET demo_flag = '1'
WHERE demo_flag = 't';

UPDATE edware_lz.dim_section
SET primary_subject_key = '-9999'
WHERE primary_subject_key = '';

UPDATE edware_lz.dim_section
SET course_credits = '-9999'
WHERE course_credits = '';

UPDATE edware_lz.dim_section
SET marking_period_max = '-9999'
WHERE marking_period_max = '';

UPDATE edware_lz.dim_section
SET dim_parent_section_key = '-9999'
WHERE dim_parent_section_key = '';

UPDATE edware_lz.dim_section
SET dim_parent_section_key = '-9999'
WHERE dim_parent_section_key = '';

UPDATE edware_lz.dim_section
SET dim_instructional_content_group_key = '-9999'
WHERE dim_instructional_content_group_key = '';

UPDATE edware_lz.dim_section
SET staff_1_sid = '-9999'
WHERE staff_1_sid = '';

UPDATE edware_lz.dim_section
SET staff_2_sid = '-9999'
WHERE staff_2_sid = '';

UPDATE edware_lz.dim_section
SET staff_3_sid = '-9999'
WHERE staff_3_sid = '';

UPDATE edware_lz.dim_section
SET staff_4_sid = '-9999'
WHERE staff_4_sid = '';

UPDATE edware_lz.dim_section
SET part_key = '-9999'
WHERE part_key = '';

UPDATE edware_lz.dim_section
SET course_sid = '-9999'
WHERE course_sid = '';

UPDATE edware_lz.dim_section
SET subject_sid = '-9999'
WHERE subject_sid = '';

DELETE FROM edware.dim_section;
INSERT INTO edware.dim_section
(
    dim_section_key
,   section_sid 
,   section_name
,   display_name
,   course_code
,   course_name
,   primary_subject_key
,   duplicate_offering_flag
,   section_type_code
,   section_subtype_code
,   avg_student_grade_level_code
,   updated_flag
,   course_credits
,   marking_period_max
,   elective_flag
,   course_level_code
,   course_site_code
,   course_site_name
,   dim_parent_section_key
,   sif_student_group_type
,   sif_student_group_type_attribute
,   student_group_start_time
,   student_group_end_time
,   active_flag
,   completed_flag 
,   dim_instructional_content_group_key
,   custom_id_1_code
,   custom_id_1_type_code
,   custom_id_2_code
,   custom_id_2_type_code
,   custom_id_3_code
,   custom_id_3_type_code
,   custom_id_4_code
,   custom_id_4_type_code
,   custom_id_5_code
,   custom_id_5_type_code
,   staff_1_sid 
,   staff_1_is_primary
,   staff_1_role_desc
,   staff_2_sid
,   staff_2_is_primary
,   staff_2_role_desc
,   staff_3_sid
,   staff_3_is_primary
,   staff_3_role_desc
,   staff_4_sid
,   staff_4_is_primary
,   staff_4_role_desc
,   managed_by_code
,   managed_by_name
,   status_code
,   demo_flag
,   create_date
,   mod_date
,   part_key
,   course_sid
,   subject_sid
,   subject_code
,   subject_name
)
SELECT
    CAST(dim_section_key AS int),
    CAST(section_sid AS int),
    CAST(section_name AS varchar(255)),
    CAST(display_name AS varchar(255)),
    CAST(course_code AS varchar(255)),
    CAST(course_name AS varchar(255)),
    CAST(primary_subject_key AS int),
    CAST(duplicate_offering_flag AS boolean),
    CAST(section_type_code AS varchar(255)),
    CAST(section_subtype_code AS varchar(255)),
    CAST(avg_student_grade_level_code AS varchar(255)),
    CAST(updated_flag AS boolean),
    CAST(course_credits AS int),
    CAST(marking_period_max AS int),
    CAST(elective_flag AS boolean),
    CAST(course_level_code AS varchar(255)),
    CAST(course_site_code AS varchar(255)),
    CAST(course_site_name AS varchar(255)),
    CAST(dim_parent_section_key AS int),
    CAST(sif_student_group_type AS varchar(255)),
    CAST(sif_student_group_type_attribute AS varchar(255)),
    CAST(student_group_start_time AS date),
    CAST(student_group_end_time AS date),
    CAST(active_flag AS boolean),
    CAST(completed_flag AS boolean),
    CAST(dim_instructional_content_group_key AS int),
    CAST(custom_id_1_code AS varchar(255)),
    CAST(custom_id_1_type_code AS varchar(255)),
    CAST(custom_id_2_code AS varchar(255)),
    CAST(custom_id_2_type_code AS varchar(255)),
    CAST(custom_id_3_code AS varchar(255)),
    CAST(custom_id_3_type_code AS varchar(255)),
    CAST(custom_id_4_code AS varchar(255)),
    CAST(custom_id_4_type_code AS varchar(255)),
    CAST(custom_id_5_code AS varchar(255)),
    CAST(custom_id_5_type_code AS varchar(255)),
    CAST(staff_1_sid AS int),
    CAST(staff_1_is_primary AS boolean),
    CAST(staff_1_role_desc AS varchar(255)),
    CAST(staff_2_sid AS int),
    CAST(staff_2_is_primary AS boolean),
    CAST(staff_2_role_desc AS varchar(255)),
    CAST(staff_3_sid AS int),
    CAST(staff_3_is_primary AS boolean),
    CAST(staff_3_role_desc AS varchar(255)),
    CAST(staff_4_sid AS int),
    CAST(staff_4_is_primary AS boolean),
    CAST(staff_4_role_desc AS varchar(255)),
    CAST(managed_by_code AS varchar(255)),
    CAST(managed_by_name AS varchar(255)),
    CAST(status_code AS varchar(255)),
    CAST(demo_flag AS boolean),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(course_sid AS int),
    CAST(subject_sid AS int),
    CAST(subject_code AS varchar(255)),
    CAST(subject_name AS varchar(255))
FROM edware_lz.dim_section
;

SELECT count(*) AS _lz_count_ from edware_lz.dim_section;
SELECT count(*) AS _load_count_ FROM edware.dim_section;

--PASS/FAIL... no data.
DELETE FROM edware.dim_section_group;
INSERT INTO edware.dim_section_group
(
    dim_section_group_key
,   integerized_section_keys
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_section_group_key AS int),
    CAST(integerized_section_keys AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_section_group
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_section;
SELECT count(*) AS _load_count_ FROM edware.dim_section_group;

--PASS/FAIL no data...
DELETE FROM edware.map_sect_group_sect;
INSERT INTO edware.map_sect_group_sect
(
    map_sect_group_sect_key
,   dim_section_group_key
,   dim_section_key
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(map_sect_group_sect_key AS int),
    CAST(dim_section_group_key AS int),
    CAST(dim_section_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.map_sect_group_sect
;

SELECT count(*) AS _lz_count_ FROM edware_lz.map_sect_group_sect;
SELECT count(*) AS _load_count_ FROM edware.map_sect_group_sect;

--PASS/FAIL no data...
DELETE FROM edware.map_staff_group_sect;
INSERT INTO edware.map_staff_group_sect
(
    map_staff_group_sect_key
,   dim_staff_group_key
,   dim_section_key
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(map_staff_group_sect_key AS int),
    CAST(dim_staff_group_key AS int),
    CAST(dim_section_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.map_staff_group_sect
;

SELECT count(*) AS _lz_count_ FROM edware_lz.map_staff_group_sect;
SELECT count(*) AS _load_count_ FROM edware.map_staff_group_sect;

--PASS
DELETE FROM edware.dim_enroll_attr;
INSERT INTO edware.dim_enroll_attr
(
    dim_enroll_attr_key
,   sped_environ_code
,   sped_environ_name
,   s504_status_code
,   s504_status_name
,   disability_status_code
,   disability_status_name
,   specific_disability_code
,   specific_disability_name
,   ell_status_code
,   ell_status_name
,   home_lang_code
,   home_lang_name
,   ethnicity_code
,   ethnicity_name
,   housing_status_code
,   housing_status_name
,   meal_status_code
,   meal_status_name
,   econ_disadvantage_code
,   econ_disadvantage_name
,   title_1_status_code
,   title_1_status_name
,   migrant_status_code
,   migrant_status_name
,   alt_assmt_code
,   alt_assmt_name
,   english_prof_code
,   english_prof_name
,   is_classed_code
,   is_classed_name
,   create_date
,   mod_date
,   part_key
,   ethnicity_abbrev
,   sped_environ_abbrev
,   disability_status_abbrev
,   specific_disability_abbrev 
,   s504_status_abbrev
,   econ_disadvantage_abbrev
,   meal_status_abbrev
,   title_1_status_abbrev
,   migrant_status_abbrev
,   english_prof_abbrev
,   ell_status_abbrev
,   home_lang_abbrev
,   alt_assmt_abbrev
,   housing_status_abbrev
)
SELECT
    CAST(dim_enroll_attr_key AS int),
    CAST(sped_environ_code AS varchar(255)),
    CAST(sped_environ_name AS varchar(255)),
    CAST(s504_status_code AS varchar(255)),
    CAST(s504_status_name AS varchar(255)),
    CAST(disability_status_code AS varchar(255)),
    CAST(disability_status_name AS varchar(255)),
    CAST(specific_disability_code AS varchar(255)),
    CAST(specific_disability_name AS varchar(255)),
    CAST(ell_status_code AS varchar(255)),
    CAST(ell_status_name AS varchar(255)),
    CAST(home_lang_code AS varchar(255)),
    CAST(home_lang_name AS varchar(255)),
    CAST(ethnicity_code AS varchar(255)),
    CAST(ethnicity_name AS varchar(255)),
    CAST(housing_status_code AS varchar(255)),
    CAST(housing_status_name AS varchar(255)),
    CAST(meal_status_code AS varchar(255)),
    CAST(meal_status_name AS varchar(255)),
    CAST(econ_disadvantage_code AS varchar(255)),
    CAST(econ_disadvantage_name AS varchar(255)),
    CAST(title_1_status_code AS varchar(255)),
    CAST(title_1_status_name AS varchar(255)),
    CAST(migrant_status_code AS varchar(255)),
    CAST(migrant_status_name AS varchar(255)),
    CAST(alt_assmt_code AS varchar(255)),
    CAST(alt_assmt_name AS varchar(255)),
    CAST(english_prof_code AS varchar(255)),
    CAST(english_prof_name AS varchar(255)),
    CAST(is_classed_code AS varchar(255)),
    CAST(is_classed_name AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(ethnicity_abbrev AS varchar(255)),
    CAST(sped_environ_abbrev AS varchar(255)),
    CAST(disability_status_abbrev AS varchar(255)),
    CAST(specific_disability_abbrev AS varchar(255)),
    CAST(s504_status_abbrev AS varchar(255)),
    CAST(econ_disadvantage_abbrev AS varchar(255)),
    CAST(meal_status_abbrev AS varchar(255)),
    CAST(title_1_status_abbrev AS varchar(255)),
    CAST(migrant_status_abbrev AS varchar(255)),
    CAST(english_prof_abbrev AS varchar(255)),
    CAST(ell_status_abbrev AS varchar(255)),
    CAST(home_lang_abbrev AS varchar(255)),
    CAST(alt_assmt_abbrev AS varchar(255)),
    CAST(housing_status_abbrev AS varchar(255)) --*/
FROM edware_lz.dim_enroll_attr
--LIMIT 10
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_enroll_attr;
SELECT count(*) AS _load_count_ FROM edware.dim_enroll_attr;

--PASS... no data
UPDATE edware_lz.dim_term
SET current_term_flag = '0'
WHERE current_term_flag = '';

UPDATE edware_lz.dim_term
SET current_term_flag = '0'
WHERE current_term_flag = 'f';

UPDATE edware_lz.dim_term
SET current_term_flag = '1'
WHERE current_term_flag = 't';

UPDATE edware_lz.dim_term
SET summer_term_flag = '0'
WHERE summer_term_flag = '';

UPDATE edware_lz.dim_term
SET summer_term_flag = '0'
WHERE summer_term_flag = 'f';

UPDATE edware_lz.dim_term
SET summer_term_flag = '1'
WHERE summer_term_flag = 't';

DELETE FROM edware_lz.dim_term;
INSERT INTO edware_lz.dim_term
(
    dim_term_key
,   school_year_sid
,   term_code
,   term_name
,   current_term_flag
,   summer_term_flag
,   create_date
,   mod_date 
,   part_key
)
SELECT
    CAST(dim_term_key AS int),
    CAST(school_year_sid AS int),
    CAST(term_code AS varchar(255)),
    CAST(term_name AS varchar(255)),
    CAST(current_term_flag AS boolean),
    CAST(summer_term_flag AS boolean),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_term
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_term;
SELECT count(*) AS _load_count_ FROM edware.dim_term;

/*PASS
    CAST(period_order AS int),
    CAST(period_start_date date),
    CAST(period_end_date AS date),
    CAST(current_year_flag AS boolean),
    CAST(previous_year_flag AS boolean),
    CAST(current_period_flag AS boolean),
    CAST(previous_period_flag AS boolean),
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_period
SET part_key = '-9999'
WHERE part_key = '';

UPDATE edware_lz.dim_period
SET period_order = '-9999'
WHERE period_order = '';

UPDATE edware_lz.dim_period
SET period_start_date = '1970-01-01'
WHERE period_start_date = '';

UPDATE edware_lz.dim_period
SET period_end_date = '1970-01-01'
WHERE period_end_date = '';

UPDATE edware_lz.dim_period
SET current_year_flag = '0'
WHERE current_year_flag = '';

UPDATE edware_lz.dim_period
SET current_year_flag = '0'
WHERE current_year_flag = 'f';

UPDATE edware_lz.dim_period
SET current_year_flag = '1'
WHERE current_year_flag = 't';

UPDATE edware_lz.dim_period
SET previous_year_flag = '0'
WHERE previous_year_flag = '';

UPDATE edware_lz.dim_period
SET previous_year_flag = '0'
WHERE previous_year_flag = 'f';

UPDATE edware_lz.dim_period
SET previous_year_flag = '1'
WHERE previous_year_flag = 't';
--
UPDATE edware_lz.dim_period
SET current_period_flag = '0'
WHERE current_period_flag = '';

UPDATE edware_lz.dim_period
SET current_period_flag = '0'
WHERE current_period_flag = 'f';

UPDATE edware_lz.dim_period
SET current_period_flag = '1'
WHERE current_period_flag = 't';

UPDATE edware_lz.dim_period
SET previous_period_flag = '0'
WHERE previous_period_flag = '';

UPDATE edware_lz.dim_period
SET previous_period_flag = '0'
WHERE previous_period_flag = 'f';

UPDATE edware_lz.dim_period
SET previous_period_flag = '1'
WHERE previous_period_flag = 't';

DELETE FROM edware.dim_period;
INSERT INTO edware.dim_period
(
    dim_period_key
,   assmt_code
,   academic_year_name
,   academic_year_abbrev
,   academic_year_code
,   period_code
,   period_abbrev
,   period_order
,   period_start_date
,   period_end_date
,   current_year_flag
,   previous_year_flag
,   current_period_flag
,   previous_period_flag
,   period_name
,   create_date 
,   mod_date
,   part_key
)
SELECT 
    CAST(dim_period_key AS int),
    CAST(assmt_code AS varchar(255)),
    CAST(academic_year_name AS varchar(255)),
    CAST(academic_year_abbrev AS varchar(255)),
    CAST(academic_year_code AS varchar(255)),
    CAST(period_code AS varchar(255)),
    CAST(period_abbrev AS varchar(255)),
    CAST(period_order AS int),
    CAST(period_start_date AS date),
    CAST(period_end_date AS date),
    CAST(current_year_flag AS boolean),
    CAST(previous_year_flag AS boolean),
    CAST(current_period_flag AS boolean),
    CAST(previous_period_flag AS boolean),
    CAST(period_name AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_period
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_period;
SELECT count(*) AS _load_count_ FROM edware.dim_period;

/*PASS
    CAST(level_order AS int),
    CAST(part_key AS int),
    CAST(account_sid AS int)
*/
UPDATE edware_lz.dim_perf_level
SET level_order = '-9999'
WHERE level_order = '';

UPDATE edware_lz.dim_perf_level
SET part_key = '-9999'
WHERE part_key = '';

UPDATE edware_lz.dim_perf_level
SET account_sid = '-9999'
WHERE account_sid = '';

DELETE FROM edware.dim_perf_level;
INSERT INTO edware.dim_perf_level
(
    dim_perf_level_key
,   level_order
,   level_type_code
,   level_type_name
,   general_level_code
,   general_level_name
,   measure_type_specific_level_code
,   measure_type_specific_level_name
,   measure_specific_level_code
,   measure_specific_level_name
,   level_code
,   level_name
,   level_order_name
,   create_date
,   mod_date
,   part_key
,   account_sid
)
SELECT
    CAST(dim_perf_level_key AS int),
    CAST(level_order AS int),
    CAST(level_type_code AS varchar(255)),
    CAST(level_type_name AS varchar(255)),
    CAST(general_level_code AS varchar(255)),
    CAST(general_level_name AS varchar(255)),
    CAST(measure_type_specific_level_code AS varchar(255)),
    CAST(measure_type_specific_level_name AS varchar(255)),
    CAST(measure_specific_level_code AS varchar(255)),
    CAST(measure_specific_level_name AS varchar(255)),
    CAST(level_code AS varchar(255)),
    CAST(level_name AS varchar(255)),
    CAST(level_order_name AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(account_sid AS int)
FROM edware_lz.dim_perf_level
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_perf_level;
SELECT count(*) AS _load_count_ FROM edware.dim_perf_level;

/*PASS... no data
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_assmt_subject
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.dim_assmt_subject;
INSERT INTO edware.dim_assmt_subject
(
    dim_assmt_subject_key
,   assmt_subject_code
,   assmt_subject_name
,   custom_id_1_code
,   custom_id_1_type_code
,   custom_id_2_code
,   custom_id_2_type_code
,   custom_id_3_code
,   custom_id_3_type_code
,   custom_id_4_code
,   custom_id_4_type_code
,   custom_id_5_code
,   custom_id_5_type_code
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_assmt_subject_key AS int),
    CAST(assmt_subject_code AS varchar(255)),
    CAST(assmt_subject_name AS varchar(255)),
    CAST(custom_id_1_code AS varchar(255)),
    CAST(custom_id_1_type_code AS varchar(255)),
    CAST(custom_id_2_code AS varchar(255)),
    CAST(custom_id_2_type_code AS varchar(255)),
    CAST(custom_id_3_code AS varchar(255)),
    CAST(custom_id_3_type_code AS varchar(255)),
    CAST(custom_id_4_code AS varchar(255)),
    CAST(custom_id_4_type_code AS varchar(255)),
    CAST(custom_id_5_code AS varchar(255)),
    CAST(custom_id_5_type_code AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_assmt_subject
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_assmt_subject;
SELECT count(*) AS _load_count_ FROM edware.dim_assmt_subject;


/*PASS... no data
    CAST(dim_assmt_subject_key AS int),
    CAST(dim_subject_key AS int),
    CAST(part_key AS int)
*/
UPDATE edware_lz.map_assmt_subj_subj
SET dim_assmt_subject_key = '-9999'
WHERE dim_assmt_subject_key = '';

UPDATE edware_lz.map_assmt_subj_subj
SET dim_subject_key = '-9999'
WHERE dim_subject_key = '';

UPDATE edware_lz.map_assmt_subj_subj
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.map_assmt_subj_subj;
INSERT INTO edware.map_assmt_subj_subj
(
    map_assmt_subj_subj_key
,   dim_assmt_subject_key
,   dim_subject_key
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(map_assmt_subj_subj_key AS int),
    CAST(dim_assmt_subject_key AS int),
    CAST(dim_subject_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.map_assmt_subj_subj
;

SELECT count(*) AS _lz_count_ FROM edware_lz.map_assmt_subj_subj;
SELECT count(*) AS _load_count_ FROM edware.map_assmt_subj_subj;


/*PASS
    CAST(grade_level_sid AS int),
    CAST(grade_level_order AS int),
    CAST(updated_flag AS boolean),
    CAST(grade_band_flag AS boolean),
    CAST(grade_band_min AS int),
    CAST(grade_band_max AS int),
    CAST(part_key AS int)
*/

UPDATE edware_lz.dim_grade
SET grade_level_sid = '-9999'
WHERE grade_level_sid = '';

UPDATE edware_lz.dim_grade
SET grade_level_order = '-9999'
WHERE grade_level_order = '';

UPDATE edware_lz.dim_grade
SET updated_flag = '0'
WHERE updated_flag = '';

UPDATE edware_lz.dim_grade
SET updated_flag = '0'
WHERE updated_flag = 'f';

UPDATE edware_lz.dim_grade
SET updated_flag = '1'
WHERE updated_flag = 't';

UPDATE edware_lz.dim_grade
SET grade_band_flag = '0'
WHERE grade_band_flag = '';

UPDATE edware_lz.dim_grade
SET grade_band_flag = '0'
WHERE grade_band_flag = 'f';

UPDATE edware_lz.dim_grade
SET grade_band_flag = '1'
WHERE grade_band_flag = 't';

UPDATE edware_lz.dim_grade
SET grade_band_min = '-9999'
WHERE grade_band_min = '';

UPDATE edware_lz.dim_grade
SET grade_band_max = '-9999'
WHERE grade_band_max = '';

UPDATE edware_lz.dim_grade
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.dim_grade;
INSERT INTO edware.dim_grade
(
    dim_grade_key
,   grade_level_sid 
,   grade_level_name
,   grade_band_code
,   grade_band_name
,   grade_level_order
,   updated_flag
,   grade_band_flag
,   grade_band_min
,   grade_band_max
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_grade_key AS int),
    CAST(grade_level_sid AS int),
    CAST(grade_level_name AS varchar(255)),
    CAST(grade_band_code AS varchar(255)),
    CAST(grade_band_name AS varchar(255)),
    CAST(grade_level_order AS int),
    CAST(updated_flag AS boolean),
    CAST(grade_band_flag AS boolean),
    CAST(grade_band_min AS int),
    CAST(grade_band_max AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_grade
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_grade;
SELECT count(*) AS _load_count_ FROM edware.dim_grade;

/*PASS
    CAST(dim_time_key AS int),
    CAST(calendar_date AS date),
    CAST(day_of_year AS int),
    CAST(day_of_month AS int),
    CAST(day_of_week AS int),
    CAST(week_of_year AS int),
    CAST(week_of_month AS int),
    CAST(week_ending AS date),
    CAST(month_of_year AS int),
    CAST(quarter_of_year AS int),
    CAST(_year AS int),
    CAST(is_holiday AS boolean),
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_time
SET dim_time_key = '-9999'
WHERE dim_time_key = '';

UPDATE edware_lz.dim_time
SET calendar_date = '1970-01-01'
WHERE calendar_date = '';

UPDATE edware_lz.dim_time
SET day_of_year = '-9999'
WHERE day_of_year = '';

UPDATE edware_lz.dim_time
SET day_of_month = '-9999'
WHERE day_of_month = '';

UPDATE edware_lz.dim_time
SET day_of_week = '-9999'
WHERE day_of_week = '';

UPDATE edware_lz.dim_time
SET week_of_year = '-9999'
WHERE week_of_year = '';

UPDATE edware_lz.dim_time
SET week_of_month = '-9999'
WHERE week_of_month = '';

UPDATE edware_lz.dim_time
SET week_ending = '1970-01-01'
WHERE week_ending = '';

UPDATE edware_lz.dim_time
SET month_of_year = '-9999'
WHERE month_of_year = '';

UPDATE edware_lz.dim_time
SET quarter_of_year = '-9999'
WHERE quarter_of_year = '';

UPDATE edware_lz.dim_time
SET year = '-9999'
WHERE year = '';
--
UPDATE edware_lz.dim_time
SET is_holiday = '0'
WHERE is_holiday = '';

UPDATE edware_lz.dim_time
SET is_holiday = '0'
WHERE is_holiday = 'f';

UPDATE edware_lz.dim_time
SET is_holiday = '1'
WHERE is_holiday = 't';

UPDATE edware_lz.dim_time
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.dim_time;
INSERT INTO edware.dim_time
(
    dim_time_key
,   calendar_date
,   day_of_year
,   day_of_month
,   day_of_week
,   day_name
,   week_of_year
,   week_of_month
,   week_ending
,   month_of_year
,   month_name
,   quarter_of_year
,   _year
,   is_holiday
,   holiday_name
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_time_key AS int),
    CAST(calendar_date AS date),
    CAST(day_of_year AS int),
    CAST(day_of_month AS int),
    CAST(day_of_week AS int),
    CAST(day_name AS varchar(255)),
    CAST(week_of_year AS int),
    CAST(week_of_month AS int),
    CAST(week_ending AS date),
    CAST(month_of_year AS int),
    CAST(month_name AS varchar(255)),
    CAST(quarter_of_year AS int),
    CAST(year AS int),
    CAST(is_holiday AS boolean),
    CAST(holiday_name AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)--*/
FROM edware_lz.dim_time
--LIMIT 10
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_time;
SELECT count(*) AS _load_count_ FROM edware.dim_time;

--jsbiii
/*PASS/FAIL
    CAST(current_acad_year_flag AS boolean),
    CAST(school_year_sid AS int),
    CAST(school_sid AS int),
    CAST(district_sid AS int),
    CAST(municipality_sid AS int),
    CAST(account_sid AS int),
    CAST(state_sid AS int),
    CAST(country_sid AS int),
    CAST(school_open_date AS date),
    CAST(school_years_open AS int),
    CAST(title_1_flag AS boolean),
    CAST(reading_first_flag AS boolean),
    CAST(dim_curr_institution_key AS int),
    CAST(demo_flag AS boolean),
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_institution
SET current_acad_year_flag = '0'
WHERE current_acad_year_flag = '';

UPDATE edware_lz.dim_institution
SET current_acad_year_flag = '0'
WHERE current_acad_year_flag = 'f';

UPDATE edware_lz.dim_institution
SET current_acad_year_flag = '1'
WHERE current_acad_year_flag = 't';

UPDATE edware_lz.dim_institution
SET school_year_sid = '-9999'
WHERE school_year_sid = '';

UPDATE edware_lz.dim_institution
SET district_sid = '-9999'
WHERE district_sid = '';

UPDATE edware_lz.dim_institution
SET municipality_sid = '-9999'
WHERE municipality_sid = '';

UPDATE edware_lz.dim_institution
SET account_sid = '-9999'
WHERE account_sid = '';

UPDATE edware_lz.dim_institution
SET country_sid = '-9999'
WHERE country_sid = '';

UPDATE edware_lz.dim_institution
SET country_sid = '-9999'
WHERE country_sid = '';

UPDATE edware_lz.dim_institution
SET school_open_date = '1970-01-01'
WHERE school_open_date = '';

UPDATE edware_lz.dim_institution
SET school_years_open = '-9999'
WHERE school_years_open = '';

UPDATE edware_lz.dim_institution
SET title_1_flag = '0'
WHERE title_1_flag = '';

UPDATE edware_lz.dim_institution
SET title_1_flag = '0'
WHERE title_1_flag = 'f';

UPDATE edware_lz.dim_institution
SET title_1_flag = '1'
WHERE title_1_flag = 't';

UPDATE edware_lz.dim_institution
SET reading_first_flag = '0'
WHERE reading_first_flag = '';

UPDATE edware_lz.dim_institution
SET reading_first_flag = '0'
WHERE reading_first_flag = 'f';

UPDATE edware_lz.dim_institution
SET reading_first_flag = '1'
WHERE reading_first_flag = 't';

UPDATE edware_lz.dim_institution
SET dim_curr_institution_key = '-9999'
WHERE dim_curr_institution_key = '';
--
UPDATE edware_lz.dim_institution
SET demo_flag = '0'
WHERE demo_flag = '';

UPDATE edware_lz.dim_institution
SET demo_flag = '0'
WHERE demo_flag = 'f';

UPDATE edware_lz.dim_institution
SET demo_flag = '1'
WHERE demo_flag = 't';

UPDATE edware_lz.dim_institution
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.dim_institution;
INSERT INTO edware.dim_institution
(
    dim_institution_key
,   academic_year_code
,   academic_year_name
,   current_acad_year_flag
,   grade_config_code
,   grade_config_name
,   school_year_sid
,   school_sid
,   school_name 
,   school_phone
,   school_address_1
,   school_address_2
,   school_city
,   school_zip_code
,   district_sid
,   district_name
,   municipality_sid
,   municipality_name
,   account_sid
,   account_name
,   state_sid
,   state_code
,   state_name
,   country_sid
,   country_name
,   location_1_code
,   location_1_name
,   location_2_code
,   location_2_name
,   location_3_code
,   location_3_name
,   location_4_code
,   location_4_name
,   location_5_code
,   location_5_name
,   location_1_type_code
,   location_1_type_name
,   location_2_type_code
,   location_2_type_name
,   location_3_type_code 
,   location_3_type_name
,   location_4_type_code
,   location_4_type_name
,   location_5_type_code
,   location_5_type_name
,   school_open_date
,   school_years_open
,   title_1_flag
,   reading_first_flag
,   url
,   custom_id_1_code
,   custom_id_1_type_code
,   custom_id_2_code
,   custom_id_2_type_code
,   custom_id_3_code
,   custom_id_3_type_code
,   custom_id_4_code
,   custom_id_4_type_code
,   custom_id_5_code
,   custom_id_5_type_code
,   dim_curr_institution_key
,   status_code
,   demo_flag
,   create_date
,   mod_date 
,   part_key
)
SELECT
    CAST(dim_institution_key AS int),
    CAST(academic_year_code AS varchar(255)),
    CAST(academic_year_name AS varchar(255)),
    CAST(current_acad_year_flag AS boolean),
    CAST(grade_config_code AS varchar(255)),
    CAST(grade_config_name AS varchar(255)),
    CAST(school_year_sid AS int),
    CAST(school_sid AS int),
    CAST(school_name AS varchar(255)),
    CAST(school_phone AS varchar(255)),
    CAST(school_address_1 AS varchar(255)),
    CAST(school_address_2 AS varchar(255)),
    CAST(school_city AS varchar(255)),
    CAST(school_zip_code AS varchar(255)),
    CAST(district_sid AS int),
    CAST(district_name AS varchar(255)),
    CAST(municipality_sid AS int),
    CAST(municipality_name AS varchar(255)),
    CAST(account_sid AS int),
    CAST(account_name AS varchar(255)),
    CAST(state_sid AS int),
    CAST(state_code AS varchar(255)),
    CAST(state_name AS varchar(255)),
    CAST(country_sid AS int),
    CAST(country_name AS varchar(255)),
    CAST(location_1_code AS varchar(255)),
    CAST(location_1_name AS varchar(255)),
    CAST(location_2_code AS varchar(255)),
    CAST(location_2_name AS varchar(255)),
    CAST(location_3_code AS varchar(255)),
    CAST(location_3_name AS varchar(255)),
    CAST(location_4_code AS varchar(255)),
    CAST(location_4_name AS varchar(255)),
    CAST(location_5_code AS varchar(255)),
    CAST(location_5_name AS varchar(255)),
    CAST(location_1_type_code AS varchar(255)),
    CAST(location_1_type_name AS varchar(255)),
    CAST(location_2_type_code AS varchar(255)),
    CAST(location_2_type_name AS varchar(255)),
    CAST(location_3_type_code AS varchar(255)),
    CAST(location_3_type_name AS varchar(255)),
    CAST(location_4_type_code AS varchar(255)),
    CAST(location_4_type_name AS varchar(255)),
    CAST(location_5_type_code AS varchar(255)),
    CAST(location_5_type_name AS varchar(255)),
    CAST(school_open_date AS date),
    CAST(school_years_open AS int),
    CAST(title_1_flag AS boolean),
    CAST(reading_first_flag AS boolean),
    CAST(url AS varchar(255)),
    CAST(custom_id_1_code AS varchar(255)),
    CAST(custom_id_1_type_code AS varchar(255)),
    CAST(custom_id_2_code AS varchar(255)),
    CAST(custom_id_2_type_code AS varchar(255)),
    CAST(custom_id_3_code AS varchar(255)),
    CAST(custom_id_3_type_code AS varchar(255)),
    CAST(custom_id_4_code AS varchar(255)),
    CAST(custom_id_4_type_code AS varchar(255)),
    CAST(custom_id_5_code AS varchar(255)),
    CAST(custom_id_5_type_code AS varchar(255)),
    CAST(dim_curr_institution_key AS int),
    CAST(status_code AS varchar(255)),
    CAST(demo_flag AS boolean),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)-- */
FROM edware_lz.dim_institution
-- LIMIT 10
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_institution;
SELECT count(*) AS _load_count_ FROM edware.dim_institution;

/*PASS
    CAST(parent_inst_group_key AS int),
    CAST(account_sid AS int),
    CAST(group_start_time AS date),
    CAST(group_end_time AS date),
    CAST(state_sid AS int),
    CAST(is_internal AS boolean),
    CAST(is_funding_source AS boolean),
    CAST(is_study AS boolean),
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_inst_group
SET parent_inst_group_key = '-9999'
WHERE parent_inst_group_key = '';

UPDATE edware_lz.dim_inst_group
SET account_sid = '-9999'
WHERE account_sid = '';

UPDATE edware_lz.dim_inst_group
SET group_start_time = '1970-01-01'
WHERE group_start_time = '';

UPDATE edware_lz.dim_inst_group
SET group_end_time = '1970-01-01'
WHERE group_end_time = '';

UPDATE edware_lz.dim_inst_group
SET state_sid = '-9999'
WHERE state_sid = '';

UPDATE edware_lz.dim_inst_group
SET is_internal = '0'
WHERE is_internal = '';

UPDATE edware_lz.dim_inst_group
SET is_internal = '0'
WHERE is_internal = 'f';

UPDATE edware_lz.dim_inst_group
SET is_internal = '1'
WHERE is_internal = 't';

UPDATE edware_lz.dim_inst_group
SET is_funding_source = '0'
WHERE is_funding_source = '';

UPDATE edware_lz.dim_inst_group
SET is_funding_source = '0'
WHERE is_funding_source = 'f';

UPDATE edware_lz.dim_inst_group
SET is_funding_source = '1'
WHERE is_funding_source = 't';

UPDATE edware_lz.dim_inst_group
SET is_funding_source = '0'
WHERE is_funding_source = '';

UPDATE edware_lz.dim_inst_group
SET is_funding_source = '0'
WHERE is_funding_source = 'f';

UPDATE edware_lz.dim_inst_group
SET is_funding_source = '1'
WHERE is_funding_source = 't';

UPDATE edware_lz.dim_inst_group
SET is_study = '0'
WHERE is_study = '';

UPDATE edware_lz.dim_inst_group
SET is_study = '0'
WHERE is_study = 'f';

UPDATE edware_lz.dim_inst_group
SET is_study = '1'
WHERE is_study = 't';

UPDATE edware_lz.dim_inst_group
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.dim_inst_group;
INSERT INTO edware.dim_inst_group
(
    dim_inst_group_key
,   parent_inst_group_key
,   inst_group_name
,   inst_group_type_name
,   account_sid
,   account_name
,   sif_inst_group_type
,   sif_inst_group_type_attribute
,   group_start_time
,   group_end_time
,   status_code
,   address_1 
,   address_2
,   city
,   zip_code
,   state_sid
,   state_code
,   state_name
,   phone 
,   url
,   managed_by_code
,   managed_by_name
,   is_internal
,   is_funding_source
,   is_study
,   inst_group_code
,   inst_group_type_code
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(dim_inst_group_key AS int),
    CAST(parent_inst_group_key AS int),
    CAST(inst_group_name AS varchar(255)),
    CAST(inst_group_type_name AS varchar(255)),
    CAST(account_sid AS int),
    CAST(account_name AS varchar(255)),
    CAST(sif_inst_group_type AS varchar(255)),
    CAST(sif_inst_group_type_attribute AS varchar(255)),
    CAST(group_start_time AS date),
    CAST(group_end_time AS date),
    CAST(status_code AS varchar(255)),
    CAST(address_1 AS varchar(255)),
    CAST(address_2 AS varchar(255)),
    CAST(city AS varchar(255)),
    CAST(zip_code AS varchar(255)),
    CAST(state_sid AS int),
    CAST(state_code AS varchar(255)),
    CAST(state_name AS varchar(255)),
    CAST(phone AS varchar(255)),
    CAST(url AS varchar(255)),
    CAST(managed_by_code AS varchar(255)),
    CAST(managed_by_name AS varchar(255)),
    CAST(is_internal AS boolean),
    CAST(is_funding_source AS boolean),
    CAST(is_study AS boolean),
    CAST(inst_group_code AS varchar(255)),
    CAST(inst_group_type_code AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.dim_inst_group
-- LIMIT 10
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_inst_group;
SELECT count(*) AS _load_count_ FROM edware.dim_inst_group;

/*PASS
    CAST(dim_institution_key AS int),
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_institution
SET dim_institution_key = '-9999'
WHERE dim_institution_key = '';

UPDATE edware_lz.dim_institution
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.map_inst_group_inst;
INSERT INTO edware.map_inst_group_inst
(
    map_inst_group_inst_key
,   dim_inst_group_key
,   dim_institution_key
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(map_inst_group_inst_key AS int),
    CAST(dim_inst_group_key AS int),
    CAST(dim_institution_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.map_inst_group_inst
;

SELECT count(*) AS _lz_count_ FROM edware_lz.map_inst_group_inst;
SELECT count(*) AS _load_count_ FROM edware.map_inst_group_inst;

/*PASS/FAIL
    CAST(student_sid AS int),
    CAST(eternal_student_sid AS int),
    CAST(dob AS date),
    CAST(age_as_of_curr_year AS int),
    CAST(demo_flag AS boolean),
    CAST(source_create_date AS date),
    CAST(source_mod_date AS date),
    CAST(part_key AS int)
*/
UPDATE edware_lz.dim_student
SET student_sid = '-9999'
WHERE student_sid = '';

UPDATE edware_lz.dim_student
SET eternal_student_sid = '-9999'
WHERE eternal_student_sid = '';

UPDATE edware_lz.dim_student
SET dob = '1970-01-01'
WHERE dob = '';

UPDATE edware_lz.dim_student
SET age_as_of_curr_year = '-9999'
WHERE age_as_of_curr_year = '';

UPDATE edware_lz.dim_student
SET demo_flag = '0'
WHERE demo_flag = '';

UPDATE edware_lz.dim_student
SET demo_flag = '0'
WHERE demo_flag = 'f';

UPDATE edware_lz.dim_student
SET demo_flag = '1'
WHERE demo_flag = 't';

UPDATE edware_lz.dim_student
SET source_create_date = '0'
WHERE source_create_date = '';

UPDATE edware_lz.dim_student
SET source_create_date = '0'
WHERE source_create_date = 'f';

UPDATE edware_lz.dim_student
SET source_create_date = '1'
WHERE source_create_date = 't';

UPDATE edware_lz.dim_student
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.dim_student;
INSERT INTO edware.dim_student
(
    dim_student_key
,   student_sid
,   eternal_student_sid
,   first_name
,   middle_name
,   last_name
,   suffix
,   dob
,   email
,   home_phone
,   place_of_birth_code
,   place_of_birth_name
,   gender_code
,   gender_name
,   grad_cohort_year_code
,   grad_cohort_year_name
,   age_as_of_curr_year
,   status_code
,   demo_flag
,   custom_id_1_code
,   custom_id_1_type_code
,   custom_id_2_code
,   custom_id_2_type_code
,   custom_id_3_code
,   custom_id_3_type_code
,   custom_id_4_code
,   custom_id_4_type_code
,   custom_id_5_code
,   custom_id_5_type_code
,   source_create_date
,   source_mod_date
,   create_date
,   mod_date
,   part_key
,   inst_sid
,   year_sid
)
SELECT
    CAST(dim_student_key AS int),
    CAST(student_sid AS int),
    CAST(eternal_student_sid AS int),
    CAST(first_name AS varchar(255)),
    CAST(middle_name AS varchar(255)),
    CAST(last_name AS varchar(255)),
    CAST(suffix AS varchar(255)),
    CAST(dob AS date),
    CAST(email AS varchar(255)),
    CAST(home_phone AS varchar(255)),
    CAST(place_of_birth_code AS varchar(255)),
    CAST(place_of_birth_name AS varchar(255)),
    CAST(gender_code AS varchar(255)),
    CAST(gender_name AS varchar(255)),
    CAST(grad_cohort_year_code AS varchar(255)),
    CAST(grad_cohort_year_name AS varchar(255)),
    CAST(age_as_of_curr_year AS int),
    CAST(status_code AS varchar(255)),
    CAST(demo_flag AS boolean),
    CAST(custom_id_1_code AS varchar(255)),
    CAST(custom_id_1_type_code AS varchar(255)),
    CAST(custom_id_2_code AS varchar(255)),
    CAST(custom_id_2_type_code AS varchar(255)),
    CAST(custom_id_3_code AS varchar(255)),
    CAST(custom_id_3_type_code AS varchar(255)),
    CAST(custom_id_4_code AS varchar(255)),
    CAST(custom_id_4_type_code AS varchar(255)),
    CAST(custom_id_5_code AS varchar(255)),
    CAST(custom_id_5_type_code AS varchar(255)),
    CAST(source_create_date AS date),
    CAST(source_mod_date AS date),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(inst_sid AS int),
    CAST(year_sid AS int)
FROM edware_lz.dim_student
-- LIMIT 10
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_student;
SELECT count(*) AS _load_count_ FROM edware.dim_student;

/*PASS... no data
    CAST(dim_staff_group_key AS int),
    CAST(dim_staff_key AS int),
    CAST(part_key AS int)
*/
UPDATE edware_lz.map_staff_group_staff
SET dim_staff_group_key = '-9999'
WHERE dim_staff_group_key = '';

UPDATE edware_lz.map_staff_group_staff
SET dim_staff_key = '-9999'
WHERE dim_staff_key = '';

UPDATE edware_lz.map_staff_group_staff
SET part_key = '-9999'
WHERE part_key = '';

DELETE FROM edware.map_staff_group_staff;
INSERT INTO edware.map_staff_group_staff
(
    map_staff_group_staff_key
,   dim_staff_group_key
,   dim_staff_key
,   create_date
,   mod_date
,   part_key
)
SELECT
    CAST(map_staff_group_staff_key AS int),
    CAST(dim_staff_group_key AS int),
    CAST(dim_staff_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.map_staff_group_staff
LIMIT 10
;

SELECT count(*) AS _lz_count_ FROM edware_lz.map_staff_group_staff;
SELECT count(*) AS _load_count_ FROM edware.map_staff_group_staff;

/*PASS/FAIL
    CAST(part_key AS int),
    CAST(dim_institution_key AS int),
    CAST(dim_student_key AS int),
    CAST(dim_grade_key AS int),
    CAST(dim_section_key AS int),
    CAST(dim_term_key AS int),
    CAST(dim_teacher_staff_key AS int),
    CAST(dim_enroll_attr_key AS int),
    CAST(dim_inst_admit_time_key AS int),
    CAST(dim_inst_disc_time_key AS int),
    CAST(dim_sect_admit_time_key AS int) ,
    CAST(dim_sect_disc_time_key AS int),
    CAST(enrolled_in_inst_flag AS boolean) ,
    CAST(enrolled_in_sect_flag AS boolean),
    CAST(student_sid AS int),
    CAST(eternal_student_sid AS int),
    CAST(section_sid AS int),
    CAST(year_sid AS int),
    CAST(is_reporting_classe AS boolean),
*/
UPDATE edware_lz.fact_enroll
SET part_key = '-9999'
WHERE part_key = '';

UPDATE edware_lz.fact_enroll
SET dim_institution_key = '-9999'
WHERE dim_institution_key = '';

UPDATE edware_lz.fact_enroll
SET dim_student_key = '-9999'
WHERE dim_student_key = '';

UPDATE edware_lz.fact_enroll
SET dim_grade_key = '-9999'
WHERE dim_grade_key = '';

UPDATE edware_lz.fact_enroll
SET dim_section_key = '-9999'
WHERE dim_section_key = '';

UPDATE edware_lz.fact_enroll
SET dim_term_key = '-9999'
WHERE dim_term_key = '';

UPDATE edware_lz.fact_enroll
SET dim_teacher_staff_key = '-9999'
WHERE dim_teacher_staff_key = '';

UPDATE edware_lz.fact_enroll
SET dim_enroll_attr_key = '-9999'
WHERE dim_enroll_attr_key = '';

UPDATE edware_lz.fact_enroll
SET dim_inst_admit_time_key = '-9999'
WHERE dim_inst_admit_time_key = '';

UPDATE edware_lz.fact_enroll
SET dim_inst_disc_time_key = '-9999'
WHERE dim_inst_disc_time_key = '';

UPDATE edware_lz.fact_enroll
SET dim_sect_admit_time_key = '-9999'
WHERE dim_sect_admit_time_key = '';

UPDATE edware_lz.fact_enroll
SET dim_sect_disc_time_key = '-9999'
WHERE dim_sect_disc_time_key = '';

UPDATE edware_lz.fact_enroll
SET enrolled_in_inst_flag = '0'
WHERE enrolled_in_inst_flag = '';

UPDATE edware_lz.fact_enroll
SET enrolled_in_inst_flag = '0'
WHERE enrolled_in_inst_flag = 'f';

UPDATE edware_lz.fact_enroll
SET enrolled_in_inst_flag = '1'
WHERE enrolled_in_inst_flag = 't';

UPDATE edware_lz.fact_enroll
SET enrolled_in_sect_flag = '0'
WHERE enrolled_in_sect_flag = '';

UPDATE edware_lz.fact_enroll
SET enrolled_in_sect_flag = '0'
WHERE enrolled_in_sect_flag = 'f';

UPDATE edware_lz.fact_enroll
SET enrolled_in_sect_flag = '1'
WHERE enrolled_in_sect_flag = 't';

UPDATE edware_lz.fact_enroll
SET student_sid = '-9999'
WHERE student_sid = '';

UPDATE edware_lz.fact_enroll
SET eternal_student_sid = '-9999'
WHERE eternal_student_sid = '';

UPDATE edware_lz.fact_enroll
SET section_sid = '-9999'
WHERE section_sid = '';

UPDATE edware_lz.fact_enroll
SET year_sid = '-9999'
WHERE year_sid = '';

UPDATE edware_lz.fact_enroll
SET is_reporting_classe = '0'
WHERE is_reporting_classe = '';

UPDATE edware_lz.fact_enroll
SET is_reporting_classe = '0'
WHERE is_reporting_classe = 'f';

UPDATE edware_lz.fact_enroll
SET is_reporting_classe = '1'
WHERE is_reporting_classe = 't';

DELETE FROM edware.fact_enroll;
INSERT INTO edware.fact_enroll
(
    fact_enroll_key
,   part_key
,   dim_institution_key
,   dim_student_key
,   dim_grade_key
,   dim_section_key
,   dim_term_key
,   dim_teacher_staff_key
,   dim_enroll_attr_key
,   dim_inst_admit_time_key
,   dim_inst_disc_time_key
,   dim_sect_admit_time_key
,   dim_sect_disc_time_key
,   enrolled_in_inst_flag
,   enrolled_in_sect_flag
,   student_sid
,   eternal_student_sid
,   section_sid 
,   year_sid
,   is_reporting_classe
,   section_type_code
,   section_subtype_code
,   create_date
,   mod_date
)
SELECT
    CAST(fact_enroll_key AS int),
    CAST(part_key AS int),
    CAST(dim_institution_key AS int),
    CAST(dim_student_key AS int),
    CAST(dim_grade_key AS int),
    CAST(dim_section_key AS int),
    CAST(dim_term_key AS int),
    CAST(dim_teacher_staff_key AS int),
    CAST(dim_enroll_attr_key AS int),
    CAST(dim_inst_admit_time_key AS int),
    CAST(dim_inst_disc_time_key AS int),
    CAST(dim_sect_admit_time_key AS int) ,
    CAST(dim_sect_disc_time_key AS int),
    CAST(enrolled_in_inst_flag AS boolean) ,
    CAST(enrolled_in_sect_flag AS boolean),
    CAST(student_sid AS int),
    CAST(eternal_student_sid AS int),
    CAST(section_sid AS int),
    CAST(year_sid AS int),
    CAST(is_reporting_classe AS boolean),
    CAST(section_type_code AS varchar(255)),
    CAST(section_subtype_code AS varchar(255)),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp)
FROM edware_lz.fact_enroll
;

/*clearing out fe's with missing dimension keys.
DELETE FROM edware.fact_enroll
WHERE dim_student_key not in (select dim_student_key from edware.dim_student);

DELETE FROM edware.fact_enroll
WHERE dim_section_key not in (select dim_section_key from edware.dim_section);
*/
SELECT count(*) AS _lz_count_ FROM edware_lz.fact_enroll;
SELECT count(*) AS _load_count_ FROM edware.fact_enroll;

/*PASS/FAIL
    CAST(assmt_version_rank AS int),
    CAST(daot_measure_type_rank AS int),
    CAST(daot_hier_level AS int),
    CAST(daot_hier_level_rank AS int),
    CAST(performance_level_flag AS boolean),
    CAST(outcome_int_flag AS boolean),
    CAST(outcome_float_flag AS boolean),
    CAST(outcome_string_flag AS boolean),
    CAST(outcome_rank AS int),
    CAST(part_key AS int),
    CAST(pg_by_grade_flag AS boolean),
*/
UPDATE edware_lz.dim_assmt_outcome_type
SET assmt_version_rank = '-9999'
WHERE assmt_version_rank = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET daot_measure_type_rank = '-9999'
WHERE daot_measure_type_rank = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET daot_hier_level = '-9999'
WHERE daot_hier_level = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET daot_hier_level_rank = '-9999'
WHERE daot_hier_level_rank = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET performance_level_flag = '0'
WHERE performance_level_flag = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET performance_level_flag = '0'
WHERE performance_level_flag = 'f';

UPDATE edware_lz.dim_assmt_outcome_type
SET performance_level_flag = '1'
WHERE performance_level_flag = 't';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_int_flag = '0'
WHERE outcome_int_flag = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_int_flag = '0'
WHERE outcome_int_flag = 'f';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_int_flag = '1'
WHERE outcome_int_flag = 't';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_float_flag = '0'
WHERE outcome_float_flag = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_float_flag = '0'
WHERE outcome_float_flag = 'f';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_float_flag = '1'
WHERE outcome_float_flag = 't';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_string_flag = '0'
WHERE outcome_string_flag = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_string_flag = '0'
WHERE outcome_string_flag = 'f';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_string_flag = '1'
WHERE outcome_string_flag = 't';

UPDATE edware_lz.dim_assmt_outcome_type
SET outcome_rank = '-9999'
WHERE outcome_rank = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET part_key = '-9999'
WHERE part_key = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET pg_by_grade_flag = '0'
WHERE pg_by_grade_flag = '';

UPDATE edware_lz.dim_assmt_outcome_type
SET pg_by_grade_flag = '0'
WHERE pg_by_grade_flag = 'f';

UPDATE edware_lz.dim_assmt_outcome_type
SET pg_by_grade_flag = '1'
WHERE pg_by_grade_flag = 't';

DELETE FROM edware.dim_assmt_outcome_type;
INSERT INTO edware.dim_assmt_outcome_type
(
    dim_assmt_outcome_type_key
,   assmt_code
,   assmt_name
,   assmt_abbrev
,   assmt_version_code
,   assmt_version_name
,   assmt_version_abbrev
,   assmt_version_rank
,   daot_measure_type_code
,   daot_measure_type_name
,   daot_measure_type_rank
,   daot_hier_level
,   daot_hier_level_code
,   daot_hier_level_name
,   daot_hier_level_rank
,   daot_hier_level_1_code
,   daot_hier_level_1_name
,   daot_hier_level_1_abbrev
,   daot_hier_level_2_code
,   daot_hier_level_2_name
,   daot_hier_level_2_abbrev
,   daot_hier_level_3_code
,   daot_hier_level_3_name
,   daot_hier_level_3_abbrev
,   daot_hier_level_4_code
,   daot_hier_level_4_name
,   daot_hier_level_4_abbrev
,   daot_hier_level_5_code
,   daot_hier_level_5_name
,   daot_hier_level_5_abbrev
,   performance_level_flag
,   performance_level_type_code
,   outcome_int_flag
,   outcome_int_code
,   outcome_int_name
,   outcome_int_abbrev
,   outcome_float_flag
,   outcome_float_code
,   outcome_float_name
,   outcome_float_abbrev
,   outcome_string_flag
,   outcome_string_code
,   outcome_string_name
,   outcome_string_abbrev
,   outcome_rank
,   create_date
,   mod_date
,   part_key
,   pg_by_grade_flag
,   assmt_course_code
,   assmt_course_name
)
SELECT
    CAST(dim_assmt_outcome_type_key AS int),
    CAST(assmt_code AS varchar(255)),
    CAST(assmt_name AS varchar(255)),
    CAST(assmt_abbrev AS varchar(255)),
    CAST(assmt_version_code AS varchar(255)),
    CAST(assmt_version_name AS varchar(255)),
    CAST(assmt_version_abbrev AS varchar(255)),
    CAST(assmt_version_rank AS int),
    CAST(daot_measure_type_code AS varchar(255)),
    CAST(daot_measure_type_name AS varchar(255)),
    CAST(daot_measure_type_rank AS int),
    CAST(daot_hier_level AS int),
    CAST(daot_hier_level_code AS varchar(255)),
    CAST(daot_hier_level_name AS varchar(255)),
    CAST(daot_hier_level_rank AS int),
    CAST(daot_hier_level_1_code AS varchar(255)),
    CAST(daot_hier_level_1_name AS varchar(255)),
    CAST(daot_hier_level_1_abbrev AS varchar(255)),
    CAST(daot_hier_level_2_code AS varchar(255)),
    CAST(daot_hier_level_2_name AS varchar(255)),
    CAST(daot_hier_level_2_abbrev AS varchar(255)),
    CAST(daot_hier_level_3_code AS varchar(255)),
    CAST(daot_hier_level_3_name AS varchar(255)),
    CAST(daot_hier_level_3_abbrev AS varchar(255)),
    CAST(daot_hier_level_4_code AS varchar(255)),
    CAST(daot_hier_level_4_name AS varchar(255)),
    CAST(daot_hier_level_4_abbrev AS varchar(255)),
    CAST(daot_hier_level_5_code AS varchar(255)),
    CAST(daot_hier_level_5_name AS varchar(255)),
    CAST(daot_hier_level_5_abbrev AS varchar(255)),
    CAST(performance_level_flag AS boolean),
    CAST(performance_level_type_code AS varchar(255)),
    CAST(outcome_int_flag AS boolean),
    CAST(outcome_int_code AS varchar(255)),
    CAST(outcome_int_name AS varchar(255)),
    CAST(outcome_int_abbrev AS varchar(255)),
    CAST(outcome_float_flag AS boolean),
    CAST(outcome_float_code AS varchar(255)),
    CAST(outcome_float_name AS varchar(255)),
    CAST(outcome_float_abbrev AS varchar(255)),
    CAST(outcome_string_flag AS boolean),
    CAST(outcome_string_code AS varchar(255)),
    CAST(outcome_string_name AS varchar(255)),
    CAST(outcome_string_abbrev AS varchar(255)),
    CAST(outcome_rank AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(pg_by_grade_flag AS boolean),
    CAST(assmt_course_code AS varchar(255)),
    CAST(assmt_course_name AS varchar(255))
FROM edware_lz.dim_assmt_outcome_type
;

SELECT count(*) AS _lz_count_ FROM edware_lz.dim_assmt_outcome_type;
SELECT count(*) AS _load_count_ FROM edware.dim_assmt_outcome_type;

/*PASS
    CAST(part_key int),
    CAST(active_flag boolean),
    CAST(dim_student_key int),
    CAST(eternal_student_sid int),
    CAST(year_sid int),
    CAST(dim_assmt_staff_key int),
    CAST(dim_assmt_outcome_type_key int),
    CAST(dim_assmt_period_key int),
    CAST(dim_assmt_grade_key int),
    CAST(dim_assmt_time_key int),
    CAST(dim_assmt_sync_time_key int),
    CAST(dim_perf_level_key int),
    CAST(dim_custom_perf_level_key int,
    CAST(dim_assmt_institution_key int),
    CAST(dim_curr_institution_key int,
    CAST(dim_eoy_institution_key int,
    CAST(dim_curr_enroll_attr_key int,
    CAST(dim_eoy_enroll_attr_key int,
    CAST(dim_eoy_student_grade_key int,
    CAST(dim_curr_student_grade_key int,
    CAST(dim_eoy_section_group_key int,
    CAST(dim_curr_section_group_key int,
    CAST(dim_offic_section_key int,
    CAST(dim_curr_offic_section_key int,
    CAST(outcome_int int,
    CAST(concat(assmt_date, '.000000-05:00') AS timestamp), 
    CAST(concat(sync_date, '.000000-05:00') AS timestamp),
    CAST(outcome_float float,
    CAST(assmt_instance_sid int),
    CAST(assmt_instance_rank int),
*/
UPDATE edware_lz.fact_assmt_outcome
SET part_key = '-9999'
WHERE part_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET active_flag = '0'
WHERE active_flag = '';

UPDATE edware_lz.fact_assmt_outcome
SET active_flag = '0'
WHERE active_flag = 'f';

UPDATE edware_lz.fact_assmt_outcome
SET active_flag = '1'
WHERE active_flag = 't';

UPDATE edware_lz.fact_assmt_outcome
SET dim_student_key = '-9999'
WHERE dim_student_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET eternal_student_sid = '-9999'
WHERE eternal_student_sid = '';

UPDATE edware_lz.fact_assmt_outcome
SET year_sid = '-9999'
WHERE year_sid = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_staff_key = '-9999'
WHERE dim_assmt_staff_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_outcome_type_key = '-9999'
WHERE dim_assmt_outcome_type_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_period_key = '-9999'
WHERE dim_assmt_period_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_grade_key = '-9999'
WHERE dim_assmt_grade_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_time_key = '-9999'
WHERE dim_assmt_time_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_sync_time_key = '-9999'
WHERE dim_assmt_sync_time_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_perf_level_key = '-9999'
WHERE dim_perf_level_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_custom_perf_level_key = '-9999'
WHERE dim_custom_perf_level_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_assmt_institution_key = '-9999'
WHERE dim_assmt_institution_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_curr_institution_key = '-9999'
WHERE dim_curr_institution_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_eoy_institution_key = '-9999'
WHERE dim_eoy_institution_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_curr_enroll_attr_key = '-9999'
WHERE dim_curr_enroll_attr_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_eoy_enroll_attr_key = '-9999'
WHERE dim_eoy_enroll_attr_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_eoy_student_grade_key = '-9999'
WHERE dim_eoy_student_grade_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_curr_student_grade_key = '-9999'
WHERE dim_curr_student_grade_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_eoy_section_group_key = '-9999'
WHERE dim_eoy_section_group_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_curr_section_group_key = '-9999'
WHERE dim_curr_section_group_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_offic_section_key = '-9999'
WHERE dim_offic_section_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET dim_curr_offic_section_key = '-9999'
WHERE dim_curr_offic_section_key = '';

UPDATE edware_lz.fact_assmt_outcome
SET outcome_int = '-9999'
WHERE outcome_int = '';

UPDATE edware_lz.fact_assmt_outcome
SET outcome_float = '-9999.99'
WHERE outcome_float = '';

UPDATE edware_lz.fact_assmt_outcome
SET assmt_instance_sid = '-9999'
WHERE assmt_instance_sid = '';

UPDATE edware_lz.fact_assmt_outcome
SET assmt_instance_rank = '-9999'
WHERE assmt_instance_rank = '';

UPDATE edware_lz.fact_assmt_outcome
SET assmt_date = '1970-01-01'
WHERE assmt_date = ''
OR assmt_date IS NULL;

UPDATE edware_lz.fact_assmt_outcome
SET sync_date = '1970-01-01'
WHERE sync_date = ''
OR sync_date IS NULL;

select now() as _fao_load_start_;
DELETE FROM edware.fact_assmt_outcome;
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
    CAST(outcome_int AS bigint),
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
FROM edware_lz.fact_assmt_outcome
;
select now() as _fao_load_end_;

--clearing out fao's with missing dimension keys.
/*
DELETE FROM edware.fact_assmt_outcome
WHERE dim_student_key not in (select dim_student_key from edware.dim_student);

DELETE FROM edware.fact_assmt_outcome
WHERE dim_assmt_outcome_type_key not in (select dim_assmt_outcome_type_key from edware.dim_assmt_outcome_type);
*/
SELECT count(*) AS _lz_count_ FROM edware_lz.fact_assmt_outcome;
SELECT count(*) AS _load_count_ FROM edware.fact_assmt_outcome;

--PASS... no data
DELETE FROM edware.etl_date;
INSERT INTO edware.etl_date
(
    etl_date_key
,   etl_date_code
,   etl_date_name
,   academic_year_code
,   etl_lastrun_timestamp
,   etl_currentrun_starttime
,   etl_currentrun_endtime
)
SELECT
    CAST(etl_date_key AS int),
    CAST(etl_date_code AS varchar(32)),
    CAST(etl_date_name AS varchar(255)),
    CAST(academic_year_code AS varchar(10)),
    CAST(etl_lastrun_timestamp AS timestamp),
    CAST(etl_currentrun_starttime AS timestamp),
    CAST(etl_currentrun_endtime AS timestamp)
FROM edware_lz.etl_date
;

SELECT count(*) AS _lz_count_ FROM edware_lz.etl_date;
SELECT count(*) AS _load_count_ FROM edware.etl_date;

--PASS
DELETE FROM edware.mv_academic_year_period;
INSERT INTO edware.mv_academic_year_period
(
    mv_academic_year_period_key
,   school_sid
,   state_code
,   municipality_sid
,   district_sid
,   dim_institution_key
,   status_code
,   demo_flag
,   dim_period_key
,   academic_year_code
,   academic_year_name
,   academic_year_abbrev
,   period_code
,   period_abbrev
,   period_order
,   assmt_code
,   assmt_name
,   assmt_abbrev
,   assmt_version_code
,   assmt_version_name
,   assmt_version_abbrev
,   assmt_version_rank
,   daot_hier_level
,   daot_hier_level_1_code
,   daot_hier_level_2_code
,   daot_hier_level_3_code
,   daot_hier_level_4_code
,   daot_hier_level_5_code
,   calendar_date
,   part_key
,   create_date 
,   mod_date
,   daot_hier_level_code
,   daot_measure_type_code
,   daot_measure_type_name
,   account_sid
,   year_sid
,   assmt_course_code
,   assmt_course_name
,   daot_hier_level_1_abbrev
,   daot_hier_level_2_abbrev
,   daot_hier_level_3_abbrev
,   daot_hier_level_4_abbrev
,   daot_hier_level_5_abbrev
,   performance_level_flag
,   assmt_custom_id_name
)
SELECT 
    CAST(mv_academic_year_period_key AS int),
    CAST(school_sid AS int),
    CAST(state_code AS varchar(255)),
    CAST(municipality_sid AS int),
    CAST(district_sid AS int),
    CAST(dim_institution_key AS int),
    CAST(status_code AS varchar(255)),
    CAST(demo_flag AS boolean),
    CAST(dim_period_key AS int),
    CAST(academic_year_code AS varchar(255)),
    CAST(academic_year_name AS varchar(255)),
    CAST(academic_year_abbrev AS varchar(255)),
    CAST(period_code AS varchar(255)),
    CAST(period_abbrev AS varchar(255)),
    CAST(period_order AS int),
    CAST(assmt_code AS varchar(255)),
    CAST(assmt_name AS varchar(255)),
    CAST(assmt_abbrev AS varchar(255)),
    CAST(assmt_version_code AS varchar(255)),
    CAST(assmt_version_name AS varchar(255)),
    CAST(assmt_version_abbrev AS varchar(255)),
    CAST(assmt_version_rank AS int),
    CAST(daot_hier_level AS int),
    CAST(daot_hier_level_1_code AS varchar(255)),
    CAST(daot_hier_level_2_code AS varchar(255)),
    CAST(daot_hier_level_3_code AS varchar(255)),
    CAST(daot_hier_level_4_code AS varchar(255)),
    CAST(daot_hier_level_5_code AS varchar(255)),
    CAST(calendar_date AS date),
    CAST(part_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(daot_hier_level_code AS varchar(255)),
    CAST(daot_measure_type_code AS varchar(255)),
    CAST(daot_measure_type_name AS varchar(255)),
    CAST(account_sid AS int),
    CAST(year_sid AS int),
    CAST(assmt_course_code AS varchar(255)),
    CAST(assmt_course_name AS varchar(255)),
    CAST(daot_hier_level_1_abbrev AS varchar(255)),
    CAST(daot_hier_level_2_abbrev AS varchar(255)),
    CAST(daot_hier_level_3_abbrev AS varchar(255)),
    CAST(daot_hier_level_4_abbrev AS varchar(255)),
    CAST(daot_hier_level_5_abbrev AS varchar(255)),
    CAST(performance_level_flag AS boolean),
    CAST(assmt_custom_id_name AS varchar(255))
FROM edware_lz.mv_academic_year_period
;

SELECT count(*) AS _lz_count_ FROM edware_lz.mv_academic_year_period;
SELECT count(*) AS _load_count_ FROM edware.mv_academic_year_period;

--PASS... no data
DELETE FROM edware.mv_amp_user_inst;
INSERT INTO edware.mv_amp_user_inst
(
    mv_amp_user_inst_key
,   amp_user_sid
,   inst_sid
,   inst_type_sid
,   inst_name
,   account_sid
,   spa_flag
,   pii_flag
,   home_flag
,   part_key
,   create_date
,   mod_date
)
SELECT 
    CAST(mv_amp_user_inst_key AS int),
    CAST(amp_user_sid AS int),
    CAST(inst_sid AS int),
    CAST(inst_type_sid AS int),
    CAST(inst_name AS varchar(255)),
    CAST(account_sid AS int),
    CAST(spa_flag AS boolean),
    CAST(pii_flag AS boolean),
    CAST(home_flag AS boolean),
    CAST(part_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp)
FROM edware_lz.mv_amp_user_inst
;

SELECT count(*) AS _lz_count_ FROM edware_lz.mv_amp_user_inst;
SELECT count(*) AS _load_count_ FROM edware.mv_amp_user_inst;

--PASS
DELETE FROM edware.mv_amp_user_assmt;
INSERT INTO edware.mv_amp_user_assmt
(
    mv_amp_user_assmt_key
,   amp_user_sid
,   assmt_code
,   spa_flag
,   part_key
,   create_date
,   mod_date
)
SELECT
    CAST(mv_amp_user_assmt_key AS int),
    CAST(amp_user_sid AS int),
    CAST(assmt_code AS varchar(255)),
    CAST(spa_flag AS boolean),
    CAST(part_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp)
FROM edware_lz.mv_amp_user_assmt
;

SELECT count(*) AS _lz_count_ FROM edware_lz.mv_amp_user_assmt;
SELECT count(*) AS _load_count_ FROM edware.mv_amp_user_assmt;

--PASS... no data
DELETE FROM edware.mv_amp_user_program;
INSERT INTO edware.mv_amp_user_program
(
    mv_amp_user_program_key
,   amp_user_sid
,   program_sid
,   is_admin_enabled
,   is_reporting_enabled
,   is_pii_enabled
,   is_trad_view_enabled
,   part_key
,   create_date
,   mod_date
)
SELECT 
    CAST(mv_amp_user_program_key AS int),
    CAST(amp_user_sid AS int),
    CAST(program_sid AS int),
    CAST(is_admin_enabled AS boolean),
    CAST(is_reporting_enabled AS boolean),
    CAST(is_pii_enabled AS boolean),
    CAST(is_trad_view_enabled AS boolean),
    CAST(part_key AS int),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp)
FROM edware_lz.mv_amp_user_program
;

SELECT count(*) AS _lz_count_ FROM edware_lz.mv_amp_user_program;
SELECT count(*) AS _load_count_ FROM edware.mv_amp_user_program;

--PASS... no data
DELETE FROM edware.executionlog;
INSERT INTO edware.executionlog
(
    instancename
,   reportid
,   user_name
,   requesttype
,   format 
,   parameters
,   time_begin
,   time_end
,   time_data_retrieval
,   time_processing
,   time_rendering
,   source
,   status
,   bytecount
,   rowcount
,   path
,   name
,   app
)
SELECT 
    CAST(instancename AS varchar(50)),
    CAST(reportid AS varchar(50)),
    CAST(user_name AS varchar(260)),
    CAST(requesttype AS int),
    CAST(format AS varchar(50)),
    CAST(parameters AS varchar(4000)),
    CAST(time_begin AS timestamp),
    CAST(time_end AS timestamp),
    CAST(time_data_retrieval AS int),
    CAST(time_processing AS int),
    CAST(time_rendering AS int),
    CAST(source AS int),
    CAST(status AS varchar(50)),
    CAST(bytecount AS int),
    CAST(rowcount AS int),
    CAST(path AS varchar(500)),
    CAST(name AS varchar(500)),
    CAST(app AS varchar(50))
FROM edware_lz.executionlog
;

SELECT count(*) AS _lz_count_ FROM edware_lz.executionlog;
SELECT count(*) AS _load_count_ FROM edware.executionlog;

--PASS
DELETE FROM edware.pm_periods;
INSERT INTO edware.pm_periods
(
    pm_periods_key
,   eternal_student_sid
,   assmt_code
,   assmt_version_code
,   academic_year_code
,   period_code
,   sync_time
,   assmt_time
,   create_date
,   mod_date
,   part_key
)
SELECT 
    CAST(pm_periods_key AS int),
    CAST(eternal_student_sid AS int),
    CAST(assmt_code AS varchar(255)),
    CAST(assmt_version_code AS varchar(255)),
    CAST(academic_year_code AS varchar(255)),
    CAST(period_code AS varchar(255)),
    CAST(sync_time AS timestamp),
    CAST(assmt_time AS timestamp),
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int)
FROM edware_lz.pm_periods
;

SELECT count(*) AS _lz_count_ FROM edware_lz.pm_periods;
SELECT count(*) AS _load_count_ FROM edware.pm_periods;






