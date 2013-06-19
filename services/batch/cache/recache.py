'''
Created on Jun 19, 2013

@author: dip
'''
from services.tasks.cache.cache import cache_state_view_report,\
    cache_district_view_report
from batch.base import BatchBase


class Recache(BatchBase):

    def __init__(self, settings, tenant):
        super().__init__(settings, tenant)

        url = settings.get('application.url', 'localhost:6543')
        parsed_url = url.split(':')
        self.__host = parsed_url[0]
        self.__port = parsed_url[1]

    def send_state_recache_request(self, state_code):
        cache_state_view_report.delay(self.tenant, state_code, self.__host, self.__port, self.cookie_name, self.cookie_value)  # @UndefinedVariable

    def send_district_recache_request(self, state_code, district_guid):
        cache_district_view_report.delay(self.tenant, state_code, district_guid, self.__host, self.__port, self.cookie_name, self.cookie_value)  # @UndefinedVariable
