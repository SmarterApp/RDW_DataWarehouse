import os

from distutils.core import run_setup

here = os.path.abspath(os.path.dirname(__file__))

dependencies = [
    'config',
    'edschema']


for dependency in dependencies:
    pkg_path = os.path.abspath(here + "/../" + dependency + "/")
    os.chdir(pkg_path)
    run_setup("setup.py")
    os.chdir(here)
run_setup("setup.py")
