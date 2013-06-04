'''
Created on May 28, 2013

@author: swimberly
'''
from distutils.core import setup


requires = ['psycopg2',
            'SQLAlchemy',
            'py-postgresql',
            'mock',
            'zope.component >= 4.0.2',
            'zope.interface >= 4.0.3']

setup(name='CreateGenerateLoad',
      version='0.1',
      description="Script to Wrap all data generation steps",
      author="Amplify Insight Edware Team",
      author_email="edwaredev@wgen.net",
      packages=[],
      package_dir={},
      package_data={'udl2': ['datafiles/*.csv']},
      url='',
      requires=requires,
)
