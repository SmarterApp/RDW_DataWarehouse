import logging
from edudl2.json_util.json_util import get_value_from_json
from edudl2.udl2.celery import udl2_conf

__author__ = 'ablum'
logger = logging.getLogger(__name__)


def get_callback_params(json_file_dir, load_type):
    """
    Get the callback parameter for this UDL job from the json file

    @param json_file_dir: A directory that houses the json file
    @param load_type: The key path of an attribute in a nested json structure

    @return: the callback parameter
    @rtype: string
    """
    student_reg_guid = None
    reg_system_id = None
    callback_url = None

    try:
        student_reg_guid = get_value_from_json(json_file_dir, udl2_conf['student_reg_guid_key'][load_type])
        reg_system_id = get_value_from_json(json_file_dir, udl2_conf['reg_system_id_key'][load_type])
        callback_url = get_value_from_json(json_file_dir, udl2_conf['callback_url_key'][load_type])

    except KeyError:
        logger.error('Loadtype %s is not configured for callback notification' % load_type)

    return student_reg_guid, reg_system_id, callback_url


def get_academic_year_param(json_file_dir, load_type):
    """
    Get the academic year parameter from the json file for this job

    @param json_file_dir: A directory that houses the json file
    @param load_type: The key path of an attribute in a nested json structure

    @return: the academic year parameter
    @rtype: string
    """
    academic_year = None
    try:
        academic_year = get_value_from_json(json_file_dir, udl2_conf['academic_year_key'][load_type])

    except KeyError:
        logger.error('Loadtype %s is not configured for academic year' % load_type)

    return int(academic_year)
