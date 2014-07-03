import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = ['FixtureDataGeneration_Core == 0.4']

tests_require = requires + ['nose',
                            'pep8',
                            'coverage']

private_repositories = ['lib']

setuptools.setup(name='FixtureDataGeneration-SBAC',
                 version='0.2',
                 description='Fixture data generator for the SBAC project',
                 author='Sonic - Amplify Insight',
                 author_email='insight_ed-ware-sonic@amplify.com',
                 maintainer='Sonic - Amplify Insight',
                 maintainer_email='insight_ed-ware-sonic@amplify.com',
                 license='proprietary',
                 url='https://github.wgenhq.net/Data-Generation/project-sbac',
                 classifiers=['Programming Language :: Python', 'Programming Language :: Python :: 3.3',
                              'Operating System :: OS Independent', 'Intended Audience :: Developers',
                              'Topic :: Education', 'Topic :: Software Development :: Quality Assurance',
                              'Topic :: Software Development :: Testing', 'Topic :: Utilities'],
                 keywords='fixture data generation education SBAC',
                 packages=['sbac_data_generation', 'sbac_data_generation.config', 'sbac_data_generation.generators',
                           'sbac_data_generation.model', 'sbac_data_generation.util', 'sbac_data_generation.writers'],
                 zip_safe=False,
                 test_suite='nose.collector',
                 install_requires=requires,
                 tests_require=tests_require,
                 dependency_links=private_repositories,
                 entry_points='')
