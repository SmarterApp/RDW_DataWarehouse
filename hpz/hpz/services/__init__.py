def includeme(config):
    '''
    Routes to service endpoints
    '''

    # heartbeat
    config.add_route('heartbeat', '/services/heartbeat')
