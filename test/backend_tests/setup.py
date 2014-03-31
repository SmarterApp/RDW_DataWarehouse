import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_requires = [
    'nose >= 1.2.1',  # functional testing framework
    'SQLAlchemy==0.8.3',
    'edschema'
]

setup(name='backend_tests',
      version='0.1',
      description='Backend tests for the edware project',
      classifiers=[
          "Programming Language :: Python 3.3",
          "Functional Testing Framework :: Pyunit/nosetests"
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      )
