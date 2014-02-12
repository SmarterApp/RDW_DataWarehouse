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
    export PATH=$PATH:/opt/python3/bin
    VIRTUALENV_DIR="$WORKSPACE/edwaretest_venv"
    FUNC_VIRTUALENV_DIR="$WORKSPACE/functest_venv"
    FUNC_DIR="edware_test/edware_test/functional_tests"
    SMARTER_INI="/opt/edware/conf/smarter.ini"
    PRECACHE_FILTER_JSON="/opt/edware/conf/comparing_populations_precache_filters.json"
    EGG_REPO="/opt/edware/pynest"
    PYNEST_SERVER="repo0.qa.dum.edwdc.net"
    PYNEST_DIR="/opt/wgen/pyrepos/pynest"

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
        virtualenv-3.3 --distribute ${VIRTUALENV_DIR}
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
	echo "Usage: `basename $0` options (-n) (-u) (-f) (-b) (-e) (-m main_package) (-d dependencies) -h for help";
	exit $E_OPTERROR;
    fi
 
    # By default, make the mode to be unit
    MODE='UNIT'
    RUN_UNIT_TEST=true
    RUN_END_TO_END=false

    while getopts ":m:d:ufbhne" opt; do
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
            e)
               RUN_END_TO_END=true
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
    # Remove the pdf directory
    if [ -d /opt/edware/pdf/NY ]; then
        rm -rf /opt/edware/pdf/NY
    fi
    # Remove the extract directory
    #if [ -d /sftp/opt/edware/home/cat/kswimberly/reports ]; then
    #    rm -rf /sftp/opt/edware/home/cat/kswimberly/reports
    #fi
    # Remove the tmp/FTs_extracted_files directory that is used for extract FTs
    if [-d /tmp/FTs_extracted_files]; then
    		rm -rf /tmp/FTs_extracted_files
    	fi
    rm -rf $WORKSPACE/edware_test
    mkdir  $WORKSPACE/edware_test
    cd $WORKSPACE/edware_test
    git clone -b ${BRANCH} git@github.wgenhq.net:Ed-Ware-SBAC/edware_test.git

    # we should be inside the python 3.3 venv, so deactivate that first
    deactivate
    enable_python27
    cd "$WORKSPACE/$FUNC_DIR"
    python setup.py develop

    pip install pep8
    echo "Finish functional test dependencies setup"
}

function enable_python27 {
    echo "Enable python2.7 environment"
    if [ ! -d "$FUNC_VIRTUALENV_DIR" ]; then
        /opt/python2.7/bin/virtualenv --distribute $FUNC_VIRTUALENV_DIR
    fi

    source ${FUNC_VIRTUALENV_DIR}/bin/activate
    echo "Now in python2.7"
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
    #enable python environment
    enable_python27

    cd "$WORKSPACE/$FUNC_DIR"

    sed -i.bak 's/port = 6543/port = 80/g' test.ini
    sed -i.bak "s/host=localhost/host=$HOSTNAME/g" test.ini
    export DISPLAY=:6.0
    
    if $RUN_END_TO_END; then
       cd e2e_tests
       nosetests -v --with-xunit --xunit-file=$WORKSPACE/nosetests.xml
    else
       nosetests --exclude-dir=e2e_tests -v --with-xunit --xunit-file=$WORKSPACE/nosetests.xml
       generate_docs edware_test/edware_test/functional_tests
    fi

    echo "Finish running functional tests"
}

function create_sym_link_for_apache {
    echo "Creating symbolic links"

    APACHE_DIR="/var/lib/jenkins/apache_dir"
    if [ -d ${APACHE_DIR} ]; then
        rm -rf ${APACHE_DIR}
    fi
    mkdir -p ${APACHE_DIR}
    /bin/ln -sf ${VIRTUALENV_DIR}/lib/python3.3/site-packages ${APACHE_DIR}/pythonpath
    /bin/ln -sf ${WORKSPACE}/config/${INI_FILE_FOR_ENV} ${SMARTER_INI}
    /bin/ln -sf ${WORKSPACE}/config/comparing_populations_precache_filters.json ${PRECACHE_FILTER_JSON}
    /bin/ln -sf ${WORKSPACE}/smarter/smarter.wsgi ${APACHE_DIR}/pyramid_conf
    /bin/ln -sf ${VIRTUALENV_DIR} ${APACHE_DIR}/venv

    compile_assets true

    echo "Creating sym links for celery purposes"
   
    EDWARE_VENV_DIR="/opt/virtualenv"
    if [ -d ${EDWARE_VENV_DIR} ]; then
        rm -rf ${EDWARE_VENV_DIR}
    fi
    /bin/ln -sf ${VIRTUALENV_DIR} ${EDWARE_VENV_DIR}
    sed -i.bak "s/CELERYD_USER=\"celery\"/CELERYD_USER=\"jenkins\"/" ${WORKSPACE}/services/config/linux/opt/edware/conf/celeryd-services.conf
    sed -i.bak "s/CELERYD_GROUP=\"celery\"/CELERYD_GROUP=\"functional_test\"/" ${WORKSPACE}/services/config/linux/opt/edware/conf/celeryd-services.conf
   
    sed -i.bak "s/CELERYD_USER=\"celery\"/CELERYD_USER=\"jenkins\"/" ${WORKSPACE}/edextract/config/linux/opt/edware/conf/celeryd-edextract.conf
    sed -i.bak "s/CELERYD_GROUP=\"celery\"/CELERYD_GROUP=\"functional_test\"/" ${WORKSPACE}/edextract/config/linux/opt/edware/conf/celeryd-edextract.conf
}

function compile_assets {
    OPTIMIZE_JS=${1:-"false"}
    cd "$WORKSPACE/scripts"
    WORKSPACE_PATH=${WORKSPACE//\//\\\/}

    sed -i.bak "s/assets.directory = \/path\/assets/assets.directory = ${WORKSPACE_PATH}\/assets/g" compile_assets.ini
    sed -i.bak "s/smarter.directory = \/path\/smarter/smarter.directory = ${WORKSPACE_PATH}\/smarter/g" compile_assets.ini
    sed -i.bak "s/\(optimize.javascript = \)\(true\|false\)/\1${OPTIMIZE_JS}/g" compile_assets.ini

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

function restart_celeryd {
   /usr/bin/sudo /etc/init.d/celeryd-services restart
   /usr/bin/sudo /etc/init.d/celeryd-edextract restart
   RES=$?
   if [ $RES != 0 ]; then
      echo "celeryd failed to restart"
      exit 1
   fi
}

function import_data_from_csv {
    echo "Import data from csv"
    
    # This needs to run in python3.3 
    cd "$WORKSPACE/test_utils"
    
    # This is a workaround as pgpool is read-only, replace pgpool server with db master
    echo "${WORKSPACE}/config/data_copy.ini"
    echo "${WORKSPACE}/config/${INI_FIlE_FOR_ENV}"
    cp "${WORKSPACE}/config/${INI_FIlE_FOR_ENV}" "${WORKSPACE}/config/data_copy.ini"
    sed -i.bak "s/edwdbsrv4.poc.dum.edwdc.net:9999/edwdbsrv1.poc.dum.edwdc.net:5432/" ${WORKSPACE}/config/data_copy.ini
    
    python import_data.py --config ${WORKSPACE}/config/data_copy.ini --resource ${WORKSPACE}/edschema/database/tests/resources
}

function build_rpm {
    # parameter $1 : $MAIN_PKG to be built
    # prerequisite there is a venv inside workspace (ie. run setup_virtualenv)
    rm -rf /var/lib/jenkins/rpmbuild

    echo "Build RPM for: "
    echo $1
    echo "Build Number: "
    echo $BUILD_NUMBER
    echo "RPM_VERSION: "
    echo $RPM_VERSION

    export GIT_COMMIT="$(git rev-parse HEAD)"

    cd "$WORKSPACE/rpm/SPEC"
    rpmbuild -bb $1.spec

    ENV_NAME=$(echo ${1}_env_name | tr '[:lower:]' '[:upper:]')
    scp /var/lib/jenkins/rpmbuild/RPMS/x86_64/$1${!ENV_NAME}-${RPM_VERSION}-${BUILD_NUMBER}.el6.x86_64.rpm pynest@${PYNEST_SERVER}:/opt/wgen/rpms
    ssh pynest@${PYNEST_SERVER} "ln -sf /opt/wgen/rpms/$1${!ENV_NAME}-${RPM_VERSION}-${BUILD_NUMBER}.el6.x86_64.rpm /opt/wgen/rpms/$1-latest.rpm"

    echo "Upload to pulp"
    pulp-admin content upload --dir /var/lib/jenkins/rpmbuild/RPMS/x86_64 --repoid edware-el6-x86_64-upstream --nosig -v

    echo "Finished building RPM"
}

function build_egg {
    # prerequisite we're inside a python3.3 venv

    echo "Build an egg"
    if [ ${1:=""} == "smarter" ]; then
        compile_assets
    fi

    cd "$WORKSPACE/$1"
    rm -f *.tar.gz
    python setup.py sdist -d ${EGG_REPO}/$1
    cd "${EGG_REPO}/$1"
    # We need this because we have two jenkins server and one of them cannot access pynest
    # In the jenkins job, we need to set PUBLISH_EGG env variable to TRUE if we want to publish the egg to pynest
    if [ ${PUBLISH_EGG:=""} == "TRUE" ]; then
        echo "Publishing egg to pynest"
        scp *.tar.gz pynest@${PYNEST_SERVER}:"$PYNEST_DIR/$1"
    fi
}

function generate_ini {
	cd "$WORKSPACE/config"
	python generate_ini.py -e jenkins_dev -i settings.yaml
}

function generate_docs {
    # Generate docs if docs directory exists 
    if [ -d "$WORKSPACE/$1/docs" ]; then
        echo "***************"
        echo "Generating Docs"
        echo "***************"
        cd "$WORKSPACE/$1"
	python setup.py docs
        cd "$WORKSPACE/$1/docs"
        make clean
        make html
    fi
    echo "Docs created in $WORKSPACE/$1/docs/_build/html"
}

function run_javascript_tests {
    echo "Running javascript phantomjs tests"
    cd "$WORKSPACE/assets/test/js/3p"
    phantomjs run-qunit.js http://localhost/assets/test/TEST.EDWARE.test.html?coverage=true
}

function run_javascript_yslow_tests {
    echo "Running javascript phantomjs yslow tests"
    cd "$WORKSPACE/assets/test/js/3p"
    phantomjs /opt/yslow/yslow.js --help
}

function main {
	
    get_opts $@
    check_vars
    set_vars
    if [ ${MODE:=""} == "UNIT" ]; then
        setup_virtualenv $@
        setup_unit_test_dependencies
        if $RUN_UNIT_TEST ; then
            run_unit_tests $MAIN_PKG
        fi
        check_pep8 $MAIN_PKG
        generate_docs $MAIN_PKG
        #build_egg $MAIN_PKG
    elif [ ${MODE:=""} == "FUNC" ]; then
        setup_virtualenv $@
        generate_ini
        create_sym_link_for_apache
        restart_apache
        restart_celeryd
        import_data_from_csv
        if (! $RUN_END_TO_END;) then
           setup_python33_functional_test_dependencies
           run_python33_functional_tests
        fi
        setup_functional_test_dependencies
        run_functional_tests
        check_pep8 "$FUNC_DIR"
    elif [ ${MODE:=""} == "RPM" ]; then
        build_rpm $MAIN_PKG
    fi
}

main $@

# Completed successfully
exit 0
