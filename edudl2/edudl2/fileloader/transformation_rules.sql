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

CREATE OR REPLACE FUNCTION map_gender
(
    p_gender  IN  VARCHAR
)
RETURNS VARCHAR AS
$$
DECLARE
    v_gender      VARCHAR(255);
    v_return      VARCHAR(255);
BEGIN
    v_gender := TRIM(REPLACE(UPPER(p_gender), CHR(13), ''));

    IF SUBSTRING(v_gender, 1,1) = 'M' OR SUBSTRING(v_gender, 1,1) = 'B' THEN  
       v_return := 'M';
    ELSIF SUBSTRING(v_gender, 1,1) = 'F' OR SUBSTRING(v_gender, 1,1) = 'G' THEN  
       v_return := 'F';
    ELSIF SUBSTRING(v_gender, 1,2) = 'NS' 
	   OR SUBSTRING(v_gender, 1,13) = 'NOT_SPECIFIED' 
	   OR SUBSTRING(v_gender, 1,13) = 'NOT SPECIFIED' THEN  
          v_return := 'NS';
    ELSE
       v_return := v_gender;
    END IF;
        
    RETURN v_return;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_gender;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION map_yn
(
    p_yn      IN  VARCHAR
)
RETURNS VARCHAR AS
$$
DECLARE
    v_yn          VARCHAR(255);
    v_return      VARCHAR(255);
BEGIN
    v_yn := TRIM(REPLACE(UPPER(p_yn), CHR(13), ''));

    IF SUBSTRING(v_yn, 1,1) = 'Y' OR SUBSTRING(v_yn, 1,1) = '1' THEN  
       v_return := 'Y';
    ELSIF SUBSTRING(v_yn, 1,1) = 'N' OR SUBSTRING(v_yn, 1,1) = '0' THEN  
       v_return := 'N';
    ELSE
       v_return := v_yn;
    END IF;
        
    RETURN v_return;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_yn;
END;
$$ LANGUAGE plpgsql;