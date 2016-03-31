# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid == 1.4',
    'pyramid_beaker==0.8',
    'SQLAlchemy==0.9.9',
    'transaction==1.4.1',
    'pyramid_tm==0.7',
    'pyramid_debugtoolbar==1.0.8',
    'zope.sqlalchemy==0.7.3',
    'waitress==0.8.7',
    'lxml==3.3.5',
    'config',
    'edcore',
    'edschema',
    'edapi',
    'edauth',
    'edworker',
    'smarter_common',
    'pyramid_exclog==0.7',
    'py-postgresql==1.1.0',
    'psycopg2==2.5.1',
    'python3-memcached == 1.51',

    # current version of pyramid doesn't have fixed version of WebOb in its requirements
    # so we're fixing it here, because new versions are breaking the service
    # (it's starting to return unexpected HTTP status codes, e.g 404 instead of 412)
    # we should figure this out when we'll decide to upgrade pyramid version
    'WebOb==1.5.1',
]

docs_extras = [
    'Sphinx',
    'docutils',
]

setup(
    name='smarter_score_batcher',
    version='0.1',
    description='smarter_score_batcher',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    extras_require={'docs': docs_extras},
    test_suite="smarter_score_batcher",
    entry_points="""\
      [paste.app_factory]
      main = smarter_score_batcher:main
      """,
)
