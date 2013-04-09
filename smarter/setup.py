import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
assets = []
idp_metadata = os.path.join(os.path.join(os.path.join(here, ".."), "resource"), "idp_metadata.xml")

for root, subFolders, files in os.walk(os.path.join(os.path.dirname(__file__), "..", "assets")):
    for file in files:
        assets.append(os.path.join(root, file))

requires = [
    'pyramid',
    'pyramid_beaker',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'edauth',
    'edapi',
    'edschema',
    'py-postgresql',
    'pyramid_exclog']


setup(name='smarter',
      version='0.1',
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
      test_suite='nose.collector',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = smarter:main
      [console_scripts]
      initialize_smarter_db = smarter.scripts.initializedb:main
      """,
      data_files=[('smarter/assets', assets),
                  ('resource', [idp_metadata])]
      )
