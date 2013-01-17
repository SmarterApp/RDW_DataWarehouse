def add_report_config(self, delegate, **kwargs):
    # directive used to save report_config decorators to configurator registry
    settings = kwargs.copy()
    #TODO validation for alias, reference, duplicated alias
    settings['reference'] = delegate
    self.registry[settings['alias']] = settings
        
def includeme(config):
    # routing for the GET and OPTIONS verbs
    config.add_route('report', '/report/{name}')
    # routing for the POST verb 
    config.add_route('report_for_post', '/report/{name}/_query')
    # directive to handle report_config decorators
    config.add_directive('add_report_config', add_report_config)
    # scans edapi, ignoring test package
    config.scan(ignore='edapi.test')