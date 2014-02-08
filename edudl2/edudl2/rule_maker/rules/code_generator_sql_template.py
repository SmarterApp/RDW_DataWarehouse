'''
Created on June 13, 2013

@author: lichen
'''


# code version
POSTGRES = 'POSTGRES'
ORACLE = 'ORACLE'

# supported code version for code generator
SUPPORTED_VERSIONS = [POSTGRES, ORACLE]

# all components in code template
FUNCTION_DEF = 'fun_def'
PARAMETER_DEF = 'parameter_def'
RETURN_DEF = 'return_def'
DECLEAR_DEF = 'declare_def'
BEGIN = 'begin'
COMMENTS = 'comments'
RETURN_STATEMENT = 'return_statement'
EXCEPTION = 'exception'
END = 'end'

# all ORDERED components in code template
TEMPLATE_COMPONENT = [FUNCTION_DEF, PARAMETER_DEF, RETURN_DEF, DECLEAR_DEF, BEGIN, COMMENTS, RETURN_STATEMENT, EXCEPTION, END]

# three kinds of code ending part
BASIC = 'basic'
IF_ELSE = 'if_else'
NOT_FOUND = 'not_found'

# code for components defined in TEMPLATE_COMPONENT
# each part has versions of code defined in SUPPORTED_VERSIONS
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
    {rclean_exp}
    RETURN v_result;
""",
            NOT_FOUND: """
    IF v_result = 'NOT FOUND' THEN
        v_result := v_{col_name};
    END IF;
    {rclean_exp}
    RETURN v_result;
""",
            IF_ELSE: """
    ELSE
        v_result := v_{col_name};
    END IF;
    {rclean_exp}
    RETURN v_result;
"""
        },
        ORACLE: {
            BASIC: """
    v_result := t_{col_name};
    {rclean_exp}
    RETURN v_result;
""",
            NOT_FOUND: """
    IF v_result = 'NOT FOUND' THEN
        v_result := v_{col_name};
    END IF;
    {rclean_exp}
    RETURN v_result;
""",
            IF_ELSE: """
    ELSE
        v_result := v_{col_name};
    END IF;
    {rclean_exp}
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


for_loop_exp = {
    POSTGRES: """
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
"""
}


# length expression
length_exp = {
    POSTGRES: """CHAR_LENGTH""",
    ORACLE: """LENGTH"""
}


# index expression for different code version
index_exp = {
    POSTGRES: """[cntr]""",
    ORACLE: """(cntr)"""
}


# substring expression for different code version
substr_exp = {
    POSTGRES: """SUBSTRING""",
    ORACLE: """SUBSTR"""
}

# array expression for different code version
array_exp = {
    POSTGRES: """{prefix}{col_name} text[] = ARRAY['{value_list}'];""",
    ORACLE: """ TYPE arr{col_name}_t IS VARRAY(255) OF VARCHAR2(255);
        {prefix}{col_name} arr{col_name}_t := {col_name}_t ('{value_list}');
        """
}


# replacing expression for different code version
repace_exp = {
    POSTGRES: """REGEXP_REPLACE({col_name}, E\'[\\n\\r]+\', \'\', 'g')""",
    ORACLE: """ REPLACE({col_name}, CHR(13), NULL)"""
}


# comment expression for different code version
comment_exp = {
    POSTGRES: """-- {comment}""",
    ORACLE: """-- {comment}"""
}

# to_char expression for different code version
tochar_exp = {
    POSTGRES: """{col_name} := CAST ({col_name} AS TEXT);""",
    ORACLE: """TO_CHAR({col_name});"""
}

# min 0 expression for different code version
min0_exp = {
    POSTGRES: """
        IF {col_name} ~ '^[0-9]+$' AND
            CAST({col_name} AS BIGINT) < 0 THEN
            {col_name} := '0';
        END IF;
""",
    # this expression might be modified
    ORACLE: """
        IF pkg_utils.is_number({col_name}) = 1 AND
           TO_NUMBER({col_name}) < 0 THEN
           {col_name} := '0';
        END IF;
"""
}


def generate_func_top(code_version):
    '''
    Function to generate the top part of the procedure code
    It is consist of function_definition, parameter_definition,
    return_definition and declaring_parameters_in _function
    '''
    fun_top_list = [TEMPLATE_CONTENT[FUNCTION_DEF][code_version],
                    TEMPLATE_CONTENT[PARAMETER_DEF][code_version],
                    TEMPLATE_CONTENT[RETURN_DEF][code_version],
                    TEMPLATE_CONTENT[DECLEAR_DEF][code_version]]
    return ''.join(fun_top_list)


def generate_func_end(code_version, second_key):
    '''
    Function to generate the ending part of the procedure code
    It is consist of return_statement, exception_handling and ending_statement
    '''
    return ''.join([TEMPLATE_CONTENT[RETURN_STATEMENT][code_version][second_key],
                    TEMPLATE_CONTENT[EXCEPTION][code_version],
                    TEMPLATE_CONTENT[END][code_version]])
