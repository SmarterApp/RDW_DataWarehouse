import json
import os
import logging
from udl2.celery import udl2_conf

__author__ = 'tshewchuk'

logger = logging.getLogger(__name__)

load_types = udl2_conf['load_type'].values()


def _has_duplicate_or_no_content_key(json_file_path, key, json_file_name):
    returnval = False
    with open(json_file_path) as file:
        found = False
        for line in file:
            line_key = line.split(':')[0].lower()
            if key in line_key:
                if found:
                    logger.error('Duplicate content in json file %s' % json_file_name)
                    returnval = True
                    break
                else:
                    found = True
        if not found:
            logger.error('Non-existent content in json file %s' % json_file_name)
            returnval = True
    return returnval


def _get_content_type_from_json(json_file_path, json_file_name):
    '''
    Determine the content type from the JSON file

    @param json_object: A dictionary that represents some json object
    @type json_object: dict
    @return: content type
    @rtype: string
    '''
    content = None
    with open(json_file_path) as file:
        try:
            json_object = json.load(file)
            for key in json_object:
                if key.lower() == udl2_conf['load_type_key']:
                    content = json_object.get(key).lower()
                    break
            if content not in load_types:
                logger.error('Invalid content specified in json file %s' % json_file_name)
        except ValueError:
            logger.error('Malformed json file %s' % json_file_name)
    return content


def get_load_type(dir_path, json_file):
    """
    Get the load type for this UDL job from the JSON file

    @param json_file_path: the full pathname of the JSON file
    @return: UDL job load type
    @rtype: string
    """
    json_file_path = os.path.join(dir_path, json_file)
    if _has_duplicate_or_no_content_key(json_file_path, 'content', json_file):
        raise KeyError('Non-existant or duplicate content in JSON file -- %s' % json_file)
    load_type = _get_content_type_from_json(json_file_path, json_file)
    if load_type not in load_types:
        raise ValueError('No valid load type specified in JSON file -- %s' % json_file)
    return load_type
