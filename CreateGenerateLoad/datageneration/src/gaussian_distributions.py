# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:10:09 2013

@author: kallen
"""

import random as rnd
# import matplotlib.pyplot as plt
# import numpy as np


def gauss_one(rmin, rmax, ravg=-1, rstd=-1):
    """ Generate & return a single random number according to a GAUSSIAN distribution

    If you know AVG and STD use the Python random.gauss() function directly.

    If a value for STD is supplied then it is used
    This is similar to calling random.gauss(AVG, STD) directly,
        but the output generated number is constrained to be between MIN and MAX

    If you know MIN, MAX and AVG this function first estimates a value for STD
        it is ok if AVG is not midway between MIN and MAX

    If you only know MIN and MAX the this function also calculates AVG
    """
    if (rstd == -1 or ravg == -1):
        rstd, ravg = guess_std(rmin, rmax, ravg)
    rout = rmin - 1
    while (rout < rmin or rout > rmax):
        rout = rnd.gauss(ravg, rstd)
    return rout


def gauss_list(rnum, rmin, rmax, ravg, rstd):
    """ return list of random number with gauss distribution"""
    result = [0] * rnum
    for i in range(rnum):
        rnum = int(rnd.gauss(ravg, rstd))
        if (rnum >= rmin and rnum <= rmax):
            result[i] = rnum
    return result


def guess_std(rmin, rmax, ravg=-1, rdiv=3):
    """ estimate an STD based only on min/max/avg
    allow for the avg NOT being mid way between min and max
    if avg is not supplied, that is also calculated"""
    if (ravg == -1):
        ravg = rmin + (abs(rmax - rmin)) / 2
    rstd = min(abs(ravg - rmin), abs(rmax - ravg)) / rdiv
    return rstd, ravg

# def graph_scores(smin, smax, step, values):
#    xrng = range(smin, smax, step)  # make range for the X-axis
#    h,b = np.histogram(values, xrng)
#    yAxis = list(h)             # y-axis
#    xAxis = xrng[:-1]           # x-axis
#    plt.plot(xAxis, yAxis)
#    plt.show()
#
# def list_and_show(rnum, rmin, rmax, ravg=-1, rstd=-1):
#    if (rstd == -1):
#        rstd, ravg = guess_std(rmin, rmax, ravg)
#    vals = gauss_list(rnum, rmin, rmax, ravg, rstd)
#    step = int(len(vals)/500)
#    graph_scores(rmin, rmax, step, vals)
#
# def list_and_show_2(rnum, rmin, rmax, ravg):
#    """ testing gauss_one() """
#    vals = [0] * rnum
#    for i in range(rnum):
#        val = gauss_one(rmin, rmax, ravg)
#        vals[i] = val
#    step = int(len(vals)/500)
#    graph_scores(rmin, rmax, step, vals)
#

xmin, xmax, xavg = 50, 200, 150
xnum = 1000

# list_and_show(xnum, xmin, xmax, xavg)
#
# list_and_show_2(xnum, xmin, xmax, xavg)
