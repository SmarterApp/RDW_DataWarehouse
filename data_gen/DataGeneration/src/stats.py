'''
Created on Apr 19, 2013

@author: kallen
'''

import random


def weighted_sum(values, percentages):
    """ given a list of numeric values and a corresponding list of percentages
        return a weighted sum : sum of each value multiplied by its percentage

        INPUT:
        values = list of numeric values
        percentages = list of percentages

        OUTPUT:
        wsum = weighted sum (rounded down to the nearest integer)

    """

    assert(len(values) > 0 and len(percentages) == len(values))

    wsum = sum([(val * pct) for (val, pct) in zip(values, percentages)])

    return wsum


def approx_equal(x, y, tol=1e-11, msg=False):
    if x == y:
        return True

    if x + tol >= y and x - tol <= y:
        return True

    if msg:
        print(" X is NOT approximatly equal to Y with: X=%s, Y=%s, tol=%s" % (x, y, tol))

    return False


def distribute_by_percentages(value, range_min, range_max, percentages):
    """ given a value, its range (min/max) and a list of percentages
        return a list of values 'close' to the input value
        and where the weighted sum of the return list is equal to the input value

        INPUT:
        value = value to be distributed
        range_min = minimum allowed value
        range_max = maximum allowed value
        percentages = list of percentages

        OUTPUT:
        out = list of values (the weighted sum of which is equal to the input value)

        NOTES:
        The current purpose of this function is to 'reverse engineer' a list of claim scores
            from a single overall score and a list of percentages.

        The overall score and the claim scores all have the same min/max range values.
        If this changes then the approach here will need to change.

        Since we have one 'equation' and N unknowns there is no one right answer.

        So, we will use a simple Heuristic to generate the output values:

        0. If the input value is 'too close' to either min or max (i.e. < 10% away)
            just return a list with all elements == value

        1. Generate some small number that is the maximum unscaled variation between
            the input value and any output value - call this R
            a. calculate the distance between the input value and the closest extreme (min or max)
            b. multiply by the smallest input percentage
                this helps keep the later scaled up out value within the min/max range

        2. If we need N output values, split R into N/2 positive parts and N/2 negative parts
            so that they all sum to zero
        3. Randomly shuffle the list of generated numbers
        4. Scale up the numbers by the inverse of the supplied percentages
        5. Add the input value to each number

        This should produce a list of numbers which when combined as a weighted sum equal the input value
        Due to rounding errors there might be a very slight difference between the weighted sum & the input value
            but (probably) not more that +/- 1

    """

    assert(range_min >= 0)
    assert(range_min <= value <= range_max)
    assert(approx_equal(sum(percentages), 1))

    assert(len(percentages) > 0)

    # all percentages in the list must be greater than or equal to 1%
    # just so that the scaled values do not get to extreme
    for pc in percentages:
        assert(pc >= 0.01)

    # distance between value and nearest extreme (min or max)
    distance = min(value - range_min, range_max - value)

    half_width = (range_max - range_min) / 2

    # if the input value is less than 10% from either min or max
    #    just return a list with all elements == value
    BUFFER_PCT = 0.1
    if (distance / half_width) < BUFFER_PCT:
        out = [value] * len(percentages)
        return out

    # make fudge depend on smallest percentage, so that when scaled up output value
    #    is between range_min anmd range_max
    distance_fudge = distance * min(percentages)

    # make fudge no more than some fraction of the range width
    #    so that it is not too large for center values
    width_fudge = half_width * 0.05

    fudge = int(min(distance_fudge, width_fudge))

    # a list of numbers which sum to zero
    zero_list = _zero_sum_split(fudge, len(percentages))

    # scale them up and add the input value
    out = _scaled_up(zero_list, percentages, value)

    return out


def _scaled_up(num_list, percentages, base_value=0):
    out = [base_value + int(v / p) for (v, p) in zip(num_list, percentages)]
    return out


def _zero_sum_split(value, need):
    """ split a value into a list which sums to the value and where half the list is positive and half is negative
    """
    need_pos = int(need / 2)
    need_neg = need - need_pos

    neg_list = _random_split(-value, need_pos)
    pos_list = _random_split(value, need_neg)
    out = neg_list + pos_list
    random.shuffle(out)

    assert(sum(out) == 0)

    return out


def _random_split(value, parts):
    """ split an integer value into N parts which sum to that value - no part is ever less than 1

        INPUT:
        value = value to be split
        parts = number of parts

        OUTPUT:
        out = list of parts : where sum(out) == value

    """

    assert(parts > 0)

    pval = abs(value)
    out = [0] * parts
    sign = value / pval

    need = parts - 1
    left = pval
    for i in range(need):
        val = random.randint(0, left)
        out[i] = sign * val
        left -= val

    out[need] = sign * left

    assert(value == sum(out))

    return out
