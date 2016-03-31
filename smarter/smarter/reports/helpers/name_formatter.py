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
Helper functions to format names for display on reports

Created on Mar 4, 2013

@author: dwu
'''


def format_full_name(first_name, middle_name, last_name):
    '''
    Format a name to "<first> <middle init> <last>"
    '''
    if (middle_name is not None) and (len(middle_name) > 0):
        middle_init = middle_name[0] + '.'
    else:
        middle_init = ''
    return "{0} {1} {2}".format(first_name, middle_init, last_name).replace('  ', ' ')


def format_full_name_rev(first_name, middle_name, last_name):
    '''
    Format a name to "<last>, <first> <middle init>"
    '''
    if (middle_name is not None) and (len(middle_name) > 0):
        middle_init = middle_name[0] + '.'
    else:
        middle_init = ''
    return "{0}, {1} {2}".format(last_name, first_name, middle_init).replace('  ', ' ')
