'''
Created on Jan 24, 2013

@author: ejen
'''
from setuptools import setup, find_packages

requires = [
    'SQLAlchemy',
    "billiard==2.7.3.33",
    "celery==3.0.23",
    "anyjson",
    "amqp==1.0.11",
    "apscheduler",
    "python-gnupg"
]

tests_require = requires

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='edextract',
      version='0.1',
      description='Generic Request Extraction for Edware Reporting',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application", ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid celery',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          'docs': docs_extras, },
      entry_points="""\
      """,
      )
