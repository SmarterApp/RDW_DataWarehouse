__author__ = 'sravi'

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = []

scripts = ['sftp_driver.py']

tests_require = requires + [
    'nose == 1.3.0',
    'coverage == 3.6', ]

setup(name='edsftp',
      version='0.1',
      description='EdWare SFTP zone setup tool',
      classifiers=["Programming Language :: Python", ],
      author='',
      author_email='',
      url='',
      keywords='python sftp edware',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      scripts=scripts,
      tests_require=tests_require,
      entry_points="""\
      """,
      )
