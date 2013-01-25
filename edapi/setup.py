import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

install_requires = [
    'pyramid == 1.3.1',
    'venusian >= 1.0a3',
    'validictory == 0.8'
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'nose',
    'coverage',
    'virtualenv'  # for scaffolding tests
    ]

docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface',
    ]

setup(name='edapi',
      version='0.1',
      description='Generic Reporting Platform',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=["http://packages.wgenhq.net/pynest/"],
      tests_require=tests_require,
      test_suite="nose.collector",
      install_requires=install_requires,
      extras_require={
          'docs': docs_extras,
          },
      )
