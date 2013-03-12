'''
Created on Mar 11, 2013

@author: dwu
'''


def normalize_percentages(percentages):
    '''
    normalize a list of percentages to always add up to 100
    '''

    # round each percentage down and calculate sum
    # also, keep track of decimal values
    pct_decimals = []
    pct_rounded = []
    for idx, percentage in enumerate(percentages):
        val = idx, percentage % 1
        pct_decimals.append(val)
        pct_rounded.append(int(percentage))

    # if sum is less than 100, add 1 to percentages in decreasing order of decimals
    num_to_add = 100 - sum(pct_rounded)
    if num_to_add > 0:
        pct_decimals = sorted(pct_decimals, key=lambda element: element[1])
        for i in range(num_to_add):
            idx = pct_decimals[len(pct_decimals) - i - 1][0]
            pct_rounded[idx] = pct_rounded[idx] + 1

    return pct_rounded
