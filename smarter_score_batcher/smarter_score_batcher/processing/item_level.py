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

class ItemLevelCsvColumns:
    '''
    Constants for item level csv file
    '''
    # In the order of csv headers
    KEY = 'key'
    SEGMENT_ID = 'segmentId'
    POSTITION = 'position'
    CLIENT_ID = 'clientId'
    OPERATIONAL = 'operational'
    ISSELECTED = 'isSelected'
    FORMAT = 'format'
    SCORE = 'score'
    SCORE_STATUS = 'scoreStatus'
    ADMIN_DATE = 'adminDate'
    NUMBER_VISITS = 'numberVisits'
    STRAND = 'strand'
    CONTENT_LEVEL = 'contentLevel'
    PAGE_NUMBER = 'pageNumber'
    PAGE_VISITS = 'pageVisits'
    PAGE_TIME = 'pageTime'
    DROPPED = 'dropped'

    @staticmethod
    def get_item_level_csv_keys():
        '''
        Returns the landing zone format of assessment csv file
        :param self: self
        :returns: item levels for csv
        '''
        return [ItemLevelCsvColumns.KEY,
                ItemLevelCsvColumns.SEGMENT_ID,
                ItemLevelCsvColumns.POSTITION,
                ItemLevelCsvColumns.CLIENT_ID,
                ItemLevelCsvColumns.OPERATIONAL,
                ItemLevelCsvColumns.ISSELECTED,
                ItemLevelCsvColumns.FORMAT,
                ItemLevelCsvColumns.SCORE,
                ItemLevelCsvColumns.SCORE_STATUS,
                ItemLevelCsvColumns.ADMIN_DATE,
                ItemLevelCsvColumns.NUMBER_VISITS,
                ItemLevelCsvColumns.STRAND,
                ItemLevelCsvColumns.CONTENT_LEVEL,
                ItemLevelCsvColumns.PAGE_NUMBER,
                ItemLevelCsvColumns.PAGE_VISITS,
                ItemLevelCsvColumns.PAGE_TIME,
                ItemLevelCsvColumns.DROPPED]
