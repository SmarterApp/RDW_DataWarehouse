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

import logging
from smarter_score_batcher.utils.constants import Constants
from datetime import datetime


def get_all_elements(root, xpath_of_element):
    '''
    Returns a list of dictionaries of element attributes for all the times the element appears
    :param root: xml root document
    :param xpath_of_element: xpath of element
    :returns: a list of matched elements
    '''
    list_of_dict = []
    for element_item in root.findall(xpath_of_element):
        attribute_dict = dict(element_item.items())
        list_of_dict.append(attribute_dict)
    return list_of_dict


def extract_meta_with_fallback_helper(root, element_xpath, attribute_to_get, attribute_to_compare):
    '''
    Returns the value in the attribute to get for the given element from the xml root provided.
    Handles context INITIAL and FINAL
    :param root: xml root document
    :param element_xpath: xpath of element
    :param attribute_to_get: attribute to get
    :param attribute_to_compare: attribute to compare
    :returns: matched element
    '''
    element = None
    if (root.find(element_xpath)) is not None:
        try:
            element = [e.get(attribute_to_get, Constants.DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib[attribute_to_compare] == Constants.ATTRIBUTE_CONTEXT_VALUE_FINAL][0]
        except IndexError:
            try:
                element = [e.get(attribute_to_get, Constants.DEFAULT_VALUE) for e in root.findall(element_xpath) if e.attrib[attribute_to_compare] == Constants.ATTRIBUTE_CONTEXT_VALUE_INITIAL][0]
            except IndexError:
                element = Constants.DEFAULT_VALUE
    return element


def extract_meta_without_fallback_helper(root, element_xpath, attribute_to_get):
    '''
    Returns the value in the attribute to get for the given element from the xml root provided.
    :param root: xml root document
    :param element_xpath: xpath of element
    :param attribute_to_get: attribute to get
    :returns: matched element
    '''
    element = None
    if (root.find(element_xpath)) is not None:
        if(root.find(element_xpath).get(attribute_to_get)) is not None:
            element = root.find(element_xpath).get(attribute_to_get, Constants.DEFAULT_VALUE)
    return element
