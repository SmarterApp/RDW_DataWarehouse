__author__ = 'npandey'


class EdOrgDataProcessor:

    def __init__(self, category_trackers, ed_org_hierarchy):
        self.category_trackers = category_trackers
        self.ed_org_hierarchy = ed_org_hierarchy

    def _add_to_edorg_heirarchy(self, guid, state_name, district_name='', school_name=''):
        self.ed_org_hierarchy[(state_name, district_name, school_name)] = guid

    def _call_trackers(self, guid, data_row):
        for tracker in self.category_trackers:
            tracker.track(guid, data_row)

    def process_data(self, data_row):
        pass
