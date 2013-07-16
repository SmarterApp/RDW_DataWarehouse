import re

FUNC_NAME = 'func'


_calc_func_parameters = """
CREATE OR REPLACE FUNCTION {func_name}
(
{parameter_declarations}
)
RETURNS VARCHAR AS
$$
"""

_calc_func_variables = """
DECLARE
{variable_declarations}
"""

_calc_func_prepare_variables = """
BEGIN
{variable_preparations}
"""

_calc_func_check_variables = """
CASE
{variable_checks}
"""

_calc_func_body = """
THEN
{formula}
"""

__calc_func_end = """
ELSE
v_return := v_{unknown_col}
END IF;

RETURN v_return;

EXCEPTION
WHEN OTHERS THEN
RETURN v_{unknown_col};
END;
$$ LANGUAGE plpgsql
    """


def create_calculated_value_sql_function(function_name, function_formula, known_column_names, unknown_column_name):
    result = ''

    all_column_names = known_column_names[:]
    all_column_names.append(unknown_column_name)

    parameter_declarations = generate_parameter_declarations(all_column_names)
    sql_params = _calc_func_parameters.format(func_name=function_name, parameter_declarations=parameter_declarations)

    variable_declarations = generate_variable_declarations(all_column_names)
    sql_vars = _calc_func_variables.format(variable_declarations=variable_declarations)

    variable_preparations = generate_variable_preparations(all_column_names)
    sql_preparations = _calc_func_prepare_variables.format(variable_preparations=variable_preparations)

    variable_checks = generate_variable_checks(unknown_column_name, known_column_names)
    sql_var_checks = _calc_func_check_variables.format(variable_checks=variable_checks)

    function_body = generate_function_body(function_formula)

    function_end = generate_function_end(unknown_column_name)

    result = sql_params + sql_vars + sql_preparations + sql_var_checks + function_body + function_end

    return result


def generate_parameter_declarations(param_list):
    result = []
    for param in param_list:
        param_base_name = param
        declaration = generate_parameter_declaration(param_base_name)
        result.append(declaration)
    return ',\n'.join(result).strip()


def generate_parameter_declaration(base_name, var_type='VARCHAR(255)'):
    parameter_declaration = 'p_{base_name} {var_type}'
    result = parameter_declaration.format(base_name=base_name, var_type=var_type.upper())
    return result


def generate_variable_declarations(var_list):
    declarations = []
    for var in var_list:
        var_base_name = var
        declaration = generate_variable_declaration(var_base_name)
        declarations.append(declaration)
    # Declare the 'return' variable too
    return_declaration = generate_variable_declaration('result')
    declarations.append(return_declaration)
    result = '\n'.join(declarations)
    return result


def generate_variable_declaration(base_name, var_type='VARCHAR(255)'):
    variable_declaration = 'v_{base_name} {var_type};'
    result = variable_declaration.format(base_name=base_name, var_type=var_type)
    return result


def generate_variable_preparations(var_list):
    result = ''
    for var in var_list:
        var_base_name = var
        preparation = generate_variable_preparation(var_base_name)
        result = result + preparation + '\n'
    return result.strip()


def generate_variable_preparation(base_name):
    variable_preparation = 'v_{base_name} := TRIM(REPLACE(p_{base_name}, CHR(13), NULL));'
    result = variable_preparation.format(base_name=base_name)
    return result


def generate_variable_checks(unknown_column_name, known_column_names):
    result = ''
    variable_checks = []

    unknown_variable_check = generate_variable_check(unknown_column_name, is_null=True)
    variable_checks.append(unknown_variable_check)

    for column_name in known_column_names:
        variable_check = generate_variable_check(column_name, include_when=False)
        variable_checks.append(variable_check)
        result = result + variable_check
    result = ' AND\n'.join(variable_checks)
    return result.strip()


def generate_variable_check(base_name, is_null=False, include_when=True):
    variable_check = "WHEN v_{base_name} IS {null_or_not}" if include_when else "v_{base_name} IS {null_or_not}"
    null_or_not = "NULL" if is_null else "NOT NULL"
    result = variable_check.format(base_name=base_name, null_or_not=null_or_not)
    return result


def generate_function_body(formula):
    sql_formula = format_formula(formula)
    body = _calc_func_body.format(formula=sql_formula)
    return body.strip()


def format_formula(formula):
    col_names = find_all_cols(formula)
    for col_name in col_names:
        var_name = format_variable_name(col_name)
        var_name = wrap_variable(var_name)
        formula = formula.replace(col_name, var_name)
    formula = wrap_formula(formula)
    return formula


def format_variable_name(col_name):
    variable_name = col_name.strip()
    variable_name = remove_brackets(variable_name)
    variable_name = 'v_' + variable_name
    return variable_name


def remove_brackets(string_with_brackets):
    string_without_brackets = string_with_brackets.replace('{', '')
    string_without_brackets = string_without_brackets.replace('}', '')
    return string_without_brackets


def find_all_cols(formula):
    regex = re.compile("{.*?}")
    var_names = regex.findall(formula)
    return var_names


# vclean
def wrap_variable(var_name, wrapper="(%s::int)"):
    return wrapper % var_name


# rclean
def wrap_formula(formula, wrapper="ceiling(%s)::int;"):
    return wrapper % formula


def generate_function_end(unknown_column_name):
    func_end = __calc_func_end.format(unknown_col=unknown_column_name)
    return func_end


if __name__ == '__main__':
    unknown_column_name = 'daze_correct'
    known_column_names = ['daze_incorrect', 'daze_adjusted']
    function_name = 'function_1'
    function_formula = '({daze_incorrect}-{daze_adjusted})/2'
    result = create_calculated_value_sql_function(function_name, function_formula, known_column_names, unknown_column_name)
    print(str(result))


'''
 FUNCTION calc_daze_correct
    (
        p_!!NEED## IN VARCHAR
        p_!!HAVE#1 IN VARCHAR
        p_!!HAVE#2 IN VARCHAR
    )
    RETURN udl_stg.dnext_stg.daze_correct%TYPE
    IS
        v_daze_correct   udl_stg.dnext_stg.daze_correct%TYPE;
        v_daze_incorrect udl_stg.dnext_stg.daze_incorrect%TYPE;
        v_daze_adjusted  udl_stg.dnext_stg.daze_adjusted%TYPE;
        v_return         udl_stg.dnext_stg.daze_correct%TYPE;
    BEGIN
        v_daze_correct := TRIM(REPLACE(p_daze_correct, CHR(13), NULL));
        v_daze_incorrect := TRIM(REPLACE(p_daze_incorrect, CHR(13), NULL));
        v_daze_adjusted := TRIM(REPLACE(p_daze_adjusted, CHR(13), NULL));
        v_return := CASE
                    WHEN v_daze_correct IS NULL
                     AND v_daze_incorrect IS NOT NULL
                     AND v_daze_adjusted IS NOT NULL
                     AND pkg_utils.is_number(v_daze_incorrect) = 1
                     AND pkg_utils.is_number(v_daze_adjusted) = 1
                    THEN
                         TO_CHAR(CEIL(TO_NUMBER(v_daze_adjusted) + (TO_NUMBER(v_daze_incorrect)/2)))
                    ELSE
                         v_daze_correct
                     END;

        IF pkg_utils.is_number(v_return) = 1 AND
           TO_NUMBER(v_return) < 0 THEN
           v_return := '0';
        END IF;

        RETURN v_return;
    END calc_daze_correct;
'''

"""
v_{need} := TRIM(REPLACE(p_{need}, CHR(13), NULL));
    v_{have_1} := TRIM(REPLACE(v_{have_1}, CHR(13), NULL));
    v_{have_2} := TRIM(REPLACE(v_{have_2}, CHR(13), NULL));
"""
