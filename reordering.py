import numpy as np
from random import shuffle
from itertools import izip
from operator import itemgetter
from nltk import tokenize
from collections import deque

"""
def train(sourceF,aligns):
    toker = tokenize.RegexpTokenizer('\w+|\S+')
    with open(sourceF) as srcF, open(aligns) as srcRef:
        for g,gAl in izip(srcF, srcRef):
            gToks = toker.tokenize(g.decode('utf8'))
            gP = permute(gToks) # according to ITG neigbor
            gRef = getReference(gToks,gAl)
"""


def train(toksF, aligns):
    toker = tokenize.RegexpTokenizer('\w+|\S+')
    i = 0
    with open(toksF) as srcF, open(aligns) as srcRef:
        for toks, refAlign in izip(srcF, srcRef):
            src, tar = getSents(toker.tokenize(toks))
            srcP = permute(src)  # according to ITG neigbor
            refOrder = getReference(src, refAlign)
            i += 1
            if i > 5:
                quit()


def getSents(toks):
    i = toks.index('|||')
    return toks[:i], toks[i + 1:]


def permute(srcS):
    shuffled = np.arange(len(srcS))
    shuffle(shuffled)
    return [srcS[i] for i in shuffled]


def getReference(src, alignsS):
    ltoker = tokenize.RegexpTokenizer('\d+-\d+')
    ptoker = tokenize.RegexpTokenizer('\d+')
    srcPos = []
    aligns = deque([ptoker.tokenize(al) for al in ltoker.tokenize(alignsS)])

    print "-----"
    print aligns
    try:
        while True:
            al = aligns.popleft()
            srcPos.append((src[int(al[0])], int(al[1])))
    except IndexError:
        check = [p[0] for p in srcPos]
        for s in src:
            if s not in check:
                srcPos.append((s, 0))

    srcPos.sort(key=itemgetter(1))

    print src
    # print srcPos
    # print 'src len:', len(src)
    refOrder = [p[0] for p in srcPos]

    print refOrder
    return refOrder


if __name__ == "__main__":
    train("data/train.tok.en-de", "data/training.gdfa")

"""
def train():
    i = 0
    for gW1 in gP:
        i += 1
        for gW2 in gP[i:]:
            score[gP] += B(gW1,gW2)
            
"""
