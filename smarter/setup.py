import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'edapi',
    'edschema',
    'py-postgresql',
    'lesscss', ]


setup(name='smarter',
      version='0.0',
      description='smarter',
      long_description=README + '\n\n' + CHANGES,
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
      test_suite='smarter',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = smarter:main
      [console_scripts]
      initialize_smarter_db = smarter.scripts.initializedb:main
      """,
      dependency_links=[
          'file://' + here + '/../edapi#egg=edapi',
          'file://' + here + '/../edschema#egg=edschema', ]
      )

# Copying the assets folder during setup to be inside the application folder
application_asset_folder = os.getcwd() + '/assets'
# if os.path.lexists(application_asset_folder):
#    shutil.rmtree(application_asset_folder)
# shutil.copytree('../assets', application_asset_folder)
