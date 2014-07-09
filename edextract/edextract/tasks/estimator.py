'''
Created on Jul 8, 2014

@author: tosako
'''
import logging
from edextract.data_extract_generation.item_level_generator import _get_path_to_item_csv
from edextract.utils.file_utils import generate_file_group


log = logging.getLogger('edextract')


def estimate_files(root_dir, state_code, asmt_year, asmt_type, asmt_subject, asmt_grade, threshold_size):
    path = _get_path_to_item_csv(root_dir, state_code=state_code, asmt_year=asmt_year, asmt_type=asmt_type,
                                 asmt_subject=asmt_subject, asmt_grade=asmt_grade)
    group = generate_file_group(path, threshold_size)
    return len(group)
