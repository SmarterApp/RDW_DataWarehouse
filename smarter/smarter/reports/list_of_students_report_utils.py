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
Created on Oct 21, 2014

@author: tosako
'''


def get_group_filters(results):
    # TODO: use list comprehension, format grouping information for filters
    all_groups = set()
    for result in results:
        for i in range(1, 11):
            if result['group_{i}_id'.format(i=i)]:
                all_groups.add((result['group_{i}_id'.format(i=i)], result['group_{i}_text'.format(i=i)]))

    options = [{"value": k, "label": v} for k, v in all_groups]
    filters = sorted(options, key=lambda k: k['label'])
    return filters


def __reverse_map(map_object):
    '''
    reverse map for FE
    '''
    return {v: k for k, v in map_object.items()}
