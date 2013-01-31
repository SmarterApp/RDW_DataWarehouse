import os

from setuptools import setup, find_packages
import shutil
from distutils.core import run_setup

here = os.path.abspath(os.path.dirname(__file__))

dependencies = [
    'edapi',
    'edschema', ]


class EasyOver:
    def __init__(self, dependency_name):
        self.__dependency_name = dependency_name
        self.__pkg_path = os.path.abspath(here + "/../" + dependency_name + "/")
        for path in os.sys.path:
            if(path.endswith('site-packages')):
                self._site_packages = path

    def write_egg_link(self):
        egg_file = self._site_packages + "/" + self.__dependency_name + ".egg-link"
        if not os.path.isfile(egg_file):
            f = open(egg_file, "w")
            f.write(self.__pkg_path + "\n.")
            f.close()

    def update_easy_install_pth(self):
        f = open(self._site_packages + "/easy-install.pth", "r+")
        pkg_name = []
        for line in f:
            pkg_name.append(line.rstrip(os.linesep))
        if not self.__pkg_path in pkg_name:
            f.write(self.__pkg_path + os.linesep)
        f.close()

    def run_setup(self):
        run_setup(self.__pkg_path + "/setup.py")
        self.write_egg_link()
        self.update_easy_install_pth()


run_setup("setup.py")
for dependency in dependencies:
    easyOver = EasyOver(dependency)
    easyOver.run_setup()
