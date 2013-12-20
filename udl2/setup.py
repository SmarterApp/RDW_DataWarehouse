'''
Created on May 2, 2013

@author: ejen
'''
from setuptools import setup
import sys

install_requires = ['billiard==2.7.3.32',
                    'celery == 3.0.23',
                    'Sphinx == 1.2b1',
                    'docutils == 0.11',
                    'repoze.sphinx.autointerface == 0.7.1',
                    'python-gnupg == 0.3.5',
                    'anyjson == 0.3.3',
                    'SQLAlchemy == 0.8.1',
                    'psycopg2 == 2.5.1',
                    'nose == 1.3.0',
                    'coverage == 3.6',
                    'nose-cov == 1.6',
                    'mock == 1.0.1',
                    'pep8 == 1.4.6',
                    'py-postgresql == 1.1.0', ]

install_requires.append('pyinotify') if sys.platform == 'linux' else None

scripts = ['scripts/initialize_udl2_database.sh',
           'scripts/initialize_udl2_system.sh',
           'scripts/initialize_udl2_database_user.sh',
           'scripts/initialize_udl2_directories.sh',
           'scripts/start_rabbitmq.sh',
           'scripts/start_celery.sh',
           'scripts/start_udl.sh',
           'scripts/teardown_udl2_database.sh',
           'scripts/initialize_udl2_database_user.py',
           'scripts/start_rabbitmq.py',
           'scripts/start_celery.py',
           'scripts/stop_celery.sh',
           'scripts/driver.py',
           'scripts/add_tenant.sh', ]

setup(name='udl2',
      version='0.1',
      description="Edware's Universal Data Loader",
      author="Amplify Insight Edware Team",
      author_email="edwaredev@wgen.net",
      packages=['fileloader', 'filearrived', 'filesplitter', 'post_etl', 'move_to_integration', 'move_to_target',
                'sfv', 'udl2', 'udl2_util', 'udl2_tests', 'fileexpander', 'filedecrypter', 'rule_maker',
                'rule_maker.makers', 'rule_maker.rules', 'preetl', 'scripts', 'benchmarking', 'file_finder'],
      package_dir={'fileloader': 'src/fileloader',
                   'filesplitter': 'src/filesplitter',
                   'post_etl': 'src/post_etl',
                   'move_to_integration': 'src/move_to_integration',
                   'move_to_target': 'src/move_to_target',
                   'sfv': 'src/sfv',
                   'udl2': 'src/udl2',
                   'udl2_util': 'src/udl2_util',
                   'udl2_tests': 'tests',
                   'rule_maker': 'src/rule_maker',
                   'preetl': 'src/preetl',
                   'scripts': 'scripts',
                   'benchmarking': 'benchmarking',
                   'fileexpander': 'src/fileexpander',
                   'filedecrypter': 'src/filedecrypter',
                   'filearrived': 'src/filearrived',
                   'file_finder': 'src/file_finder',
                   },
      package_data={'udl2': ['datafiles/*.csv']},
      url='https://github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0/',
      scripts=scripts,
      install_requires=install_requires,
      )
