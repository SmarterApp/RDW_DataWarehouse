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
    'SQLAlchemy==0.9.9',
    'pyramid==1.4',
    'apscheduler==2.1.1',
    "python-gnupg==0.3.5",
    'requests == 2.2.1',
    'httpretty == 0.8.0',
    'psycopg2==2.5.1',
    'boto == 2.36.0',

    # current version of pyramid doesn't have fixed version of WebOb in its requirements
    # so we're fixing it here, because new versions are breaking the service
    # (it's starting to return unexpected HTTP status codes, e.g 404 instead of 412)
    # we should figure this out when we'll decide to upgrade pyramid version
    'WebOb==1.5.1',
]

tests_require = [
    'WebTest == 1.3.6',  # py3 compat
    'nose == 1.3.3',
    'coverage',
    'virtualenv']  # for scaffolding tests


docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='edcore',
      version='0.1',
      description='Generic Reporting Platform',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application", ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      test_suite="nose.collector",
      install_requires=install_requires,
      extras_require={
          'docs': docs_extras, },
      entry_points="""\
      """,
      )
