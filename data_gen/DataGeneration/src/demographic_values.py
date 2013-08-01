

def get_demo_values(total, possible_value_list, percentage_list):
    '''
    Main function to generate demographic value
    @param total: total number of students
    @param possible_value_list: list of lists. Each list has possible values for one demographic
    @param percentage_list: list of lists. Each list has percentage number for one demographic of four performance level.
    '''
    results = []
    if total > 0:
        if len(possible_value_list) == len(percentage_list) and len(possible_value_list) > 0:
            for i in range(len(possible_value_list)):
                results.append(get_single_demo_value(total, possible_value_list[i], percentage_list[i]))
    return results


def get_single_demo_value(total, possible_value, percentage):
    results = {}

    # ensure valid values
    if len(possible_value) != len(percentage) or len(possible_value) <= 0:
        return results

    # loop values and calculate count
    for i in range(len(possible_value)):
        value = possible_value[i]
        perc = percentage[i]
        count = total * perc / 100
        results[value] = count

    return results


if __name__ == '__main__':

    total = 1235
    possible_value_list = [['male', 'female', 'not stated'],
                           ['1', '2', '3', '4', '5', '6', '7', '8']]
    percentage_list = [[33, 34, 33],
                       [10, 10, 10, 5, 5, 5, 5, 50]]
    results = get_demo_values(total, possible_value_list, percentage_list)
    for r in results:
        print(len(r))
    print(results)
