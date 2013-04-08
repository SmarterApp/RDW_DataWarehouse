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
    VIRTUALENV_DIR="$WORKSPACE/edwaretest_venv"
    FUNC_VIRTUALENV_DIR="$WORKSPACE/functest_venv"
    FUNC_DIR="edware_test/edware_test/functional_tests"

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
           python setup-developer.py develop
        else 
           echo "running setup.py"
           python setup.py develop
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
    echo "********************************"
    echo "Checking code style against pep8"
    echo "********************************" 
    ignore="E501"
    
    pep8 --ignore=$ignore $WORKSPACE/$1

    echo "Finished checking code style against pep8"
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
    if ( ! getopts ":m:d:ufhb" opt); then
	echo "Usage: `basename $0` options (-n) (-u) (-f) (-b) (-m main_package) (-d dependencies) -h for help";
	exit $E_OPTERROR;
    fi
 
    # By default, make the mode to be unit
    MODE='UNIT'
    RUN_UNIT_TEST=true

    while getopts ":m:d:ufbhn" opt; do
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
            b)
               echo "Build RPM mode"
               MODE='RPM'
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
    
    rm -rf $WORKSPACE/edware_test
    mkdir  $WORKSPACE/edware_test
    cd $WORKSPACE/edware_test
    git clone git@github.wgenhq.net:Ed-Ware-SBAC/edware_test.git

    # we should be inside the python 3.3 venv, so deactivate that first
    deactivate 
     
    if [ ! -d "$FUNC_VIRTUALENV_DIR" ]; then
         /opt/python2.7/bin/virtualenv --distribute $FUNC_VIRTUALENV_DIR
    fi
   
    source ${FUNC_VIRTUALENV_DIR}/bin/activate

    cd "$WORKSPACE/$FUNC_DIR"
    python setup.py develop
    
    pip install pep8

    echo "Finish functional test dependencies setup"
}

function setup_python33_functional_test_dependencies {
    echo "Setup python 33functional test dependencies"
    
    cd "$WORKSPACE/test/backend_tests"
    python setup.py develop

    echo "Finish python33 functional test dependencies setup"
}

function run_python33_functional_tests {
    echo "Run python33 functional tests"

    cd "$WORKSPACE/test/backend_tests"

    nosetests -v --with-xunit --xunit-file=$WORKSPACE/nosetests.xml

    echo "Finish running python33 functional tests"
}	

function run_functional_tests {
    echo "Run functional tests"

    cd "$WORKSPACE/$FUNC_DIR"

    sed -i.bak 's/port = 6543/port = 80/g' test.ini
    sed -i.bak "s/host=localhost/host=$HOSTNAME/g" test.ini
    export DISPLAY=:6.0

    nosetests -v --with-xunit --xunit-file=$WORKSPACE/nosetests.xml

    echo "Finish running functional tests"
}	

function create_sym_link_for_apache {
    APACHE_DIR="/var/lib/jenkins/apache_dir"
    if [ -d ${APACHE_DIR} ]; then
        rm -rf ${APACHE_DIR}
    fi
    mkdir -p ${APACHE_DIR}
    /bin/ln -sf ${VIRTUALENV_DIR}/lib/python3.3/site-packages ${APACHE_DIR}/pythonpath
    /bin/ln -sf ${WORKSPACE}/smarter/test.ini /opt/edware/smarter/smarter.ini
    /bin/ln -sf ${WORKSPACE}/smarter/smarter.wsgi ${APACHE_DIR}/pyramid_conf
    /bin/ln -sf ${VIRTUALENV_DIR} ${APACHE_DIR}/venv

    cd "$WORKSPACE/scripts"
    WORKSPACE_PATH=${WORKSPACE//\//\\\/}

    sed -i.bak "s/assets.directory = \/path\/assets/assets.directory = ${WORKSPACE_PATH}\/assets/g" compile_assets.ini
    sed -i.bak "s/smarter.directory = \/path\/smarter/smarter.directory = ${WORKSPACE_PATH}\/smarter/g" compile_assets.ini
    python compile_assets.py
}

function restart_apache {
    /usr/bin/sudo /etc/rc.d/init.d/httpd graceful 
    RES=$?
    if [ $RES != 0 ]; then
       echo "httpd graceful failed to restart"
       exit 1
    fi
}

function import_data_from_csv {
    echo "Import data from csv"
    
    # This needs to run in python3.3 
    cd "$WORKSPACE/test_utils"
    python import_data.py --config ${WORKSPACE}/smarter/test.ini --resource ${WORKSPACE}/edschema/database/tests/resources
}

function build_rpm {
    # prerequisite there is a venv inside workspace (ie. run setup_virtualenv)

    # deactivate python 3.3 venv
    deactivate
    

    echo "Build RPM"
    echo "Build Number:"
    echo $BUILD_NUMBER
    echo "RPM_VERSION:"
    echo $RPM_VERSION

    GIT_HASH="$(git rev-parse HEAD)"

    #echo "clone git://mcgit.mc.wgenhq.net/wgen/rpmtools"
    #rm -rf $WORKSPACE/rpmtools
    #mkdir  $WORKSPACE/rpmtools
    #cd $WORKSPACE/rpmtools
    #git clone git://mcgit.mc.wgenhq.net/wgen/rpmtools

    #cd rpmtools

    # Need to run on python 2.7
    /opt/python2.7/bin/python2.7 /var/lib/jenkins/wg_rpmbuild.py --dont-clean-staging --ignore-existing-staging -r "$WORKSPACE" -D_topdir="$WORKSPACE" -Dbuild_number="$BUILD_NUMBER" -Dcheckoutroot="$WORKSPACE" -Dversion="$RPM_VERSION" -o "$RPM_REPO" "$RPM_SPEC"

    echo "Finished building RPM"
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
    elif [ ${MODE:=""} == "FUNC" ]; then
        create_sym_link_for_apache
        restart_apache
        import_data_from_csv
        setup_python33_functional_test_dependencies
        run_python33_functional_tests
        setup_functional_test_dependencies
        run_functional_tests
        check_pep8 "$FUNC_DIR"
    elif [ ${MODE:=""} == "RPM" ]; then
        build_rpm
    fi
}

main $@

# Completed successfully
exit 0
