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
Created on Oct 25, 2013

@author: tosako
'''
import unittest
import os
from smarter.utils.remote_config import get_remote_config, json_to_config,\
    config_to_json
import json
import configparser
from smarter.utils.constants import Constants


class Test(unittest.TestCase):

    def test_get_remote_config(self):
        here = os.path.abspath(os.path.dirname(__file__))
        config_json = os.path.abspath(os.path.join(here, 'config.json'))
        config = get_remote_config('file:' + config_json)
        app_main = config['app:main']
        self.assertEqual(62, len(app_main.items()))
        self.assertEqual("True", app_main.get('pyramid.reload_templates'))

    def test_json_to_config(self):
        json_string = '''{
          "properties": [
            {
              "encrypt": true,
              "propertyValue": "hello world",
              "propertyKey": "test.abc"
            }
          ],
          "id": "8bc6dad5-f013-4ae5-9b8a-5fd4dd2cae6d",
          "envName": "app:main",
          "name": "ini"
        }'''
        json_obj = json.loads(json_string)
        config = json_to_config(json_obj)
        app_main = config['app:main']
        self.assertEqual(1, len(app_main.items()))
        self.assertEqual('hello world', app_main.get('test.abc'))

    def test_config_to_json(self):
        ini_string = '''[app:main]
        test.abc = hello world
        '''
        config = configparser.ConfigParser()
        config.read_string(ini_string)
        json_obj = config_to_json(config, 'app:main')
        self.assertEqual(1, len(json_obj[Constants.PROPERTIES]))
        self.assertEqual('test.abc', json_obj[Constants.PROPERTIES][0][Constants.PROPERTYKEY])
        self.assertEqual('hello world', json_obj[Constants.PROPERTIES][0][Constants.PROPERTYVALUE])
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
