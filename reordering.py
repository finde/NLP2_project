import numpy as np
from random import shuffle
from itertools import izip
from operator import itemgetter
from nltk import tokenize
from collections import deque
from sklearn.linear_model import Perceptron
from scipy.sparse import csr_matrix
from multiprocessing import Pool

# feature templates as defined in Tromble
templateFts = ['tlm1','wl','tl','tlp1','tb','trm1','wr','tr','trp1']
templates = [[1,2,6,7],
             [1,2,6],
             [1,6,7],
             [1,2,7],
             [2,6,7],
             [1,6],
             [2,7],
             [1,2],
             [6,7],
             [1],[2],[6],[7],
             [2,4,7],
             [2,3,5,7],
             [2,3,7],
             [2,3,7,8],
             [2,7,8],
             [0,2,7,8],
             [0,2,7],
             [0,2,5,7],
             [2,5,7]]

feats = []

# main procedure
def main(sourceF, aligns):
    toker = tokenize.RegexpTokenizer('\w+|\S+')
    global feats
    feats = setFeatures(sourceF)
    print 'nr.of feats: ', len(feats)
    trainVecs = []
    srcSs = []
    refs = []
    with open(sourceF) as srcF, open(aligns) as srcRef:
        for src, refAlign in izip(srcF, srcRef):
            src = toker.tokenize(src)
            srcSs.append(src)
            refs.append(refAlign)
    split = len(srcSs)/4
    print 'start pool'
    p = Pool(processes=4)
    vecs = p.map(getFeatsMP,[(srcSs[:split],refs[:split]),(srcSs[split:2*split],refs[split:2*split]),
                             (srcSs[2*split:3*split],refs[2*split:3*split]),(srcSs[3*split:],refs[3*split:])])
    for v in vecs:
        trainVecs.extend(v)
    #print trainVecs
    print 'start training'
    X,y = getTrainVecs(trainVecs,feats)
    perceptron = Perceptron(penalty=None, alpha=0.0001, fit_intercept=True, n_iter=1, shuffle=True, verbose=0, eta0=1.0,
                            n_jobs=1, random_state=0, class_weight=None, warm_start=False)

    split = int(len(y)*.8)
    perceptron.fit(X[:split],y[:split])
    py = perceptron.predict(X[split:])
    correct = 0
    for i in range(len(py)):
        if y[split:] is py[i]:
            correct +=1
    print (float)(correct)/len(py)

def getFeatsMP((srcS,refs)):
    vecs = [] 
    for src,refAlign in izip(srcS,refs):
        srcP = permute(src)  # according to ITG neigbor
        refOrder = getReference(src, refAlign)
        vecs.extend(getFeats(srcP,refOrder,feats))
    #print 'vecs', vecs
    return vecs    
def getTrainVecs(samples, feats):
    X = []
    y = []
    for trS in samples:
        if len(trS) > 3:
            x = [0 for i in range(len(feats))]
            for f in trS[:-1]:
                x[f] = 1
            X.append(x)
            y.append(trS[-1])
            
    return csr_matrix(X), np.array(y)
    
# random reordering, must be replaced by ITG neigbor
def permute(srcS):
    shuffled = np.arange(len(srcS))
    shuffle(shuffled)
    return [srcS[i] for i in shuffled]

# sets source tokens in target order
def getReference(src, alignsS):
    ltoker = tokenize.RegexpTokenizer('\d+-\d+')
    ptoker = tokenize.RegexpTokenizer('\d+')
    srcPos = []
    aligns = deque([ptoker.tokenize(al) for al in ltoker.tokenize(alignsS)])

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
    return [p[0] for p in srcPos]

# gets for every wordpair the features as defined by the templates
# then checks if they are actually features, if so, feature index is added to vec and label is added
# return all vecs for a sentence
def getFeats(srcP,refOrder,features):
    vecs = []
    for l in range(len(srcP)):
        for i in range(len(srcP)-(l+1)):
            r = l+i+1
            feats = []
            vec = []
            for t in templates:
                feat = getFeat(srcP,l,r,[templateFts[n] for n in t])
                feats.append(feat)
                d = r-l
                if d > 10:
                    d = 11
                elif d > 5:
                    d = 6
                feat+='_'+str(d)
                feats.append(feat)
                
            for f in feats:
                try:
                    i = features.index(f)
                    vec.append(i)
                except ValueError:
                    pass
            # add label
            if refOrder.index(srcP[l]) < refOrder.index(srcP[r]):
                vec.append(1)
            #elif refOrder.index(srcP[l]) > refOrder.index(srcP[r]):
            else:
                vec.append(0)
            vecs.append(vec)
    return vecs

def setFeatures(sourceF):
    toker = tokenize.RegexpTokenizer('\w+|\S+')
    feats = []
    with open(sourceF) as srcF:
        for src in srcF:
            srcS = toker.tokenize(src)
            for l in range(len(srcS)):
                for i in range(len(srcS)-(l+1)):
                    r = l+i+1
                    for t in templates:
                        feat = getFeat(srcS,l,r,[templateFts[n] for n in t])
                        feats.append(feat)
                        d = r-l
                        if d > 10:
                            d = 11
                        elif d > 5:
                            d = 6
                        feat+='_'+str(d)
                        feats.append(feat)

    return list(set(feats))

def getFeat(w,l,r,t):
    feat = ''
    for f in t:
        try:
            if f is 'tlm1' and l>0:
                feat+=w[l-1].split('_')[1]+'_'
            if f is 'wl':
                feat+=w[l].split('_')[0]+'_'
            if f is 'tl':
                feat+=w[l].split('_')[1]+'_'
            if f is 'tlp1':
                feat+=w[l+1].split('_')[1]+'_'
            if f is 'tb':
                for i in range(len(w)):
                    if i > l and i < r:
                        feat+=w[i].split('_')[1]+'_'
            if f is 'trm1':
                feat+=w[r-1].split('_')[1]+'_'
            if f is 'wr':
                feat+=w[r].split('_')[0]+'_'
            if f is 'tr':
                feat+=w[r].split('_')[1]+'_'
            if f is 'trp1' and r<len(w)-2:
                feat+=w[r+1].split('_')[1]+'_'
        except IndexError:
            pass
    return feat[:-1]
            
if __name__ == "__main__":
    main("data/training.tagged.en.test", "data/training.gdfa.test")

