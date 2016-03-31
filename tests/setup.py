# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'selenium == 2.48.0',  # for UI testing
    'requests == 2.2.1',  # for restful web services
    'requests-toolbelt == 0.2.0',  # extension of Requests
    'sqlalchemy',  # for PostgreSQL python connection
    # 'pyramid >= 1.3.1',  # Using pyramid libraries for cookie creation
    'zope.component == 4.0.2',
    'zope.interface == 4.0.3',
    'psycopg2',
    'Sphinx==1.3.6',  # generate documentation
    'python-gnupg',
    'pytest == 2.8.5',  # tests runner
    'pytest-allure-adaptor == 1.6.8',  # create pretty HTML reports
]

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='edware_testing_automation',
      version='0.2',
      description='Provides code and/or sources for automation of EDWARE project testing',
      classifiers=[
          "Programming Language :: Python 3.3",
          "Functional Testing Framework :: pytest",
          "Web Automation Tool :: Selenium Webdriver",
          "HTML reporting :: Allure"
      ],
      packages=find_packages(),
      entry_points={
          'pytest11': [
              'webdriver-adaptor = edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor',
          ],
      },
      include_package_data=True,
      extras_require={'docs': docs_extras},
      zip_safe=False,
      install_requires=install_requires,
      )
