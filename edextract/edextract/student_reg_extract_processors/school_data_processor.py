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
        self._call_academic_year_trackers(data_row[AttributeFieldConstants.SCHOOL_GUID], data_row)
        self._add_to_edorg_hierarchy(data_row[AttributeFieldConstants.SCHOOL_GUID], data_row[AttributeFieldConstants.STATE_NAME],
                                     data_row[AttributeFieldConstants.DISTRICT_NAME], data_row[AttributeFieldConstants.SCHOOL_NAME])

    def process_matched_ids_data(self, data_row):
        if self._is_matched_school(data_row):
            self._call_matched_ids_trackers(data_row[AttributeFieldConstants.SCHOOL_GUID], data_row)

    def process_asmt_outcome_data(self, data_row):
        pass

    def _is_matched_school(self, data_row):
        return data_row[AttributeFieldConstants.SCHOOL_GUID] == data_row[AttributeFieldConstants.PREV_SCHOOL_GUID]
