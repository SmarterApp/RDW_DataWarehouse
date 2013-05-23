from collections import OrderedDict

# column mapping between source/integration table and target/star schema table
def get_column_mapping(map_type):
    '''
    Key: {target table name}, e.g. dim_asmt
    Value: ordered dictionary: (column_in_target_table, column_in_source_table), e.g. 'asmt_guid': 'guid_asmt'
    '''
    column_mappings = {
        'sbac_staging_to_integration': {
            'source': 'STG_SBAC_ASMT_OUTCOME',
            'target': 'INT_SBAC_ASMT_OUTCOME',
            'mapping': OrderDict([
            ('batch_id', "batch_id",),
            ('guid_asmt', "substr(guid_asmt, 0, 50)", ),
            ('guid_asmt_location', "substr(guid_asmt_location, 0, 50)",),
            ('name_asmt_location', "substr(name_asmt_location, 0, 256)",),
            ('grade_asmt', "substr(grade_asmt, 0, 10)", ),
            ('inst_hier_guid', "substr(inst_hier_guid, 0, 50)",),
            ('name_state', "substr(name_state, 0, 32)", ),
            ('code_state', "substr(code_state, 0, 2)", ),
            ('guid_district', "substr(guid_district, 0, 50)", ),
            ('name_district', "substr(name_district, 0, 256)", ),
            ('guid_school', "substr(guid_school, 0, 50)", ),
            ('name_school', "substr(name_school, 0, 256)", ),
            ('type_school', "substr(type_school, 0, 20)", ),
            ('guid_student', "substr(guid_student, 0, 50)", ),
            ('name_student_first', "substr(name_student_first, 0, 256)", ),
            ('name_student_middle', "substr(name_student_middle, 0, 256)",  ),
            ('name_student_last', "substr(name_student_last, 0, 256)", ),
            ('address_student_line1', "substr(address_student_line1, 0, 256)", ),
            ('address_student_line2', "substr(address_student_line2, 0, 256)", ),
            ('address_student_city', "substr(address_student_city, 0, 100)", ),
            ('address_student_zip', "substr(address_student_zip, 0, 5)", ),
            ('gender_student', "substr(gender_student, 0, 10)", ),
            ('email_student', "substr(email_student, 0, 256)",),
            ('dob_student', "substr(dob_student, 0, 8)", ),
            ('grade_enrolled', "substr(grade_enrolled, 0, 10)", ),
            ('date_assessed', "substr(date_assessed, 0, 8)", ),
            ('score_asmt', "to_number(score_asmt, '99999')", ),
            ('score_asmt_min', "to_number(score_asmt_min, '99999')", ),
            ('score_asmt_max', "to_number(score_asmt_max, '99999')", ),
            ('score_perf_level', "to_number(score_perf_level, '99999')", ),
            ('score_claim_1', "to_number(score_claim_1, '99999')", ),
            ('score_claim_1_min', "to_number(score_claim_1_min, '99999')", ),
            ('score_claim_1_max', "to_number(score_claim_1_max, '99999')", ),
            ('score_claim_2', "to_number(score_claim_2, '99999')", ),
            ('score_claim_2_min', "to_number(score_claim_2_min, '99999')", ),
            ('score_claim_2_max', "to_number(score_claim_2_max, '99999')", ),
            ('score_claim_3', "to_number(score_claim_3, '99999')", ),
            ('score_claim_3_min', "to_number(score_claim_3_min, '99999')", ),
            ('score_claim_3_max', "to_number(score_claim_3_max, '99999')", ),
            ('score_claim_4', "to_number(score_claim_4, '99999')", ),
            ('score_claim_4_min', "to_number(score_claim_4_min, '99999')", ),
            ('score_claim_4_max', "to_number(score_claim_4_max, '99999')", ),
            ('guid_staff', "substr(guid_staff, 0, 50)",),
            ('name_staff_first', "substr(name_staff_first, 0, 256)",),
            ('name_staff_middle', "substr(name_staff_middle, 0, 256)", ),
            ('name_staff_last', "substr(name_staff_last, 0, 256)", ),
            ('type_staff', "substr(type_staff, 0, 10)",),
            ('created_date', 'created_date', ),
        ])},
    }
    return column_mappings[map_type]