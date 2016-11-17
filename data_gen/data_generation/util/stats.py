__author__ = 'mjacob'
import math
import random
import bisect
import itertools


def mean(counts: [int]) -> float:
    """ find the mean *value* of the given *counts*

    @param counts: the 0th element is taken to be the relative count of the value "0", the 1st element the counts of
    the value "1", and so on.
    """
    return sum(value * count for value, count in enumerate(counts)) / sum(counts)


def stdv(counts: [int], mean_: int=None) -> float:
    """ find the stdv *value* of the given *counts*

    @param counts: the 0th element is taken to be the relative count of the value "0", the 1st element the counts of
    the value "1", and so on.
    @param mean_: If you already know the mean, save some computation by supplying it!"""
    if mean_ is None:
        mean_ = mean(counts)

    print(mean_)

    for value, count in enumerate(counts):
        print(value, (value-mean_) ** 2, count)

    return math.sqrt(sum(((value - mean_) ** 2) * count
                         for value, count in enumerate(counts))
                     / sum(counts))


def normalize(values: [float], total: float=1.0) -> [float]:
    """normalize an array of numeric values, so that the sum of the elements corresponds to the given total.
    """
    assert(all(value >= 0 for value in values))
    sum_ = sum(values)

    if sum_ == 0.0:
        return values

    else:
        return tuple(total * value / sum_ for value in values)
