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

from edextract.trackers.category_tracker import DataCounter

__author__ = 'npandey'

'''
School Data Processor for Student Registration Report
'''

from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgDataProcessor
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants


class SchoolDataProcessor(EdOrgDataProcessor):

    def __init__(self, category_trackers):
        ed_org_hierarchy = {}
        super().__init__(category_trackers, ed_org_hierarchy)

    def process_yearly_data(self, data_row):
        self._call_academic_year_trackers(data_row[AttributeFieldConstants.SCHOOL_ID], data_row)
        self._add_to_edorg_hierarchy(data_row[AttributeFieldConstants.SCHOOL_ID], data_row[AttributeFieldConstants.STATE_NAME],
                                     data_row[AttributeFieldConstants.DISTRICT_NAME], data_row[AttributeFieldConstants.SCHOOL_NAME])

    def process_matched_ids_data(self, data_row):
        if self._is_matched_school(data_row):
            self._call_matched_ids_trackers(data_row[AttributeFieldConstants.SCHOOL_ID], data_row)

    def process_asmt_outcome_data(self, data_row):
        self._call_asmt_trackers(data_row[AttributeFieldConstants.SCHOOL_ID], data_row)

    def _is_matched_school(self, data_row):
        return data_row[AttributeFieldConstants.SCHOOL_ID] == data_row[AttributeFieldConstants.PREV_SCHOOL_ID]
