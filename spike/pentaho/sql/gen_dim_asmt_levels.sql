-- \i gen_dim_asmt_levels.sql
-- substiute TABLE_NAME (dim_asmt) below with the table_name you want to analyze to generate the column analysis queries you wish to browse...
-- add the columns you wish to exclude from your analysis to the NOT IN clause...
-- update the name of the target file to "table_name"_levels.sql
-- and you should be good to go.

\! rm dim_asmt_levels.sql
\t
\o dim_asmt_levels.sql

SELECT DISTINCT 'select distinct ' || column_name || ' from dim_asmt;'
FROM information_schema.columns
WHERE table_name='dim_asmt'
AND column_name NOT IN ('asmt_guid', 'asmt_rec_id')
;

\t
\! rm dim_asmt_levels.sql.out
\o dim_asmt_levels.sql.out
\i dim_asmt_levels.sql
\! less dim_asmt_levels.sql.out
