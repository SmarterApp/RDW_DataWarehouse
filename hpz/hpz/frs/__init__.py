__author__ = 'tshewchuk'


def includeme(config):
    '''
    Routes to service endpoints
    '''

    # Add File Registration end point
    config.add_route('registration', '/registration')

    # Add File Upload end point
    config.add_route('files_with_default_notification', '/files/default/{registration_id}')
    config.add_route('files_with_custom_notification', '/files/custom/{registration_id}')
