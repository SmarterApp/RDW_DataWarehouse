import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'nose >= 1.2.1',  # functional testing framework
    'nose-exclude',
    'selenium == 2.48.0',  # for UI testing
    'requests >= 2.2.1',  # for restful web services
    'requests-toolbelt >= 0.2.0',  # extension of Requests
    'sqlalchemy',  # for PostgreSQL python connection
    # 'pyramid >= 1.3.1',  # Using pyramid libraries for cookie creation
    'zope.component >= 4.0.2',
    'zope.interface >= 4.0.3',
    'psycopg2',
    # 'sphinx',
    'python-gnupg',
    'pytest >= 2.8.5',  # tests runner
    'pytest-allure-adaptor >= 1.6.8',  # create pretty HTML reports
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
      include_package_data=True,
      extras_require={'docs': docs_extras,},
      zip_safe=False,
      install_requires=install_requires,
      )
