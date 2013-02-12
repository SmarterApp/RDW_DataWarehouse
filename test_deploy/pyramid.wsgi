import site
from pyramid.paster import get_app
# The path below is used for symbolic link to development.ini
ini_path = '/var/lib/jenkins/apache_dir/development_ini'
application = get_app(ini_path, 'main')
