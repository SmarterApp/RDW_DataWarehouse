import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid == 1.4',
    'pyramid_beaker==0.8',
    'SQLAlchemy==0.8.3',
    'transaction==1.4.1',
    'pyramid_tm==0.7',
    'pyramid_debugtoolbar==1.0.8',
    'zope.sqlalchemy==0.7.3',
    'waitress==0.8.7',
    'config',
    'edauth',
    'edapi',
    'edworker',
    'edschema',
    'edidentity',
    'py-postgresql==1.1.0',
    'psycopg2==2.5.1',
    'pyramid_exclog==0.7',
    'pyyaml==3.10',
    'requests == 2.2.1',
    'services',
    'python3-memcached == 1.51']

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='smarter',
      version='0.1',
      description='smarter',
      long_description=README + '\n\n' + CHANGES,
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
      test_suite='nose.collector',
      install_requires=requires,
      extras_require={
          'docs': docs_extras, },
      entry_points="""\
      [paste.app_factory]
      main = smarter:main
      [console_scripts]
      initialize_smarter_db = smarter.scripts.initializedb:main
      """
      )
