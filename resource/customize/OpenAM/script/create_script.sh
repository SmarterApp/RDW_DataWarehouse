#!/bin/sh
DIR=`dirname $0`
TEMPLATE=${DIR}/"OpenAM_customize_deploy_script.sh.template"
SCRIPT=${DIR}/"OpenAM_customize_deploy_script.sh"
cp ${TEMPLATE} ${SCRIPT}
GZIP=-9 tar -C ../src/ -czf - html css >> ${SCRIPT}
echo "Please copy ${SCRIPT} to the OpenAM server and execute it"
