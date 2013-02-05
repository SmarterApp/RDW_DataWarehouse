import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'nose',  # functional testing framework
    'selenium',  # for UI testing
    'Requests',  # for restful web services
    'virtualenv'  # for scaffolding tests
]

setup(name='functional_tests',
      version='0.1',
      description='Functional tests for the edware project',
      classifiers=[
          "Programming Language :: Python 3.3",
          "Functional Testing Framework :: Pyunit/nosetests",
          "Web Automation Tool :: Selenium Webdriver"
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=["file://"+os.path.abspath(here + "/../" + "resource/selenium-2.29.0-wgen#egg=selenium-wgen")],
      install_requires=install_requires,
      )
