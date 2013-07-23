from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['psycopg2',
            'SQLAlchemy',
            'py-postgresql',
            'mock',
            'zope.component >= 4.0.2',
            'zope.interface >= 4.0.3']

tests_require = requires + [
    'nose >= 1.2.1',
    'coverage', ]

setup(name='DataGeneration',
      version='0.1',
      description='Data generator for edware',
      classifiers=[
          "Programming Language :: Python", ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      # packages=find_packages(),
      packages=['DataGeneration', 'DataGeneration.functional_tests', 'DataGeneration.src', 'DataGeneration.tests'],
      package_dir={'DataGeneration': '../DataGeneration',
                   },
      package_data={'DataGeneration': ['../DataGeneration/datafiles/*.csv', '../DataGeneration/datafiles/*/*']},
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      tests_require=tests_require,
      entry_points="""\
      """,
      )
