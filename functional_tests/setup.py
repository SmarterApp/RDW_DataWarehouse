from setuptools import setup, find_packages

install_requires = [
    'behave',  # BDD tool
    'Requests', # for restful web services
    'PyHamcrest', # for assertion
    'virtualenv'  # for scaffolding tests
    ]

setup(name='functional_tests',
      version='0.1',
      description='Functional tests for the edware project',
      classifiers=[
        "Programming Language :: Python",
        "BDD Tool :: Behave",
        "Web Automation Tool :: Selenium Webdriver"
        ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=["http://packages.wgenhq.net/pynest/"],
      install_requires=install_requires,
      )
