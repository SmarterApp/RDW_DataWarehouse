#!python
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2

try:
    conn = psycopg2.connect("dbname='edware' user='edware' host='10.8.0.40' password='edware2013'")
except:
    print ("I am unable to connect to the database")

print ("I am able to connect to the database")

cur = conn.cursor()

cur.execute("""SELECT bar, baz from public.foo""")

rows = cur.fetchall()

print ("\nWhere is the BEEF!:\n")

for row in rows:
    print( "\n", row[0], row[1])