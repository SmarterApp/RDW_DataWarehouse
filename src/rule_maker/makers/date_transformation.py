_calc_func_parameters = """
CREATE OR REPLACE FUNCTION {function_name}
(
{parameter_declarations}
)
RETURNS VARCHAR AS
$$
"""


def generate_transform_date_function(format_list, function_name):
    parameter_declarations = generate_parameter_declarations()
    function_top = _calc_func_parameters.format(function_name=function_name, parameter_declarations=parameter_declarations)


def generate_parameter_declarations():
    declaration = 'p_input_date VARCHAR(255);'
    return declaration


if __name__ == '__main__':
    format_list = ['Month DD, YYYY', 'Mon DD, YYYY']
    function_name = 'transform_date'
    sql_function = generate_transform_date_function(format_list, function_name)
    print(str(sql_function))
