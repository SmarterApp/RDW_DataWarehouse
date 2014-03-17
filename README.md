data-generation
========

The goal of this project is to provide a platform to generate fixtures data for system testing. Aimed at education
data, the data-generation project will create schools, students, and exam scores. It will populate a flexible schema.

##Installation

This is a Python 3 project and as such you will need Python 3 installed to use and/or develop the project. One note to
Mac OS X users: If you installed your Python 3 prior to upgrading to Mavericks, you will need to uninstall and
re-install Python 3.

###pip

The easiest way to get `pip` is to download it from [here](https://raw.github.com/pypa/pip/master/contrib/get-pip.py)
and then run:

    python get-pip.py

Just make sure the `python` binary is a version 3 binary.

###virtualenv

Optional, but it is recommended that you use a virtual environment for development of this project. This can be
installed with pip.

    pip install virtualenv

Again, if you have multiple `pip`s, make sure this is a Python 3 version.

###Create virtual environment

Optional, but recommended. To set up a virtual environment, execute the following command:

    virtualenv data-gen-env

Where `data-gen-env` is the name of the directory where you want your environment files placed. You can activate the
virtual environment with this command:

    source data-gen-env/bin/activate

Note that `data-gen-env` is the same name that was used with the creation of the environment. If you change the name of
the environment in the first command, change it in this command too.

###Install Run Dependencies

Once you have your environment activated (or you've decided not to use an environment), go into your repository and run
this command to finish setup:

    python setup.py develop

Note the use of `develop` in the call to `setup.py`. This will create a sym-link from the site-packages directory to the
working directory of your code. If instead you use `install`, it will copy the code and changes you make to the code
will probably not be picked up.

###Install Development Dependencies

You will need `nose` and `nose-mongoengine` to run the test suites. Along with those, we are using
[`coverage`](http://nedbatchelder.com/code/coverage/) for a unit testing code coverage report and
[`pep8`](http://pep8.readthedocs.org/en/latest/) as a style checker. If you have a virtual environment, run this within
it:

    pip install nose nose-mongoengine coverage pep8

##Usage

The main file for running the project is `generate.py`. The following options for the script exist:

* `--task TASK_FILE_NAME`: Specify the name of the task file to run

For the SBAC task:

* `--team TEAM_NAME`: Specify the team name to generate SBAC data for (expects `sonics` or `arkanoids`)

##Unit Tests

Within the project is a suite of unit tests that cover a large percentage of the codebase. We are using `nose` for the
unit tests and [`nose-mongoengine`](https://github.com/mbanton/nose-mongoengine) to mock a MongoDB for unit testing
purposes. To run the unit tests, start from the root of the project and call:

    nosetests --mongoengine --mongoengine-clear-after-module unit_tests/*

As you develop new functionality, make sure to write accompanying unit tests so as maintain good code coverage and the
confidence that comes with it.

##Branching

We are following a specific branching strategy for this project.

###master

As is common, all code on the `master` branch is fully functional and believed to be defect free. The only merges that
should be made into `master` should be from the `development` branch.

###development

This is the branch that new work is merged in to. Note that active development work should not take place in this
branch. When a feature is complete it is merged into the `development` branch. It is acceptable to make bug fixes
directly on development if the bug exists on `development`.

###Feature

A feature branch is where active development work should take place. Create a feature branch using this command:

    git checkout -b <branch_name> development

`<branch_name>` should be substituted with the desired name of the branch. As you can see, the branch is created from
the `development` branch. Once work is complete and verified, merge the code into `development`:

    git checkout development
    git merge --no-ff <branch_name>
    git push origin development

Note the `--no-ff` flag. This prevents git from doing a fast-forward merge, if one is possible. By preventing this, git
is forced to create a new commit object which preserves historical information.

You should also make it a habit to clean up feature branches after they have been merged back into `development`:

    git branch -d <branch_name>

###Other Notes

There is no expectation that feature branches be published to origin. It is recommended that you use many small
check-ins during your daily development on a feature branch.