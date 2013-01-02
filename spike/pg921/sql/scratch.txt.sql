select dim_student_key
, eternal_student_sid   
, year_sid
, dim_assmt_period_key
, dim_assmt_grade_key
, assmt_code
, assmt_name
, assmt_version_code
, daot_hier_level
, daot_hier_level_code
, daot_hier_level_name          
, daot_hier_level_rank
, daot.daot_hier_level_1_code 
, daot.daot_hier_level_1_name
, daot.daot_hier_level_1_abbrev     
, daot.daot_hier_level_2_code 
, daot.daot_hier_level_2_name
, daot.daot_hier_level_2_abbrev
, daot.daot_hier_level_3_code 
, daot.daot_hier_level_3_name
, daot.daot_hier_level_3_abbrev
, daot.daot_hier_level_4_code 
, daot.daot_hier_level_4_name
, daot.daot_hier_level_4_abbrev
, daot.daot_hier_level_5_code 
, daot.daot_hier_level_5_name
, daot.daot_hier_level_5_abbrev
, dim_perf_level_key
--, (case when performance_level_flag then 1 else 0 end) performance_level_flag
from edware.fact_assmt_outcome fao
join edware.dim_assmt_outcome_type daot
  on fao.dim_assmt_outcome_type_key  = daot.dim_assmt_outcome_type_key
 and daot.daot_hier_level_code    in ('2')
 and daot.assmt_code         in ('7')
 and case
       when daot.assmt_code = '706' then true
       when daot.assmt_code = '706s' then true
       else (daot.assmt_version_code in ('1'))
     end
 and  case 
        when daot.daot_hier_level = 1 then daot.daot_hier_level_1_code 
        when daot.daot_hier_level = 2 then daot.daot_hier_level_2_code 
        when daot.daot_hier_level = 3 then daot.daot_hier_level_3_code 
        when daot.daot_hier_level = 4 then daot.daot_hier_level_4_code 
        when daot.daot_hier_level = 5 then daot.daot_hier_level_5_code 
      end in ('INSTREC')
where fao.assmt_instance_rank=1 -- avoid duplicate assmt results in the same period
and fao.year_sid in ('8')
and daot.daot_measure_type_code = 'BM_AM'
;

Edware Spike Server Access
--------------------------
To access the Edware Spike server via ssh, log in with these creds.

ssh kallen@monetdb1.poc.dum.edwdc.net
password: 'your wgen password'

Postgres 
--------
There is no security on the postgres db, so you can access the database on the command line using the following incantation...

psql -Upostgres edware

To stop, start, restart the db, you will need to be postgres.

sudo su - postgres

pg_ctl -D /opt/edware/pg921/data -l logfile [start | stop | restart]

The most current project directory is

cd /var/lib/pgsql/workspace/spike/pg921/edware/

Most of the interesting files live in edware/data

We should store our benchmark queries in edware/sql

Monetdb
-------
The MonetDBD is running so you should be able to access it via...

mclient -uedware -dedware
password: edware

If you need to start | stop the server run this.

monetdbd [start | stop] /opt/edware/monetdb/data/

If you want to load data, you will have to be the monetdb user, connect like this.

mclient -umonetdb -dedware
password: monetdb

I did alot of the work to set up monetdb as root, which was the lazy way, so if you want to browse the command history, for whatever reason, then you should...

sudo su -

history | less

The most recent monetdb files are found in

Vertica
-------
The getting started page.

https://twiki.wgenhq.net/bin/view/DBA/GettingStarted

The RPT load test query repo.

http://repository.wgenhq.net/trac/RPT/browser/trunk/loadtest/vertica/queries

The RPT query naming convention cypher

The queries have a naming convention like this :
 
Cp – comparing populations
G stands for by grade
Sch for school
Sg – for school groups i.e. district
Account – It’s higher level than schoo.
 
If the first letter is g then it stands for growth.
Pmf stand for progress monitor fidelity
 
So g_g_sg.sql stands for growth report by grade and school group.

I will tidy this up into a proper readme file asap, but this is the gist of it.

~jj

p.s.

And for extra credit, if you can help me figure out why these queries to clean out fao's that have no student records are hanging in postgres, I will give you a cookie!

delete from edware.fact_enroll
where dim_student_key not in
    (
        select dim_student_key
        from edware.dim_student
    )
;

COPY
(select dim_student_key as _fao_not_in_dim_student_key_
from edware.fact_enroll
where dim_student_key not in
    (
        select dim_student_key
        from edware.dim_student
    )
-- and 1 = 2
) TO '/var/lib/pgsql/workspace/spike/pg921/edware/data/fao_not_in_dim_student.csv'
;


select count(dim_student_key) as _fao_not_in_dim_student_key_cnt_
from edware.fact_enroll
where dim_student_key not in
    (
        select dim_student_key
        from edware.dim_student
    )
;