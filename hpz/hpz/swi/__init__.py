__author__ = 'okrook'


def includeme(config):
    '''
    Routes to service endpoints
    '''

    # Add File Download end point
    config.add_route('download', '/download/{reg_id}')
