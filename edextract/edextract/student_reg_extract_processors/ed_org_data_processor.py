__author__ = 'npandey'

from abc import ABCMeta, abstractmethod
from collections import namedtuple


EdOrgNameKey = namedtuple('EdOrgNameKey', ['state_code', 'district_name', 'school_name'])


class EdOrgDataProcessor(metaclass=ABCMeta):

    def __init__(self, category_trackers, ed_org_hierarchy):
        self.category_trackers = category_trackers
        self.ed_org_hierarchy = ed_org_hierarchy

    def _add_to_edorg_hierarchy(self, guid, state_code, district_name='', school_name=''):
        self.ed_org_hierarchy[EdOrgNameKey(state_code=state_code, district_name=district_name, school_name=school_name)] = guid

    def _call_academic_year_trackers(self, guid, data_row):
        for tracker in self.category_trackers:
            tracker.track_academic_year(guid, data_row)

    def _call_matched_ids_trackers(self, guid, data_row):
        for tracker in self.category_trackers:
            tracker.track_matched_ids(guid, data_row)

    def _call_asmt_trackers(self, guid, data_row):
        for tracker in self.category_trackers:
            tracker.track_asmt(guid, data_row)

    def get_ed_org_hierarchy(self):
        return self.ed_org_hierarchy

    @abstractmethod
    def process_yearly_data(self, data_row):
        return

    @abstractmethod
    def process_matched_ids_data(self, data_row):
        return

    @abstractmethod
    def process_asmt_outcome_data(self, data_row):
        return
