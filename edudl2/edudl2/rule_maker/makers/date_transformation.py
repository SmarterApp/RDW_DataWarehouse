_date_transformation = """
CREATE OR REPLACE FUNCTION {function_name}(p_input_date VARCHAR)
RETURNS VARCHAR AS
$$
DECLARE
v_date_formats text[] := array{date_formats};
v_date_format text;
v_date_output_format text := '{output_format}';
v_format_found int;
v_date VARCHAR(255) := NULL;
v_date_mapped date := NULL;

BEGIN
    v_date := p_input_date;
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
        RETURN to_char(v_date_mapped, v_date_output_format);
    ELSE
        RETURN v_date;
    END IF;
END;
$$LANGUAGE plpgsql;
"""

_conf = {
    'function_name': 'transform_date',
    'formats': ['YYYY-MM-DD', 'YYYYMMDD', 'Month DD, YYYY', 'Mon DD, YYYY', 'MM-DD-YY'],
    'output_format': 'YYYYMMDD'
}


def generate_transform_date_function(date_formats, function_name, output_format):
    sql_function = _date_transformation.format(function_name=function_name, date_formats=date_formats, output_format=output_format)
    return sql_function


def stringify_list(str_list):
    double_quote_list = []
    for s in str_list:
        current_str = '\'' + s + '\''
        double_quote_list.append(current_str)
    return ','.join(double_quote_list)


if __name__ == '__main__':
    formats = stringify_list(_conf['formats'])
    output_format = _conf['output_format']
    function_name = _conf['function_name']
    sql_function = generate_transform_date_function(formats, function_name, output_format)
    print(str(sql_function))
