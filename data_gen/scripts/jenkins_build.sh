#!/bin/bash

set -e # Exit on errors

function check_vars {
	if [ -z "$WORKSPACE"]; then
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

function set_vars_for_epydoc {
    VIRTUALENV_DIR="$WORKSPACE/datagen_epy"

    # delete existing xml files
    if [ -f $WORKSPACE/coverage.xml ]; then
        rm $WORKSPACE/coverage.xml
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
           python setup-developer.py develop
        else 
           echo "running setup.py"
           python setup.py install 
        fi
    done
 
    echo "Finished setting up virtualenv"

}

function setup_python2_virtualenv {
    echo "Setting up virtualenv using python2.7"
    if [ ! -d "$VIRTUALENV_DIR" ]; then
        /opt/python2.7/bin/virtualenv --distribute ${VIRTUALENV_DIR}
    fi

    # This will change your $PATH to point to the virtualenv bin/ directory,

    source ${VIRTUALENV_DIR}/bin/activate
 
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

	pep8 --exclude='*/docs/*' --ignore=$ignore $WORKSPACE/$1

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

function run_func_tests {
    echo "Running Functional Tests"

    cd "$WORKSPACE/$1"

    python src/generate_data.py --config configs.dg_types_test
    nosetests functional_tests/fTest*.py
}

function setup_epydoc_dependencies {
    echo "setting up epydoc dependencies"

    pip install epydoc

    echo "finished setting up epydoc dependencies"
}

function run_epydoc {
    echo "Creating epydocs"
    
    epydoc --html -o $WORKSPACE/epydoc --name DataGeneration --parse-only --no-sourcecode "$WORKSPACE/$1"

    cd "$WORKSPACE"
    if [ -d "epydoc_gh_pages" ]; then
        rm -rf epydoc_gh_pages    
    fi
    
    mkdir epydoc_gh_pages
    cd epydoc_gh_pages

    git clone -b gh-pages git@github.wgenhq.net:Ed-Ware-SBAC/fixture_data_generation.git
    cd fixture_data_generation
    rm *
    cp -r "$WORKSPACE/epydoc/"* .

    git add -A
    git commit -m "Adding New epydocs"
    git push

    echo "New Epydoc Pushed"
}

function get_opts {
    if ( ! getopts ":m:d:ufh" opt); then
	echo "Usage: `basename $0` options (-n) (-u) (-m main_package) (-d dependencies) -h for help";
	exit $E_OPTERROR;
    fi
 
    # By default, make the mode to be unit
    MODE='UNIT'
    RUN_UNIT_TEST=true

    while getopts ":m:d:uhnef" opt; do
        case $opt in 
            u)
               echo "Unit test mode"
               MODE='UNIT'
               ;;
            f)
               echo "Functional test mode"
               MODE='FUNC'
               ;;
            e)
               echo "EPYDOC mode"
               MODE='EPYD'
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

function generate_docs {
    # Generate docs if docs directory exists 
    if [ -d "$WORKSPACE/$1/docs" ]; then
        echo "***************"
        echo "Generating Docs"
        echo "***************"
        cd "$WORKSPACE/$1/docs"
        make clean
        make html
    fi
    echo "Docs created in $WORKSPACE/$1/docs/_build/html"
}

function main {

    get_opts $@
    check_vars
    if [ ${MODE:=""} == "UNIT" ]; then
        set_vars
        setup_virtualenv $@
        setup_unit_test_dependencies
        if $RUN_UNIT_TEST ; then
            run_unit_tests $MAIN_PKG
        fi
        check_pep8 $MAIN_PKG
        generate_docs $MAIN_PKG
    elif [ ${MODE:=""} == "EPYD" ]; then
        set_vars_for_epydoc
        setup_python2_virtualenv
        setup_epydoc_dependencies
        run_epydoc $MAIN_PKG
    elif [ ${MODE:=""} == "FUNC" ]; then
          echo "func mode"
          set_vars
          setup_virtualenv $@
          setup_unit_test_dependencies
          run_func_tests $MAIN_PKG
    fi
}

main $@

#Completed Successfully
exit 0
