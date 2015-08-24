from sqlalchemy.schema import MetaData, Sequence, Index
from sqlalchemy import Table, Column, text
from sqlalchemy.types import Text, Boolean, TIMESTAMP, Interval, TIME
from sqlalchemy.types import BigInteger, SmallInteger, String
from sqlalchemy import CheckConstraint
import sqlalchemy.sql.expression


def generate_udl2_metadata(schema_name=None, bind=None):
    '''
    generate_udl2_metadata function creates a metadata object that contains all udl2 related staging tables.
    '''

    metadata = MetaData(schema=schema_name, bind=bind)

    stg_mock_load = Table('stg_mock_load', metadata,
                          Column('record_sid', BigInteger, primary_key=True),
                          Column('guid_batch', String(256), nullable=False),
                          Column('substr_test', String(256), nullable=False),
                          Column('number_test', String(256), nullable=False),
                          )

    int_mock_load = Table('int_mock_load', metadata,
                          Column('record_sid', BigInteger, primary_key=True),
                          Column('guid_batch', String(256), CheckConstraint("guid_batch != ''"), nullable=False),
                          Column('substr_test', String(256), CheckConstraint("substr_test != ''"), nullable=False),
                          Column('number_test', String(256), CheckConstraint("number_test != ''"), nullable=False),
                          )

    udl_batch = Table('udl_batch', metadata,
                      Column('batch_sid', BigInteger, primary_key=True),
                      Column('guid_batch', String(256), nullable=False),
                      Column('tenant', String(256), nullable=False, server_default=''),
                      Column('input_file', Text, nullable=False, server_default=''),
                      Column('load_type', String(50), nullable=True),
                      Column('working_schema', String(50), nullable=True),
                      Column('udl_phase', String(256), nullable=True),
                      Column('udl_phase_step', String(50), nullable=True),
                      Column('udl_phase_step_status', String(50), nullable=True),
                      Column('error_desc', Text, nullable=True),
                      Column('stack_trace', Text, nullable=True),
                      Column('udl_leaf', Boolean, nullable=True),
                      Column('size_records', BigInteger, nullable=True),
                      Column('size_units', BigInteger, nullable=True),
                      Column('start_timestamp', TIMESTAMP, nullable=True, server_default=text('NOW()')),
                      Column('end_timestamp', TIMESTAMP, nullable=True, server_default=text('NOW()')),
                      Column('duration', Interval, nullable=True),
                      Column('time_for_one_million_records', TIME, nullable=True),
                      Column('records_per_hour', BigInteger, nullable=True),
                      Column('task_id', String(256), nullable=True),
                      Column('task_status_url', String(256), nullable=True),
                      Column('user_sid', BigInteger, nullable=True),
                      Column('user_email', String(256), nullable=True),
                      Column('created_date', TIMESTAMP, nullable=True, server_default=text('NOW()')),
                      Column('mod_date', TIMESTAMP, nullable=False, server_default=text('NOW()')),
                      )

    stg_sbac_stu_reg = Table('stg_sbac_stu_reg', metadata,
                             Column('record_sid', BigInteger, primary_key=True),
                             Column('src_file_rec_num', BigInteger, nullable=False),
                             Column('name_state', String(256), nullable=True),
                             Column('code_state', String(256), nullable=True),
                             Column('guid_district', String(256), nullable=True),
                             Column('name_district', String(256), nullable=True),
                             Column('guid_school', String(256), nullable=True),
                             Column('name_school', String(256), nullable=True),
                             Column('guid_student', String(256), nullable=True),
                             Column('external_ssid_student', String(256), nullable=True),
                             Column('name_student_first', String(256), nullable=True),
                             Column('name_student_middle', String(256), nullable=True),
                             Column('name_student_last', String(256), nullable=True),
                             Column('birthdate_student', String(256), nullable=True),
                             Column('sex_student', String(256), nullable=True),
                             Column('grade_enrolled', String(256), nullable=True),
                             Column('dmg_eth_hsp', String(256), nullable=True),
                             Column('dmg_eth_ami', String(256), nullable=True),
                             Column('dmg_eth_asn', String(256), nullable=True),
                             Column('dmg_eth_blk', String(256), nullable=True),
                             Column('dmg_eth_pcf', String(256), nullable=True),
                             Column('dmg_eth_wht', String(256), nullable=True),
                             Column('dmg_prg_iep', String(256), nullable=True),
                             Column('dmg_prg_lep', String(256), nullable=True),
                             Column('dmg_prg_504', String(256), nullable=True),
                             Column('dmg_sts_ecd', String(256), nullable=True),
                             Column('dmg_sts_mig', String(256), nullable=True),
                             Column('dmg_multi_race', String(256), nullable=True),
                             Column('code_language', String(256), nullable=True),
                             Column('eng_prof_lvl', String(256), nullable=True),
                             Column('us_school_entry_date', String(256), nullable=True),
                             Column('lep_entry_date', String(256), nullable=True),
                             Column('lep_exit_date', String(256), nullable=True),
                             Column('t3_program_type', String(256), nullable=True),
                             Column('prim_disability_type', String(256), nullable=True),
                             Column('created_date', TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()')),
                             Column('guid_batch', String(256), nullable=False),
                             )
    Index('stg_sbac_stu_reg_guid_batchx', stg_sbac_stu_reg.c.guid_batch, unique=False)

    stg_sbac_asmt_outcome = Table('stg_sbac_asmt_outcome', metadata,
                                  Column('record_sid', BigInteger, primary_key=True),
                                  Column('op', String(1), nullable=True, server_default='C'),
                                  Column('src_file_rec_num', BigInteger, nullable=False),
                                  Column('assessmentguid', String(256), nullable=True),
                                  Column('assessmentsessionlocationid', String(256), nullable=True),
                                  Column('assessmentsessionlocation', String(256), nullable=True),
                                  Column('assessmentlevelforwhichdesigned', String(256), nullable=True),
                                  Column('stateabbreviation', String(256), nullable=True),
                                  Column('responsibledistrictidentifier', String(256), nullable=True),
                                  Column('organizationname', String(256), nullable=True),
                                  Column('responsibleschoolidentifier', String(256), nullable=True),
                                  Column('nameofinstitution', String(256), nullable=True),
                                  Column('studentidentifier', String(256), nullable=True),
                                  Column('externalssid', String(256), nullable=True),
                                  Column('firstname', String(256), nullable=True),
                                  Column('middlename', String(256), nullable=True),
                                  Column('lastorsurname', String(256), nullable=True),
                                  Column('birthdate', String(256), nullable=True),
                                  Column('sex', String(256), nullable=True),
                                  Column('gradelevelwhenassessed', String(256), nullable=True),
                                  Column('group1id', String(256), nullable=True),
                                  Column('group1text', String(256), nullable=True),
                                  Column('group2id', String(256), nullable=True),
                                  Column('group2text', String(256), nullable=True),
                                  Column('group3id', String(256), nullable=True),
                                  Column('group3text', String(256), nullable=True),
                                  Column('group4id', String(256), nullable=True),
                                  Column('group4text', String(256), nullable=True),
                                  Column('group5id', String(256), nullable=True),
                                  Column('group5text', String(256), nullable=True),
                                  Column('group6id', String(256), nullable=True),
                                  Column('group6text', String(256), nullable=True),
                                  Column('group7id', String(256), nullable=True),
                                  Column('group7text', String(256), nullable=True),
                                  Column('group8id', String(256), nullable=True),
                                  Column('group8text', String(256), nullable=True),
                                  Column('group9id', String(256), nullable=True),
                                  Column('group9text', String(256), nullable=True),
                                  Column('group10id', String(256), nullable=True),
                                  Column('group10text', String(256), nullable=True),
                                  Column('hispanicorlatinoethnicity', String(256), nullable=True),
                                  Column('americanindianoralaskanative', String(256), nullable=True),
                                  Column('asian', String(256), nullable=True),
                                  Column('blackorafricanamerican', String(256), nullable=True),
                                  Column('nativehawaiianorotherpacificislander', String(256), nullable=True),
                                  Column('white', String(256), nullable=True),
                                  Column('demographicracetwoormoreraces', String(256), nullable=True),
                                  Column('ideaindicator', String(256), nullable=True),
                                  Column('lepstatus', String(256), nullable=True),
                                  Column('section504status', String(256), nullable=True),
                                  Column('economicdisadvantagestatus', String(256), nullable=True),
                                  Column('migrantstatus', String(256), nullable=True),
                                  Column('assessmentadministrationfinishdate', String(256), nullable=True),
                                  Column('assessmentsubtestresultscorevalue', String(256), nullable=True),
                                  Column('assessmentsubtestminimumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestmaximumvalue', String(256), nullable=True),
                                  Column('assessmentperformancelevelidentifier', String(256), nullable=True),
                                  Column('assessmentsubtestresultscoreclaim1value', String(256), nullable=True),
                                  Column('assessmentsubtestclaim1minimumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim1maximumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim1performancelevelidentifier', String(256), nullable=True),
                                  Column('assessmentsubtestresultscoreclaim2value', String(256), nullable=True),
                                  Column('assessmentsubtestclaim2minimumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim2maximumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim2performancelevelidentifier', String(256), nullable=True),
                                  Column('assessmentsubtestresultscoreclaim3value', String(256), nullable=True),
                                  Column('assessmentsubtestclaim3minimumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim3maximumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim3performancelevelidentifier', String(256), nullable=True),
                                  Column('assessmentsubtestresultscoreclaim4value', String(256), nullable=True),
                                  Column('assessmentsubtestclaim4minimumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim4maximumvalue', String(256), nullable=True),
                                  Column('assessmentsubtestclaim4performancelevelidentifier', String(256), nullable=True),
                                  Column('assessmenttype', String(256), nullable=True),
                                  Column('assessmentacademicsubject', String(256), nullable=True),
                                  Column('assessmentyear', String(256), nullable=True),
                                  Column('created_date', TIMESTAMP, nullable=False, server_default=text('NOW()')),
                                  Column('accommodationamericansignlanguage', String(256), nullable=True),
                                  Column('accommodationbraille', String(256), nullable=True),
                                  Column('accommodationclosedcaptioning', String(256), nullable=True),
                                  Column('accommodationtexttospeech', String(256), nullable=True),
                                  Column('accommodationabacus', String(256), nullable=True),
                                  Column('accommodationalternateresponseoptions', String(256), nullable=True),
                                  Column('accommodationcalculator', String(256), nullable=True),
                                  Column('accommodationmultiplicationtable', String(256), nullable=True),
                                  Column('accommodationprintondemand', String(256), nullable=True),
                                  Column('accommodationprintondemanditems', String(256), nullable=True),
                                  Column('accommodationreadaloud', String(256), nullable=True),
                                  Column('accommodationscribe', String(256), nullable=True),
                                  Column('accommodationspeechtotext', String(256), nullable=True),
                                  Column('accommodationstreamlinemode', String(256), nullable=True),
                                  Column('accommodationnoisebuffer', String(256), nullable=True),
                                  Column('guid_batch', String(256), nullable=False),
                                  Column('assessmentstatus', String(2), nullable=True),
                                  Column('completestatus', String(4), nullable=True),
                                  )

    err_list = Table('err_list', metadata,
                     Column('record_sid', BigInteger, primary_key=True, nullable=False),
                     Column('guid_batch', String(256), primary_key=True, nullable=False),
                     Column('err_code', BigInteger, nullable=True),
                     Column('err_source', BigInteger, nullable=True),
                     Column('err_code_text', Text, nullable=True),
                     Column('err_source_text', Text, nullable=True),
                     Column('created_date', TIMESTAMP, nullable=False, server_default=text('NOW()')),
                     Column('err_input', Text, nullable=False, server_default='')
                     )

    int_sbac_asmt = Table('int_sbac_asmt', metadata,
                          Column('record_sid', BigInteger, primary_key=True),
                          Column('guid_asmt', String(255), CheckConstraint("guid_asmt != ''"), nullable=False),
                          Column('type', String(32), CheckConstraint("type != ''"), nullable=False),
                          Column('period', String(32), CheckConstraint("period != ''"), nullable=True),
                          Column('year', SmallInteger, nullable=False),
                          Column('version', String(40), CheckConstraint("version != ''"), nullable=False),
                          Column('subject', String(64), nullable=True),
                          Column('score_overall_min', SmallInteger, nullable=True),
                          Column('score_overall_max', SmallInteger, nullable=True),
                          Column('name_claim_1', String(128), nullable=True),
                          Column('score_claim_1_min', SmallInteger, nullable=True),
                          Column('score_claim_1_max', SmallInteger, nullable=True),
                          Column('name_claim_2', String(128), nullable=True),
                          Column('score_claim_2_min', SmallInteger, nullable=True),
                          Column('score_claim_2_max', SmallInteger, nullable=True),
                          Column('name_claim_3', String(128), nullable=True),
                          Column('score_claim_3_min', SmallInteger, nullable=True),
                          Column('score_claim_3_max', SmallInteger, nullable=True),
                          Column('name_claim_4', String(128), nullable=True),
                          Column('score_claim_4_min', SmallInteger, nullable=True),
                          Column('score_claim_4_max', SmallInteger, nullable=True),
                          Column('asmt_claim_perf_lvl_name_1', String(128), nullable=True),
                          Column('asmt_claim_perf_lvl_name_2', String(128), nullable=True),
                          Column('asmt_claim_perf_lvl_name_3', String(128), nullable=True),
                          Column('name_perf_lvl_1', String(25), nullable=True),
                          Column('name_perf_lvl_2', String(25), nullable=True),
                          Column('name_perf_lvl_3', String(25), nullable=True),
                          Column('name_perf_lvl_4', String(25), nullable=True),
                          Column('name_perf_lvl_5', String(25), nullable=True),
                          Column('score_cut_point_1', SmallInteger, nullable=True),
                          Column('score_cut_point_2', SmallInteger, nullable=True),
                          Column('score_cut_point_3', SmallInteger, nullable=True),
                          Column('score_cut_point_4', SmallInteger, nullable=True),
                          Column('effective_date', String(8), nullable=True),
                          Column('created_date', TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()')),
                          Column('guid_batch', String(36), CheckConstraint("guid_batch != ''"), nullable=False),
                          )

    int_sbac_asmt_outcome = Table('int_sbac_asmt_outcome', metadata,
                                  Column('record_sid', BigInteger, primary_key=True),
                                  Column('op', String(1), CheckConstraint("op != ''"), server_default='C', nullable=False),
                                  Column('guid_asmt', String(255), nullable=True),
                                  Column('guid_asmt_location', String(40), nullable=True),
                                  Column('name_asmt_location', String(60), nullable=True),
                                  Column('grade_asmt', String(10), CheckConstraint("grade_asmt != ''"), nullable=False),
                                  Column('code_state', String(2), CheckConstraint("code_state != ''"), nullable=False),
                                  Column('guid_district', String(40), CheckConstraint("guid_district != ''"), nullable=False),
                                  Column('name_district', String(60), CheckConstraint("name_district != ''"), nullable=False),
                                  Column('guid_school', String(40), CheckConstraint("guid_school != ''"), nullable=False),
                                  Column('name_school', String(60), CheckConstraint("name_school != ''"), nullable=False),
                                  Column('guid_student', String(40), CheckConstraint("guid_student != ''"), nullable=False),
                                  Column('external_student_id', String(40), nullable=True),
                                  Column('name_student_first', String(35), nullable=True),
                                  Column('name_student_middle', String(35), nullable=True),
                                  Column('name_student_last', String(35), nullable=True),
                                  Column('birthdate_student', String(8), nullable=True),
                                  Column('sex_student', String(10), nullable=True),
                                  Column('grade_enrolled', String(10), CheckConstraint("grade_enrolled != ''"), nullable=False),
                                  Column('group_1_id', String(40), nullable=True),
                                  Column('group_1_text', String(60), nullable=True),
                                  Column('group_2_id', String(40), nullable=True),
                                  Column('group_2_text', String(60), nullable=True),
                                  Column('group_3_id', String(40), nullable=True),
                                  Column('group_3_text', String(60), nullable=True),
                                  Column('group_4_id', String(40), nullable=True),
                                  Column('group_4_text', String(60), nullable=True),
                                  Column('group_5_id', String(40), nullable=True),
                                  Column('group_5_text', String(60), nullable=True),
                                  Column('group_6_id', String(40), nullable=True),
                                  Column('group_6_text', String(60), nullable=True),
                                  Column('group_7_id', String(40), nullable=True),
                                  Column('group_7_text', String(60), nullable=True),
                                  Column('group_8_id', String(40), nullable=True),
                                  Column('group_8_text', String(60), nullable=True),
                                  Column('group_9_id', String(40), nullable=True),
                                  Column('group_9_text', String(60), nullable=True),
                                  Column('group_10_id', String(40), nullable=True),
                                  Column('group_10_text', String(60), nullable=True),
                                  Column('dmg_eth_derived', SmallInteger, nullable=True),
                                  Column('dmg_eth_hsp', Boolean, nullable=True),
                                  Column('dmg_eth_ami', Boolean, nullable=True),
                                  Column('dmg_eth_asn', Boolean, nullable=True),
                                  Column('dmg_eth_blk', Boolean, nullable=True),
                                  Column('dmg_eth_pcf', Boolean, nullable=True),
                                  Column('dmg_eth_wht', Boolean, nullable=True),
                                  Column('dmg_eth_2om', Boolean, nullable=True),
                                  Column('dmg_prg_iep', Boolean, nullable=True),
                                  Column('dmg_prg_lep', Boolean, nullable=True),
                                  Column('dmg_prg_504', Boolean, nullable=True),
                                  Column('dmg_sts_ecd', Boolean, nullable=True),
                                  Column('dmg_sts_mig', Boolean, nullable=True),
                                  Column('date_assessed', String(8), CheckConstraint("date_assessed != ''"), nullable=False),
                                  Column('date_taken_day', SmallInteger, nullable=False),
                                  Column('date_taken_month', SmallInteger, nullable=False),
                                  Column('date_taken_year', SmallInteger, nullable=False),
                                  Column('score_asmt', SmallInteger, nullable=True),
                                  Column('score_asmt_min', SmallInteger, nullable=True),
                                  Column('score_asmt_max', SmallInteger, nullable=True),
                                  Column('score_perf_level', SmallInteger, nullable=True),
                                  Column('score_claim_1', SmallInteger, nullable=True),
                                  Column('score_claim_1_min', SmallInteger, nullable=True),
                                  Column('score_claim_1_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_1_perf_lvl', SmallInteger, nullable=True),
                                  Column('score_claim_2', SmallInteger, nullable=True),
                                  Column('score_claim_2_min', SmallInteger, nullable=True),
                                  Column('score_claim_2_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_2_perf_lvl', SmallInteger, nullable=True),
                                  Column('score_claim_3', SmallInteger, nullable=True),
                                  Column('score_claim_3_min', SmallInteger, nullable=True),
                                  Column('score_claim_3_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_3_perf_lvl', SmallInteger, nullable=True),
                                  Column('score_claim_4', SmallInteger, nullable=True),
                                  Column('score_claim_4_min', SmallInteger, nullable=True),
                                  Column('score_claim_4_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_4_perf_lvl', SmallInteger, nullable=True),
                                  Column('asmt_type', String(32), CheckConstraint("asmt_type != ''"), nullable=False),
                                  Column('asmt_subject', String(64), CheckConstraint("asmt_subject != ''"), nullable=False),
                                  Column('asmt_year', SmallInteger, nullable=False),
                                  Column('created_date', TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()')),
                                  Column('acc_asl_video_embed', SmallInteger, nullable=False),
                                  Column('acc_braile_embed', SmallInteger, nullable=False),
                                  Column('acc_closed_captioning_embed', SmallInteger, nullable=False),
                                  Column('acc_text_to_speech_embed', SmallInteger, nullable=False),
                                  Column('acc_abacus_nonembed', SmallInteger, nullable=False),
                                  Column('acc_alternate_response_options_nonembed', SmallInteger, nullable=False),
                                  Column('acc_calculator_nonembed', SmallInteger, nullable=False),
                                  Column('acc_multiplication_table_nonembed', SmallInteger, nullable=False),
                                  Column('acc_print_on_demand_nonembed', SmallInteger, nullable=False),
                                  Column('acc_print_on_demand_items_nonembed', SmallInteger, nullable=False),
                                  Column('acc_read_aloud_nonembed', SmallInteger, nullable=False),
                                  Column('acc_scribe_nonembed', SmallInteger, nullable=False),
                                  Column('acc_speech_to_text_nonembed', SmallInteger, nullable=False),
                                  Column('acc_streamline_mode', SmallInteger, nullable=False),
                                  Column('acc_noise_buffer_nonembed', SmallInteger, nullable=False),
                                  Column('guid_batch', String(36), CheckConstraint("guid_batch != ''"), nullable=False),
                                  Column('asmt_status', String(2), nullable=False, server_default='OK'),
                                  Column('complete', Boolean, nullable=False, server_default=sqlalchemy.sql.expression.false()),
                                  )

    int_sbac_stu_reg = Table('int_sbac_stu_reg', metadata,
                             Column('record_sid', BigInteger, primary_key=True),
                             Column('name_state', String(50), CheckConstraint("name_state != ''"), nullable=False),
                             Column('code_state', String(2), CheckConstraint("code_state != ''"), nullable=False),
                             Column('guid_district', String(40), CheckConstraint("guid_district != ''"), nullable=False),
                             Column('name_district', String(60), CheckConstraint("name_district != ''"), nullable=False),
                             Column('guid_school', String(40), CheckConstraint("guid_school != ''"), nullable=False),
                             Column('name_school', String(60), CheckConstraint("name_school != ''"), nullable=False),
                             Column('guid_student', String(40), CheckConstraint("guid_student != ''"), nullable=False),
                             Column('external_ssid_student', String(40), nullable=True),
                             Column('name_student_first', String(35), nullable=True,),
                             Column('name_student_middle', String(35), nullable=True,),
                             Column('name_student_last', String(35), nullable=True,),
                             Column('birthdate_student', String(10), nullable=True,),
                             Column('sex_student', String(10), CheckConstraint("sex_student != ''"), nullable=False),
                             Column('grade_enrolled', String(2), CheckConstraint("grade_enrolled != ''"), nullable=False),
                             Column('dmg_eth_hsp', Boolean, nullable=False),
                             Column('dmg_eth_ami', Boolean, nullable=False),
                             Column('dmg_eth_asn', Boolean, nullable=False),
                             Column('dmg_eth_blk', Boolean, nullable=False),
                             Column('dmg_eth_pcf', Boolean, nullable=False),
                             Column('dmg_eth_wht', Boolean, nullable=False),
                             Column('dmg_multi_race', Boolean, nullable=False),
                             Column('dmg_prg_iep', Boolean, nullable=False),
                             Column('dmg_prg_lep', Boolean, nullable=False),
                             Column('dmg_prg_504', Boolean, nullable=True,),
                             Column('dmg_sts_ecd', Boolean, nullable=False),
                             Column('dmg_sts_mig', Boolean, nullable=True,),
                             Column('code_language', String(3), nullable=True,),
                             Column('eng_prof_lvl', String(20), nullable=True,),
                             Column('us_school_entry_date', String(10), nullable=True,),
                             Column('lep_entry_date', String(10), nullable=True,),
                             Column('lep_exit_date', String(10), nullable=True,),
                             Column('t3_program_type', String(27), nullable=True,),
                             Column('prim_disability_type', String(3), nullable=True,),
                             Column('created_date', TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()')),
                             Column('guid_batch', String(36), CheckConstraint("guid_batch != ''"), nullable=False),
                             )
    Index('int_sbac_stu_reg_guid_batchx', int_sbac_stu_reg.c.guid_batch, unique=False)

    int_sbac_stu_reg_meta = Table('int_sbac_stu_reg_meta', metadata,
                                  Column('record_sid', BigInteger, primary_key=True),
                                  Column('guid_registration', String(40), CheckConstraint("guid_registration != ''"), nullable=False),
                                  Column('academic_year', SmallInteger, nullable=False),
                                  Column('extract_date', String(10), CheckConstraint("extract_date != ''"), nullable=False),
                                  Column('test_reg_id', String(50), CheckConstraint("test_reg_id != ''"), nullable=False),
                                  Column('callback_url', String(512), CheckConstraint("callback_url != ''"), nullable=False),
                                  Column('created_date', TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()')),
                                  Column('guid_batch', String(36), CheckConstraint("guid_batch != ''"), nullable=False),
                                  )

    ref_column_mapping = Table('ref_column_mapping', metadata,
                               Column('column_map_key', BigInteger, primary_key=True),
                               Column('phase', SmallInteger, nullable=True),
                               Column('source_table', String(50), nullable=False),
                               Column('source_column', String(256), nullable=True),
                               Column('target_table', String(50), nullable=True),
                               Column('target_column', String(50), nullable=True),
                               Column('transformation_rule', String(50), nullable=True),
                               Column('stored_proc_name', String(256), nullable=True),
                               Column('stored_proc_created_date', TIMESTAMP(timezone=True), nullable=True),
                               Column('created_date', TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False),
                               )

    sr_ref_column_mapping = Table('sr_ref_column_mapping', metadata,
                                  Column('column_map_key', BigInteger, primary_key=True),
                                  Column('phase', SmallInteger, nullable=True),
                                  Column('source_table', String(50), nullable=False),
                                  Column('source_column', String(256), nullable=True),
                                  Column('target_table', String(50), nullable=True),
                                  Column('target_column', String(50), nullable=True),
                                  Column('transformation_rule', String(50), nullable=True),
                                  Column('stored_proc_name', String(256), nullable=True),
                                  Column('stored_proc_created_date', TIMESTAMP(timezone=True), nullable=True),
                                  Column('created_date', TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()')),
                                  )

    return metadata


def generate_udl2_sequences(schema_name=None, metadata=None):
    '''
    generate_udl2_sequences returns all udl2 related sequences as a tuple.
    '''
    seq1 = Sequence(name='global_rec_seq', start=1, increment=1, schema=schema_name,
                    optional=True, quote='Global record id sequences. form 1 to 2^63 -1 on postgresql', metadata=metadata)
    return (seq1, )
