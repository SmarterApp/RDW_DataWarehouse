import logging
from edudl2.json_util.json_util import get_value_from_json
from edudl2.udl2.celery import udl2_conf

__author__ = 'ablum'
logger = logging.getLogger(__name__)


def get_callback_param(json_file_dir, load_type, key_name):
    """
    Get the callback parameter for this UDL job from the json file

    @param json_file_dir: A directory that houses the json file
    @param load_type: The load type for the UDL job
    @param key_name: The configured key name for finding the path to the value in the json file

    @return: the callback parameter
    @rtype: string
    """

    param = None

    try:
        param_key_path = udl2_conf[key_name][load_type]
        param_keys = param_key_path.split('.')
        param = get_value_from_json(json_file_dir, *param_keys)

    except KeyError:
        logger.error('Loadtype %s is not configured for callback notification' % load_type)

    return param
