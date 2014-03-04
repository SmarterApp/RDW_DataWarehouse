import logging
from edudl2.json_util.json_util import get_key_from_json
from edudl2.udl2.celery import udl2_conf

__author__ = 'ablum'
logger = logging.getLogger(__name__)


def get_callback_url(json_file_dir, load_type):
    """
    Get the callback url for this UDL job from the json file
    @param json_file_dir: A directory that houses the json file
    @return: the callback url
    @rtype: string
    """

    callback_url = None

    try:
        callback_url_key_path = udl2_conf['callback_url_key'][load_type]
        callback_url_keys = callback_url_key_path.split('.')
        callback_url = get_key_from_json(json_file_dir, *callback_url_keys)

    except KeyError:
        logger.error('Loadtype %s is not configured for callback notification' % load_type)

    return callback_url
