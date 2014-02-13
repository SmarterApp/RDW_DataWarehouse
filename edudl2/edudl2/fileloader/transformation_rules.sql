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