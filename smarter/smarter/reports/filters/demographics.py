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


def get_ethnicity(filters, table):
    selected = filters.get(Constants_filter_names.ETHNICITY)

    true_filter_map = {Constants_filter_names.AMI: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN],
                       Constants_filter_names.ASN: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN],
                       Constants_filter_names.BLK: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK],
                       Constants_filter_names.WHT: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE],
                       Constants_filter_names.PCF: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC],
                       Constants_filter_names.HSP: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC]}

    false_filter_map = {Constants_filter_names.AMI: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC],
                        Constants_filter_names.ASN: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC],
                        Constants_filter_names.BLK: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC],
                        Constants_filter_names.WHT: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC],
                        Constants_filter_names.PCF: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                                                     Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE],
                        Constants_filter_names.NOT_STATED: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
                                                            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
                                                            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
                                                            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE,
                                                            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC,
                                                            Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC]}

    rtn_list = []

    for ethnic in selected:
        # Handle 'Two or more' ethnics selection differently
        if ethnic == Constants_filter_names.TWO:
            # Merge the list
            rtn_list.append(two_or_more_ethnicity(table))
        else:
            criterias = get_new_criterias()
            true_value_column = true_filter_map.get(ethnic)
            false_value_column = false_filter_map.get(ethnic)

            if true_value_column:
                for column in true_value_column:
                    criterias[column] = True
            if false_value_column:
                for column in false_value_column:
                    criterias[column] = False

            expr = convert_to_binary_expr(criterias, table)
            rtn_list.append(expr)

    return or_(*rtn_list)


def get_new_criterias():
    criterias = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: None,
                 Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE: None}
    return criterias.copy()


def convert_to_binary_expr(convert_map, table):
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


def two_or_more_ethnicity(table):
    ethnics = [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN,
               Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN,
               Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK,
               Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC,
               Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE]
    # initialize expression
    expr = 0
    no_hisp = or_(table.c[Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC] == false(), table.c[Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC] == null())
    for ethnic in ethnics:
        and_clause = and_(table.c[ethnic] == true(), no_hisp)
        case_stmt = case([(and_clause, 1)], else_=0)
        expr = expr + case_stmt
    return expr >= 2
