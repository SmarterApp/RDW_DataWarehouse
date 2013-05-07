Proof of Concept code for using Foreign Data Wrapper to import files

For US14726 https://rally1.rallydev.com/#/10258177071d/detail/userstory/11244475296

Requirement:

Python 3.3
Psycopg2 driver
Postgresql Server 9.2

This code will run on a machine with Postgresql server 9.2 running.

I use virtualenv, and install psycopg2, also I have Postgres.App running as my postgresql on my Macbook Pro.

the command is 

   python3.3 FdwCsvLoader.py 
   
It will read REALDATA_ASMT_ID_20.csv in current directory and output it from foreign data wrapper.
