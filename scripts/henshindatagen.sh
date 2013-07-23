#!/bin/sh

python -m edschema.metadata_generator --metadata edware -s edware_udl_test -d edware --host=localhost:5432 -u edware -p edware2013
cd ../data_gen/DataGeneration/src
python generate_data.py --config dg_types_test_endtoend
cd ../dataload/
python load_data.py -c ../datafiles/csv -t edware_udl_test edware2013
cd ../../Henshin/src/
python henshin.py -d ../../DataGeneration/datafiles/csv/dim_asmt.csv -o ../../../udl2/tests/integration_tests --schema edware_udl_test --host localhost
