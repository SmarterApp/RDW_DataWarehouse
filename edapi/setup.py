import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

install_requires = [
    'pyramid == 1.4',
    'venusian >= 1.0a3',
    'validictory >= 0.8',
    'simplejson==3.3.1',
    'Beaker==1.6.4']

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'nose >= 1.2.1',
    'coverage',
    'virtualenv']  # for scaffolding tests


docs_extras = [
    'Sphinx',
    'docutils',
    'repoze.sphinx.autointerface']

setup(name='edapi',
      version='0.1',
      description='Generic Reporting Platform',
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
      tests_require=tests_require,
      test_suite="nose.collector",
      install_requires=install_requires,
      extras_require={
          'docs': docs_extras, },
      entry_points="""\
      """,
      )
