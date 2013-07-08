'''
Created on May 28, 2013

@author: swimberly
'''
from setuptools import setup, find_packages


requires = ['psycopg2',
            'SQLAlchemy',
            'py-postgresql',
            'mock',
            'zope.component >= 4.0.2',
            'zope.interface >= 4.0.3']

# setup(name='CreateGenerateLoad',
#       version='0.1',
#       description="Script to Wrap all data generation steps",
#       author="Amplify Insight Edware Team",
#       author_email="edwaredev@wgen.net",
#       packages=find_packages(),
#     packages=['datageneration', 'datainfo', 'dataload', 'henshin'],
#     package_dir={'datageneration': 'datageneration/src',
#                  'datainfo': 'datainfo',
#                  'dataload': 'dataload',
#                  'henshin': 'henshin/src'
#     },
#       package_data={'udl2': ['datafiles/*.csv']},
#       url='',
#       requires=requires,
# )


setup(name='CreateGenerateLoad',
      version='0.1',
      description="Script to Wrap all data generation steps",
      author="Amplify Insight Edware Team",
      author_email="edwaredev@wgen.net",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      entry_points="""\
      """,
)
