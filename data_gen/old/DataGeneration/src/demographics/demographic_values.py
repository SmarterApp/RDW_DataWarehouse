

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
