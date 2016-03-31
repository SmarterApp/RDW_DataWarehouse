-- (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
-- below.
--
-- Education agencies that are members of the Smarter Balanced Assessment
-- Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
-- paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
-- display, distribute, perform and create derivative works of the software
-- included in the Reporting Platform, including the source code to such software.
-- This license includes the right to grant sublicenses by such consortium members
-- to third party vendors solely for the purpose of performing services on behalf
-- of such consortium member educational agencies.

DROP FUNCTION transform_date(VARCHAR);

CREATE OR REPLACE FUNCTION transform_date(p_input_date VARCHAR)
RETURNS DATE AS
$$
DECLARE 
v_date_formats text[] := array['Month DD, YYYY', 'Mon DD, YYYY']; 
v_date_format text;
v_format_found int;
v_date VARCHAR(255) := NULL;
v_date_mapped VARCHAR(255) := NULL;

BEGIN
    v_date := TRIM(REPLACE(p_input_date, CHR(13), ''));
    v_format_found := 0;
    FOREACH v_date_format IN ARRAY v_date_formats
    LOOP
        BEGIN
        v_date_mapped := to_date(v_date, v_date_format);
        IF v_date_mapped IS NOT NULL THEN
            v_format_found := 1;
            EXIT;
	END IF;
	EXCEPTION WHEN OTHERS THEN
	    -- Do nothing
	    raise notice 'exception';
        END;
    END LOOP;
    IF v_format_found = 1 THEN
        RETURN v_date_mapped;
    ELSE
        RETURN v_date;
    END IF;
END;
$$LANGUAGE plpgsql;



SELECT transform_date('Dec 20, 2000');

CREATE OR REPLACE FUNCTION test_date()
RETURNS DATE AS
$$
BEGIN
RETURN to_date('Dec 20, 2000', 'Mon DD, YYYY');
END;
$$LANGUAGE plpgsql;

SELECT test_date();



CREATE OR REPLACE FUNCTION transform_date(p_input_date VARCHAR)
RETURNS DATE AS
$$
DECLARE
v_date_formats text[] := array['Month DD, YYYY','Mon DD, YYYY'];
v_date_format text;
v_format_found int;
v_date VARCHAR(255) := NULL;
v_date_mapped VARCHAR(255) := NULL;

BEGIN
    v_date := TRIM(REPLACE(p_input_date, CHR(13), ''));
    v_format_found := 0;
    FOREACH v_date_format IN ARRAY v_date_formats
    LOOP
        BEGIN
        v_date_mapped := to_date(v_date, v_date_format);
        IF v_date_mapped IS NOT NULL THEN
            v_format_found := 1;
            EXIT;
	END IF;
	EXCEPTION WHEN OTHERS THEN
	    -- Do nothing
        END;
    END LOOP;
    IF v_format_found = 1 THEN
        RETURN v_date_mapped;
    ELSE
        RETURN v_date;
    END IF;
END;
$$LANGUAGE plpgsql;
