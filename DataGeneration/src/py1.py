'''
Created on Dec 26, 2012

@author: kallen
'''
import random


def makeup_core(avgin, stdin, minin, maxin, countin):
    '''
    @param: avgin -- average number of a sequence
            stdin -- standard deviation of a sequence
            minin -- minimum value of a sequence
            maxin -- maximum value of a sequence
            countin -- number of required items
    @return: A sequence of number which has length of countin, and approximately
             the same average value as avgin, standard deviation value as stdin
             The sequence is calculated by Gauss distribution function
    '''
    out1 = []
    total = round(avgin * countin)
    needmore = countin
    while(needmore):
        rnd1 = random.gauss(avgin, stdin)
        # if the random number is <min or >max adjust it
        if (rnd1 < minin):
            rnd1 = minin * (1 + random.uniform(0, 0.1))
        if (rnd1 > maxin):
            rnd1 = maxin * (1 - random.uniform(0, 0.1))
        out1.append(int(rnd1))
        needmore -= 1
        total -= rnd1

    return out1


def extract_value_from_normal_distribution(avgin, stdin, minin, maxin):

    rnd1 = random.gauss(avgin, stdin)

    if (rnd1 < minin):
        rnd1 = minin * (1 + random.uniform(0, 0.1))
    if (rnd1 > maxin):
        rnd1 = maxin * (1 - random.uniform(0, 0.1))

    return rnd1


def avg(seqin):
    '''
    @return: the average number of the given sequence
    '''
    if(len(seqin) < 1):
        return None
    else:
        return sum(seqin) / len(seqin)


def std(seqin):
    '''
    @return: the standard deviation value of the given sequence
    '''
    if(len(seqin) < 1):
        return None
    else:
        ave = avg(seqin)
        sds = sum([(val - ave) ** 2 for val in seqin])
        dev = (sds / (len(seqin))) ** 0.5
        return dev
