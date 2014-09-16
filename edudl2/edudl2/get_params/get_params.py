import logging
from edudl2.json_util.json_util import get_value_from_json
from edudl2.udl2.constants import Constants

__author__ = 'ablum'
logger = logging.getLogger(__name__)


def get_callback_params_for_studentregistration(json_file_dir):
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
        student_reg_guid = get_value_from_json(json_file_dir, Constants.IDENTIFICATION_GUID)
        reg_system_id = get_value_from_json(json_file_dir, Constants.SOURCE_TESTREGSYSID)
        callback_url = get_value_from_json(json_file_dir, Constants.SOURCE_TESTREGCALLBACKURL)
        emailnotification = get_value_from_json(json_file_dir, Constants.EMAIL_NOTIFICATION)

    except KeyError:
        logger.error('Student Registration is not configured for callback notification')

    return student_reg_guid, reg_system_id, callback_url, emailnotification


def get_callback_params_for_assessment(json_file_dir):
    '''
    '''
    emailnotification = None
    try:
        callback_url = get_value_from_json(json_file_dir, Constants.SOURCE_CALLBACKURL)
        emailnotification = get_value_from_json(json_file_dir, Constants.EMAIL_NOTIFICATION)
    except KeyError:
        logger.error('Assessment is not configured for callback notification')
    return callback_url, emailnotification


def get_academic_year_param(json_file_dir):
    """
    Get the academic year parameter from the json file for this job

    @param json_file_dir: A directory that houses the json file

    @return: the academic year parameter
    @rtype: string
    """
    academic_year = None
    try:
        academic_year = get_value_from_json(json_file_dir, Constants.IDENTIFICATION_ACADEMICYEAR)

    except KeyError:
        logger.error('Not configured for academic year')

    if academic_year:
        return int(academic_year)
    else:
        return academic_year
