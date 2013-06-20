'''
Created on Jun 19, 2013

@author: dip
'''
from batch.base import BatchBase
from services.tasks.cache import cache_state_view_report, cache_district_view_report


class Recache(BatchBase):
    '''
    Re-caching reports for a particular tenant
    '''
    def __init__(self, settings, tenant):
        '''
        :params settings: python dictionary containing configurations
        :params tenant:  name of tenant used for batch re-caching of reports
        '''
        super().__init__(settings, tenant)

        url = settings.get('application.url')
        parsed_url = url.split(':')
        self.__host = parsed_url[0]
        self.__port = None
        if len(parsed_url) > 1:
            self.__port = parsed_url[1]

    def send_state_recache_request(self, state_code, namespace):
        '''
        Flushes comparing populations state view from cache and re-caches it by calling a celery task asynchronously

        :param state_code:  stateCode representing the state
        :param namespace:  the namespace used to cache state view report
        '''
        return cache_state_view_report.delay(self.tenant, state_code, self.__host, self.__port, self.cookie_name, self.cookie_value, namespace)  # @UndefinedVariable

    def send_district_recache_request(self, state_code, district_guid, namespace):
        '''
        Flushes comparing populations district view from cache and re-caches it by calling a celery task asynchronously

        :param state_code:  stateCode representing the state
        :param district_guid:  guid representing the district
        :param namespace:  the namespace used to cache district view report
        '''
        return cache_district_view_report.delay(self.tenant, state_code, district_guid, self.__host, self.__port, self.cookie_name, self.cookie_value, namespace)  # @UndefinedVariable
