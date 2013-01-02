-- rpt_fqa_ddl.sql
-- create rpt tables
SET search_path = edware;

CREATE TABLE edware.dim_subject
(
    dim_subject_key int NOT NULL,
    subject_code varchar(255),
    subject_name varchar(255),
    is_summary_flag boolean,
    hs_required_credits int,
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
    dim_parent_subject_key int,
    subject_level int,
    subject_group_code varchar(255),
    subject_group_name varchar(255),
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_subject ADD CONSTRAINT dim_subject_pkey PRIMARY KEY (dim_subject_key); 

CREATE TABLE edware.dim_staff
(
    dim_staff_key int NOT NULL,
    staff_sid int NOT NULL,
    school_year_sid int NOT NULL,
    amp_user_sid int NOT NULL,
    amp_user_handle varchar(255) NOT NULL,
    first_name varchar(255),
    middle_name varchar(255),
    last_name varchar(255),
    dob date,
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
    demo_flag boolean NOT NULL,
    spa_pii_flag boolean NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL,
    staff_type_code varchar(255),
    staff_type_name varchar(255),
    staff_role_code varchar(255),
    staff_role_name varchar(255),
    opt_out boolean
)
;

ALTER TABLE edware.dim_staff ADD CONSTRAINT dim_staff_pkey PRIMARY KEY (dim_staff_key);

-- ALTER TABLE edware.dim_staff ADD CONSTRAINT dim_staff_nkey UNIQUE (staff_sid); 

CREATE TABLE edware.dim_staff_group
(
    dim_staff_group_key int NOT NULL,
    integerized_staff_keys varchar(255),
    staff_group_name varchar(255),
    staff_group_type varchar(255),
    primary_staff_key int,
    group_start_time date,
    group_end_time date,
    active_flag boolean,
    staff_group_code varchar(255),
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_staff_group ADD CONSTRAINT dim_staff_group_pkey PRIMARY KEY (dim_staff_group_key); 

CREATE TABLE edware.dim_section
(
    dim_section_key int NOT NULL,
    section_sid int NOT NULL,
    section_name varchar(255) NOT NULL,
    display_name varchar(255),
    course_code varchar(255),
    course_name varchar(255),
    primary_subject_key int,
    duplicate_offering_flag boolean,
    section_type_code varchar(255) NOT NULL,
    section_subtype_code varchar(255) NOT NULL,
    avg_student_grade_level_code varchar(255),
    updated_flag boolean,
    course_credits int,
    marking_period_max int,
    elective_flag boolean,
    course_level_code varchar(255),
    course_site_code varchar(255),
    course_site_name varchar(255),
    dim_parent_section_key int,
    sif_student_group_type varchar(255),
    sif_student_group_type_attribute varchar(255),
    student_group_start_time date,
    student_group_end_time date,
    active_flag boolean,
    completed_flag boolean,
    dim_instructional_content_group_key int,
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
    staff_1_sid int,
    staff_1_is_primary boolean,
    staff_1_role_desc varchar(255),
    staff_2_sid int,
    staff_2_is_primary boolean,
    staff_2_role_desc varchar(255),
    staff_3_sid int,
    staff_3_is_primary boolean,
    staff_3_role_desc varchar(255),
    staff_4_sid int,
    staff_4_is_primary boolean,
    staff_4_role_desc varchar(255),
    managed_by_code varchar(255),
    managed_by_name varchar(255),
    status_code varchar(255) NOT NULL,
    demo_flag boolean NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL,
    course_sid int,
    subject_sid int,
    subject_code varchar(255),
    subject_name varchar(255)
)
;

ALTER TABLE edware.dim_section ADD CONSTRAINT dim_section_pkey PRIMARY KEY (dim_section_key); 
-- ALTER TABLE edware.dim_section ADD CONSTRAINT dim_section_nkey UNIQUE (section_sid); 

CREATE TABLE edware.dim_section_group
(
    dim_section_group_key int NOT NULL,
    integerized_section_keys varchar(255),
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_section_group ADD CONSTRAINT dim_section_group_pkey PRIMARY KEY (dim_section_group_key); 

CREATE TABLE edware.map_sect_group_sect
(
    map_sect_group_sect_key int NOT NULL,
    dim_section_group_key int NOT NULL,
    dim_section_key int NOT NULL,
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.map_sect_group_sect ADD CONSTRAINT map_sect_group_sect_pkey PRIMARY KEY (map_sect_group_sect_key); 

CREATE TABLE edware.map_staff_group_sect
(
    map_staff_group_sect_key int NOT NULL,
    dim_staff_group_key int NOT NULL,
    dim_section_key int NOT NULL,
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.map_staff_group_sect ADD CONSTRAINT map_staff_group_sect_pkey PRIMARY KEY (map_staff_group_sect_key); 

CREATE TABLE edware.dim_enroll_attr
(
    dim_enroll_attr_key int NOT NULL,
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
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL,
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

ALTER TABLE edware.dim_enroll_attr ADD CONSTRAINT dim_enroll_attr_pkey PRIMARY KEY (dim_enroll_attr_key); 
-- ALTER TABLE edware.dim_enroll_attr ADD CONSTRAINT dim_enroll_attr_nkey UNIQUE (ethnicity_code, sped_environ_code, disability_status_code, specific_disability_code, s504_status_code, econ_disadvantage_code, meal_status_code, title_1_status_code, migrant_status_code, english_prof_code, ell_status_code, home_lang_code, alt_assmt_code, housing_status_code, is_classed_code); 

CREATE TABLE edware.dim_term
(
    dim_term_key int NOT NULL,
    school_year_sid int,
    term_code varchar(255),
    term_name varchar(255),
    current_term_flag boolean,
    summer_term_flag boolean,
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_term ADD CONSTRAINT dim_term_pkey PRIMARY KEY (dim_term_key); 

CREATE TABLE edware.dim_period
(
    dim_period_key int NOT NULL,
    assmt_code varchar(255) NOT NULL,
    academic_year_name varchar(255) NOT NULL,
    academic_year_abbrev varchar(255),
    academic_year_code varchar(255) NOT NULL,
    period_code varchar(255) NOT NULL,
    period_abbrev varchar(255),
    period_order int NOT NULL,
    period_start_date date,
    period_end_date date,
    current_year_flag boolean,
    previous_year_flag boolean,
    current_period_flag boolean,
    previous_period_flag boolean,
    period_name varchar(255) NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_period ADD CONSTRAINT dim_period_pkey PRIMARY KEY (dim_period_key); 
-- ALTER TABLE edware.dim_period ADD CONSTRAINT dim_period_nkey UNIQUE (assmt_code, academic_year_code, period_code); 

CREATE TABLE edware.dim_perf_level
(
    dim_perf_level_key int NOT NULL,
    level_order int NOT NULL,
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
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL,
    account_sid int DEFAULT 0
)
;

ALTER TABLE edware.dim_perf_level ADD CONSTRAINT dim_perf_level_pkey PRIMARY KEY (dim_perf_level_key); 
-- ALTER TABLE edware.dim_perf_level ADD CONSTRAINT dim_perf_level_nkey UNIQUE (measure_specific_level_code, level_type_code, account_sid); 

CREATE TABLE edware.dim_assmt_subject
(
    dim_assmt_subject_key int NOT NULL,
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
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_assmt_subject ADD CONSTRAINT dim_assmt_subject_pkey PRIMARY KEY (dim_assmt_subject_key); 

CREATE TABLE edware.map_assmt_subj_subj
(
    map_assmt_subj_subj_key int NOT NULL,
    dim_assmt_subject_key int NOT NULL,
    dim_subject_key int NOT NULL,
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.map_assmt_subj_subj ADD CONSTRAINT map_assmt_subj_subj_pkey PRIMARY KEY (map_assmt_subj_subj_key); 

--drop table edware.dim_grade;
CREATE TABLE edware.dim_grade
(
    dim_grade_key int NOT NULL,
    grade_level_sid int NOT NULL,
    grade_level_name varchar(255) NOT NULL,
    grade_band_code varchar(255),
    grade_band_name varchar(255),
    grade_level_order int NOT NULL,
    updated_flag boolean DEFAULT FALSE,
    grade_band_flag boolean DEFAULT FALSE,
    grade_band_min int,
    grade_band_max int,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_grade ADD CONSTRAINT dim_grade_pkey PRIMARY KEY (dim_grade_key); 
-- ALTER TABLE edware.dim_grade ADD CONSTRAINT dim_grade_nkey UNIQUE (grade_level_sid);


CREATE TABLE edware.dim_time
(
    dim_time_key int NOT NULL,
    calendar_date date NOT NULL,
    day_of_year int NOT NULL,
    day_of_month int NOT NULL,
    day_of_week int NOT NULL,
    day_name varchar(255) NOT NULL,
    week_of_year int NOT NULL,
    week_of_month int NOT NULL,
    week_ending date NOT NULL,
    month_of_year int NOT NULL,
    month_name varchar(255) NOT NULL,
    quarter_of_year int NOT NULL,
    year int NOT NULL,
    is_holiday boolean NOT NULL,
    holiday_name varchar(255) NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_time ADD CONSTRAINT dim_time_pkey PRIMARY KEY (dim_time_key); 
-- ALTER TABLE edware.dim_time ADD CONSTRAINT dim_time_nkey UNIQUE (calendar_date); 

CREATE TABLE edware.dim_institution
(
    dim_institution_key int NOT NULL,
    academic_year_code varchar(255) NOT NULL,
    academic_year_name varchar(255) NOT NULL,
    current_acad_year_flag boolean NOT NULL,
    grade_config_code varchar(255),
    grade_config_name varchar(255),
    school_year_sid int NOT NULL,
    school_sid int NOT NULL,
    school_name varchar(255) NOT NULL,
    school_phone varchar(255),
    school_address_1 varchar(255),
    school_address_2 varchar(255),
    school_city varchar(255),
    school_zip_code varchar(255),
    district_sid int NOT NULL,
    district_name varchar(255) NOT NULL,
    municipality_sid int,
    municipality_name varchar(255),
    account_sid int NOT NULL,
    account_name varchar(255) NOT NULL,
    state_sid int NOT NULL,
    state_code varchar(255) NOT NULL,
    state_name varchar(255) NOT NULL,
    country_sid int NOT NULL,
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
    school_open_date date,
    school_years_open int,
    title_1_flag boolean,
    reading_first_flag boolean,
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
    dim_curr_institution_key int,
    status_code varchar(255) NOT NULL,
    demo_flag boolean NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_institution ADD CONSTRAINT dim_institution_pkey PRIMARY KEY (dim_institution_key); 
-- ALTER TABLE edware.dim_institution ADD CONSTRAINT dim_institution_nkey UNIQUE (school_year_sid); 

CREATE TABLE edware.dim_inst_group
(
    dim_inst_group_key int NOT NULL,
    parent_inst_group_key int NOT NULL,
    inst_group_name varchar(255) NOT NULL,
    inst_group_type_name varchar(255) NOT NULL,
    account_sid int,
    account_name varchar(255),
    sif_inst_group_type varchar(255),
    sif_inst_group_type_attribute varchar(255),
    group_start_time date,
    group_end_time date,
    status_code varchar(255) NOT NULL,
    address_1 varchar(255),
    address_2 varchar(255),
    city varchar(255),
    zip_code varchar(255),
    state_sid int,
    state_code varchar(255),
    state_name varchar(255),
    phone varchar(255),
    url varchar(255),
    managed_by_code varchar(255),
    managed_by_name varchar(255),
    is_internal boolean,
    is_funding_source boolean,
    is_study boolean,
    inst_group_code varchar(255) NOT NULL,
    inst_group_type_code varchar(255) NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL
)
;

ALTER TABLE edware.dim_inst_group ADD CONSTRAINT dim_inst_group_pkey PRIMARY KEY (dim_inst_group_key); 
-- ALTER TABLE edware.dim_inst_group ADD CONSTRAINT dim_inst_group_nkey UNIQUE (inst_group_code, inst_group_type_code); 

CREATE TABLE edware.map_inst_group_inst
(
    map_inst_group_inst_key int NOT NULL,
    dim_inst_group_key int NOT NULL,
    dim_institution_key int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL
)
;

ALTER TABLE edware.map_inst_group_inst ADD CONSTRAINT map_inst_group_inst_pkey PRIMARY KEY (map_inst_group_inst_key); 

CREATE TABLE edware.dim_student
(
    dim_student_key int NOT NULL,
    student_sid int NOT NULL,
    eternal_student_sid int NOT NULL,
    first_name varchar(255),
    middle_name varchar(255),
    last_name varchar(255),
    suffix varchar(255),
    dob date,
    email varchar(255),
    home_phone varchar(255),
    place_of_birth_code varchar(255),
    place_of_birth_name varchar(255),
    gender_code varchar(255),
    gender_name varchar(255),
    grad_cohort_year_code varchar(255),
    grad_cohort_year_name varchar(255),
    age_as_of_curr_year int,
    status_code varchar(255) NOT NULL,
    demo_flag boolean NOT NULL,
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
    source_create_date date,
    source_mod_date date,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL,
    inst_sid int,
    year_sid int
)
;

ALTER TABLE edware.dim_student ADD CONSTRAINT dim_student_pkey PRIMARY KEY (dim_student_key); 
-- ALTER TABLE edware.dim_student ADD CONSTRAINT dim_student_nkey UNIQUE (student_sid); 

CREATE TABLE edware.map_staff_group_staff
(
    map_staff_group_staff_key int NOT NULL,
    dim_staff_group_key int NOT NULL,
    dim_staff_key int NOT NULL,
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.map_staff_group_staff ADD CONSTRAINT map_staff_group_staff_pkey PRIMARY KEY (map_staff_group_staff_key); 

CREATE TABLE edware.fact_enroll
(
    fact_enroll_key int NOT NULL,
    part_key int NOT NULL,
    dim_institution_key int NOT NULL,
    dim_student_key int NOT NULL,
    dim_grade_key int NOT NULL,
    dim_section_key int NOT NULL,
    dim_term_key int,
    dim_teacher_staff_key int NOT NULL,
    dim_enroll_attr_key int NOT NULL,
    dim_inst_admit_time_key int NOT NULL,
    dim_inst_disc_time_key int NOT NULL,
    dim_sect_admit_time_key int NOT NULL,
    dim_sect_disc_time_key int NOT NULL,
    enrolled_in_inst_flag boolean NOT NULL,
    enrolled_in_sect_flag boolean NOT NULL,
    student_sid int NOT NULL,
    eternal_student_sid int NOT NULL,
    section_sid int NOT NULL,
    year_sid int NOT NULL,
    is_reporting_classe boolean NOT NULL,
    section_type_code varchar(255) NOT NULL,
    section_subtype_code varchar(255) NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL
)
;

ALTER TABLE edware.fact_enroll ADD CONSTRAINT fact_enroll_pkey PRIMARY KEY (fact_enroll_key); 
-- ALTER TABLE edware.fact_enroll ADD CONSTRAINT fact_enroll_nkey UNIQUE (student_sid, section_sid); 

CREATE TABLE edware.dim_assmt_outcome_type
(
    dim_assmt_outcome_type_key int NOT NULL,
    assmt_code varchar(255) NOT NULL,
    assmt_name varchar(255) NOT NULL,
    assmt_abbrev varchar(255),
    assmt_version_code varchar(255) NOT NULL,
    assmt_version_name varchar(255) NOT NULL,
    assmt_version_abbrev varchar(255),
    assmt_version_rank int NOT NULL,
    daot_measure_type_code varchar(255) NOT NULL,
    daot_measure_type_name varchar(255) NOT NULL,
    daot_measure_type_rank int NOT NULL,
    daot_hier_level int NOT NULL,
    daot_hier_level_code varchar(255) NOT NULL,
    daot_hier_level_name varchar(255) NOT NULL,
    daot_hier_level_rank int NOT NULL,
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
    performance_level_flag boolean NOT NULL,
    performance_level_type_code varchar(255) NOT NULL,
    outcome_int_flag boolean NOT NULL,
    outcome_int_code varchar(255) NOT NULL,
    outcome_int_name varchar(255) NOT NULL,
    outcome_int_abbrev varchar(255),
    outcome_float_flag boolean NOT NULL,
    outcome_float_code varchar(255) NOT NULL,
    outcome_float_name varchar(255) NOT NULL,
    outcome_float_abbrev varchar(255),
    outcome_string_flag boolean NOT NULL,
    outcome_string_code varchar(255) NOT NULL,
    outcome_string_name varchar(255) NOT NULL,
    outcome_string_abbrev varchar(255),
    outcome_rank int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    part_key int NOT NULL,
    pg_by_grade_flag boolean,
    assmt_course_code varchar(255),
    assmt_course_name varchar(255)
)
;

ALTER TABLE edware.dim_assmt_outcome_type ADD CONSTRAINT dim_assmt_outcome_type_pkey PRIMARY KEY (dim_assmt_outcome_type_key); 
-- ALTER TABLE edware.dim_assmt_outcome_type ADD CONSTRAINT dim_assmt_outcome_type_nkey UNIQUE (assmt_code, assmt_version_code, daot_measure_type_code, daot_hier_level_1_code, daot_hier_level_2_code, daot_hier_level_3_code, daot_hier_level_4_code, daot_hier_level_5_code, outcome_int_code, outcome_float_code, outcome_string_code, performance_level_type_code, assmt_course_code); 

CREATE TABLE edware.fact_assmt_outcome
(
    fact_assmt_outcome_key int NOT NULL,
    part_key int NOT NULL,
    active_flag boolean NOT NULL,
    dim_student_key int NOT NULL,
    eternal_student_sid int NOT NULL,
    year_sid int NOT NULL,
    dim_assmt_staff_key int NOT NULL,
    dim_assmt_outcome_type_key int NOT NULL,
    dim_assmt_period_key int NOT NULL,
    dim_assmt_grade_key int NOT NULL,
    dim_assmt_time_key int NOT NULL,
    dim_assmt_sync_time_key int NOT NULL,
    dim_perf_level_key int NOT NULL,
    dim_custom_perf_level_key int,
    dim_assmt_institution_key int NOT NULL,
    dim_curr_institution_key int,
    dim_eoy_institution_key int,
    dim_curr_enroll_attr_key int,
    dim_eoy_enroll_attr_key int,
    dim_eoy_student_grade_key int,
    dim_curr_student_grade_key int,
    dim_eoy_section_group_key int,
    dim_curr_section_group_key int,
    dim_offic_section_key int,
    dim_curr_offic_section_key int,
    outcome_int bigint,
    outcome_string varchar(255),
    outcome_float float,
    assmt_date timestamp,
    sync_date timestamp,
    assmt_instance_sid int NOT NULL,
    assmt_instance_rank int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    assmt_custom_id_code varchar(255),
    assmt_custom_id_name varchar(255)
)
;

ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fact_assmt_outcome_pkey PRIMARY KEY (fact_assmt_outcome_key); 
-- ALTER TABLE edware.fact_assmt_outcome ADD CONSTRAINT fact_assmt_outcome_nkey UNIQUE (dim_student_key, dim_assmt_outcome_type_key, dim_assmt_period_key, dim_assmt_grade_key, assmt_instance_sid); 

CREATE TABLE edware.etl_date
(
    etl_date_key int NOT NULL,
    etl_date_code varchar(32) NOT NULL,
    etl_date_name varchar(255),
    academic_year_code varchar(10) NOT NULL,
    etl_lastrun_timestamp timestamp,
    etl_currentrun_starttime timestamp,
    etl_currentrun_endtime timestamp
);


CREATE TABLE edware.mv_academic_year_period
(
    mv_academic_year_period_key int NOT NULL,
    school_sid int NOT NULL,
    state_code varchar(255) NOT NULL,
    municipality_sid int,
    district_sid int NOT NULL,
    dim_institution_key int NOT NULL,
    status_code varchar(255) NOT NULL,
    demo_flag boolean NOT NULL,
    dim_period_key int NOT NULL,
    academic_year_code varchar(255) NOT NULL,
    academic_year_name varchar(255) NOT NULL,
    academic_year_abbrev varchar(255),
    period_code varchar(255) NOT NULL,
    period_abbrev varchar(255),
    period_order int NOT NULL,
    assmt_code varchar(255) NOT NULL,
    assmt_name varchar(255) NOT NULL,
    assmt_abbrev varchar(255),
    assmt_version_code varchar(255) NOT NULL,
    assmt_version_name varchar(255) NOT NULL,
    assmt_version_abbrev varchar(255),
    assmt_version_rank int NOT NULL,
    daot_hier_level int NOT NULL,
    daot_hier_level_1_code varchar(255) NOT NULL,
    daot_hier_level_2_code varchar(255) NOT NULL,
    daot_hier_level_3_code varchar(255) NOT NULL,
    daot_hier_level_4_code varchar(255) NOT NULL,
    daot_hier_level_5_code varchar(255) NOT NULL,
    calendar_date date,
    part_key int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL,
    daot_hier_level_code varchar(255),
    daot_measure_type_code varchar(255),
    daot_measure_type_name varchar(255),
    account_sid int,
    year_sid int,
    assmt_course_code varchar(255),
    assmt_course_name varchar(255),
    daot_hier_level_1_abbrev varchar(255),
    daot_hier_level_2_abbrev varchar(255),
    daot_hier_level_3_abbrev varchar(255),
    daot_hier_level_4_abbrev varchar(255),
    daot_hier_level_5_abbrev varchar(255),
    performance_level_flag boolean,
    assmt_custom_id_name varchar(255)
)
;

ALTER TABLE edware.mv_academic_year_period ADD CONSTRAINT mv_academic_year_period_pkey PRIMARY KEY (mv_academic_year_period_key); 

CREATE TABLE edware.mv_amp_user_inst
(
    mv_amp_user_inst_key int NOT NULL,
    amp_user_sid int NOT NULL,
    inst_sid int NOT NULL,
    inst_type_sid int NOT NULL,
    inst_name varchar(255),
    account_sid int NOT NULL,
    spa_flag boolean NOT NULL,
    pii_flag boolean NOT NULL,
    home_flag boolean NOT NULL,
    part_key int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL
)
;

ALTER TABLE edware.mv_amp_user_inst ADD CONSTRAINT mv_amp_user_inst_pkey PRIMARY KEY (mv_amp_user_inst_key); 

CREATE TABLE edware.mv_amp_user_assmt
(
    mv_amp_user_assmt_key int NOT NULL,
    amp_user_sid int NOT NULL,
    assmt_code varchar(255) NOT NULL,
    spa_flag boolean NOT NULL,
    part_key int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL
)
;

ALTER TABLE edware.mv_amp_user_assmt ADD CONSTRAINT mv_amp_user_assmt_pkey PRIMARY KEY (mv_amp_user_assmt_key); 

CREATE TABLE edware.mv_amp_user_program
(
    mv_amp_user_program_key int NOT NULL,
    amp_user_sid int NOT NULL,
    program_sid int NOT NULL,
    is_admin_enabled boolean,
    is_reporting_enabled boolean,
    is_pii_enabled boolean,
    is_trad_view_enabled boolean,
    part_key int NOT NULL,
    create_date timestamp NOT NULL,
    mod_date timestamp NOT NULL
)
;

ALTER TABLE edware.mv_amp_user_program ADD CONSTRAINT mv_amp_user_program_pkey PRIMARY KEY (mv_amp_user_program_key); 

CREATE TABLE edware.executionlog
(
    instancename varchar(50),
    reportid varchar(50),
    user_name varchar(260),
    requesttype int,
    format varchar(50),
    parameters varchar(4000),
    time_begin timestamp,
    time_end timestamp,
    time_data_retrieval int,
    time_processing int,
    time_rendering int,
    source int,
    status varchar(50),
    bytecount int,
    rowcount int,
    path varchar(500),
    name varchar(500),
    app varchar(50)
)
;


CREATE TABLE edware.pm_periods
(
    pm_periods_key int NOT NULL,
    eternal_student_sid int,
    assmt_code varchar(255),
    assmt_version_code varchar(255),
    academic_year_code varchar(255),
    period_code varchar(255),
    sync_time timestamp,
    assmt_time timestamp,
    create_date timestamp,
    mod_date timestamp,
    part_key int NOT NULL
)
;

ALTER TABLE edware.pm_periods ADD CONSTRAINT pm_periods_pkey PRIMARY KEY (pm_periods_key);
