from collections import OrderedDict
from udl2_util.measurement import measure_cpu_plus_elasped_time

# column mapping between source/integration table and target/star schema table
@measure_cpu_plus_elasped_time
def get_column_mapping(map_type):
    '''
    Key: {map_type}, e.g. 'unit_test', 'staging_to_integration_sbac_asmt_outcome',  'staging_to_integration_sbac_asmt'
    Value: {'source': 'table_name' , eg string for source table name
            'target': 'table_name', eg string for target table name
            'error': 'table_name', eg string for error table name that contain list we want to exclude
            'mapping': ordered dictionary: (column_in_target_table, (type_convertion_code, column_in_source_table)),
                e.g. ('asmt_guid': ('substr({src_field}, 1, 50)', guid_asmt'))
    @param map_type: type of mapping for task, this may be in long run be a databse object.
    '''
    column_mappings = {
        'unit_test' : {
          'source': 'STG_MOCK_LOAD',
          'target': 'INT_MOCK_LOAD',
          'error': 'ERR_LIST',
          'mapping': OrderedDict([
            ('batch_id', ("{src_field}", "batch_id")),
            ('substr_test', ("SUBSTR({src_field}, 1, 10)", "substr_test")),
            ('number_test', ("TO_NUMBER({src_field}, '99999')", "number_test")),
            ])
        },
        'staging_to_integration_sbac_asmt': {
            'source': 'STG_SBAC_ASMT',
            'target': 'INT_SBAC_ASMT',
            'error': 'ERR_LIST',
            'mapping': OrderedDict([
              ('batch_id', ("{src_field}", "batch_id")),
              ('substr_test', ("SUBSTR({src_field}, 1, 10)", "substr_test")),
              ('number_test', ("TO_NUMBER({src_field}, '99999')", "number_test")),
            ])
        },
        'staging_to_integration_sbac_asmt_outcome': {
            'source': 'STG_SBAC_ASMT_OUTCOME',
            'target': 'INT_SBAC_ASMT_OUTCOME',
            'error': 'ERR_LIST',
            'mapping': OrderedDict([
                ('batch_id', ("{src_field}", "batch_id",), ), # temporary hack to make it work. 
                ('guid_asmt', ("substr({src_field}, 1, 50)", "guid_asmt"), ),
                ('guid_asmt_location', ("substr({src_field}, 1, 50)", "guid_asmt_location"), ),
                ('name_asmt_location', ("substr({src_field}, 1, 256)", "name_asmt_location"), ),
                ('grade_asmt', ("substr({src_field}, 1, 10)", "grade_asmt"), ),
                ('name_state', ("substr({src_field}, 1, 32)", "name_state"), ),
                ('code_state', ("substr({src_field}, 1, 2)", "code_state"), ),
                ('guid_district', ("substr({src_field}, 1, 50)", "guid_district"), ),
                ('name_district', ("substr({src_field}, 1, 256)", "name_district"), ),
                ('guid_school', ("substr({src_field}, 1, 50)", "guid_school"), ),
                ('name_school', ("substr({src_field}, 1, 256)", "name_school"), ),
                ('type_school', ("substr({src_field}, 1, 20)", "type_school"), ),
                ('guid_student', ("substr({src_field}, 1, 50)", "guid_student"), ),
                ('name_student_first', ("substr({src_field}, 1, 256)", "name_student_first"), ),
                ('name_student_middle', ("substr({src_field}, 1, 256)", "name_student_middle"), ),
                ('name_student_last', ("substr({src_field}, 1, 256)", "name_student_last"), ),
                ('address_student_line1', ("substr({src_field}, 1, 256)", "address_student_line1"), ),
                ('address_student_line2', ("substr({src_field}, 1, 256)", "address_student_line2"), ),
                ('address_student_city', ("substr({src_field}, 1, 100)", "address_student_city"), ),
                ('address_student_zip', ("substr({src_field}, 1, 5)", "address_student_zip"), ),
                ('gender_student', ("substr({src_field}, 1, 10)", "gender_student"), ),
                ('email_student', ("substr({src_field}, 1, 256)", "email_student"), ),
                ('dob_student', ("substr({src_field}, 1, 8)", "dob_student"), ),
                ('grade_enrolled', ("substr({src_field}, 1, 10)", "grade_enrolled"), ),
                ('date_assessed', ("substr({src_field}, 1, 8)", "date_assessed"), ),
                ('date_taken_day', ("extract(day from to_date({src_field}, 'YYYYMMDD'))", "date_assessed"), ),
                ('date_taken_month', ("extract(month from to_date({src_field}, 'YYYYMMDD'))", "date_assessed"), ),
                ('date_taken_year', ("extract(year from to_date({src_field}, 'YYYYMMDD'))", "date_assessed"), ),
                ('score_asmt', ("to_number({src_field}, '99999')", "score_asmt" ), ), 
                ('score_asmt_min', ("to_number({src_field}, '99999')", "score_asmt_min"), ),
                ('score_asmt_max', ("to_number({src_field}, '99999')", "score_asmt_max"), ),
                ('score_perf_level', ("to_number({src_field}, '99999')", "score_perf_level"), ),
                ('score_claim_1', ("to_number(score_claim_1, '99999')", "score_claim_1"), ),
                ('score_claim_1_min', ("to_number({src_field}, '99999')", "score_claim_1_min"), ),
                ('score_claim_1_max', ("to_number({src_field}, '99999')", "score_claim_1_max"), ),
                ('score_claim_2', ("to_number({src_field}, '99999')", "score_claim_2"), ),
                ('score_claim_2_min', ("to_number({src_field}, '99999')", "score_claim_2_min"), ),
                ('score_claim_2_max', ("to_number({src_field}, '99999')", "score_claim_2_max"), ),
                ('score_claim_3', ("to_number({src_field}, '99999')", "score_claim_3"), ),
                ('score_claim_3_min', ("to_number({src_field}, '99999')", "score_claim_3_min"), ),
                ('score_claim_3_max', ("to_number({src_field}, '99999')", "score_claim_3_max"), ),
                ('score_claim_4', ("to_number({src_field}, '99999')", "score_claim_4"), ),
                ('score_claim_4_min', ("to_number({src_field}, '99999')", "score_claim_4_min"), ),
                ('score_claim_4_max', ("to_number({src_field}, '99999')", "score_claim_4_max"), ),
                ('guid_staff', ("substr({src_field}, 1, 50)", "guid_staff"), ), 
                ('name_staff_first', ("substr({src_field}, 1, 256)", "name_staff_first"), ),
                ('name_staff_middle', ("substr({src_field}, 1, 256)", "name_staff_middle"), ),
                ('name_staff_last', ("substr({src_field}, 1, 256)", "name_staff_last"), ),
                ('type_staff', ("substr({src_field}, 1, 10)", "type_staff"), ),
                ('created_date', ("{src_field}", "created_date"), ), # temporary hack to make it work.
        ])},
    }
    return column_mappings[map_type]