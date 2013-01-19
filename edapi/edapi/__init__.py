EDAPI_REPORTS_PLACEHOLDER = 'edapi_reports'

def add_report_config(self, delegate, **kwargs):
    # directive used to save report_config decorators to configurator registry
    settings = kwargs.copy()
    #TODO validation for name, reference, duplicated name
    settings['reference'] = delegate
    if self.registry.get(EDAPI_REPORTS_PLACEHOLDER) is None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
    # Only process decorators with an name defined
    if settings.get('name') is not None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER][settings['name']] = settings
        
def includeme(config):
    # routing for retrieving list of report names with GET
    config.add_route('list_of_reports', '/data')
    # routing for the GET, POST, OPTIONS verbs
    config.add_route('report_get_option_post', '/data/{name}')
    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)
    # scans edapi, ignoring test package
    config.scan(ignore='edapi.test')
