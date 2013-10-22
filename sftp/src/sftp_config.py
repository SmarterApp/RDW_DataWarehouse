__author__ = 'sravi'

sftp_conf = {
    'sftp_home': '/',
    'sftp_base_dir': 'sftp',
    'sftp_arrivals_dir': 'arrivals',
    'sftp_departures_dir': 'departures',
    'groups': ['sftparrivals', 'tenantadmin'],
    'group_directories': {
        'sftparrivals': 'arrivals',
        'tenantadmin': 'departures'
    }
}
