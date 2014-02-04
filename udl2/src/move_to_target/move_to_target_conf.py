__author__ = 'swimberly'


def get_move_to_target_conf():
    """

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
        }]
    return conf