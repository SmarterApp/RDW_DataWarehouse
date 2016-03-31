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
Created on Aug 7, 2014

@author: tosako
'''

xsd = None


class XSD():
    '''
    XSD file data place holder
    '''
    def __init__(self, filepath):
        '''
        :param filepath: xsd file to read
        '''
        with open(filepath) as f:
            self.__xsd = f.read()

    def get_xsd(self):
        '''
        return xsd data
        :returns: xsd data
        '''
        return self.__xsd
