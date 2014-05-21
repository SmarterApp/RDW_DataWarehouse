from jinja2 import Template, Environment, FileSystemLoader
import argparse

__author__ = 'npandey'


class CustomNS:
    pass


customNS = CustomNS()
parser = argparse.ArgumentParser(description='Generate HPZ apache config')
parser.add_argument('-v', help='Path to virtual environment', required=True)
parser.add_argument('-r', help='Path to local repository', required=True)
parser.add_argument('-u', help='User name', required=True)

args = parser.parse_args(namespace=customNS)


env = Environment(loader=FileSystemLoader('./'))

template = env.get_template('./wsgi_template')
templatevars = {'venv': customNS.v, 'repo': customNS.r, 'user': customNS.u}

result = template.render(templatevars)

with open('wsgi_hpz.conf', mode='w',) as new_file:
    new_file.write(result)
