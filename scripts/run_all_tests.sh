#!/bin/bash

# Assume starting in <repo>/scripts
cd ..

# Style check all sub-projects
echo
echo
echo Style checking
echo
pep8 edcore/ --ignore=E501
pep8 edschema/ --ignore=E501
pep8 edudl2/ --ignore=E501
pep8 edextract/ --ignore=E501
pep8 edapi/ --ignore=E501
pep8 edauth/ --ignore=E501
pep8 edmigrate/ --ignore=E501
pep8 edworker/ --ignore=E501
pep8 edsftp/ --ignore=E501
pep8 services/ --ignore=E501
pep8 smarter/ --ignore=E501

# Perform EdAPI tests
echo
echo
echo EdAPI tests
echo
cd edapi/edapi/tests
nosetests

# Perform EdAuth tests
echo
echo
echo EdAuth tests
echo
cd ../../../edauth/edauth/tests
nosetests

# Perform EdCore tests
echo
echo
echo EdCore tests
echo
cd ../../../edcore/edcore/tests
nosetests

# Perform EdExtract tests
echo
echo
echo EdExtract tests
echo
cd ../../../edextract/edextract/tests
nosetests

# Perform EdMigrate tests
echo
echo
echo EdMigrate tests
echo
cd ../../../edmigrate/edmigrate/tests
nosetests

# Perform EdSchema tests
echo
echo
echo EdSchema tests
echo
cd ../../../edschema/edschema/tests
nosetests

# Perform EdSFTP tests
echo
echo
echo EdSFTP tests
echo
cd ../../../edsftp/edsftp/tests
nosetests

# Perform EdUDL2 tests
echo
echo
echo EdUDL2 tests
echo
cd ../../../edudl2/edudl2/tests
nosetests unit_tests/*
nosetests functional_tests/*
nosetests e2e_tests/*

# Perform EdWorker tests
echo
echo
echo EdWorker tests
echo
cd ../../../edworker/edworker/tests
nosetests

# Perform Services tests
echo
echo
echo Services tests
echo
cd ../../../services/services/tests
nosetests

# Perform Smarter tests
echo
echo
echo Smarter tests
echo
cd ../../../smarter/smarter/tests
nosetests

# Return to scripts directory
cd ../../../scripts

# Done
echo
echo
echo
echo Testing Complete
echo

