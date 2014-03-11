import json
import os
import logging
from requests.structures import CaseInsensitiveDict

__author__ = 'tshewchuk'
logger = logging.getLogger(__name__)


def get_json_file_in_dir(json_file_dir):
    '''
    Get the name of the json file which resides in the directory
    @param json_file_dir: The directory which houses the json file
    @type string
    @return: JSON file name
    @rtype: string
    '''

    json_file_name = None
    for file_name in os.listdir(json_file_dir):
        if os.path.splitext(file_name)[1][1:].strip().lower() == 'json':
            json_file_name = file_name
            break

    if not json_file_name:
        raise IOError('No json file in upload file')

    return json_file_name


def get_attribute_value_from_json_keypath(json_file_path, *attribute_key_path):
    '''
    Determine the attribute value from the json file contents
    @param json_file_path: The full directory pathname of the json file
    @type string
    @param attribute_key_path: the key path to search the json for
    @type tuple
    @return: value of the key
    @rtype: string
    '''

    attribute_value = None

    with open(json_file_path) as json_file:
        try:
            json_object = json.load(json_file, object_hook=CaseInsensitiveDict)
            attribute_value = json_object
            for key in attribute_key_path:
                attribute_value = attribute_value.get(key)
        except ValueError:
            logger.error('Malformed json file %s' % json_file_path)
        except KeyError:
            logger.error('Cannot find key %s in file %s' % (str(attribute_key_path), json_file_path))
        except AttributeError:
            logger.error('The given path %s in file %s is invalid' % (str(attribute_key_path), json_file_path))

    return attribute_value


def get_value_from_json(json_file_dir, attribute_key_path):
    '''
    Gets a nested attribute from a json file
    @param json_file_dir: The directory name which contains a json file
    @type string
    @param attribute_key_path: The key for which to retrieve the value. A nested value can be denoted using '.' between each key.
    @type string
    @return: the value of the key from the json
    '''

    json_file_name = get_json_file_in_dir(json_file_dir)
    json_file_path = os.path.join(json_file_dir, json_file_name)

    keys = attribute_key_path.split('.')
    attribute = get_attribute_value_from_json_keypath(json_file_path, *keys)

    return attribute
