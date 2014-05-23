import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = ['pyyaml==3.10']

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='config',
      version='0.1',
      description='config',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application", ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      extras_require={
          'docs': docs_extras, },
      entry_points="""\
      """,
      )
