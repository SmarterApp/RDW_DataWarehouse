from edextract.trackers.category_tracker import DataCounter

__author__ = 'ablum'

from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgDataProcessor
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants


class DistrictDataProcessor(EdOrgDataProcessor):

    def __init__(self, category_trackers):
        ed_org_hierarchy = {}
        super().__init__(category_trackers, ed_org_hierarchy)

    def process_yearly_data(self, data_row):
        self._call_academic_year_trackers(data_row[AttributeFieldConstants.DISTRICT_GUID], data_row)
        self._add_to_edorg_hierarchy(data_row[AttributeFieldConstants.DISTRICT_GUID],
                                     data_row[AttributeFieldConstants.STATE_NAME],
                                     data_row[AttributeFieldConstants.DISTRICT_NAME])

    def process_matched_ids_data(self, data_row):
        if self._is_matched_district(data_row):
            self._call_matched_ids_trackers(data_row[AttributeFieldConstants.DISTRICT_GUID], data_row)

    def _is_matched_district(self, data_row):
        return data_row[AttributeFieldConstants.DISTRICT_GUID] == data_row[AttributeFieldConstants.PREV_DISTRICT_GUID]
