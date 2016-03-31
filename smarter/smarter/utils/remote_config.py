# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

'''
Created on Oct 23, 2013

@author: tosako
'''

from urllib import request
import configparser
import json
import uuid
from smarter.utils.constants import Constants


def get_remote_config(remote_url):
    '''
    Retrieve remote config in JSON format and convert to Pyramid config
    '''
    content = request.urlopen(remote_url).read().decode('utf-8')
    json_obj = json.loads(content)
    config = json_to_config(json_obj)
    return config


def json_to_config(json_obj):
    '''
    convert from JSON to config
    '''
    properties = json_obj[Constants.PROPERTIES]
    config = configparser.ConfigParser(allow_no_value=True)
    config[json_obj[Constants.ENVNAME]] = {}
    for property_json in properties:
        config[json_obj[Constants.ENVNAME]][property_json[Constants.PROPERTYKEY]] = property_json[Constants.PROPERTYVALUE]
    return config


def config_to_json(config, envName):
    '''
    convert from config to JSON
    '''
    json_obj = {}
    json_obj[Constants.ID] = str(uuid.uuid4())
    json_obj[Constants.NAME] = 'ini'
    json_obj[Constants.ENVNAME] = envName
    properties = []
    if envName in config:
        for k, v in config[envName].items():
            p = {}
            p[Constants.PROPERTYKEY] = k
            p[Constants.PROPERTYVALUE] = v
            p[Constants.ENCRYPT] = True
            properties.append(p)
        json_obj[Constants.PROPERTIES] = properties
    return json_obj
