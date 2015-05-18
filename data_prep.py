#!/usr/bin/python2


import sys
import nltk
from itertools import izip

reload(sys)
sys.setdefaultencoding("utf-8")


def loaddata(sourceF, targetF, outFile):
    toker = nltk.tokenize.RegexpTokenizer('\w+|\S+')

    sents = []
    out = open(outFile, 'w')
    with open(sourceF) as sF, open(targetF) as tF:
        for s, t in izip(sF, tF):
            if len(s) < 40 and len(t) < 40:
                for w in toker.tokenize(s.decode('utf8')):
                    out.write(w.lower() + ' ')
                out.write("||| ")
                for w in toker.tokenize(t.decode('utf8')):
                    out.write(w.lower() + ' ')
                out.write("\n")


if __name__ == "__main__":
    loaddata("data/train.es", "data/train.en", "data/train")
