REPORTS := reports
REQUIREMENTS := requirements.txt
KILL_OUTPUT = >/dev/null 2>&1
report := $(shell echo "$(REPORTS)/`date +'%Y-%m-%d--%H-%M-%S'`")
path ?= edware_testing_automation

.SILENT: run html open help install $(REQUIREMENTS) $(REPORTS)
.IGNORE: run $(REQUIREMENTS)

# Code
all: run html open

install:
	python setup.py develop $(KILL_OUTPUT)

run:
	py.test --alluredir=$(report) $(path)

html: 
	allure generate -o $(report) $(report)

open: 
	allure report open -o $(report)

$(REPORTS):
	rm -rf $@

$(REQUIREMENTS):
	pip freeze > $@
	pip uninstall -y -q -r $@ $(KILL_OUTPUT)
	rm $@
	pip install -q wheel

clean: $(REPORTS) $(REQUIREMENTS)

help:
	echo "Usage:"
	echo "    make"
	echo "    make path=path/to/test/file"
	echo "    make path=functional_tests/database_tests/ report=custom-report-folder"
	echo ""
	echo "Available commands:"
	echo "    all - run tests, generate and open Allure HTML report. This commands is default."
	echo "    run - run tests located by 'path' option. Default is $(path)."
	echo "    html - generate Allure HTML report by 'report' option."
	echo "    open - open Allure HTML report by 'report' option." 
	echo "    clean - remove all reports and uninstall all packages from python environment."
	echo "    install - set up Python's dependencies."
	echo ""
	echo "Options:"
	echo "    path - path to a folder or a file with test(s)."
	echo "    report - path to a folder for report generation."
