#!/bin/bash

set -e # Exit on errors

function check_vars {

    # This is really just to make sure that we're running this on Jenkins
    if [ -z "$WORKSPACE" ]; then
        echo "\$WORKSPACE is not defined"
        exit 2
    fi
    if [ ! -d "$WORKSPACE" ]; then
        echo "WORKSPACE: '$WORKSPACE' not found"
        exit 2
    fi
}

function set_vars {
    export VIRTUALENV_DIR="$WORKSPACE/edwaretest_venv"

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
        /usr/local/bin/virtualenv -p /usr/local/bin/python3 --no-site-packages ${VIRTUALENV_DIR}
    fi

# This will change your $PATH to point to the virtualenv bin/ directory,
# to find python, paster, nosetests, pep8, pip, easy_install, etc.
    
    source ${VIRTUALENV_DIR}/bin/activate
    for var in "${INSTALL_PKGS[@]}" 
    do
        cd "$WORKSPACE/$var"
        python setup.py develop
    done
 
    echo "Finished setting up virtualenv"

} 

function setup_unit_test_dependencies {
    
    echo "Setting up unit tests dependencies"
    
    pip install nose
    pip install coverage
    pip install pep8

    echo "Finished setting up unit tests dependencies"
}

function check_pep8 {
    echo "Checking code style against pep8"
   
    ignore="E124,E128,E501"
    
    pep8 --ignore=$ignore $WORKSPACE/$1

    echo "Finished checking code style against pep8"
}

function run_unit_tests {
    echo "Running unit tests"

    cd "$WORKSPACE/$1"
    nosetests -v --with-coverage --cover-package=$1  --with-xunit --xunit-file=$WORKSPACE/nosetests.xml --cover-xml --cover-xml-file=$WORKSPACE/coverage.xml
}

function get_opts {
    if ( ! getopts ":m:d:ufh" opt); then
	echo "Usage: `basename $0` options (-n) (-u) (-f) (-m main_package) (-d dependencies) -h for help";
	exit $E_OPTERROR;
    fi
 
    # By default, make the mode to be unit
    MODE='UNIT'
    RUN_UNIT_TEST=true

    while getopts ":m:d:ufhn" opt; do
        case $opt in 
            u)
               echo "Unit test mode"
               MODE='UNIT'
               ;;
            f)
               echo "Functional test mode"
               MODE='FUNC'
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

function setup_functional_test_dependencies {
    echo "Setup functional test dependencies"

    cd "$WORKSPACE/functional_tests"
    python setup.py develop

    echo "Finish functional test dependencies setup"
}

function run_functional_tests {
    echo "Run functional tests"

    cd "$WORKSPACE/functional_tests/edapi"
    behave --junit --junit-directory=$WORKSPACE

    echo "Finish running functional tests"
}	

function create_sym_link_for_apache {
    /bin/ln -sf "$VIRTUALENV_DIR/lib/python3.3/site-packages" /home/jenkins/pythonpath
    /bin/ln -sf "$WORKSPACE/smarter/development.ini" /home/jenkins/development_ini
    /bin/ln -sf "$WORKSPACE/test_deploy/pyramid.wsgi" /home/jenkins/pyramid_conf
    /bin/ln -sf "$VIRTUALENV_DIR" /home/jenkins/venv
}

function restart_apache {
    /usr/bin/sudo /etc/rc.d/init.d/httpd graceful 
    RES=$?
    if [ $RES != 0 ]; then
       echo "httpd graceful failed to restart"
       exit 1
    fi
}

function main {
    get_opts $@
    check_vars
    set_vars
    setup_virtualenv $@
    if [ ${MODE:=""} == "UNIT" ]; then
        setup_unit_test_dependencies
        if [ $RUN_UNIT_TEST -eq true ]; then
            run_unit_tests $MAIN_PKG
        fi
        check_pep8 $MAIN_PKG
    elif [ ${MODE:=""} == "FUNC" ]; then
        create_sym_link_for_apache
        restart_apache
        setup_functional_test_dependencies
        run_functional_tests
    fi
}

main $@

# Completed successfully
exit 0
