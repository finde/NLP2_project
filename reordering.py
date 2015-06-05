import numpy as np
from random import shuffle
from itertools import izip
from operator import itemgetter
from nltk import tokenize

def train(sourceF,aligns):
    toker = tokenize.RegexpTokenizer('\w+|\S+')
    with open(sourceF) as srcF, open(aligns) as srcRef:
        for g,gAl in izip(srcF, srcRef):
            gP = permute(toker.tokenize(g.decode('utf8'))) # according to ITG neigbor
            gRef = getReference(g,gAl)

def permute(gerS):
    shuffled = np.arange(len(gerS))
    shuffle(shuffled)
    return [gerS[i] for i in shuffled]

def getReference(g, gAl):
    ltoker = tokenize.RegexpTokenizer('\d-\d')
    ptoker = tokenize.RegexpTokenizer('\d')
    gRef = []
    for al in ltoker.tokenize(gAl):
        pair = ptoker.tokenize(al)
        gRef.append(g[int(pair[1])])

    print "-----\n"
    print g
    print gRef
    
    return gRef
if __name__ == "__main__":
    train("data/train.de", "data/training.gdfa")

"""
def train():
    i = 0
    for gW1 in gP:
        i += 1
        for gW2 in gP[i:]:
            score[gP] += B(gW1,gW2)
            
"""
