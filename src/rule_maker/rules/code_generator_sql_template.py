func_top = """
CREATE OR REPLACE FUNCTION {func_name}
(
    p_{col_name} IN VARCHAR
)
RETURNS VARCHAR AS
$$
DECLARE
    v_{col_name} VARCHAR(255);
    t_{col_name} VARCHAR(255);
    v_result VARCHAR(255);
BEGIN
    """

func_end = """
    ELSE
        v_result := t_{col_name};
    END IF;

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql;
"""


func_end_basic = """
    v_result := t_{col_name};

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql;
"""
