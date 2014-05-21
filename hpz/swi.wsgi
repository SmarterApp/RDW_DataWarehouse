import site
from pyramid.paster import get_app, setup_logging

# The path below is used for symbolic link to development.ini
ini_path = '/opt/edware/conf/hpz.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
