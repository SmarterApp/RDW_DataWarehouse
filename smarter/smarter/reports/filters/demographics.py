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
                  Constants_filter_names.NOT_STATED: null()
                  }
    where_clause = None
    expr = []
    target_filter = filters.get(filter_name, None)
    if target_filter:
        for f in target_filter:
            try:
                expr.append(column == filter_map[f])
            except:
                pass
    if expr:
        where_clause = or_(*expr)
    return where_clause


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
            value_map = get_ethnicity_value_map()
            false_value_columns = get_false_value_columns(ethnic)

            # "Not stated" will not have to set any columns to True
            if ethnic in value_map:
                value_map[ethnic].append(Constants_filter_names.YES)

            for column in false_value_columns:
                # values of FALSE or NULL
                value_map[column].append(Constants_filter_names.NO)
                value_map[column].append(Constants_filter_names.NOT_STATED)

            # convert to sqlalchemy expressions for current ethnic selection
            expr = convert_to_expression(value_map, table)
            # append to list of all clauses
            clauses.append(expr)

    return or_(*clauses)


def get_ethnicity_value_map():
    '''
    Returns a map of ethnicity columns used to store column values

    :rtype dict
    :returns a dictionary that maps column names to a value of None
    '''
    value_map = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN: [],
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN: [],
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK: [],
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC: [],
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: [],
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE: []}
    return value_map.copy()


def get_false_value_columns(name):
    '''
    Based on the ethnicity filter, return the columns that should be set to False

    :param string name:  name of the ethnicity filter
    '''
    if name == Constants_filter_names.NOT_STATED:
        return list_of_ethnics
    elif name == Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC:
        return []
    else:
        # Remove itself from the list
        results = list_of_ethnics.copy()
        results.remove(name)
        return results


def convert_to_expression(filters, table):
    '''
    Given a map of column names and value, convert to sqlalchemy expression

    :param filters: dict containing column values mapped to a value of YES/NO/NOT STATED
    :param table:  sqlalchemy table that contains the columns for demographics
    '''
    and_clause = []
    for column in filters.keys():
        clause = get_demographic_filter(column, table.c[column], filters)
        if clause is not None:
            and_clause.append(clause)
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
    for ethnic in non_hisp_ethnics:
        and_clause = and_(table.c[ethnic] == true(), no_hisp)
        # Creates a case expression that returns 1 if row contains an ethnicity and hispanic is False or NULL
        # Case statements are added together to produce how many ethnics a student has
        expr = expr + case([(and_clause, 1)], else_=0)
    # Final expression is that the sum of all the case statements should be at least 2
    return expr >= 2
