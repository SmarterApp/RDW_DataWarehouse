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

# check null -- column
NULL_ALL_SQL = """
INSERT INTO "{schema}"."err_list" (record_sid,
                                   guid_batch,
                                   err_code,
                                   err_source,
                                   created_date)
       SELECT -1 AS record_sid,
                    '{guid_batch}' AS guid_batch,
                    {error_code} AS error_code,
                    {err_source} AS err_source,
                    now() AS create_date
       FROM ( SELECT SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END) AS null_rec_count,COUNT(*) AS total_rec
              FROM "{schema}"."{table}"
              WHERE guid_batch = '{guid_batch}') COLS
       WHERE COLS.null_rec_count = COLS.total_rec;
"""


# check null -- row
NULL_SQL = """
INSERT INTO "{schema}"."err_list" (record_sid,
                                   guid_batch,
                                   err_code,
                                   err_source,
                                   created_date)
        SELECT record_sid,
               guid_batch,
               {error_code} AS error_code,
               {err_source} AS err_source,
               now() AS create_date
        FROM "{schema}"."{table}"
        WHERE guid_batch = '{guid_batch}'
        AND TRIM({column}) IS NULL;
"""


# check unique record -- row
UNIQUE_SQL = """
INSERT INTO "{schema}"."err_list" (record_sid,
                                   guid_batch,
                                   err_code,
                                   err_source,
                                   created_date
                                    )
                             SELECT record_sid,
                                    guid_batch,
                                    {error_code} AS error_code,
                                    {err_source} AS err_source,
                                    now() AS create_date
                               FROM (
                                    SELECT guid_batch
                                          ,record_sid
                                          ,ROW_NUMBER() OVER (PARTITION BY LOWER({column}) ORDER BY record_sid ASC)
                                           AS recnum
                                      FROM "{schema}"."{table}"
                                     WHERE guid_batch = '{guid_batch}'
                                    ) a
                              WHERE a.recnum > 1;
"""

# check date format sql
DATE_FORMAT_SQL = """
--This function needs another proc function is_valid_date_year_format defined in pkg_utils
INSERT INTO "{schema}"."err_list" (record_sid,
                                   guid_batch,
                                   err_code,
                                   err_source,
                                   created_date
                                    )
                             SELECT record_sid,
                                    guid_batch,
                                    {error_code} AS error_code,
                                    {err_source} AS err_source,
                                    now() AS create_date
                               FROM "{schema}"."{table}"
                              WHERE batch_sid = '{guid_batch}'
                                AND pkg_utils.is_valid_date_year_format({column},'{date_format}') = 0
"""
