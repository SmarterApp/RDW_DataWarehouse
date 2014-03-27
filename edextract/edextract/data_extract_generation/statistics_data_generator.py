__author__ = 'ablum'


def generate_data_row(current_year_count, previous_year_count, current_year_total, previous_year_total):
    '''
    Generates a data row with statistics
    @param current_year_count: The count of a certain demographic for the current year
    @param previous_year_count: The count of a certain demographic for the previous year
    @param current_year_total: The total for the current year
    @param previous_year_total: The total for the previous year
    @return: A data row including all statistics
    '''

    percent_of_prev_year_total = _percentage(previous_year_count, previous_year_total)
    percent_of_current_year_total = _percentage(current_year_count, current_year_total)

    change_in_count = _subtract(current_year_count, previous_year_count)
    percent_difference_of_count = _percentage(change_in_count, previous_year_count)

    change_in_percentage_of_total = _subtract(percent_of_current_year_total, percent_of_prev_year_total)

    return [_format_intval(previous_year_count), _format_floatval(percent_of_prev_year_total),
            _format_intval(current_year_count), _format_floatval(percent_of_current_year_total),
            _format_intval(change_in_count), _format_floatval(percent_difference_of_count),
            _format_floatval(change_in_percentage_of_total)]


def _percentage(count, total):
    """
    Safe percentage calculating function.

    @param count: Count for some category for the year
    @param total: Total for the year

    @return: Adjusted percentage of count to total (int or None)
    """

    if count is not None and total:
        return (count / total) * 100
    else:
        return None


def _subtract(subtractor, subtractee):
    """
    Safe subtraction calculating function.

    @param subtractor: Number from which to subtract subtractee
    @param subtractee: Number which to subtract from subtractor

    @return: Adjusted subtraction of subtractee from subtractor (int or None)
    """

    if subtractor is not None and subtractee is not None:
        return subtractor - subtractee
    else:
        return None


def _format_floatval(floatval):
    """
    Convert floating point value to formatted string for report.

    @param floatval: Floating point value

    @return: Formatted string representation of floating point value
    """
    if floatval is not None:
        return str(round(floatval, 2)).rstrip('0').rstrip('.')
    else:
        return ''


def _format_intval(intval):
    """
    Convert integer value to formatted string for report.

    @param intval: Integer value

    @return: Formatted string representation of integer value
    """
    if intval is not None:
        return str(intval)
    else:
        return ''
