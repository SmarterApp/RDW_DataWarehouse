'''
Created on May 28, 2013

@author: swimberly
'''
# from distutils.core import setup
from setuptools import setup


requires = ['psycopg2',
            'SQLAlchemy==0.8.3',
            'py-postgresql',
            'mock',
            'zope.component == 4.1.0',
            'zope.interface == 4.0.3']


setup(name='CreateGenerateLoad',
      version='0.1',
      description="Script to Wrap all data generation steps",
      author="Amplify Insight Edware Team",
      author_email="edwaredev@wgen.net",
      packages=['edschema', 'edschema.metadata', 'edschema.tests',
                'Henshin', 'Henshin.src', 'Henshin.tests',
                'DataGeneration', 'DataGeneration.functional_tests', 'DataGeneration.src', 'DataGeneration.tests', 'DataGeneration.src.util_scripts',
                'datainfo',
                'dataload',
                ],
      package_dir={'edschema': '../../edschema/edschema',
                   'Henshin': '../Henshin',
                   'DataGeneration': '../DataGeneration',
                   'datainfo': '../DataGeneration/dataload/datainfo',
                   'dataload': '../DataGeneration/dataload',
                   },
      package_data={'Henshin': ['../Henshin/datafiles/*.json'],
                    'DataGeneration': ['../DataGeneration/datafiles/*.csv', '../DataGeneration/datafiles/name_lists/*']},
      # include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      entry_points="""\
      """,
      )
