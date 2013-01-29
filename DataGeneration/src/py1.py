'''
Created on Dec 26, 2012

@author: kallen
'''


import random
import math


def calc():
    # real counts of schools in the 25 SBAC states
    s1 = [10124, 3233, 3877, 2567, 2338, 2410, 2238, 1600, 1214, 1296, 1157, 1436, 1378, 645, 757, 748, 289, 631, 480, 827, 214, 710, 516, 320, 360]

    # numbers just of testing
    s2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

    schools = sorted(s1)

    avg1 = int(avg(schools))
    std1 = int(std(schools))
    sum1 = int(sum(schools))
    min1 = min(schools)
    max1 = max(schools)

    # make up some fake school data,
    # based ONLY on derived statistical information
    # uses only: average, standard-deviation, minimum & maximum values
    madeup = makeup(schools)

    avg2 = int(avg(madeup))
    std2 = int(std(madeup))
    sum2 = int(sum(madeup))
    min2 = min(madeup)
    max2 = max(madeup)

    mup2 = makeup2(schools)

    avg3 = int(avg(mup2))
    std3 = int(std(mup2))
    sum3 = int(sum(mup2))
    min3 = min(mup2)
    max3 = max(mup2)

    print("SCHOOLS: ", schools)
    print("MADEUP:  ", madeup)
    print("MADEUP2: ", mup2)

    print("schools / made-up / made-up-2")
    print("avg=", avg1, avg2, avg3)
    print("std=", std1, std2, std3)
    print("sum=", sum1, sum2, sum3)
    print("min=", min1, min2, min3)
    print("max=", max1, max2, max3)

    print()

    print("Percentage difference between old and new values")

    avg2dif = pct(avg1, avg2)
    avg3dif = pct(avg1, avg3)
    print("avg: makeup1 then makeup2 % =", avg2dif, avg3dif)

    std2dif = pct(std1, std2)
    std3dif = pct(std1, std3)
    print("std: makeup1 then makeup2 % =", std2dif, std3dif)

    sum2dif = pct(sum1, sum2)
    sum3dif = pct(sum1, sum3)
    print("sum: makeup1 then makeup2 % =", sum2dif, sum3dif)


def pct(oldin, newin):
    return int(100 * (abs(oldin - newin) / newin))


def makeup2(seqin):
    # different approach, split sequence into two parts, lo & hi & generate random fake data on each & join together
    srt1 = sorted(seqin)
    len1 = len(srt1)
    mid1 = len1 // 2
    slo1 = srt1[:mid1]
    shi1 = srt1[mid1 + 1:]
    print("lo=", slo1)
    print("hi=", shi1)
    out1 = makeup(slo1)
    out2 = makeup(shi1)
    out3 = out1 + out2
    return out3


def makeup(seqin):
    avg1 = avg(seqin)
    std1 = std(seqin)
    min1 = min(seqin)
    max1 = max(seqin)
    len1 = len(seqin)

    out1 = makeup_core(avg1, std1, min1, max1, len1)

    out2 = sorted(out1)
    return out2


def makeup_core(avgin, stdin, minin, maxin, countin):
    # make sure the output contains at least one example of min, average and max
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
        # all values we want are integer, so covert & add to output list
        '''
        dis = math.fabs(rnd1 - total)
        if(needmore == 1 and (dis > 0.5 * avgin * countin)):
            print("keep generate, invalid ", rnd1)

        else:
        '''
        out1.append(int(rnd1))
        needmore -= 1
        total -= rnd1
        
    return out1


def avg(seqin):
    if(len(seqin) < 1):
        return None
    else:
        return sum(seqin) / len(seqin)


def std(seqin):
    if(len(seqin) < 1):
        return None
    else:
        ave = avg(seqin)
        sds = sum([(val - ave) ** 2 for val in seqin])
        dev = (sds / (len(seqin))) ** 0.5
        return dev


def mean(seqin):
    if(len(seqin) > 0):
        s_seqin = sorted(seqin)
        half = round(len(s_seqin) / 2)
        if(len(s_seqin) % 2 == 0):
            return round(s_seqin[half] + s_seqin[half - 1]) / 2
        else:
            return round(s_seqin[half])
    return None


if __name__ == '__main__':
    calc()
