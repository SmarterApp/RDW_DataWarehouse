__author__ = 'swimberly'


def get_move_to_target_conf():
    """
    configurations for move_to_target to match tables for foreign key rec ids for dim_asmt, dim_student,
    and dim_inst_hier. It also containts matcher configuration for UDL delete/update against production tables.
    :return:
    """

    conf = [
        {
            'rec_id': 'asmt_rec_id',
            'target_table': 'dim_asmt',
            'source_table': 'INT_SBAC_ASMT',
            'guid_column_name': 'asmt_guid',
            'guid_column_in_source': 'guid_asmt'
        },
        {
            'rec_id_map': ('inst_hier_rec_id', 'inst_hier_rec_id'),
            'table_map': ('dim_inst_hier', 'fact_asmt_outcome'),
            'guid_column_map': {
                'state_code': 'state_code',
                'district_guid': 'district_guid',
                'school_guid': 'school_guid'
            },
        },
        {
            'rec_id': 'section_rec_id',
            'value': '1'
        },
        {
            'rec_id_map': ('student_rec_id', 'student_rec_id'),
            'table_map': ('dim_student', 'fact_asmt_outcome'),
            'guid_column_map': {
                'student_guid': 'student_guid'
            },
        },
        {
            'prod_rec_id': 'asmnt_outcome_rec_id',
            'source_rec_id': 'asmnt_outcome_rec_id',
            'prod_table': 'fact_asmt_outcome',
            'source_table': 'fact_asmt_outcome',
            'matched_columns': [
                ('date_taken', 'date_taken'),
                ('asmt_guid', 'asmt_guid'),
                ('student_guid', 'student_guid')
            ],
            'matched_status': {
                'source_table': [('status', 'W')],
                'prod_table': [('status', 'C')]
            }
        },
        {
            'dim_tables': [
                {
                    'prod_table': 'dim_student',
                    'guid_column': 'student_guid',
                    'matched_columns': [
                        # 'student_rec_id',
                        # 'batch_guid',
                        'student_guid',
                        'first_name',
                        'middle_name',
                        'last_name',
                        'address_1',
                        'address_2',
                        'city',
                        'zip_code',
                        'gender',
                        'email',
                        'dob',
                        'section_guid',
                        'grade',
                        'state_code',
                        'district_guid',
                        'school_guid',
                        'from_date',
                        'to_date',
                        # 'most_recent',
                    ],
                    'update_columns': [
                        'student_rec_id'
                    ]
                }
            ]
        }]

    return conf
