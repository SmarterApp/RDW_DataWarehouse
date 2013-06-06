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
    v_date := TRIM(REPLACE(p_input_date, CHR(13), NULL));
    v_format_found := 0;
    FOREACH v_date_format IN ARRAY v_date_formats
    LOOP
        BEGIN
        raise notice '%', v_date_format;
        v_date_mapped := to_date(v_date, v_date_format);
        v_format_found := 1;
        EXIT;
        EXCEPTION WHEN OTHERS THEN
            -- Do nothing, continue with loop
        END;
    END LOOP;
    IF v_format_found == 1 THEN
        RETURN v_date_mapped;
    ELSE
        RETURN v_date;
    END IF;
EXCEPTION
WHEN OTHERS THEN
RETURN v_date;
END;
$$LANGUAGE plpgsql;



SELECT transform_date('Dec 20, 2000');