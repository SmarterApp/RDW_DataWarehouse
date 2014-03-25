__author__ = 'npandey'

'''
School Data Processor for Student Registration Report
'''

from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgDataProcessor
from edextract.student_reg_extract_processors.attribute_constants import AttributeConstants


class SchoolDataProcessor(EdOrgDataProcessor):

    def __init__(self, category_trackers, ed_org_hierarchy):
        super().__init__(category_trackers, ed_org_hierarchy)

    def process_data(self, data_row):
        self._call_trackers(data_row[AttributeConstants.SCHOOL_GUID], data_row)
        self._add_to_edorg_heirarchy(data_row[AttributeConstants.SCHOOL_GUID], data_row[AttributeConstants.STATE_NAME],
                                     data_row[AttributeConstants.DISTRICT_NAME], data_row[AttributeConstants.SCHOOL_NAME])
