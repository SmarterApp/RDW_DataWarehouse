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
Created on Sep 22, 2014

@author: agrebneva
'''


def deep_merge(dict1, dict2):
    '''
    deep merge of nested dicts
    '''
    dict_merge = dict1.copy()
    dict1_keys = dict1.keys()
    for k, v in dict2.items():
        if k in dict1_keys:
            if isinstance(dict1[k], dict) and isinstance(v, dict):
                dict_merge[k] = deep_merge(dict1[k], v)
            elif isinstance(v, dict) != isinstance(dict1[k], dict):
                raise Exception("Dictionaries are not mergable")
            else:
                dict_merge[k] = v
        else:
            dict_merge[k] = v
    return dict_merge
