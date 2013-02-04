from setuptools import setup, find_packages

install_requires = [
    'nose',  # functional testing framework
    'selenium',  # for UI testing
    'Requests',  # for restful web services
    'PyHamcrest',  # for assertion
    'virtualenv'  # for scaffolding tests
]

setup(name='functional_tests',
      version='0.1',
      description='Functional tests for the edware project',
      classifiers=[
          "Programming Language :: Python 3.3",
          "Functional Testing Framework :: Pyunit/nosetests",
          "Web Automation Tool :: Selenium Webdriver"
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=["http://packages.wgenhq.net/pynest/"],
      install_requires=install_requires,
      )

