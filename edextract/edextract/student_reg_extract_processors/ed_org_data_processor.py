__author__ = 'npandey'

from abc import ABCMeta, abstractmethod
from collections import namedtuple


EdOrgNameKey = namedtuple('EdOrgNameKey', ['state_name', 'district_name', 'school_name'])


class EdOrgDataProcessor(metaclass=ABCMeta):

    def __init__(self, category_trackers, ed_org_hierarchy):
        self.category_trackers = category_trackers
        self.ed_org_hierarchy = ed_org_hierarchy

    def _add_to_edorg_hierarchy(self, guid, state_name, district_name='', school_name=''):
        self.ed_org_hierarchy[EdOrgNameKey(state_name=state_name, district_name=district_name, school_name=school_name)] = guid

    def _call_trackers(self, guid, data_row):
        for tracker in self.category_trackers:
            tracker.track(guid, data_row)

    def get_ed_org_hierarchy(self):
        return self.ed_org_hierarchy

    @abstractmethod
    def process_data(self, data_row):
        return
