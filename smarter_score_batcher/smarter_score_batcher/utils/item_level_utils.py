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
from smarter_score_batcher.utils.xml_utils import get_all_elements
from smarter_score_batcher.processing.item_level import ItemLevelCsvColumns

logger = logging.getLogger("smarter_score_batcher")


def get_item_level_data(root, meta):
    '''
    Generate and return item level data as list of lists for given xml root
    :param root: xml root document
    :returns: csv rows
    '''
    student_guid = meta.student_id
    matrix = []
    list_of_elements = get_all_elements(root, './Opportunity/Item')
    attribute_name_keys = ItemLevelCsvColumns.get_item_level_csv_keys()
    for element_item in list_of_elements:
        row = [element_item.get(key) for key in attribute_name_keys]
        row.insert(1, student_guid)
        matrix.append(row)
    return matrix
