"""
Define the output format for SBAC assessment and registration data.

@author, nestep
@date, February 24, 2014
"""

FAO_FORMAT = {'format': 'csv',
              'name': 'fact_assmt_outcome.csv',
              'columns': [{'name': 'asmnt_outcome_rec_id', 'val': 'assessment_outcome.rec_id'},
                          {'name': 'asmt_rec_id', 'val': 'assessment.rec_id'},
                          {'name': 'student_guid', 'val': 'student.guid'},
                          {'name': 'student_rec_id', 'val': 'student.rec_id'},
                          {'name': 'state_code', 'val': 'state.code'},
                          {'name': 'district_guid', 'val': 'district.guid'},
                          {'name': 'school_guid', 'val': 'school.guid'},
                          {'name': 'section_guid', 'val': 'section.guid'},
                          {'name': 'inst_hier_rec_id', 'val': 'institution_hierarchy.rec_id'},
                          {'name': 'section_rec_id', 'val': 'section.rec_id'},
                          {'name': 'where_taken_id', 'val': 'school.guid'},
                          {'name': 'where_taken_name', 'val': 'school.name'},
                          {'name': 'asmt_grade', 'val': 'student.grade'},
                          {'name': 'enrl_grade', 'val': 'student.grade'},
                          {'name': 'date_taken', 'val': 'assessment_outcome.date_taken'},
                          {'name': 'date_taken_day', 'val': 'assessment_outcome.date_taken.day'},
                          {'name': 'date_taken_month', 'val': 'assessment_outcome.date_taken.month'},
                          {'name': 'date_taken_year', 'val': 'assessment_outcome.date_taken.year'},
                          {'name': 'asmt_score', 'val': 'assessment_outcome.overall_score'},
                          {'name': 'asmt_score_range_min', 'val': 'assessment_outcome.overall_score_range_min'},
                          {'name': 'asmt_score_range_max', 'val': 'assessment_outcome.overall_score_range_max'},
                          {'name': 'asmt_perf_lvl', 'val': 'assessment_outcome.overall_perf_lvl'},
                          {'name': 'asmt_claim_1_score', 'val': 'assessment_outcome.claim_1_score'},
                          {'name': 'asmt_claim_1_score_range_min', 'val': 'assessment_outcome.claim_1_score_range_min'},
                          {'name': 'asmt_claim_1_score_range_max', 'val': 'assessment_outcome.claim_1_score_range_max'},
                          {'name': 'asmt_claim_1_perf_lvl', 'val': 'assessment_outcome.claim_1_perf_lvl'},
                          {'name': 'asmt_claim_2_score', 'val': 'assessment_outcome.claim_2_score'},
                          {'name': 'asmt_claim_2_score_range_min', 'val': 'assessment_outcome.claim_2_score_range_min'},
                          {'name': 'asmt_claim_2_score_range_max', 'val': 'assessment_outcome.claim_2_score_range_max'},
                          {'name': 'asmt_claim_2_perf_lvl', 'val': 'assessment_outcome.claim_2_perf_lvl'},
                          {'name': 'asmt_claim_3_score', 'val': 'assessment_outcome.claim_3_score'},
                          {'name': 'asmt_claim_3_score_range_min', 'val': 'assessment_outcome.claim_3_score_range_min'},
                          {'name': 'asmt_claim_3_score_range_max', 'val': 'assessment_outcome.claim_3_score_range_max'},
                          {'name': 'asmt_claim_3_perf_lvl', 'val': 'assessment_outcome.claim_3_perf_lvl'},
                          {'name': 'asmt_claim_4_score', 'val': 'assessment_outcome.claim_4_score'},
                          {'name': 'asmt_claim_4_score_range_min', 'val': 'assessment_outcome.claim_4_score_range_min'},
                          {'name': 'asmt_claim_4_score_range_max', 'val': 'assessment_outcome.claim_4_score_range_max'},
                          {'name': 'asmt_claim_4_perf_lvl', 'val': 'assessment_outcome.claim_4_perf_lvl'},
                          {'name': 'status', 'val': 'C'},
                          {'name': 'most_recent', 'val': 'assessment.most_recent'},
                          {'name': 'batch_guid', 'val': 'BATCH_GUID'},
                          {'name': 'asmt_type', 'val': 'assessment.amt_type'},
                          {'name': 'asmt_year', 'val': 'assessment.period_year'},
                          {'name': 'asmt_subject', 'val': 'assessment.subject'},
                          {'name': 'gender', 'val': 'student.gender'},
                          {'name': 'dmg_eth_hsp', 'val': 'student.eth_hispanic'},
                          {'name': 'dmg_eth_ami', 'val': 'student.eth_amer_ind'},
                          {'name': 'dmg_eth_asn', 'val': 'student.eth_asian'},
                          {'name': 'dmg_eth_blk', 'val': 'student.eth_black'},
                          {'name': 'dmg_eth_pcf', 'val': 'student.eth_pacific'},
                          {'name': 'dmg_eth_wht', 'val': 'student.eth_white'},
                          {'name': 'dmg_eth_iep', 'val': 'student.prg_iep'},
                          {'name': 'dmg_prg_lep', 'val': 'student.prg_lep'},
                          {'name': 'dmg_prg_504', 'val': 'student.prg_sec504'},
                          {'name': 'dmg_prg_tt1', 'val': 'student.prg_title_1'},
                          {'name': 'dmg_eth_derived', 'val': 'student.derived_demographic'}]
              }

DIM_INST_HIER_FORMAT = {'format': 'csv',
                        'name': 'dim_inst_hier.csv',
                        'columns': [{'name': 'inst_hier_rec_id', 'val': 'institution_hierarchy.rec_id'},
                                    {'name': 'state_name', 'val': 'state.name'},
                                    {'name': 'state_code', 'val': 'state.code'},
                                    {'name': 'district_guid', 'val': 'district.guid'},
                                    {'name': 'district_name', 'val': 'district.name'},
                                    {'name': 'school_guid', 'val': 'school.guid'},
                                    {'name': 'school_name', 'val': 'school.name'},
                                    {'name': 'school_category', 'val': 'school.category'},
                                    {'name': 'from_date', 'val': 'institution_hierarchy.from_date'},
                                    {'name': 'to_date', 'val': 'institution_hierarchy.to_date'},
                                    {'name': 'most_recent', 'val': 'institution_hierarchy.most_recent'}]
                        }

DIM_ASMT_FORMAT = {'format': 'csv',
                   'name': 'dim_asmt.csv',
                   'columns': [{'name': 'asmt_rec_id', 'val': 'assessment.rec_id'},
                               {'name': 'asmt_guid', 'val': 'assessment.guid'},
                               {'name': 'asmt_type', 'val': 'assessment.asmt_type'},
                               {'name': 'asmt_period', 'val': 'assessment.period'},
                               {'name': 'asmt_period_year', 'val': 'assessment.period_year'},
                               {'name': 'asmt_version', 'val': 'assessment.version'},
                               {'name': 'asmt_subject', 'val': 'assessment.subject'},
                               {'name': 'asmt_claim_1_name', 'val': 'assessment.claim_1_name'},
                               {'name': 'asmt_claim_2_name', 'val': 'assessment.claim_2_name'},
                               {'name': 'asmt_claim_3_name', 'val': 'assessment.claim_3_name'},
                               {'name': 'asmt_claim_4_name', 'val': 'assessment.claim_4_name'},
                               {'name': 'asmt_perf_lvl_name_1', 'val': 'assessment.perf_lvl_name_1'},
                               {'name': 'asmt_perf_lvl_name_2', 'val': 'assessment.perf_lvl_name_2'},
                               {'name': 'asmt_perf_lvl_name_3', 'val': 'assessment.perf_lvl_name_3'},
                               {'name': 'asmt_perf_lvl_name_4', 'val': 'assessment.perf_lvl_name_4'},
                               {'name': 'asmt_perf_lvl_name_5', 'val': 'assessment.perf_lvl_name_5'},
                               {'name': 'asmt_score_min', 'val': 'assessment.overall_score_min'},
                               {'name': 'asmt_score_max', 'val': 'assessment.overall_score_max'},
                               {'name': 'asmt_claim_1_score_min', 'val': 'assessment.claim_1_score_min'},
                               {'name': 'asmt_claim_1_score_max', 'val': 'assessment.claim_1_score_max'},
                               {'name': 'asmt_claim_1_score_weight', 'val': 'assessment.claim_1_score_weight'},
                               {'name': 'asmt_claim_perf_lvl_name_1', 'val': 'assessment.claim_perf_lvl_name_1'},
                               {'name': 'asmt_claim_2_score_min', 'val': 'assessment.claim_2_score_min'},
                               {'name': 'asmt_claim_2_score_max', 'val': 'assessment.claim_2_score_max'},
                               {'name': 'asmt_claim_2_score_weight', 'val': 'assessment.claim_2_score_weight'},
                               {'name': 'asmt_claim_perf_lvl_name_1', 'val': 'assessment.claim_perf_lvl_name_2'},
                               {'name': 'asmt_claim_3_score_min', 'val': 'assessment.claim_3_score_min'},
                               {'name': 'asmt_claim_3_score_max', 'val': 'assessment.claim_3_score_max'},
                               {'name': 'asmt_claim_3_score_weight', 'val': 'assessment.claim_3_score_weight'},
                               {'name': 'asmt_claim_perf_lvl_name_1', 'val': 'assessment.claim_perf_lvl_name_3'},
                               {'name': 'asmt_claim_4_score_min', 'val': 'assessment.claim_4_score_min'},
                               {'name': 'asmt_claim_4_score_max', 'val': 'assessment.claim_4_score_max'},
                               {'name': 'asmt_claim_4_score_weight', 'val': 'assessment.claim_4_score_weight'},
                               {'name': 'asmt_cut_point_1', 'val': 'assessment.overall_cut_point_1'},
                               {'name': 'asmt_cut_point_2', 'val': 'assessment.overall_cut_point_2'},
                               {'name': 'asmt_cut_point_3', 'val': 'assessment.overall_cut_point_3'},
                               {'name': 'asmt_cut_point_4', 'val': 'assessment.overall_cut_point_4'},
                               {'name': 'from_date', 'val': 'assessment.from_date'},
                               {'name': 'to_date', 'val': 'assessment.to_date'},
                               {'name': 'most_recent', 'val': 'assessment.most_recent'}]
                   }

ASMT_JSON_FORMAT = {'format': 'json',
                    'name': '<YEAR>_METADATA_ASMT_ID_<GUID>.json',
                    'layout': {
                        'content': 'assessment',
                        'identification': {
                            'guid': 'assessment.guid',
                            'type': 'assessment.asmt_type',
                            'year': 'assessment.period_year',
                            'period': 'assessment.period',
                            'version': 'assessment.version',
                            'subject': 'assessment.subject'
                        },
                        'overall': {
                            'min_score': 'assessment.overall_score_min',
                            'max_score': 'assessment.overall_score_max'
                        },
                        'performance_levels': {
                            'level_1': {
                                'name': 'assessment.perf_lvl_name_1',
                                'cut_point': 'assessment.overall_score_min'
                            },
                            'level_2': {
                                'name': 'assessment.perf_lvl_name_2',
                                'cut_point': 'assessment.overall_cut_point_1'
                            },
                            'level_3': {
                                'name': 'assessment.perf_lvl_name_3',
                                'cut_point': 'assessment.overall_cut_point_2'
                            },
                            'level_4': {
                                'name': 'assessment.perf_lvl_name_4',
                                'cut_point': 'assessment.overall_cut_point_3'
                            },
                            'level_5': {
                                'name': 'assessment.perf_lvl_name_5',
                                'cut_point': 'assessment.overall_cut_point_4'
                            }
                        },
                        'claims': {
                            'claim_1': {
                                'name': 'assessment.claim_1_name',
                                'min_score': 'assessment.claim_1_score_min',
                                'max_score': 'assessment.claim_1_score_max',
                                'weight': 'assessment.claim_1_score_weight'
                            },
                            'claim_2': {
                                'name': 'assessment.claim_2_name',
                                'min_score': 'assessment.claim_2_score_min',
                                'max_score': 'assessment.claim_2_score_max',
                                'weight': 'assessment.claim_2_score_weight'
                            },
                            'claim_3': {
                                'name': 'assessment.claim_3_name',
                                'min_score': 'assessment.claim_3_score_min',
                                'max_score': 'assessment.claim_3_score_max',
                                'weight': 'assessment.claim_3_score_weight'
                            },
                            'claim_4': {
                                'name': 'assessment.claim_4_name',
                                'min_score': 'assessment.claim_4_score_min',
                                'max_score': 'assessment.claim_4_score_max',
                                'weight': 'assessment.claim_4_score_weight'
                            }
                        },
                        'claim_performance_levels': {
                            'level_1': {
                                'name': 'assessment.claim_perf_lvl_name_1'
                            },
                            'level_2': {
                                'name': 'assessment.claim_perf_lvl_name_2'
                            },
                            'level_3': {
                                'name': 'assessment.claim_perf_lvl_name_3'
                            }
                        }
                    }}

LZ_REALDATA_FORMAT = {'format': 'csv',
                      'name': '<YEAR>_REALDATA_RECORDS.csv',
                      'columns': [{'name': 'guid_asmt', 'val': 'assessment.guid'},
                                  {'name': 'guid_asmt_location', 'val': 'school.guid'},
                                  {'name': 'name_asmt_location', 'val': 'school.name'},
                                  {'name': 'grade_asmt', 'val': 'student.grade'},
                                  {'name': 'name_state', 'val': 'state.name'},
                                  {'name': 'code_state', 'val': 'state.code'},
                                  {'name': 'guid_district', 'val': 'district.guid'},
                                  {'name': 'name_district', 'val': 'district.name'},
                                  {'name': 'guid_school', 'val': 'school.guid'},
                                  {'name': 'name_school', 'val': 'school.name'},
                                  {'name': 'type_school', 'val': 'school.category'},
                                  {'name': 'guid_student', 'val': 'student.guid'},
                                  {'name': 'name_student_first', 'val': 'student.first_name'},
                                  {'name': 'name_student_middle', 'val': 'student.middle_name'},
                                  {'name': 'name_student_last', 'val': 'student.last_name'},
                                  {'name': 'address_student_line_1', 'val': 'student.address_line_1'},
                                  {'name': 'address_student_line_2', 'val': 'student.address_line_2'},
                                  {'name': 'address-student_city', 'val': 'student.address_city'},
                                  {'name': 'address_student_zip', 'val': 'student.address_zip'},
                                  {'name': 'gender_student', 'val': 'student.gender'},
                                  {'name': 'email_student', 'val': 'student.email'},
                                  {'name': 'dob_student', 'val': 'student.dob'},
                                  {'name': 'grade_enrolled', 'val': 'student.grade'},
                                  {'name': 'date_assessed', 'val': 'assessment_outcome.date_taken'},
                                  {'name': 'score_asmt', 'val': 'assessment_outcome.overall_score'},
                                  {'name': 'score_asmt_min', 'val': 'assessment_outcome.overall_score_range_min'},
                                  {'name': 'score_asmt_max', 'val': 'assessment_outcome.overall_score_range_max'},
                                  {'name': 'score_perf_level', 'val': 'assessment_outcome.overall_perf_lvl'},
                                  {'name': 'score_claim_1', 'val': 'assessment_outcome.claim_1_score'},
                                  {'name': 'score_claim_1_min', 'val': 'assessment_outcome.claim_1_score_range_min'},
                                  {'name': 'score_claim_1_max', 'val': 'assessment_outcome.claim_1_score_range_max'},
                                  {'name': 'score_claim_1_perf_lvl', 'val': 'assessment_outcome.claim_1_perf_lvl'},
                                  {'name': 'score_claim_2', 'val': 'assessment_outcome.claim_2_score'},
                                  {'name': 'score_claim_2_min', 'val': 'assessment_outcome.claim_2_score_range_min'},
                                  {'name': 'score_claim_2_max', 'val': 'assessment_outcome.claim_2_score_range_max'},
                                  {'name': 'score_claim_2_perf_lvl', 'val': 'assessment_outcome.claim_2_perf_lvl'},
                                  {'name': 'score_claim_3', 'val': 'assessment_outcome.claim_3_score'},
                                  {'name': 'score_claim_3_min', 'val': 'assessment_outcome.claim_3_score_range_min'},
                                  {'name': 'score_claim_3_max', 'val': 'assessment_outcome.claim_3_score_range_max'},
                                  {'name': 'score_claim_3_perf_lvl', 'val': 'assessment_outcome.claim_3_perf_lvl'},
                                  {'name': 'score_claim_4', 'val': 'assessment_outcome.claim_4_score'},
                                  {'name': 'score_claim_4_min', 'val': 'assessment_outcome.claim_4_score_range_min'},
                                  {'name': 'score_claim_4_max', 'val': 'assessment_outcome.claim_4_score_range_max'},
                                  {'name': 'score_claim_4_perf_lvl', 'val': 'assessment_outcome.claim_4_perf_lvl'},
                                  {'name': 'dmg_eth_hsp', 'val': 'student.eth_hispanic'},
                                  {'name': 'dmg_eth_ami', 'val': 'student.eth_amer_ind'},
                                  {'name': 'dmg_eth_asn', 'val': 'student.eth_asian'},
                                  {'name': 'dmg_eth_blk', 'val': 'student.eth_black'},
                                  {'name': 'dmg_eth_pcf', 'val': 'student.eth_pacific'},
                                  {'name': 'dmg_eth_wht', 'val': 'student.eth_white'},
                                  {'name': 'dmg_prg_iep', 'val': 'student.prg_iep'},
                                  {'name': 'dmg_prg_lep', 'val': 'student.prg_lep'},
                                  {'name': 'dmg_prg_504', 'val': 'student.prg_sec504'},
                                  {'name': 'dmg_prg_tt1', 'val': 'student.prg_econ_disad'},
                                  {'name': 'asmt_type', 'val': 'assessment.asmt_type'},
                                  {'name': 'asmt_year', 'val': 'assessment.period_year'},
                                  {'name': 'asmt_subject', 'val': 'assessment.subject'}
                      ]}

SR_FORMAT = {'format': 'csv',
             'name': 'sr_<YEAR>.csv',
             'columns': [{'name': 'StateName', 'val': 'state.name'},
                         {'name': 'StateAbbreviation', 'val': 'state.code'},
                         {'name': 'ResponsibleDistrictIdentifier', 'val': 'district.guid_sr'},
                         {'name': 'OrganizationName', 'val': 'district.name'},
                         {'name': 'ResponsibleSchoolIdentifier', 'val': 'school.guid_sr'},
                         {'name': 'NameOfInstitution', 'val': 'school.name'},
                         {'name': 'StudentIdentifier', 'val': 'student.guid_sr'},
                         {'name': 'ExternalSSID', 'val': 'student.external_ssid'},
                         {'name': 'FirstName', 'val': 'student.first_name'},
                         {'name': 'MiddleName', 'val': 'student.middle_name'},
                         {'name': 'LastOrSurname', 'val': 'student.last_name'},
                         {'name': 'Sex', 'val': 'student.gender'},
                         {'name': 'Birthdate', 'val': 'student.dob'},
                         {'name': 'GradeLevelWhenAssessed', 'val': 'student.grade'},
                         {'name': 'HispanicOrLatinoEthnicity', 'val': 'student.eth_hispanic', 'filter': 'yesno'},
                         {'name': 'AmericanIndianOrAlaskaNative', 'val': 'student.eth_amer_ind', 'filter': 'yesno'},
                         {'name': 'Asian', 'val': 'student.eth_asian', 'filter': 'yesno'},
                         {'name': 'BlackOrAfricanAmerican', 'val': 'student.eth_black', 'filter': 'yesno'},
                         {'name': 'NativeHawaiianOrOtherPacificIslander', 'val': 'student.eth_pacific',
                          'filter': 'yesno'},
                         {'name': 'White', 'val': 'student.eth_white', 'filter': 'yesno'},
                         {'name': 'IDEAIndicator', 'val': 'student.prg_idea', 'filter': 'yesno'},
                         {'name': 'LEPStatus', 'val': 'student.prg_lep', 'filter': 'yesno'},
                         {'name': 'Section504Status', 'val': 'student.prg_sec504', 'filter': 'yesnoblank'},
                         {'name': 'EconomicDisadvantageStatus', 'val': 'student.prg_econ_disad', 'filter': 'yesno'},
                         {'name': 'MigrantStatus', 'val': 'student.prg_migrant', 'filter': 'yesnoblank'},
                         {'name': 'DemographicRaceTwoOrMoreRaces', 'val': 'student.eth_multi', 'filter': 'yesno'},
                         {'name': 'ConfirmationCode', 'val': 'student.first_name'},
                         {'name': 'LanguageCode', 'val': 'student.lang_code'},
                         {'name': 'EnglishLanguageProficiencLevel', 'val': 'student.lang_prof_level'},
                         {'name': 'FirstEntryDateIntoUSSchool', 'val': 'student.school_entry_date'},
                         {'name': 'LimitedEnglishProficiencyEntryDate', 'val': 'student.prg_lep_entry_date'},
                         {'name': 'LEPExitDate', 'val': 'student.prg_lep_exit_date'},
                         {'name': 'TitleIIILanguageInstructionProgramType', 'val': 'student.lang_title_3_prg'},
                         {'name': 'PrimaryDisabilityType', 'val': 'student.prg_primary_disability'}]
             }

REGISTRATION_SYSTEM_FORMAT = {'format': 'json',
                              'name': 'sr_<YEAR>.json',
                              'layout': {
                                  'Content': 'StudentRegistration',
                                  'Identification': {
                                      'Guid': 'registration_system.guid',
                                      'AcademicYear': 'registration_system.academic_year',
                                      'ExtractDate': 'registration_system.extract_date'
                                  },
                                  'Source': {
                                      'TestRegSysID': 'registration_system.sys_guid',
                                      'RestRegCallbackURL': 'registration_system.callback_url'
                                  }}
                              }