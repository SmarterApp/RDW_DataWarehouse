EDAPI_REPORTS_PLACEHOLDER = 'edapi_reports'

def add_report_config(self, delegate, **kwargs):
    # directive used to save report_config decorators to configurator registry
    settings = kwargs.copy()
    settings['reference'] = delegate
    
    # Create dictionary for reports if it doesn't exist
    if self.registry.get(EDAPI_REPORTS_PLACEHOLDER) is None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER] = {}
    # Only process decorators with an alias defined
    if settings.get('alias') is not None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER][settings['alias']] = settings
        
def includeme(config):
    # routing for retrieving list of report names with GET
    config.add_route('list_of_reports', '/report')
    # routing for the GET and OPTIONS verbs
    config.add_route('report_get_option', '/report/{name}')
    # routing for the POST verb 
    config.add_route('report_post', '/report/{name}/_query')
    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)
    # ignore test package
    config.scan(ignore='edapi.test')