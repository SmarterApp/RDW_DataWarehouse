'''
Created on May 2, 2013

@author: ejen
'''
from setuptools import setup
import sys

install_requires = ['celery >= 3.0.19',
                    'Sphinx',
                    'docutils',
                    'repoze.sphinx.autointerface',
                    'python-gnupg',
                    'anyjson >= 0.3.3',
                    #'amqp >= 1.3.0',
                    'SQLAlchemy >= 0.8.1',
                    'psycopg2 >= 2.5',
                    'nose >= 1.3.0',
                    'coverage >= 3.6',
                    'nose-cov >= 1.6',
                    'mock >= 1.0.1',
                    'pep8 >= 1.4.5',
                    'py-postgresql >= 1.1.0', ]

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
      packages=['edschema', 'edschema.metadata', 'edschema.tests', 'fileloader', 'filearrived', 'filesplitter', 'post_etl', 'move_to_integration',
                'move_to_target', 'sfv', 'udl2', 'udl2_util', 'udl2_tests', 'fileexpander', 'filedecrypter',
                'rule_maker', 'rule_maker.makers', 'rule_maker.rules', 'preetl', 'scripts', 'benchmarking'],
      package_dir={'edschema': '../edschema/edschema',
                   'fileloader': 'src/fileloader',
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
                   },
      package_data={'udl2': ['datafiles/*.csv']},
      url='https://github.wgenhq.net/Ed-Ware-SBAC/edware-udl-2.0/',
      scripts=scripts,
      install_requires=install_requires,
      data_files=[('/var/log/wgen/edware-udl/logs', ['logs/udl2.audit.log', 'logs/udl2.error.log']),
                  ('/opt/wgen/edware-udl/etc', ['conf/udl2_conf.ini', 'conf/udl2_conf.cfg', 'conf/udl2_conf.py']),
                  ('/opt/wgen/edware-udl/zones/datafiles/', ['src/udl2/datafiles/seed.csv']),
                  ('/opt/wgen/edware-udl/zones/datafiles/keys', ['tests/data/keys/pubring.gpg',
                                                                 'tests/data/keys/secring.gpg',
                                                                 'tests/data/keys/trustdb.gpg']),
                  ('/opt/wgen/edware-udl/zones/datafiles/', ['tests/data/valid_csv.csv',
                                                             'tests/data/invalid_ext.xls',
                                                             'tests/data/METADATA_ASMT_3003.json',
                                                             'tests/data/METADATA_ASMT_ValidData.json',
                                                             'tests/data/REALDATA_3010.xlsx',
                                                             'tests/data/realdata_3009.csv',
                                                             'tests/data/METADATA_ASMT_3012.json',
                                                             'tests/data/REALDATA_3005.csv',
                                                             'tests/data/REALDATA_3011.csv',
                                                             'tests/data/realdata_3003.csv',
                                                             'tests/data/test_file_headers.csv',
                                                             'tests/data/METADATA_ASMT_3013.json',
                                                             'tests/data/REALDATA_3008.csv',
                                                             'tests/data/REALDATA_ASMT_ValidData.csv',
                                                             'tests/data/realdata_3008_3011.csv',
                                                             'tests/data/test_file_realdata.csv',
                                                             'tests/data/test_file_stored_proc_data.csv',
                                                             'tests/data/test_file_stored_proc_data_CLEAN.csv',
                                                             'tests/data/Benchmarking_json_file.json',
                                                             'tests/data/BENCHMARK_DATA.csv',
                                                             'tests/data/test_source_file_tar_gzipped.tar.gz',
                                                             'tests/data/test_corrupted_source_file_tar_gzipped.tar.gz',
                                                             'tests/data/test_absolute_path_coded_files.tar.gz',
                                                             'tests/data/test_missing_json_file.tar.gz',
                                                             'tests/data/test_source_file_tar_gzipped.tar.gz.gpg',
                                                             'tests/data/test_empty_jsonfile.tar.gz.gpg',
                                                             'tests/data/test_corrupted_source_file_tar_gzipped.tar.gz.gpg',
                                                             'tests/data/test_absolute_path_coded_files.tar.gz.gpg',
                                                             'tests/data/test_corrupted_json_file.tar.gz.gpg',
                                                             'tests/data/test_missing_json_file.tar.gz.gpg',
                                                             'tests/data/INT_SBAC_ASMT.csv',
                                                             'tests/data/INT_SBAC_ASMT_OUTCOME.csv']),
                  ],
      )
