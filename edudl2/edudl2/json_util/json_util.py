# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

import os
import json
import logging

from requests.structures import CaseInsensitiveDict

from edudl2.udl2_util.file_util import open_udl_file

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

    with open_udl_file(json_file_path) as json_file:
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
