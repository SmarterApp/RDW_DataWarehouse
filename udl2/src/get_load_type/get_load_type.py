import json
import os
import logging
from udl2.celery import udl2_conf

__author__ = 'tshewchuk'

logger = logging.getLogger(__name__)

load_types = udl2_conf['load_type'].values()


def _get_json_file_in_dir(json_file_dir):
    '''
    Get the name of the json file which resides in the directory
    @param json_file_dir: A directory that houses the json file
    @type string
    @return: JSON file name
    @rtype: string
    '''
    for file_name in os.listdir(json_file_dir):
        if file_name.split('.')[-1] == 'json':
            return file_name 
    return None


def _get_load_type_from_json(json_file_dir):
    '''
    Determine the udl load type from the json file in the directory
    @param json_file_dir: A directory that houses the json file
    @type string
    @return: UDL load type, JSON file name (for error reporting)
    @rtype: string, string
    '''
    json_file_name = _get_json_file_in_dir(json_file_dir)
    json_file_path = os.path.join(json_file_dir, json_file_name)
    load_type = None
    with open(json_file_path) as json_file:
        try:
            json_object = json.load(json_file)
            load_type_key = udl2_conf['load_type_key']
            for key in json_object:
                if key.lower() == load_type_key:
                    load_type = json_object.get(key).lower()
                    break
            if load_type not in load_types:
                logger.error('Invalid load type specified in json file %s' % json_file_name)
        except ValueError:
            logger.error('Malformed json file %s' % json_file_name)
    return load_type, json_file_name


def get_load_type(json_file_dir):
    """
    Get the load type for this UDL job from the json file
    @param json_file_dir: A directory that houses the json file
    @return: UDL job load type
    @rtype: string
    """
    load_type, json_file_name = _get_load_type_from_json(json_file_dir)
    if load_type not in load_types:
        raise ValueError('No valid load type specified in json file -- %s' % json_file_name)
    return load_type
