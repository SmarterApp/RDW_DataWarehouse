#!/bin/bash

set -e # Exit on errors

function check_vars {
	if [-z "$WORKSPACE"]; then
		echo "\$WORKSPACE is not defined"
		exit 2
	fi
	if [ ! -d "$WORKSPACE"]; then
		echo "WORKSPACE: '$WORKSPACE' not found"
		exit 2
	fi
}

function set_vars {
    VIRTUALENV_DIR="$WORKSPACE/datagen_venv"

    # delete existing xml files
    if [ -f $WORKSPACE/coverage.xml ]; then
        rm $WORKSPACE/coverage.xml
    fi
    if [ -f $WORKSPACE/nosetests.xml ]; then
        rm $WORKSPACE/nosetests.xml
    fi
}

function setup_virtualenv {
    echo "Setting up virtualenv using python3.3"
    if [ ! -d "$VIRTUALENV_DIR" ]; then
        /opt/python3/bin/virtualenv-3.3 --distribute ${VIRTUALENV_DIR}
    fi

    # This will change your $PATH to point to the virtualenv bin/ directory,
    
    source ${VIRTUALENV_DIR}/bin/activate
    for var in "${INSTALL_PKGS[@]}" 
    do
        cd "$WORKSPACE/$var"
        pwd
        if [ -f setup-developer.py ];  then
           echo "running setup-developer.py"
           /opt/python3/bin/python setup-developer.py develop
        else 
           echo "running setup.py"
           /opt/python3/bin/python setup.py develop
        fi
    done
 
    echo "Finished setting up virtualenv"

} 

function setup_unit_test_dependencies {

	echo "Setting up unit tests dependencies"

	pip install nose
	pip install coverage
	pip install pep8
	pip install nose-cov

	echo "Finished setting up unit tests dependencies"
}

function check_pep8 {
	echo "Checking code style against pep8"

	ignore="E501"

	pep8 --ignore=$ignore $WORKSPACE/$1

	echo "finished check code style against pep8"
}

function run_unit_tests {
    echo "Running unit tests"

    cd "$WORKSPACE/$1"
    nosetests --with-xunit --xunit-file=$WORKSPACE/nosetests.xml --cov-report xml

    if [ -f coverage.xml ]; then
       # move coverage results
       mv coverage.xml $WORKSPACE/coverage.xml
    fi
}

function get_opts {
    if ( ! getopts ":m:d:ufh" opt); then
	echo "Usage: `basename $0` options (-n) (-u) (-m main_package) (-d dependencies) -h for help";
	exit $E_OPTERROR;
    fi
 
    # By default, make the mode to be unit
    MODE='UNIT'
    RUN_UNIT_TEST=true

    while getopts ":m:d:uhn" opt; do
        case $opt in 
            u)
               echo "Unit test mode"
               MODE='UNIT'
               ;;
            h)
               show_help
               ;;
            n)
               RUN_UNIT_TEST=false
               ;; 
            m)  
               MAIN_PKG=$OPTARG
               INSTALL_PKGS=("${INSTALL_PKGS[@]}" "$MAIN_PKG")
               ;;
            d) 
               INSTALL_PKGS=("${INSTALL_PKGS[@]}" "$OPTARG")
               ;;
            ?)
               echo "Invalid params"
               ;;
        esac
    done
}

function show_help {
    echo "#To set unit test mode with main package as edapi"
    echo "jenkins_build.sh -u -m edapi" 
    echo "#To set functional test mode with main package as smarter"
    echo "jenkins_build.sh -f -m smarter -d edapi"
}

function main {
	get_opts $@
    check_vars
    set_vars
    setup_virtualenv $@
    if [ ${MODE:=""} == "UNIT" ]; then
        setup_unit_test_dependencies
        if $RUN_UNIT_TEST ; then
            run_unit_tests $MAIN_PKG
        fi
        check_pep8 $MAIN_PKG
    fi
}

main $@

#Completed Successfully
exit 0
