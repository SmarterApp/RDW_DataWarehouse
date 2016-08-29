#!/bin/sh
DIR=`dirname $0`
TEMPLATE=${DIR}/"OpenAM_customize_deploy_script.sh.template"
SCRIPT=${DIR}/"OpenAM_customize_deploy_script.sh"
CPIO=/tmp/cpio.$$
if [ -f ${SCRIPT} ]; then
    rm -f ${SCRIPT}
fi
cp ${TEMPLATE} ${SCRIPT}
cd ${DIR}/../src/
find . -print | cpio -ocv > ${CPIO}
cd -
cat ${CPIO} |gzip -9 -c >> ${SCRIPT}
rm -f ${CPIO}
RETVAL=$?
if [ ${RETVAL} != 0 ]; then
    echo "Failed to generate deploy script"
    exit 1
fi
echo "Please copy ${SCRIPT} to the OpenAM server and execute it"
