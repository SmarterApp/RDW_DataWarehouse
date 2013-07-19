'''
Created on Jul 11, 2013

@author: tosako
'''
from smarter.reports.filters import Constants_filter_names
from sqlalchemy.sql.expression import true, false, or_, null, and_, case
from smarter.reports.helpers.constants import Constants
import copy


# Maps Yes, No and Not Stated to equivalent SQLAlchemey values
filter_map = {Constants_filter_names.YES: true(),
              Constants_filter_names.NO: false(),
              Constants_filter_names.NOT_STATED: null()}

# maps filter values to column names
map_of_ethnics = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN: Constants.DMG_ETH_AMI,
                  Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN: Constants.DMG_ETH_ASN,
                  Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK: Constants.DMG_ETH_BLK,
                  Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC: Constants.DMG_ETH_HSP,
                  Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: Constants.DMG_ETH_PCF,
                  Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE: Constants.DMG_ETH_WHT}

# Map of ethnicity columns
ethnicity_value_map = {Constants.DMG_ETH_AMI: [],
                       Constants.DMG_ETH_ASN: [],
                       Constants.DMG_ETH_BLK: [],
                       Constants.DMG_ETH_HSP: [],
                       Constants.DMG_ETH_PCF: [],
                       Constants.DMG_ETH_WHT: []}


def get_demographic_filter(filter_name, column, filters):
    '''
    Apply filters for Disability

    :rtype: sqlalchemy.sql.select
    :returns: list of filters to be applied to query
    '''
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
        if ethnic == Constants_filter_names.DEMOGRAPHICS_ETHNICITY_MULTI:
            clauses.append(get_two_or_more_ethnicity_expr(table))
        else:
            value_map = get_ethnicity_value_map()
            # Based on filter name, get the corresponding column name
            column_name = map_of_ethnics.get(ethnic)
            false_value_columns = get_false_value_columns(column_name)

            # "Not stated" will not have to set any columns to True
            if column_name in value_map:
                value_map[column_name].append(Constants_filter_names.YES)

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
    return copy.deepcopy(ethnicity_value_map)


def get_false_value_columns(name):
    '''
    Based on the ethnicity filter, return the columns that should be set to False

    :param string name:  name of the ethnicity filter
    '''
    if name is None:
        # multi (two or more race) wiill have a name of none
        return get_list_of_ethnic_columns()
    elif name == Constants.DMG_ETH_HSP:
        return []
    else:
        # Remove itself from the list
        results = get_list_of_ethnic_columns()
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
    non_hisp_ethnics = get_list_of_ethnic_columns()
    non_hisp_ethnics.remove(Constants.DMG_ETH_HSP)

    # initialize expression
    expr = 0
    no_hisp = or_(table.c[Constants.DMG_ETH_HSP] == false(), table.c[Constants.DMG_ETH_HSP] == null())
    for ethnic in non_hisp_ethnics:
        and_clause = and_(table.c[ethnic] == true(), no_hisp)
        # Creates a case expression that returns 1 if row contains an ethnicity and hispanic is False or NULL
        # Case statements are added together to produce how many ethnics a student has
        expr = expr + case([(and_clause, 1)], else_=0)
    # Final expression is that the sum of all the case statements should be at least 2
    return expr >= 2


def get_list_of_ethnic_columns():
    '''
    Returns a list of ethnic column names
    '''
    return copy.deepcopy(list(map_of_ethnics.values()))
