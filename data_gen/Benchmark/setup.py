from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['SQLAlchemy',
            'psycopg2',
            'mock', ]

tests_require = requires + [
    'sqlite3',
    'nose >= 1.2.1',
    'coverage', ]

setup(name='Benchmark',
      version='0.1',
      description='Edware Query Benchmark tool',
      classifiers=[
          "Programming Language :: Python", ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      tests_require=tests_require,
      entry_points="""\
      """,
      )
