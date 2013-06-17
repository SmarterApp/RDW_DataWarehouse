POSTGRES = 'POSTGRES'
ORACLE = 'ORACLE'

SUPPORTED_VERSIONS = [POSTGRES, ORACLE]


FUNCTION_DEF = 'fun_def'
PARAMETER_DEF = 'parameter_def'
RETURN_DEF = 'return_def'
DECLEAR_DEF = 'declare'
BEGIN = 'begin'
RETURN_STATEMENT = 'return_statement'
EXCEPTION = 'exception'
END = 'end'

TEMPLATE_COMPONENT = [FUNCTION_DEF, PARAMETER_DEF, RETURN_DEF, DECLEAR_DEF, BEGIN, RETURN_STATEMENT, EXCEPTION, END]

BASIC = 'basic'
IF_ELSE = 'if_else'
NOT_FOUND = 'not_found'

TEMPLATE_CONTENT = {
FUNCTION_DEF: {
POSTGRES: """CREATE OR REPLACE FUNCTION {func_name}""",
ORACLE: """FUNCTION {func_name}"""
},

PARAMETER_DEF: {
POSTGRES: """
(
    p_{col_name} IN VARCHAR
)""",
ORACLE: """
(
    p_{col_name} IN VARCHAR2
)"""
},

RETURN_DEF: {
POSTGRES: """
RETURNS VARCHAR AS
$$""",
ORACLE: """
RETURN VARCHAR2"""
},


DECLEAR_DEF: {
POSTGRES: """
DECLARE
    v_{col_name} VARCHAR(255);
    t_{col_name} VARCHAR(255);
    v_result VARCHAR(255);
""",
ORACLE: """
IS
    v_{col_name} VARCHAR2(255);
    t_{col_name} VARCHAR2(255);
    v_result VARCHAR2(255);
"""
},


RETURN_STATEMENT: {
POSTGRES: {
           BASIC: """
    v_result := t_{col_name};

    RETURN v_result;
    """,
           NOT_FOUND: """
    IF v_result = 'NOT FOUND' THEN
        v_result := v_{col_name};
    END IF;

    RETURN v_result;
           """,
           IF_ELSE: """
    ELSE
        v_result := v_{col_name};
    END IF;
    RETURN v_result;
           """
},
ORACLE: {
           BASIC: """
    v_result := t_{col_name};

    RETURN v_result;
    """,
           NOT_FOUND: """
    IF v_result = 'NOT FOUND' THEN
        v_result := v_{col_name};
    END IF;

    RETURN v_result;
           """,
           IF_ELSE: """
    ELSE
        v_result := v_{col_name};
    END IF;
    RETURN v_result;
           """
        }
},


EXCEPTION: {
POSTGRES: """
EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
""",
ORACLE: """
EXCEPTION
    WHEN OTHERS THEN
        RETURN v_{col_name};
"""
},


END: {
POSTGRES: """END;
$$ LANGUAGE plpgsql;
""",
ORACLE: """END {func_name};
"""
}
}


for_loop_exp = {POSTGRES: """
    FOR cntr IN array_lower({count_value}{col_name}, 1)..array_upper({count_value}{col_name}, 1)
    LOOP
            {if_statement}
            v_result := vals_{col_name}[cntr];
            EXIT;
        END IF;
    END LOOP;
    """,
ORACLE: """
    FOR cntr IN 1..{count_value}{col_name}.COUNT
    LOOP
            {if_statement}
            v_result := vals_{col_name}(cntr);
            EXIT;
        END IF;
    END LOOP;
    """}


length_exp = {POSTGRES: """CHAR_LENGTH""",
              ORACLE: """LENGTH"""
}


index_exp = {POSTGRES: """[cntr]""",
              ORACLE: """(cntr)"""
             }

substr_exp = {
              POSTGRES: """SUBSTRING""",
              ORACLE: """SUBSTR"""
             }

array_exp = {
             POSTGRES: """{prefix}{col_name} text[] = ARRAY['{value_list}'];""",
             ORACLE: """ TYPE {col_name}_t IS VARRAY(255) OF VARCHAR2(255);
        {prefix}{col_name} {col_name}_t := {col_name}_t ('{value_list}');
        """
             }


repace_exp = {POSTGRES: """REPLACE({col_name}, CHR(13), \'\');""",
             ORACLE: """ REPLACE({col_name}, CHR(13), NULL);"""
             }


def generate_func_top(code_version):
    return ''.join([TEMPLATE_CONTENT[FUNCTION_DEF][code_version],
                   TEMPLATE_CONTENT[PARAMETER_DEF][code_version],
                   TEMPLATE_CONTENT[RETURN_DEF][code_version],
                   TEMPLATE_CONTENT[DECLEAR_DEF][code_version]])


def generate_func_end(code_version, second_key):
    return ''.join([TEMPLATE_CONTENT[RETURN_STATEMENT][code_version][second_key],
                   TEMPLATE_CONTENT[EXCEPTION][code_version],
                   TEMPLATE_CONTENT[END][code_version]])
