import sys
__author__ = 'sravi'

from setuptools import setup, find_packages

requires = ['billiard==2.7.3.32',
            'celery == 3.0.23',
            'python-gnupg == 0.3.5',
            'anyjson == 0.3.3',
            'SQLAlchemy == 0.8.2',
            'psycopg2 == 2.5.1',
            'nose == 1.3.0',
            'coverage == 3.6',
            'nose-cov == 1.6',
            'mock == 1.0.1',
            'pep8 == 1.4.6',
            'py-postgresql == 1.1.0', 
            'config',
            'edcore',
            'edworker',
            'edschema']

requires.append('pyinotify') if sys.platform == 'linux' else None

tests_require = requires

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='edudl2',
      version='0.1',
      description='Universal data loader',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application", ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi edudl2 edware celery',
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
