'''
Created on Apr 15, 2013

@author: kallen
'''

import random


def _calc_ebmax(smin, smax, ebmax_divisor):
    """ used only for helping with unit-tests """
    return (smax - smin) / ebmax_divisor


def calc_eb_params(smin, smax, ebmin_divisor, ebmax_divisor):
    """ calculate and return the parameters needed by the calc_eb function

        INPUTS:
        smin = minimum score (1200)
        smax = maximum score (2400)
        ebmin_divisor = minimum value of the error band expressed as a fraction (actually as the divisor) of the score range (32 => 1/32)
        ebmax_divisor = maximum value of the error band expressed as a fraction (actually as the divisor) of the score range ( 8 => 1/8)

        OUTPUTS:
        scenter = center of score range
        ebmin = minimum error band size
        ebstep = error band size per step (i.e. per score point)
    """
    assert(smin > 0 and smax > smin)
    assert(ebmax_divisor > 0 and ebmin_divisor > ebmax_divisor)
    srange = smax - smin
    ebmin = srange / ebmin_divisor
    ebmax = srange / ebmax_divisor
    scenter = smin + srange / 2
    ebsteps = srange / 2
    ebrange = ebmax - ebmin
    ebstep = ebrange / ebsteps
    return scenter, ebmin, ebstep


def _calc_ebhalf(score, scenter, ebmin, ebstep):
    return ebmin + (ebstep * abs(score - scenter))


def _add_random(ebhalf, rndlo, rndhi):
    if (rndlo != 0 or rndhi != 0):
        ebhalf += random.randrange(rndlo, rndhi)
    return ebhalf


def _calc_band(score, ebhalf):
    return (score - ebhalf), (score + ebhalf)


def _clip_eb(ebleft, ebright, smin, smax, clip_eb):
    if (clip_eb):
        ebleft = max(ebleft, smin)
        ebright = min(ebright, smax)
    return ebleft, ebright


def calc_eb(score, smin, smax, scenter, ebmin, ebstep, rndlo=0, rndhi=0, clip_eb=True, ensure_symmetry=False):
    """ calculate and return the error band (ebleft, ebright)

        INPUT:
        @param score: actual score achived by student
        @param smin: minimum score
        @param smax: maximum score
        @param scenter: center of score range (1800)
        @param ebmin: minimum error band size (37.5)
        @param ebstep: size of error band per score point (step size)
        @param rndlo: low value of random number to be added to calculate error band
        @param rndhi: high value of random number to be added to calculate error band
        @param clip_eb: if True then 'clip' the calculate error band so that it does not exceed smin or smax
        @param ensure_symmetry: if True then ensure both error bands are equal distance away from the score

        Note: scenter, ebmin, ebstep can be first calculted using the function calc_eb_parms()

        OUTPUT:
        @return:
        ebleft = error band score to the left of the actual score (possibly clipped at smin)
        ebright = error band score to the right of the actual score (possibly clipped at smax)
        ebhalf = unclipped width of half the error band
    """
    ebhalf = _calc_ebhalf(score, scenter, ebmin, ebstep)    # calculate the error band half width
    ebhalf = _add_random(ebhalf, rndlo, rndhi)              # make some random adjustment if required
    ebleft, ebright = _calc_band(score, ebhalf)             # calculate actual error band scores
    ebleft, ebright = _clip_eb(ebleft, ebright, smin, smax, clip_eb)    # clip error band scores at min/max if flag set
    if ensure_symmetry:
        size_to_right = abs(round(ebright) - score)
        size_to_left = abs(round(ebleft) - score)
        if size_to_right != size_to_left:
            min_size = min(size_to_right, size_to_left)
            ebleft, ebright = (score - min_size, score + min_size)
            assert ebleft >= smin and ebright <= smax

    return ebleft, ebright, ebhalf
