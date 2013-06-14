POSTGRES = 'POSTGRES'
ORACLE = 'ORACLE'

SUPPORTED_VERSIONS = [POSTGRES]

func_top = {POSTGRES: """
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
    """}

func_end = {POSTGRES: """
    ELSE
        v_result := v_{col_name};
    END IF;

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql;
"""}


func_end_basic = {POSTGRES: """
    v_result := t_{col_name};

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql;
"""}


func_end_for_not_found = {POSTGRES: """
    IF v_result = 'NOT FOUND' THEN
        v_result := v_{col_name};
    END IF;

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
END;
$$ LANGUAGE plpgsql;
"""}


for_loop_exp = {POSTGRES: """
    FOR cntr IN array_lower({count_value}{col_name}, 1)..array_upper({count_value}{col_name}, 1)
    LOOP
            {if_statement}
            v_result := vals_{col_name}[cntr];
            EXIT;
        END IF;
    END LOOP;
    """}
