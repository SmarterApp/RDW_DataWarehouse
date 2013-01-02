-- rpt_fqa_lz_ddl.sql
-- create rpt lz tables
SET search_path = edware_lz;

CREATE TABLE edware_lz.dim_subject
(
    dim_subject_key varchar(10) NOT NULL,
    subject_code varchar(255),
    subject_name varchar(255),
    is_summary_flag varchar(10),
    hs_required_credits varchar(10),
    custom_id_1_code varchar(255),
    custom_id_1_type_code varchar(255),
    custom_id_2_code varchar(255),
    custom_id_2_type_code varchar(255),
    custom_id_3_code varchar(255),
    custom_id_3_type_code varchar(255),
    custom_id_4_code varchar(255),
    custom_id_4_type_code varchar(255),
    custom_id_5_code varchar(255),
    custom_id_5_type_code varchar(255),
    dim_parent_subject_key varchar(10),
    subject_level varchar(10),
    subject_group_code varchar(255),
    subject_group_name varchar(255),
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_staff
(
    dim_staff_key varchar(10) NOT NULL,
    staff_sid varchar(10) NOT NULL,
    school_year_sid varchar(10) NOT NULL,
    amp_user_sid varchar(10) NOT NULL,
    amp_user_handle varchar(255) NOT NULL,
    first_name varchar(255),
    middle_name varchar(255),
    last_name varchar(255),
    dob varchar(30),
    phone varchar(255),
    email varchar(255),
    custom_id_1_code varchar(255),
    custom_id_1_type_code varchar(255),
    custom_id_2_code varchar(255),
    custom_id_2_type_code varchar(255),
    custom_id_3_code varchar(255),
    custom_id_3_type_code varchar(255),
    custom_id_4_code varchar(255),
    custom_id_4_type_code varchar(255),
    custom_id_5_code varchar(255),
    custom_id_5_type_code varchar(255),
    status_code varchar(255) NOT NULL,
    demo_flag varchar(10) NOT NULL,
    spa_pii_flag varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL,
    staff_type_code varchar(255),
    staff_type_name varchar(255),
    staff_role_code varchar(255),
    staff_role_name varchar(255),
    opt_out varchar(10)
)
;

CREATE TABLE edware_lz.dim_staff_group
(
    dim_staff_group_key varchar(10) NOT NULL,
    integerized_staff_keys varchar(255),
    staff_group_name varchar(255),
    staff_group_type varchar(255),
    primary_staff_key varchar(10),
    group_start_time varchar(30),
    group_end_time varchar(30),
    active_flag varchar(10),
    staff_group_code varchar(255),
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_section
(
    dim_section_key varchar(10) NOT NULL,
    section_sid varchar(10) NOT NULL,
    section_name varchar(255) NOT NULL,
    display_name varchar(255),
    course_code varchar(255),
    course_name varchar(255),
    primary_subject_key varchar(10),
    duplicate_offering_flag varchar(10),
    section_type_code varchar(255) NOT NULL,
    section_subtype_code varchar(255) NOT NULL,
    avg_student_grade_level_code varchar(255),
    updated_flag varchar(10),
    course_credits varchar(10),
    marking_period_max varchar(10),
    elective_flag varchar(10),
    course_level_code varchar(255),
    course_site_code varchar(255),
    course_site_name varchar(255),
    dim_parent_section_key varchar(10),
    sif_student_group_type varchar(255),
    sif_student_group_type_attribute varchar(255),
    student_group_start_time varchar(30),
    student_group_end_time varchar(30),
    active_flag varchar(10),
    completed_flag varchar(10),
    dim_instructional_content_group_key varchar(10),
    custom_id_1_code varchar(255),
    custom_id_1_type_code varchar(255),
    custom_id_2_code varchar(255),
    custom_id_2_type_code varchar(255),
    custom_id_3_code varchar(255),
    custom_id_3_type_code varchar(255),
    custom_id_4_code varchar(255),
    custom_id_4_type_code varchar(255),
    custom_id_5_code varchar(255),
    custom_id_5_type_code varchar(255),
    staff_1_sid varchar(10),
    staff_1_is_primary varchar(10),
    staff_1_role_desc varchar(255),
    staff_2_sid varchar(10),
    staff_2_is_primary varchar(10),
    staff_2_role_desc varchar(255),
    staff_3_sid varchar(10),
    staff_3_is_primary varchar(10),
    staff_3_role_desc varchar(255),
    staff_4_sid varchar(10),
    staff_4_is_primary varchar(10),
    staff_4_role_desc varchar(255),
    managed_by_code varchar(255),
    managed_by_name varchar(255),
    status_code varchar(255) NOT NULL,
    demo_flag varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL,
    course_sid varchar(10),
    subject_sid varchar(10),
    subject_code varchar(255),
    subject_name varchar(255)
)
;

CREATE TABLE edware_lz.dim_section_group
(
    dim_section_group_key varchar(10) NOT NULL,
    integerized_section_keys varchar(255),
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.map_sect_group_sect
(
    map_sect_group_sect_key varchar(10) NOT NULL,
    dim_section_group_key varchar(10) NOT NULL,
    dim_section_key varchar(10) NOT NULL,
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.map_staff_group_sect
(
    map_staff_group_sect_key varchar(10) NOT NULL,
    dim_staff_group_key varchar(10) NOT NULL,
    dim_section_key varchar(10) NOT NULL,
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_enroll_attr
(
    dim_enroll_attr_key varchar(10) NOT NULL,
    sped_environ_code varchar(255) NOT NULL,
    sped_environ_name varchar(255) NOT NULL,
    s504_status_code varchar(255) NOT NULL,
    s504_status_name varchar(255) NOT NULL,
    disability_status_code varchar(255) NOT NULL,
    disability_status_name varchar(255) NOT NULL,
    specific_disability_code varchar(255) NOT NULL,
    specific_disability_name varchar(255) NOT NULL,
    ell_status_code varchar(255) NOT NULL,
    ell_status_name varchar(255) NOT NULL,
    home_lang_code varchar(255) NOT NULL,
    home_lang_name varchar(255) NOT NULL,
    ethnicity_code varchar(255) NOT NULL,
    ethnicity_name varchar(255) NOT NULL,
    housing_status_code varchar(255) NOT NULL,
    housing_status_name varchar(255) NOT NULL,
    meal_status_code varchar(255) NOT NULL,
    meal_status_name varchar(255) NOT NULL,
    econ_disadvantage_code varchar(255) NOT NULL,
    econ_disadvantage_name varchar(255) NOT NULL,
    title_1_status_code varchar(255) NOT NULL,
    title_1_status_name varchar(255) NOT NULL,
    migrant_status_code varchar(255) NOT NULL,
    migrant_status_name varchar(255) NOT NULL,
    alt_assmt_code varchar(255) NOT NULL,
    alt_assmt_name varchar(255) NOT NULL,
    english_prof_code varchar(255) NOT NULL,
    english_prof_name varchar(255) NOT NULL,
    is_classed_code varchar(255) NOT NULL,
    is_classed_name varchar(255) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL,
    ethnicity_abbrev varchar(255),
    sped_environ_abbrev varchar(255),
    disability_status_abbrev varchar(255),
    specific_disability_abbrev varchar(255),
    s504_status_abbrev varchar(255),
    econ_disadvantage_abbrev varchar(255),
    meal_status_abbrev varchar(255),
    title_1_status_abbrev varchar(255),
    migrant_status_abbrev varchar(255),
    english_prof_abbrev varchar(255),
    ell_status_abbrev varchar(255),
    home_lang_abbrev varchar(255),
    alt_assmt_abbrev varchar(255),
    housing_status_abbrev varchar(255)
)
;

CREATE TABLE edware_lz.dim_term
(
    dim_term_key varchar(10) NOT NULL,
    school_year_sid varchar(10),
    term_code varchar(255),
    term_name varchar(255),
    current_term_flag varchar(10),
    summer_term_flag varchar(10),
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_period
(
    dim_period_key varchar(10) NOT NULL,
    assmt_code varchar(255) NOT NULL,
    academic_year_name varchar(255) NOT NULL,
    academic_year_abbrev varchar(255),
    academic_year_code varchar(255) NOT NULL,
    period_code varchar(255) NOT NULL,
    period_abbrev varchar(255),
    period_order varchar(10) NOT NULL,
    period_start_date varchar(30),
    period_end_date varchar(30),
    current_year_flag varchar(10),
    previous_year_flag varchar(10),
    current_period_flag varchar(10),
    previous_period_flag varchar(10),
    period_name varchar(255) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_perf_level
(
    dim_perf_level_key varchar(10) NOT NULL,
    level_order varchar(10) NOT NULL,
    level_type_code varchar(255) NOT NULL,
    level_type_name varchar(255) NOT NULL,
    general_level_code varchar(255),
    general_level_name varchar(255),
    measure_type_specific_level_code varchar(255),
    measure_type_specific_level_name varchar(255),
    measure_specific_level_code varchar(255) NOT NULL,
    measure_specific_level_name varchar(255) NOT NULL,
    level_code varchar(255),
    level_name varchar(255),
    level_order_name varchar(255),
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL,
    account_sid varchar(10) DEFAULT 0
)
;

CREATE TABLE edware_lz.dim_assmt_subject
(
    dim_assmt_subject_key varchar(10) NOT NULL,
    assmt_subject_code varchar(255),
    assmt_subject_name varchar(255),
    custom_id_1_code varchar(255),
    custom_id_1_type_code varchar(255),
    custom_id_2_code varchar(255),
    custom_id_2_type_code varchar(255),
    custom_id_3_code varchar(255),
    custom_id_3_type_code varchar(255),
    custom_id_4_code varchar(255),
    custom_id_4_type_code varchar(255),
    custom_id_5_code varchar(255),
    custom_id_5_type_code varchar(255),
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.map_assmt_subj_subj
(
    map_assmt_subj_subj_key varchar(10) NOT NULL,
    dim_assmt_subject_key varchar(10) NOT NULL,
    dim_subject_key varchar(10) NOT NULL,
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

--drop table edware_lz.dim_grade;
CREATE TABLE edware_lz.dim_grade
(
    dim_grade_key varchar(10) NOT NULL,
    grade_level_sid varchar(10) NOT NULL,
    grade_level_name varchar(255) NOT NULL,
    grade_band_code varchar(255),
    grade_band_name varchar(255),
    grade_level_order varchar(10) NOT NULL,
    updated_flag varchar(10) DEFAULT 0,
    grade_band_flag varchar(10) DEFAULT 0,
    grade_band_min varchar(10),
    grade_band_max varchar(10),
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_time
(
    dim_time_key varchar(10) NOT NULL,
    calendar_date varchar(30) NOT NULL,
    day_of_year varchar(10) NOT NULL,
    day_of_month varchar(10) NOT NULL,
    day_of_week varchar(10) NOT NULL,
    day_name varchar(255) NOT NULL,
    week_of_year varchar(10) NOT NULL,
    week_of_month varchar(10) NOT NULL,
    week_ending varchar(30) NOT NULL,
    month_of_year varchar(10) NOT NULL,
    month_name varchar(255) NOT NULL,
    quarter_of_year varchar(10) NOT NULL,
    year varchar(10) NOT NULL,
    is_holiday varchar(10) NOT NULL,
    holiday_name varchar(255) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_institution
(
    dim_institution_key varchar(10) NOT NULL,
    academic_year_code varchar(255) NOT NULL,
    academic_year_name varchar(255) NOT NULL,
    current_acad_year_flag varchar(10) NOT NULL,
    grade_config_code varchar(255),
    grade_config_name varchar(255),
    school_year_sid varchar(10) NOT NULL,
    school_sid varchar(10) NOT NULL,
    school_name varchar(255) NOT NULL,
    school_phone varchar(255),
    school_address_1 varchar(255),
    school_address_2 varchar(255),
    school_city varchar(255),
    school_zip_code varchar(255),
    district_sid varchar(10) NOT NULL,
    district_name varchar(255) NOT NULL,
    municipality_sid varchar(10),
    municipality_name varchar(255),
    account_sid varchar(10) NOT NULL,
    account_name varchar(255) NOT NULL,
    state_sid varchar(10) NOT NULL,
    state_code varchar(255) NOT NULL,
    state_name varchar(255) NOT NULL,
    country_sid varchar(10) NOT NULL,
    country_name varchar(255) NOT NULL,
    location_1_code varchar(255),
    location_1_name varchar(255),
    location_2_code varchar(255),
    location_2_name varchar(255),
    location_3_code varchar(255),
    location_3_name varchar(255),
    location_4_code varchar(255),
    location_4_name varchar(255),
    location_5_code varchar(255),
    location_5_name varchar(255),
    location_1_type_code varchar(255),
    location_1_type_name varchar(255),
    location_2_type_code varchar(255),
    location_2_type_name varchar(255),
    location_3_type_code varchar(255),
    location_3_type_name varchar(255),
    location_4_type_code varchar(255),
    location_4_type_name varchar(255),
    location_5_type_code varchar(255),
    location_5_type_name varchar(255),
    school_open_date varchar(30),
    school_years_open varchar(10),
    title_1_flag varchar(10),
    reading_first_flag varchar(10),
    url varchar(255),
    custom_id_1_code varchar(255),
    custom_id_1_type_code varchar(255),
    custom_id_2_code varchar(255),
    custom_id_2_type_code varchar(255),
    custom_id_3_code varchar(255),
    custom_id_3_type_code varchar(255),
    custom_id_4_code varchar(255),
    custom_id_4_type_code varchar(255),
    custom_id_5_code varchar(255),
    custom_id_5_type_code varchar(255),
    dim_curr_institution_key varchar(10),
    status_code varchar(255) NOT NULL,
    demo_flag varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_inst_group
(
    dim_inst_group_key varchar(10) NOT NULL,
    parent_inst_group_key varchar(10) NOT NULL,
    inst_group_name varchar(255) NOT NULL,
    inst_group_type_name varchar(255) NOT NULL,
    account_sid varchar(10),
    account_name varchar(255),
    sif_inst_group_type varchar(255),
    sif_inst_group_type_attribute varchar(255),
    group_start_time varchar(30),
    group_end_time varchar(30),
    status_code varchar(255) NOT NULL,
    address_1 varchar(255),
    address_2 varchar(255),
    city varchar(255),
    zip_code varchar(255),
    state_sid varchar(10),
    state_code varchar(255),
    state_name varchar(255),
    phone varchar(255),
    url varchar(255),
    managed_by_code varchar(255),
    managed_by_name varchar(255),
    is_internal varchar(10),
    is_funding_source varchar(10),
    is_study varchar(10),
    inst_group_code varchar(255) NOT NULL,
    inst_group_type_code varchar(255) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.map_inst_group_inst
(
    map_inst_group_inst_key varchar(10) NOT NULL,
    dim_inst_group_key varchar(10) NOT NULL,
    dim_institution_key varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.dim_student
(
    dim_student_key varchar(10) NOT NULL,
    student_sid varchar(10) NOT NULL,
    eternal_student_sid varchar(10) NOT NULL,
    first_name varchar(255),
    middle_name varchar(255),
    last_name varchar(255),
    suffix varchar(255),
    dob varchar(30),
    email varchar(255),
    home_phone varchar(255),
    place_of_birth_code varchar(255),
    place_of_birth_name varchar(255),
    gender_code varchar(255),
    gender_name varchar(255),
    grad_cohort_year_code varchar(255),
    grad_cohort_year_name varchar(255),
    age_as_of_curr_year varchar(10),
    status_code varchar(255) NOT NULL,
    demo_flag varchar(10) NOT NULL,
    custom_id_1_code varchar(255),
    custom_id_1_type_code varchar(255),
    custom_id_2_code varchar(255),
    custom_id_2_type_code varchar(255),
    custom_id_3_code varchar(255),
    custom_id_3_type_code varchar(255),
    custom_id_4_code varchar(255),
    custom_id_4_type_code varchar(255),
    custom_id_5_code varchar(255),
    custom_id_5_type_code varchar(255),
    source_create_date varchar(30),
    source_mod_date varchar(30),
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL,
    inst_sid varchar(10) NOT NULL,
    year_sid varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.map_staff_group_staff
(
    map_staff_group_staff_key varchar(10) NOT NULL,
    dim_staff_group_key varchar(10) NOT NULL,
    dim_staff_key varchar(10) NOT NULL,
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;

CREATE TABLE edware_lz.fact_enroll
(
    fact_enroll_key varchar(10) NOT NULL,
    part_key varchar(10) NOT NULL,
    dim_institution_key varchar(10) NOT NULL,
    dim_student_key varchar(10) NOT NULL,
    dim_grade_key varchar(10) NOT NULL,
    dim_section_key varchar(10) NOT NULL,
    dim_term_key varchar(10),
    dim_teacher_staff_key varchar(10) NOT NULL,
    dim_enroll_attr_key varchar(10) NOT NULL,
    dim_inst_admit_time_key varchar(10) NOT NULL,
    dim_inst_disc_time_key varchar(10) NOT NULL,
    dim_sect_admit_time_key varchar(10) NOT NULL,
    dim_sect_disc_time_key varchar(10) NOT NULL,
    enrolled_in_inst_flag varchar(10) NOT NULL,
    enrolled_in_sect_flag varchar(10) NOT NULL,
    student_sid varchar(10) NOT NULL,
    eternal_student_sid varchar(10) NOT NULL,
    section_sid varchar(10) NOT NULL,
    year_sid varchar(10) NOT NULL,
    is_reporting_classe varchar(10) NOT NULL,
    section_type_code varchar(255) NOT NULL,
    section_subtype_code varchar(255) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL
)
;
--DROP TABLE edware_lz.dim_assmt_outcome_type;
CREATE TABLE edware_lz.dim_assmt_outcome_type
(
    dim_assmt_outcome_type_key varchar(10) NOT NULL,
    assmt_code varchar(255) NOT NULL,
    assmt_name varchar(255) NOT NULL,
    assmt_abbrev varchar(255),
    assmt_version_code varchar(255) NOT NULL,
    assmt_version_name varchar(255) NOT NULL,
    assmt_version_abbrev varchar(255),
    assmt_version_rank varchar(10) NOT NULL,
    daot_measure_type_code varchar(255) NOT NULL,
    daot_measure_type_name varchar(255) NOT NULL,
    daot_measure_type_rank varchar(10) NOT NULL,
    daot_hier_level varchar(10) NOT NULL,
    daot_hier_level_code varchar(255) NOT NULL,
    daot_hier_level_name varchar(255) NOT NULL,
    daot_hier_level_rank varchar(10) NOT NULL,
    daot_hier_level_1_code varchar(255) NOT NULL,
    daot_hier_level_1_name varchar(255) NOT NULL,
    daot_hier_level_1_abbrev varchar(255),
    daot_hier_level_2_code varchar(255) NOT NULL,
    daot_hier_level_2_name varchar(255) NOT NULL,
    daot_hier_level_2_abbrev varchar(255),
    daot_hier_level_3_code varchar(255) NOT NULL,
    daot_hier_level_3_name varchar(255) NOT NULL,
    daot_hier_level_3_abbrev varchar(255),
    daot_hier_level_4_code varchar(255) NOT NULL,
    daot_hier_level_4_name varchar(255) NOT NULL,
    daot_hier_level_4_abbrev varchar(255),
    daot_hier_level_5_code varchar(255) NOT NULL,
    daot_hier_level_5_name varchar(255) NOT NULL,
    daot_hier_level_5_abbrev varchar(255),
    performance_level_flag varchar(20) NOT NULL,
    performance_level_type_code varchar(255) NOT NULL,
    outcome_int_flag varchar(20) NOT NULL,
    outcome_int_code varchar(255) NOT NULL,
    outcome_int_name varchar(255) NOT NULL,
    outcome_int_abbrev varchar(255),
    outcome_float_flag varchar(20) NOT NULL,
    outcome_float_code varchar(255) NOT NULL,
    outcome_float_name varchar(255) NOT NULL,
    outcome_float_abbrev varchar(255),
    outcome_string_flag varchar(20) NOT NULL,
    outcome_string_code varchar(255) NOT NULL,
    outcome_string_name varchar(255) NOT NULL,
    outcome_string_abbrev varchar(255),
    outcome_rank varchar(30) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    part_key varchar(10) NOT NULL,
    pg_by_grade_flag varchar(20),
    assmt_course_code varchar(255),
    assmt_course_name varchar(255)
)
;

CREATE TABLE edware_lz.fact_assmt_outcome
(
    fact_assmt_outcome_key varchar(10) NOT NULL,
    part_key varchar(10) NOT NULL,
    active_flag varchar(10) NOT NULL,
    dim_student_key varchar(10) NOT NULL,
    eternal_student_sid varchar(10) NOT NULL,
    year_sid varchar(10) NOT NULL,
    dim_assmt_staff_key varchar(10) NOT NULL,
    dim_assmt_outcome_type_key varchar(10) NOT NULL,
    dim_assmt_period_key varchar(10) NOT NULL,
    dim_assmt_grade_key varchar(10) NOT NULL,
    dim_assmt_time_key varchar(10) NOT NULL,
    dim_assmt_sync_time_key varchar(10) NOT NULL,
    dim_perf_level_key varchar(10) NOT NULL,
    dim_custom_perf_level_key varchar(10),
    dim_assmt_institution_key varchar(10) NOT NULL,
    dim_curr_institution_key varchar(10),
    dim_eoy_institution_key varchar(10),
    dim_curr_enroll_attr_key varchar(10),
    dim_eoy_enroll_attr_key varchar(10),
    dim_eoy_student_grade_key varchar(10),
    dim_curr_student_grade_key varchar(10),
    dim_eoy_section_group_key varchar(10),
    dim_curr_section_group_key varchar(10),
    dim_offic_section_key varchar(10),
    dim_curr_offic_section_key varchar(10),
    outcome_int varchar(10),
    outcome_string varchar(255),
    outcome_float varchar(16),
    assmt_date varchar(30),
    sync_date varchar(30),
    assmt_instance_sid varchar(10) NOT NULL,
    assmt_instance_rank varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    assmt_custom_id_code varchar(255),
    assmt_custom_id_name varchar(255)
)
;

CREATE TABLE edware_lz.etl_date
(
    etl_date_key varchar(10) NOT NULL,
    etl_date_code varchar(32) NOT NULL,
    etl_date_name varchar(255),
    academic_year_code varchar(10) NOT NULL,
    etl_lastrun_timestamp varchar(30),
    etl_currentrun_starttime varchar(30),
    etl_currentrun_endtime varchar(30)
);

CREATE TABLE edware_lz.mv_academic_year_period
(
    mv_academic_year_period_key varchar(10) NOT NULL,
    school_sid varchar(10) NOT NULL,
    state_code varchar(255) NOT NULL,
    municipality_sid varchar(10),
    district_sid varchar(10) NOT NULL,
    dim_institution_key varchar(10) NOT NULL,
    status_code varchar(255) NOT NULL,
    demo_flag varchar(10) NOT NULL,
    dim_period_key varchar(10) NOT NULL,
    academic_year_code varchar(255) NOT NULL,
    academic_year_name varchar(255) NOT NULL,
    academic_year_abbrev varchar(255),
    period_code varchar(255) NOT NULL,
    period_abbrev varchar(255),
    period_order varchar(10) NOT NULL,
    assmt_code varchar(255) NOT NULL,
    assmt_name varchar(255) NOT NULL,
    assmt_abbrev varchar(255),
    assmt_version_code varchar(255) NOT NULL,
    assmt_version_name varchar(255) NOT NULL,
    assmt_version_abbrev varchar(255),
    assmt_version_rank varchar(10) NOT NULL,
    daot_hier_level varchar(10) NOT NULL,
    daot_hier_level_1_code varchar(255) NOT NULL,
    daot_hier_level_2_code varchar(255) NOT NULL,
    daot_hier_level_3_code varchar(255) NOT NULL,
    daot_hier_level_4_code varchar(255) NOT NULL,
    daot_hier_level_5_code varchar(255) NOT NULL,
    calendar_date varchar(30),
    part_key varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL,
    daot_hier_level_code varchar(255),
    daot_measure_type_code varchar(255),
    daot_measure_type_name varchar(255),
    account_sid varchar(10),
    year_sid varchar(10),
    assmt_course_code varchar(255),
    assmt_course_name varchar(255),
    daot_hier_level_1_abbrev varchar(255),
    daot_hier_level_2_abbrev varchar(255),
    daot_hier_level_3_abbrev varchar(255),
    daot_hier_level_4_abbrev varchar(255),
    daot_hier_level_5_abbrev varchar(255),
    performance_level_flag varchar(10),
    assmt_custom_id_name varchar(255)
)
;

CREATE TABLE edware_lz.mv_amp_user_inst
(
    mv_amp_user_inst_key varchar(10) NOT NULL,
    amp_user_sid varchar(10) NOT NULL,
    inst_sid varchar(10) NOT NULL,
    inst_type_sid varchar(10) NOT NULL,
    inst_name varchar(255),
    account_sid varchar(10) NOT NULL,
    spa_flag varchar(10) NOT NULL,
    pii_flag varchar(10) NOT NULL,
    home_flag varchar(10) NOT NULL,
    part_key varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL
)
;

CREATE TABLE edware_lz.mv_amp_user_assmt
(
    mv_amp_user_assmt_key varchar(10) NOT NULL,
    amp_user_sid varchar(10) NOT NULL,
    assmt_code varchar(255) NOT NULL,
    spa_flag varchar(10) NOT NULL,
    part_key varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL
)
;

CREATE TABLE edware_lz.mv_amp_user_program
(
    mv_amp_user_program_key varchar(10) NOT NULL,
    amp_user_sid varchar(10) NOT NULL,
    program_sid varchar(10) NOT NULL,
    is_admin_enabled varchar(10),
    is_reporting_enabled varchar(10),
    is_pii_enabled varchar(10),
    is_trad_view_enabled varchar(10),
    part_key varchar(10) NOT NULL,
    create_date varchar(30) NOT NULL,
    mod_date varchar(30) NOT NULL
)
;

CREATE TABLE edware_lz.executionlog
(
    instancename varchar(50),
    reportid varchar(50),
    user_name varchar(260),
    requesttype varchar(10),
    format varchar(50),
    parameters varchar(4000),
    time_begin varchar(30),
    time_end varchar(30),
    time_data_retrieval varchar(10),
    time_processing varchar(10),
    time_rendering varchar(10),
    source varchar(10),
    status varchar(50),
    bytecount varchar(10),
    rowcount varchar(10),
    path varchar(500),
    name varchar(500),
    app varchar(50)
);


CREATE TABLE edware_lz.pm_periods
(
    pm_periods_key varchar(10) NOT NULL,
    eternal_student_sid varchar(10),
    assmt_code varchar(255),
    assmt_version_code varchar(255),
    academic_year_code varchar(255),
    period_code varchar(255),
    sync_time varchar(30),
    assmt_time varchar(30),
    create_date varchar(30),
    mod_date varchar(30),
    part_key varchar(10) NOT NULL
)
;