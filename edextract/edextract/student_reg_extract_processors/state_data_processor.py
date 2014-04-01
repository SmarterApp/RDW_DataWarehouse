from edextract.trackers.category_tracker import DataCounter

__author__ = 'npandey'

from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgDataProcessor
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants


class StateDataProcessor(EdOrgDataProcessor):

    def __init__(self, category_trackers):
        ed_org_hierarchy = {}
        super().__init__(category_trackers, ed_org_hierarchy)

    def process_yearly_data(self, data_row):
        self._call_trackers(data_row[AttributeFieldConstants.STATE_CODE], data_row)
        self._add_to_edorg_hierarchy(data_row[AttributeFieldConstants.STATE_CODE], data_row[AttributeFieldConstants.STATE_NAME])

    def process_matched_ids_data(self, data_row):
        self._call_trackers(data_row[AttributeFieldConstants.STATE_CODE], data_row, DataCounter.MATCHED_IDS)
