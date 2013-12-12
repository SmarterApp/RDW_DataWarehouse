__author__ = 'sravi'

sftp_conf = {
    'sftp_home': '/',
    'sftp_base_dir': 'sftp/opt/edware/home',
    'sftp_arrivals_dir': 'arrivals',
    'sftp_departures_dir': 'departures',
    'sftp_filerouter_dir': '',
    'user_home_base_dir': '/opt/edware/home',
    'group': 'edwaredataadmin',
    'roles': ['sftparrivals', 'sftpdepartures', 'filerouter'],
    'user_path_sftparrivals_dir': 'file_drop',
    'user_path_sftpdepartures_dir': 'reports',
    'user_path_filerouter_dir': 'route'
}
