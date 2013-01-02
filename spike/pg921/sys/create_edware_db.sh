#!/bin/bash --
#create_edware_db.sh
#Project PG921 Spike
#jbecker@wgen.net
#run as postgres

echo 'creating and starting db-farm'
/usr/local/pgsql/bin/pg_ctl -D /opt/edware/pg921/data -l logfile start

echo 'creating edware db'
/usr/local/pgsql/bin/createdb edware

echo 'creating edware user'
/usr/local/pgsql/bin/psql -U postgres -d edware < ./create_edware_role.sql

echo 'creating rpt/edware schemas'
/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_lz_ddl_drop.sql > ../data/rpt_fqa_lz_ddl_drop.out
/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_lz_ddl.sql > ../data/rpt_fqa_lz_ddl.out

/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_ddl_drop.sql > ../data/rpt_fqa_ddl_drop.out
/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_ddl.sql > ../data/rpt_fqa_ddl.out

echo 'loading edware_lz schema'
/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_load.sql > ../data/rpt_fqa_load.out

echo 'ELT edware_lz into edware schema'
/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_elt.sql > ../data/rpt_fqa_elt.out

echo 'ELT edware_lz.fao into edware.fao'
/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fao_load.sql > ../data/rpt_fao_load.out

#echo 'generating constraints'
#/usr/local/pgsql/bin/psql -U postgres -d edware < ../data/rpt_fqa_keys.sql





