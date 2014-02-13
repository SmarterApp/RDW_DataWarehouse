from config import ref_table_data as ref_constants

LZ_CSV = 'LZ_CSV'
SR_STAGING_CSV = 'STG_SBAC_STU_REG'

ref_table_conf = {
    'column_definitions': ref_constants.COLUMNS,
    'column_mappings': [
        # Columns:
        # column_map_key, phase, source_table, source_column, target_table, target_column, transformation_rule, stored_proc_name, stored_proc_created_date, created_date

        #Json to Integration
        ('1', 'LZ_JSON', 'identification.Guid', 'INT_SBAC_STU_REG_META', 'guid_registration', 'clean', None),
        ('1', 'LZ_JSON', 'identification.AcademicYear', 'INT_SBAC_STU_REG_META', 'academic_year', 'clean', None),
        ('1', 'LZ_JSON', 'identification.ExtractDate', 'INT_SBAC_STU_REG_META', 'extract_date', 'srDate', None),
        ('1', 'LZ_JSON', 'source.TestRegSysID', 'INT_SBAC_STU_REG_META', 'test_reg_id', 'clean', None),
        # CSV to Staging
        ('1', 'LZ_CSV', 'StateName', 'STG_SBAC_STU_REG', 'name_state', 'clean', None),
        ('1', 'LZ_CSV', 'StateAbbreviation', 'STG_SBAC_STU_REG', 'code_state', 'cleanUpper', None),
        ('1', 'LZ_CSV', 'ResponsibleDistrictIdentifier', 'STG_SBAC_STU_REG', 'guid_district', 'clean', None),
        ('1', 'LZ_CSV', 'OrganizationName', 'STG_SBAC_STU_REG', 'name_district', 'clean', None),
        ('1', 'LZ_CSV', 'ResponsibleSchoolIdentifier', 'STG_SBAC_STU_REG', 'guid_school', 'clean', None),
        ('1', 'LZ_CSV', 'NameOfInstitution', 'STG_SBAC_STU_REG', 'name_school', 'clean', None),
        ('1', 'LZ_CSV', 'StudentIdentifier', 'STG_SBAC_STU_REG', 'guid_student', 'clean', None),
        ('1', 'LZ_CSV', 'ExternalSSID', 'STG_SBAC_STU_REG', 'external_ssid_student', 'clean', None),
        ('1', 'LZ_CSV', 'FirstName', 'STG_SBAC_STU_REG', 'name_student_first', 'clean', None),
        ('1', 'LZ_CSV', 'MiddleName', 'STG_SBAC_STU_REG', 'name_student_middle', 'clean', None),
        ('1', 'LZ_CSV', 'LastOrSurname', 'STG_SBAC_STU_REG', 'name_student_last', 'clean', None),
        ('1', 'LZ_CSV', 'Sex', 'STG_SBAC_STU_REG', 'gender_student', 'srGender', None),
        ('1', 'LZ_CSV', 'Birthdate', 'STG_SBAC_STU_REG', 'dob_student', 'srDate', None),
        ('1', 'LZ_CSV', 'GradeLevelWhenAssessed', 'STG_SBAC_STU_REG', 'grade_enrolled', 'clean', None),
        ('1', 'LZ_CSV', 'HispanicOrLatinoEthnicity', 'STG_SBAC_STU_REG', 'dmg_eth_hsp', 'srYn', None),
        ('1', 'LZ_CSV', 'AmericanIndianOrAlaskaNative', 'STG_SBAC_STU_REG', 'dmg_eth_ami', 'srYn', None),
        ('1', 'LZ_CSV', 'Asian', 'STG_SBAC_STU_REG', 'dmg_eth_asn', 'srYn', None),
        ('1', 'LZ_CSV', 'BlackOrAfricanAmerican', 'STG_SBAC_STU_REG', 'dmg_eth_blk', 'srYn', None),
        ('1', 'LZ_CSV', 'NativeHawaiianOrOtherPacificIslander', 'STG_SBAC_STU_REG', 'dmg_eth_pcf', 'srYn', None),
        ('1', 'LZ_CSV', 'White', 'STG_SBAC_STU_REG', 'dmg_eth_wht', 'srYn', None),
        ('1', 'LZ_CSV', 'IDEAIndicator', 'STG_SBAC_STU_REG', 'dmg_prg_iep', 'srYn', None),
        ('1', 'LZ_CSV', 'LEPStatus', 'STG_SBAC_STU_REG', 'dmg_prg_lep', 'srYn', None),
        ('1', 'LZ_CSV', '504Status', 'STG_SBAC_STU_REG', 'dmg_prg_504', 'clean', None),
        ('1', 'LZ_CSV', 'EconomicDisadvantageStatus', 'STG_SBAC_STU_REG', 'dmg_sts_ecd', 'srYn', None),
        ('1', 'LZ_CSV', 'MigrantStatus', 'STG_SBAC_STU_REG', 'dmg_sts_mig', 'srYn', None),
        ('1', 'LZ_CSV', 'DemographicRaceTwoOrMoreRaces', 'STG_SBAC_STU_REG', 'dmg_multi_race', 'srYn', None),
        ('1', 'LZ_CSV', 'ConfirmationCode', 'STG_SBAC_STU_REG', 'code_confirm', 'clean', None),
        ('1', 'LZ_CSV', 'LanguageCode', 'STG_SBAC_STU_REG', 'code_language', 'clean', None),
        ('1', 'LZ_CSV', 'EnglishLanguageProficiencLevel', 'STG_SBAC_STU_REG', 'eng_prof_lvl', 'clean', None),
        ('1', 'LZ_CSV', 'FirstEntryDateIntoUSSchool', 'STG_SBAC_STU_REG', 'us_school_entry_date', 'srDate', None),
        ('1', 'LZ_CSV', 'LimitedEnglishProficiencyEntryDate', 'STG_SBAC_STU_REG', 'lep_entry_date', 'srDate', None),
        ('1', 'LZ_CSV', 'LEPExitDate', 'STG_SBAC_STU_REG', 'lep_exit_date', 'srDate', None),
        ('1', 'LZ_CSV', 'TitleIIILanguageInstructionProgramType', 'STG_SBAC_STU_REG', 't3_program_type', 'clean', None),
        ('1', 'LZ_CSV', 'PrimaryDisabilityType', 'STG_SBAC_STU_REG', 'prim_disability_type', 'clean', None)
    ]
}