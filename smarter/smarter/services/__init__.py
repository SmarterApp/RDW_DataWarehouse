'''
Services are endpoints that extend and support SBAC reports, such as
heartbeat, pdf generation, cache management, and triggering of batch jobs.
'''


def includeme(config):
    '''
    Routes to service endpoints
    '''
    # Add heartbeat
    config.add_route('heartbeat', '/services/heartbeat')

    # Add pdf
    config.add_route('pdf', '/services/pdf/{report}')

    # Add cache management
    config.add_route('cache_management', '/services/cache/{cache_name}')

    # Add trigger endpoints
    config.add_route('trigger', '/services/trigger/{trigger_type}')

    # Add user information endpoints
    config.add_route('user_info', '/services/userinfo')

    # Add extract
    config.add_route('extract', '/services/extract')

    # Add extract for item level data
    config.add_route('assessment_item_level', '/services/extract/assessment_item_level')

    # Add extract for raw xml data
    config.add_route('raw_data', '/services/extract/raw_data')

    # Add extract for student registration statistics
    config.add_route('student_registration_statistics', '/services/extract/student_registration_statistics')

    # Add extract for student registration completion
    config.add_route('student_registration_completion', '/services/extract/student_registration_completion')
