"""Method for choosing an object randomly, given weights.

If many choices are to be made using the same weights, WeightedChooser might be more efficient.

:author: mjacob
:date: February 25, 2014
"""
import random
import itertools
import bisect


def weighted_choice(counter: {object: float},
                    rng: random.Random=random.Random(),
                    seed=None) -> object:
    """Choose a random item based on a weight.

    :param counter: a mapping from objects to their respective weights"""
    if seed is not None:
        rng.seed(seed)

    elements, weights = zip(*counter.items())

    assert(all(weight >= 0 for weight in weights))

    breaks = list(itertools.accumulate(weights))
    value = rng.uniform(0, breaks[-1])
    i = bisect.bisect(breaks, value)

    if i < 0 or i >= len(elements):
        raise AssertionError("chose a non-existent element? %s %s %s" % (counter, i, elements))

    return elements[i]


class WeightedChooser:
    def __init__(self,
                 weights_by_object: {object: float},
                 rng: random.Random=random.Random()):
        self.elements, weights = zip(*weights_by_object.items())
        self.breaks = tuple(itertools.accumulate(weights))
        self.rng = rng

    def choose(self, seed=None):
        if seed is not None:
            self.rng.seed(seed)

        value = self.rng.uniform(0, self.breaks[-1])  # a random float between 0 and the sum of the weights
        i = bisect.bisect(self.breaks, value)  # the index

        return self.elements[i]
