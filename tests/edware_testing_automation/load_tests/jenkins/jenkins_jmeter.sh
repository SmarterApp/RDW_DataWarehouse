#!/bin/sh
# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.


rm *.jtl
rm *.tar
cd $WORKSPACE/functional_tests/load_tests/jmeter
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=1 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=25 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=50 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=75 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=100 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=250 -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb

/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=1 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=25 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=50 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=75 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=100 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=250 -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb

/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=1 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=25 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=50 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=75 -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=100 -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=250 -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb

cd $WORKSPACE
tar -cvzf memory_results.tar *memory.jtl
tar -cvzf cpu_results.tar *cpu.jtl
tar -cvzf disk_io_results.tar *disk_io.jtl
tar -cvzf network_results.tar *network.jtl
tar -cvzf summary_results.tar *summary_report.jtl
