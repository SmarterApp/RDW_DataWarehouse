__author__ = 'swimberly'


def get_move_to_target_conf():
    """
    configurations for move_to_target to match tables for foreign key rec ids for dim_asmt, dim_student,
    and dim_inst_hier. It also containts matcher configuration for UDL delete/update against production tables.
    :return:
    """

    conf = {
        'asmt_rec_id': {
            'rec_id': 'asmt_rec_id',
            'target_table': 'dim_asmt',
            'source_table': 'int_sbac_asmt',
            'guid_column_name': 'asmt_guid',
            'guid_column_in_source': 'guid_asmt'
        },
        'section_rec_id_info': {
            'rec_id': 'section_rec_id',
            'value': '1'
        }
    }

    return conf
