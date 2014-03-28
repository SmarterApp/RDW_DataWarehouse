from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['psycopg2',
            'SQLAlchemy==0.8.3',
            'py-postgresql',
            'mock',
            'zope.component >= 4.0.2',
            'zope.interface >= 4.0.3',
            'Sphinx',
            'docutils',
            'repoze.sphinx.autointerface',
            'PyYAML']

tests_require = requires + [
    'nose >= 1.2.1',
    'pep8',
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
      packages=['DataGeneration', 'DataGeneration.functional_tests', 'DataGeneration.src', 'DataGeneration.src.configs',
                'DataGeneration.src.calc', 'DataGeneration.src.constants', 'DataGeneration.src.generators',
                'DataGeneration.src.models', 'DataGeneration.src.utils', 'DataGeneration.src.writers',
                'DataGeneration.src.demographics', 'DataGeneration.tests', 'edschema', 'edschema.metadata'],
      package_dir={'DataGeneration': '../DataGeneration',
                   'edschema': os.path.join('..', '..', 'edschema', 'edschema'),
                   },
      package_data={'DataGeneration': ['../DataGeneration/datafiles/*.csv', '../DataGeneration/datafiles/name_lists/*',
                                       '../DataGeneration/datafiles/mappings.json', '../DataGeneration/datafiles/configs/*.yaml',
                                       '../DataGeneration/src/configs/*.yaml']},
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      tests_require=tests_require,
      entry_points="""\
      """,
      )
