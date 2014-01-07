'''
Created on Jan 24, 2013

@author: ejen
'''
from setuptools import setup, find_packages

requires = [
    'SQLAlchemy==0.8.2',
    "billiard==2.7.3.32",
    "celery==3.0.23",
    "anyjson==0.3.3",
    "amqp==1.0.13",
    "apscheduler==2.1.1",
    "python-gnupg==0.3.5"
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
