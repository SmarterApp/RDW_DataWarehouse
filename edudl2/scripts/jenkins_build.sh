#!/bin/env bash

set -e # Exit on errors

function build_pep8 {
	source $WORKSPACE/python3.3/bin/activate
	cd $WORKSPACE/udl2
	python setup.py install --force
	pep8 --exclude='*config*' --ignore=E501 *.py src/ tests/
}

function build_doc {
	source $WORKSPACE/python3.3/bin/activate
	cd $WORKSPACE/udl2
	python setup.py install --force
	cd $WORKSPACE/docs
	make clean
	make html
}

function build_e2e {
	PATH=$PATH:/usr/pgsql-9.2/bin/:$WORSPACE/python3.3/bin
	export PATH
    cd $WORKSPACE
    rm -fr python3.3
	/opt/python3/bin/virtualenv-3.3 --distribute python3.3
	source $WORKSPACE/python3.3/bin/activate
	cd $WORKSPACE/config
	python setup.py install --force
	python generate_ini.py -i udl2_conf.yaml -e development -o udl2_conf.ini

	cd $WORKSPACE/edschema
    python setup.py install
    cd $WORKSPACE/edcore
    python setup.py install
	cd $WORKSPACE/udl2
	python setup_developer.py install --force
	cp $WORKSPACE/udl2/tests/data/keys/* ~/.gnupg/

	stop_celery.sh
	sleep 2
	celeryctl purge

	cd $WORKSPACE/udl2/scripts
	/bin/sh $WORKSPACE/udl2/scripts/teardown_udl2_database.sh
	/bin/sh $WORKSPACE/udl2/scripts/initialize_udl2_database.sh
	start_celery.sh &
	sleep 2
	cd $WORKSPACE/udl2/tests/e2e_tests
	nosetests test_*.py -vs
}

function build_functest {
	PATH=$PATH:/usr/pgsql-9.2/bin/:$WORSPACE/python3.3/bin
	export PATH
	cd $WORKSPACE
	rm -fr python3.3
	/opt/python3/bin/virtualenv-3.3 --distribute python3.3
	source $WORKSPACE/python3.3/bin/activate
	cd $WORKSPACE/config
	python setup.py install --force
	python generate_ini.py -i udl2_conf.yaml -e development -o udl2_conf.ini

	cd $WORKSPACE/edschema
    python setup.py install
    cd $WORKSPACE/edcore
    python setup.py install
	cd $WORKSPACE/udl2
	python setup_developer.py install --force

	stop_celery.sh
	sleep 2
	celeryctl purge

	/bin/sh $WORKSPACE/udl2/scripts/teardown_udl2_database.sh
	/bin/sh $WORKSPACE/udl2/scripts/initialize_udl2_database.sh
	start_celery.sh &
	sleep 2
	cd $WORKSPACE/udl2/tests/functional_tests
	nosetests test_*.py -vs
}

function build_unittest {
	PATH=$PATH:/usr/pgsql-9.2/bin/:$WORSPACE/python3.3/bin
	export PATH
	cd $WORKSPACE
	rm -fr python3.3
	/opt/python3/bin/virtualenv-3.3 --distribute python3.3
	source $WORKSPACE/python3.3/bin/activate
	cd $WORKSPACE/config
	python setup.py install --force
	python generate_ini.py -i udl2_conf.yaml -e development -o udl2_conf.ini
	cd $WORKSPACE/edschema
    python setup.py install
    cd $WORKSPACE/edcore
    python setup.py install
	cd $WORKSPACE/udl2
	python setup_developer.py install --force

	stop_celery.sh
	sleep 2
	/bin/sh $WORKSPACE/udl2/scripts/teardown_udl2_database.sh
	/bin/sh $WORKSPACE/udl2/scripts/initialize_udl2_database.sh

	cd $WORKSPACE/udl2
	nosetests --with-cov --cov=src/ --cov-report xml tests/unit_tests/test*.py
}

function main {
	while getopts ":m:d:upfhbse" opt; do

		case $opt in
			u)
				build_unittest
				;;
			f)
				build_functest
				;;
			s)
				build_doc
				;;
			e)
				build_e2e
				;;
			p)
				build_pep8
				;;
		esac
	done
}

main $@

# Completely successful

exit 0
