'''
Created on Aug 14, 2013

@author: kallen
'''


EX1 = {'head': ['typical1', 'math', '3'],
       'data': {'all': [0.0, 100.0, 5.0, 26.0, 39.0, 30.0],
                'male': [1.0, 51.0, 6.0, 25.0, 38.0, 31.0],
                'female': [1.0, 49.0, 5.0, 26.0, 39.0, 30.0],
                'not_stated': [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                'dmg_eth_blk': [2.0, 18.0, 10.0, 38.0, 37.0, 15.0],
                'dmg_eth_asn': [2.0, 7.0, 2.0, 10.0, 31.0, 57.0],
                'dmg_eth_hsp': [2.0, 22.0, 8.0, 33.0, 40.0, 19.0],
                'dmg_eth_wht': [2.0, 47.0, 3.0, 19.0, 41.0, 37.0],
                'dmg_eth_ami': [2.0, 1.0, 8.0, 34.0, 36.0, 22.0],
                'dmg_eth_2mr': [2.0, 1.0, 5.0, 28.0, 37.0, 30.0],
                'dmg_eth_nst': [2.0, 2.0, 4.0, 47.0, 31.0, 18.0],
                'dmg_eth_pcf': [2.0, 2.0, 2.0, 15.0, 53.0, 30.0],
                'dmg_prg_504': [3.0, 8.0, 21.0, 44.0, 26.0, 9.0],
                'dmg_prg_iep': [3.0, 16.0, 21.0, 44.0, 26.0, 9.0],
                'dmg_prg_tt1': [5.0, 56.0, 8.0, 33.0, 38.0, 21.0],
                'dmg_prg_lep': [4.0, 9.0, 15.0, 42.0, 33.0, 10.0],
                }
       }

EX2 = {'head': ['typical1', 'math', '5'],
       'data': {'all': [0.0, 100.0, 7.0, 26.0, 39.0, 28.0],
                'male': [1.0, 50.0, 8.0, 26.0, 37.0, 29.0],
                'female': [1.0, 49.0, 7.0, 25.0, 40.0, 28.0],
                'not_stated': [1.0, 1.0, 9.0, 30.0, 51.0, 10.0],
                'dmg_eth_pcf': [2.0, 2.0, 2.0, 15.0, 53.0, 30.0],
                'dmg_eth_nst': [2.0, 2.0, 4.0, 47.0, 31.0, 18.0],
                'dmg_eth_hsp': [2.0, 20.0, 10.0, 33.0, 38.0, 19.0],
                'dmg_eth_wht': [2.0, 48.0, 5.0, 21.0, 40.0, 34.0],
                'dmg_eth_ami': [2.0, 0.0, 13.0, 34.0, 35.0, 18.0],
                'dmg_eth_blk': [2.0, 19.0, 13.0, 36.0, 36.0, 15.0],
                'dmg_eth_2mr': [2.0, 1.0, 9.0, 29.0, 35.0, 27.0],
                'dmg_eth_asn': [2.0, 8.0, 3.0, 11.0, 30.0, 56.0],
                'dmg_prg_lep': [4.0, 8.0, 21.0, 42.0, 28.0, 9.0],
                'dmg_prg_504': [3.0, 8.0, 27.0, 42.0, 25.0, 6.0],
                'dmg_prg_iep': [3.0, 16.0, 27.0, 42.0, 25.0, 6.0],
                'dmg_prg_tt1': [5.0, 56.0, 10.0, 33.0, 37.0, 20.0]
                }
       }

EX3 = {'head': ['typical1', 'math', '6'],
       'data': {'female': [1.0, 49.0, 7.0, 26.0, 36.0, 31.0],
                'dmg_eth_2mr': [2.0, 1.0, 7.0, 30.0, 32.0, 31.0],
                'not_stated': [1.0, 1.0, 9.0, 30.0, 51.0, 10.0],
                'dmg_eth_asn': [2.0, 9.0, 3.0, 11.0, 26.0, 60.0],
                'dmg_eth_ami': [2.0, 0.0, 12.0, 35.0, 34.0, 19.0],
                'dmg_eth_wht': [2.0, 47.0, 5.0, 20.0, 38.0, 37.0],
                'all': [0.0, 100.0, 8.0, 27.0, 34.0, 31.0],
                'dmg_prg_504': [3.0, 8.0, 29.0, 44.0, 21.0, 6.0],
                'dmg_eth_blk': [2.0, 19.0, 14.0, 39.0, 32.0, 15.0],
                'male': [1.0, 50.0, 9.0, 28.0, 33.0, 30.0],
                'dmg_prg_iep': [3.0, 16.0, 29.0, 44.0, 21.0, 6.0],
                'dmg_prg_lep': [4.0, 6.0, 27.0, 44.0, 21.0, 8.0],
                'dmg_eth_pcf': [2.0, 2.0, 2.0, 15.0, 53.0, 30.0],
                'dmg_prg_tt1': [5.0, 54.0, 12.0, 35.0, 33.0, 20.0],
                'dmg_eth_hsp': [2.0, 20.0, 12.0, 36.0, 34.0, 18.0],
                'dmg_eth_nst': [2.0, 2.0, 4.0, 47.0, 31.0, 18.0]
                }
       }

DIFF_OK = 0.001

MIN_DIF = 0.003


def numlist2str(mylist, myformat=" % 06.4f"):
    out = ""
    for num in mylist:
        out += myformat % num
    return out


class DemogGroup():

    @classmethod
    def fromCsvBlock(cls, csv_block, group_number, type_id='', subject='', grade=''):
        total = DemogLine.fromCsvBlock(csv_block, 'all')
        demog_group = DemogGroup(total, type_id, subject, grade)

        for name in csv_block:
            line = csv_block[name]
            demog_line = DemogLine(line, name)
            if demog_line.group == group_number:
                demog_group.add_demog_line(demog_line)

        demog_group.finish_init()
        return demog_group

    def finish_init(self):
        self.rows = len(self.group)
        self.do_sums()
        self.do_difs()
        self.saved_difs = self.difs[:]
        self.saved_sums = self.sums[:]

    def __init__(self, total_demog_line, type_id='', subject='', grade=''):
        self.type_id = type_id
        self.subject = subject
        self.grade = grade
        self.rows = 0
        self.cols = len(total_demog_line.parts)
        self.total = total_demog_line
        self.group = []
        self.sums = [0] * self.cols
        self.difs = [0] * self.cols

    def add_demog_line(self, demog_line):
        self.group.append(demog_line)

    def __str__(self):
        out = "type_id: %s, subject: %s, grade: %s\n" % (self.type_id, self.subject, self.grade)
        out += str(self.total)
        for line in self.group:
            out += "\n" + str(line)
        out += "\n   sums: " + numlist2str(self.sums)
        out += "\n   difs: " + numlist2str(self.difs)
        return out

    def sum_col(self, col):
        out = 0.0
        for line in self.group:
            out += line.parts2[col]
        return out

    def do_sums(self):
        for col in range(self.cols):
            self.sums[col] = self.sum_col(col)

    def do_difs(self):
        for col in range(self.cols):
            self.difs[col] = self.total.parts2[col] - self.sums[col]

    def get_col(self, col):
        out = [0] * self.rows
        for row in range(self.rows):
            out[row] = self.group[row].parts2[col]
        return out

    def get_max(self, colnum):
        col = self.get_col(colnum)
        mymax = max(col)
        myind = col.index(mymax)
        return(myind, mymax)

    def print_ok(self, mydif, colA, colB, difA, difB, myind, mymax):
        basic = "newdif: % 06.4f : fixing column pair: %d, %d difs: % 06.4f, % 06.4f, fixing row %d, current value=% 06.4f " % (
            mydif, colA, colB, difA, difB, myind, mymax)

        if self.grade != '':
            print(" OK: [%s/%s/%s],  %s" % (self.type_id, self.subject, self.grade, basic))
        else:
            print(" OK: %s" % basic)

    def print_bad(self, mydif, colA, colB, difA, difB):
        basic = "newdif: % 06.4f : ***cannot fix pair: %d, %d difs: % 06.4f, % 06.4f" % (
            mydif, colA, colB, difA, difB)

        if self.grade != '':
            print("BAD: [%s/%s/%s],  %s" % (self.type_id, self.subject, self.grade, basic))
        else:
            print("BAD: %s" % basic)

    ###***###
    def fix_pair(self, colA, colB, TOLERANCE=0.003, showbad=True):
        difA = self.difs[colA]
        difB = self.difs[colB]

        if abs(difA) < DIFF_OK and abs(difB) < DIFF_OK:
            return True

        mydif = abs(difA + difB)
        if mydif > TOLERANCE:
            if showbad:
                self.print_bad(mydif, colA, colB, difA, difB)
            return False

        # select the smallest absolute value
        # add it to the column it comes from
        # and subtract it from the other column

        if abs(difA) <= abs(difB):
            myind, mymax = self.get_max(colA)
        else:
            myind, mymax = self.get_max(colB)

        # self.print_ok(mydif, colA, colB, difA, difB, myind, mymax)

        line = self.group[myind]

        if abs(difA) <= abs(difB):
            line.parts2[colA] += difA
            line.parts2[colB] -= difA
        else:
            line.parts2[colA] -= difB
            line.parts2[colB] += difB

        self.do_sums()
        self.do_difs()

        difA2 = self.difs[colA]
        difB2 = self.difs[colB]

        oldA = line.oldparts[colA]
        oldB = line.oldparts[colB]

        newA0 = line.parts2[colA]
        newB0 = line.parts2[colB]

        newA = (newA0 / line.total) * 100
        newB = (newB0 / line.total) * 100

        idstr2 = self.idstr(line)

        if not showbad:
            print("FIXING: %s  cols[%d,%d] old[% 04.2f, % 04.2f] new[% 07.4f, % 07.4f] newdifs[% 06.4f, % 06.4f]" % (
                idstr2, colA, colB, oldA, oldB, newA, newB, difA2, difB2))

        return True

    def idstr(self, line):
        out = "[%s/%s/%s/%s]" % (self.type_id, self.subject, self.grade, line.name)
        padto = 32
        outlen = len(out)
        need = padto - outlen
        out += " " * need
        return out

    #########################################
    def fixup(self):
        fixed1 = self.fix_pair(0, 1, 0.01, False)
        fixed2 = self.fix_pair(2, 3, 0.01, False)
        self.fix_pair(1, 2, 0.01, False)

        self.fix_pair(0, 1, 0.003)
        self.fix_pair(2, 3, 0.003)
        self.fix_pair(1, 2, 0.003)

#         if not fixed1 and not fixed2:
#             self.fix_pair(1,2, 0.01, False)
#             fixed1 = self.fix_pair(0,1, 0.003)
#             fixed2 = self.fix_pair(2,3, 0.003)
#             self.fix_pair(1,2, 0.003)
        return fixed1 and fixed2
    #########################################


class DemogLine():
    def __init__(self, line, name=""):
        self.name = name
        self.group = int(line[0])
        self.total = line[1] / 100.0
        self.oldparts = line[2:]
        self.parts = [x / 100.0 for x in line[2:]]
        self.parts2 = [x * self.total for x in self.parts]

    def __str__(self):
        return "{parts2: %s, group: %s, total: %04.2f, parts: %s,  name: %s}" % (
            numlist2str(self.parts2), str(self.group), self.total, numlist2str(self.parts, " %04.2f"), self.name)

    @classmethod
    def fromCsvBlock(cls, csv_block, name_key):
        line = csv_block[name_key]
        demog_line = DemogLine(line, name_key)

        return demog_line


def try1(csv_block):
    line = DemogLine.fromCsvBlock(csv_block, 'all')
    print(line)

    group1 = DemogGroup.fromCsvBlock(csv_block, 1)
    print("\n" + str(group1))

    group2 = DemogGroup.fromCsvBlock(csv_block, 2)
    print("\n" + str(group2))

    col0 = group2.get_col(0)
    print(numlist2str(col0))

    myind, mymax = group2.get_max(0)
    print("myind=%d, mymax=% 06.4f" % (myind, mymax))

    group2.fix_pair(0, 1)
    group2.fix_pair(2, 3)

    group1.fix_pair(0, 1)
    group1.fix_pair(2, 3)

    # group1.fix_pair(0,3)


def tryfix(csv_block, group_num):
    print("\ntrying to fix group: %d" % (group_num))
    group = DemogGroup.fromCsvBlock(csv_block, group_num)
    print("BEFORE:\n" + str(group))

    group.fixup()

    print("AFTER:\n" + str(group))


def fix1(csv_block):
    tryfix(csv_block, 1)
    tryfix(csv_block, 2)


def tryfix2(csv_block, group_num, type_id, subject, grade):
    group = DemogGroup.fromCsvBlock(csv_block, group_num, type_id, subject, grade)
    fixed = group.fixup()
    if not fixed:
        print(str(group))
    return group


def tryfixboth(csv_block, type_id, subject, grade):
    tryfix2(csv_block, 1, type_id, subject, grade)
    tryfix2(csv_block, 2, type_id, subject, grade)


def fix2(csv_more):
    print("\n")
    type_id, subject, grade = csv_more['head']
    csv_block = csv_more['data']
    tryfixboth(csv_block, type_id, subject, grade)


if __name__ == '__main__':
    # fix1(EX1['data'])
    fix2(EX1)
    fix2(EX2)
    fix2(EX3)
