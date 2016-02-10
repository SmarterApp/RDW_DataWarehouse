#!/bin/sh

rm *.jtl
rm *.tar
cd $WORKSPACE/functional_tests/load_tests/jmeter
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=1 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/1mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=25 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/1mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=50 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/1mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=75 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/1mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=100 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/1mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=250 -Jtest_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/1mtest.txt -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=1mb

/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=1 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/10mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=25 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/10mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=50 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/10mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=75 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/10mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=100 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/10mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=250 -Jtest_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/10mtest.txt -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=10mb

/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=1 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/100mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=25 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/100mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=50 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/100mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=75 -Jtest_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/100mtest.txt -Jconfig_file=$WORKSPACE/functional_tests/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=100 -Jtest_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/100mtest.txt -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb
#/opt/apache-jmeter-2.11/bin/jmeter -n -t hpz.jmx -Jusers=250 -Jtest_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/100mtest.txt -Jconfig_file=$WORKSPACE/edware_testing_automation/load_tests/jmeter/resources/qa_config.csv -Jserver_agent=hpzweb0.qa.dum.edwdc.net -Jresult_path=$WORKSPACE -Jfile_size=100mb

cd $WORKSPACE
tar -cvzf memory_results.tar *memory.jtl
tar -cvzf cpu_results.tar *cpu.jtl
tar -cvzf disk_io_results.tar *disk_io.jtl
tar -cvzf network_results.tar *network.jtl
tar -cvzf summary_results.tar *summary_report.jtl
