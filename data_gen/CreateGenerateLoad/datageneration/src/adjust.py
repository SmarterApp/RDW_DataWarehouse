'''
Created on Apr 28, 2013

@author: ken
'''


def adjust_pld(percentages, adjustment, pcs_are_floats=False, min_to_keep=1):
    """
    if adjustment is +ve make the percentages better, if -ve make them worse

    Use asjustment as a multiplier.
    if -0.5 take half of two right most percentage items and add to the left 2
    if +0.5 take half of two left most percentage items and add to the right 2
    """

    if adjustment == 0:
        return percentages

    assert(-0.90 < adjustment < 0.90)

    assert(0 < min_to_keep < 50)

    # # NOT SURE IF MAIN CODE IS USING FLOATS OR INTEGERS TO REPRESENT PERCENTAGES ...
    # # so if they are floats, make them into ints
    if pcs_are_floats:
        pcs = [round(x * 100) for x in percentages]
    else:
        pcs = list(percentages)

    # # allow for possible slight rounding error, but not more
    assert(99 <= sum(pcs) <= 101)

    # # Ok, do the work here

    mult = abs(adjustment)

    if adjustment < 0:
        from1 = -1
        from2 = -2  # take from here
        into1 = 0
        into2 = 1  # move into here
    else:
        from1 = 0
        from2 = 1
        into1 = -1
        into2 = -2

    take1 = int(mult * pcs[from1])
    pcs[from1] -= take1
    pcs[into1] += take1

    take2 = int(mult * pcs[from2])
    pcs[from2] -= take2
    pcs[into2] += take2

    assert(99 <= sum(pcs) <= 101)

    # # IF NECESSARY - convert back to floats
    if pcs_are_floats:
        newpc = [x / 100.0 for x in pcs]
    else:
        newpc = list(pcs)

    return newpc
