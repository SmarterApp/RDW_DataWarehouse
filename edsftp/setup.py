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

__author__ = 'sravi'

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = []

scripts = ['edsftp/scripts/sftp_driver.py']

tests_require = requires + [
    'nose == 1.3.0',
    'coverage == 3.6', ]

setup(name='edsftp',
      version='0.1',
      description='EdWare SFTP zone setup tool',
      classifiers=["Programming Language :: Python", ],
      author='',
      author_email='',
      url='',
      keywords='python sftp edware',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      scripts=scripts,
      tests_require=tests_require,
      entry_points="""\
      """,
      )
