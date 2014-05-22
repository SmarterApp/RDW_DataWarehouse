from jinja2 import Template, Environment, FileSystemLoader
import argparse

__author__ = 'npandey'


class CustomNS:
    pass


customNS = CustomNS()
parser = argparse.ArgumentParser(description='Generate HPZ apache config')
parser.add_argument('-v', help='Path to virtual environment', required=True)
parser.add_argument('-r', help='Path where local edware repository resides', required=True)
parser.add_argument('-u', help='User name', required=True)

args = parser.parse_args(namespace=customNS)


env = Environment(loader=FileSystemLoader('./'))

# Generate conf for frs
template = env.get_template('./wsgi_frs_template')
templatevars = {'venv': customNS.v, 'repo': customNS.r, 'user': customNS.u}

result = template.render(templatevars)

with open('wsgi_frs_hpz.conf', mode='w',) as new_file:
    new_file.write(result)

# Generate conf for swi
template = env.get_template('./wsgi_swi_template')
templatevars = {'venv': customNS.v, 'repo': customNS.r, 'user': customNS.u}

result = template.render(templatevars)

with open('wsgi_swi_hpz.conf', mode='w',) as new_file:
    new_file.write(result)
