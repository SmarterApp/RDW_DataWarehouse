import os

from setuptools import setup, find_packages
import shutil
from distutils.core import run_setup

here = os.path.abspath(os.path.dirname(__file__))

dependencies = [
    'edworker',
    'edcore',
    'edauth',
    'edschema',
    'hpz_client']


for dependency in dependencies:
    pkg_path = os.path.abspath(here + "/../" + dependency + "/")
    os.chdir(pkg_path)
    run_setup("setup.py")
    os.chdir(here)
run_setup("setup.py")
