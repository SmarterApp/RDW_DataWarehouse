'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from sqlalchemy.sql.expression import true, false, or_, null, and_, case


def get_demographic_filter(filter_name, column, filters):
    '''
    apply filters for Disability
    :rtype: sqlalchemy.sql.select
    :returns: list of filters to be applied to query
    '''
    filter_map = {Constants_filter_names.YES: true(),
                  Constants_filter_names.NO: false(),
                  Constants_filter_names.NOT_STATED: None
                  }
    where_clause = None
    disabled_filter = []
    target_filter = filters.get(filter_name, None)
    if target_filter:
        for f in target_filter:
            try:
                disabled_filter.append(column == filter_map[f])
            except:
                pass
    if disabled_filter:
        if len(disabled_filter) == 1:
            where_clause = disabled_filter[0]
        else:
            where_clause = or_(disabled_filter)
    return where_clause


# Maps filter values to column name
ethnics_filter_map = {Constants_filter_names.AMI: Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                      Constants_filter_names.ASN: Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                      Constants_filter_names.BLK: Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                      Constants_filter_names.WHT: Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE,
                      Constants_filter_names.PCF: Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC,
                      Constants_filter_names.HSP: Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC}

# list of column names of all list_of_ethnics
list_of_ethnics = [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                   Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                   Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                   Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC,
                   Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE,
                   Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC]


def get_ethnicity_filter(filters, table):
    '''
    Returns sqlalchemy binary expression based on ethnicity filters

    :param dict filters: filters specified by user
    :param table: sqlalchemy fact_asmt_outcome table
    '''
    ethnics = filters.get(Constants_filter_names.ETHNICITY)

    clauses = []

    for ethnic in ethnics:
        # Handle 'Two or more' list_of_ethnics selection differently
        if ethnic == Constants_filter_names.TWO:
            clauses.append(get_two_or_more_ethnicity_expr(table))
        else:
            criterias = get_new_criterias()
            true_value_column = ethnics_filter_map.get(ethnic)
            false_value_columns = get_false_value_columns(ethnic)

            if true_value_column:
                criterias[true_value_column] = True

            for column in false_value_columns:
                criterias[column] = False
            # convert to sqlalchemy expressions for current ethnic selection
            expr = convert_to_expression(criterias, table)
            # append to list of all clauses
            clauses.append(expr)

    return or_(*clauses)


def get_new_criterias():
    '''
    Returns a map of ethnicity columns used to store column value

    :rtype dict
    :returns a dictionary that maps column names to a value of None
    '''
    criterias = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE: None}
    return criterias.copy()


def get_false_value_columns(name):
    '''
    Based on the filter, return the columns that should be set to False
    '''
    if name == Constants_filter_names.NOT_STATED:
        return list_of_ethnics
    elif name == Constants_filter_names.HSP:
        return []
    else:
        # Based on filter value, get the corresponding column name and remove it from the list
        # Since we know that that column should have a value of True
        column_name = ethnics_filter_map.get(name)
        results = list_of_ethnics.copy()
        results.remove(column_name)
        return results


def convert_to_expression(convert_map, table):
    '''
    Given a map of column names and value of True/False/None, convert to sqlalchemy expression

    :param convert_map: dict containing column values mapped to a value of True/False/None
    :param table:  sqlalchemy table that contains the columns for demographics
    '''
    value_map = {True: [true()],
                 False: [false(), null()],
                 None: []}
    and_clause = []
    for column, value in convert_map.items():
        or_clause = []
        for map_value in value_map[value]:
            or_clause.append(table.c[column] == map_value)
        and_clause.append(or_(*or_clause))
    return and_(*and_clause)


def get_two_or_more_ethnicity_expr(table):
    '''
    Returns an expression that checks for 2 or more ethnicity

    :returns: sqlalchemy binary expression
    '''
    # Get all the list_of_ethnics except for hispanic
    non_hisp_ethnics = list_of_ethnics.copy()
    non_hisp_ethnics.remove(Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC)

    # initialize expression
    expr = 0
    no_hisp = or_(table.c[Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC] == false(), table.c[Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC] == null())
    for ethnic in list_of_ethnics:
        and_clause = and_(table.c[ethnic] == true(), no_hisp)
        expr = expr + case([(and_clause, 1)], else_=0)
    return expr >= 2
