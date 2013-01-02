select distinct custom_id_1_code from edware_lz.dim_section;
select distinct cast(dim_instructional_content_group_key AS int) from edware_lz.dim_section;


select distinct cast(custom_id_1_type_code as int)
from edware_lz.dim_section
where custom_id_1_type_code = ''
limit 10;

SELECT
    CAST(dim_section_key AS int), 
    CAST(section_sid AS int),
    CAST(section_name AS varchar(255)),
    CAST(display_name AS varchar(255)),
    CAST(course_code AS varchar(255)),
    CAST(course_name AS varchar(255)),
    CAST(primary_subject_key AS int),
    CAST(duplicate_offering_flag AS boolean), --1
    CAST(section_type_code AS varchar(255)),
    CAST(section_subtype_code AS varchar(255)),
    CAST(avg_student_grade_level_code AS varchar(255)),
    CAST(updated_flag AS boolean), --2
    CAST(course_credits AS int),
    CAST(marking_period_max AS int),
    CAST(elective_flag AS boolean), --3
    CAST(course_level_code AS varchar(255)),
    CAST(course_site_code AS varchar(255)),
    CAST(course_site_name AS varchar(255)),
    CAST(dim_parent_section_key AS int),
    CAST(sif_student_group_type AS varchar(255)),
    CAST(sif_student_group_type_attribute AS varchar(255))/*,
    CAST(student_group_start_time AS date),
    CAST(student_group_end_time AS date),
    CAST(active_flag AS boolean), --4
    CAST(completed_flag AS boolean), --5
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
    CAST(staff_1_is_primary AS boolean), --6
    CAST(staff_1_role_desc AS varchar(255)),
    CAST(staff_2_sid AS int),
    CAST(staff_2_is_primary AS boolean), --7
    CAST(staff_2_role_desc AS varchar(255)),
    CAST(staff_3_sid AS int),
    CAST(staff_3_is_primary AS boolean),--8
    CAST(staff_3_role_desc AS varchar(255)),
    CAST(staff_4_sid AS int),
    CAST(staff_4_is_primary AS boolean), --9
    CAST(staff_4_role_desc AS varchar(255)),
    CAST(managed_by_code AS varchar(255)),
    CAST(managed_by_name AS varchar(255)),
    CAST(status_code AS varchar(255)),
    CAST(demo_flag AS boolean), --10
    CAST(create_date AS timestamp),
    CAST(mod_date AS timestamp),
    CAST(part_key AS int),
    CAST(course_sid AS int),
    CAST(subject_sid AS int),
    CAST(subject_code AS varchar(255)),
    CAST(subject_name AS varchar(255))--*/
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  CAST(student_group_start_time AS date)
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  student_group_start_time
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  CAST(student_group_end_time AS date)
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  student_group_end_time
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  CAST(section_sid AS int)
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  CAST(section_name AS varchar(255))
FROM edware_lz.dim_section
limit 10
;

SELECT DISTINCT  CAST(display_name AS varchar(255))
FROM edware_lz.dim_section
limit 10
;
SELECT DISTINCT  CAST(course_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(course_name AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(section_type_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(section_subtype_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(avg_student_grade_level_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(course_level_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(course_site_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(course_site_name AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(sif_student_group_type AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(sif_student_group_type_attribute AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_1_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_1_type_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_2_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_2_type_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_3_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_3_type_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_4_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_4_type_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_5_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(custom_id_5_type_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(staff_1_role_desc AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(staff_2_role_desc AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(staff_3_role_desc AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(staff_4_role_desc AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(managed_by_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(managed_by_name AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(status_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(subject_code AS varchar(255)) FROM edware_lz.dim_section limit 10;
SELECT DISTINCT  CAST(subject_name AS varchar(255)) FROM edware_lz.dim_section limit 10;
FROM edware_lz.dim_section
limit 10
;
