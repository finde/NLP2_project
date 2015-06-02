#!/usr/bin/python2


import sys
import nltk
from itertools import izip
from subprocess import call

reload(sys)
sys.setdefaultencoding("utf-8")


def loaddata(sourceF, targetF, outFile):
    toker = nltk.tokenize.RegexpTokenizer('\w+|\S+')

    sents = []
    out = open(outFile, 'w')
    counter = 1
    with open(sourceF) as sF, open(targetF) as tF:
        for s, t in izip(sF, tF):
            s = s.rstrip()
            t = t.rstrip()
            if 40 > len(t) > 0 and 40 > len(s) > 0:
                for w in toker.tokenize(s.decode('utf8')):
                    out.write(w.lower() + ' ')
                out.write("||| ")
                for w in toker.tokenize(t.decode('utf8')):
                    out.write(w.lower() + ' ')
                out.write("\n")
            counter += 1


if __name__ == "__main__":
    loaddata("data/train.es", "data/train.en", "data/train")
    call(["./fast_align-master/fast_align-master", "-i", "data/train"])
