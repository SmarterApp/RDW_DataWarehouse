#!/bin/env bash

set -e # Exit on errors


function build_unittest {
	PATH=$PATH:/usr/pgsql-9.2/bin/
	export PATH
	source /opt/wgen/edware-udl/udl2/python3.3/bin/activate
	cd $WORKSPACE/config
	python setup.py install --force
	python generate_ini.py -i udl2_conf.yaml -e development -o udl2_conf.ini

	cd $WORKSPACE/udl2
	python setup_developer.py install --force


	#cd $WORKSPACE/config
	#python setup.py install --force
	/opt/wgen/edware-udl/udl2/python3.3/bin/stop_celery.sh
	#cd $WORKSPACE/udl2/scripts
	$WORKSPACE/udl2/scripts/teardown_udl2_database.sh
	$WORKSPACE/udl2/scripts/initialize_udl2_database.sh
	#cd ..
	cd $WORKSPACE/udl2
	nosetests --with-cov --cov=src/ --cov-report xml tests/unit_tests/test*.py
}

function main {
	build_unittest
}

main $@

# Completely successful

exit 0