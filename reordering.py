import numpy as np
from random import shuffle
from itertools import izip
from operator import itemgetter
from nltk import tokenize
from collections import deque
from sklearn.linear_model import Perceptron
from scipy.sparse import csr_matrix
from multiprocessing import Pool
from random import randint

# feature templates as defined in Tromble
templateFts = ['tlm1', 'wl', 'tl', 'tlp1', 'tb', 'trm1', 'wr', 'tr', 'trp1']
templates = [[1, 2, 6, 7],
             [1, 2, 6],
             [1, 6, 7],
             [1, 2, 7],
             [2, 6, 7],
             [1, 6],
             [2, 7],
             [1, 2],
             [6, 7],
             [1], [2], [6], [7],
             [2, 4, 7],
             [2, 3, 5, 7],
             [2, 3, 7],
             [2, 3, 7, 8],
             [2, 7, 8],
             [0, 2, 7, 8],
             [0, 2, 7],
             [0, 2, 5, 7],
             [2, 5, 7]]

features = []
perceptron = Perceptron(penalty=None, alpha=0.0001, fit_intercept=True, n_iter=1, shuffle=True, verbose=0, eta0=1.0,
                        n_jobs=1, random_state=0, class_weight=None, warm_start=False)


# main procedure
def main(sourceF, aligns):
    toker = tokenize.RegexpTokenizer('\w+|\S+')
    global features
    features = setFeatures(sourceF)
    print 'nr.of feats: ', len(features)
    trainVecs = []
    srcSs = []
    refs = []
    perms = []
    with open(sourceF) as srcF, open(aligns) as srcRef:
        for src, refAlign in izip(srcF, srcRef):
            src = toker.tokenize(src)
            srcSs.append(src)
            refs.append(refAlign)
            perms.append(randomPermute(src, 1))

    split = len(srcSs) / 5
    testSs = srcSs[4 * split:]
    testPerms = perms[4 * split:]
    testPerms.append([6, 7, 8])  # reasonable permutation, should (mostly) be chosen over random (for testing purposes)
    iters = 2  # until measure gives low error
    for i in range(iters):
        p = Pool(4)
        if i > 0:
            print 'searching best neighbors'

            srcNBs = p.map(getBestNeighbor, [(srcSs[:split], perms[:split]),
                                             (srcSs[split:2 * split], perms[split:2 * split]),
                                             (srcSs[2 * split:3 * split], perms[2 * split:3 * split]),
                                             (srcSs[3 * split:4 * split], perms[3 * split:4 * split])])
            srcSs = []
            for s in srcNBs:
                srcSs.extend(s)
                print '--', s

        p = Pool(4)
        print 'building train vectors'
        vecs = p.map(getFeatsMP, [(srcSs[:split], refs[:split]),
                                  (srcSs[split:2 * split], refs[split:2 * split]),
                                  (srcSs[2 * split:3 * split], refs[2 * split:3 * split]),
                                  (srcSs[3 * split:4 * split], refs[3 * split:4 * split])])

        for v in vecs:
            trainVecs.extend(v)

        print 'start training'
        X, y = getVecs(trainVecs)
        global perceptron
        perceptron = perceptron.fit(X, y)

    print 'start testing'
    split = len(testSs)  # /4 to use 4 parrallel (while testing use only 1 sentence)
    bestNBs = p.map(getBestNeighbor, [(testSs[:split], testPerms[:split]),
                                      (testSs[split:2 * split], testPerms[split:2 * split]),
                                      (testSs[2 * split:3 * split], testPerms[2 * split:3 * split]),
                                      (testSs[3 * split:4 * split], testPerms[3 * split:4 * split])])
    resSs = [bestNBs[i] for i in range(len(bestNBs))]

    for src, res in zip(testSs, resSs):
        print '----'
        print src, '\n', testPerms[0], '\n', resSs[0][0]
        print '---'


def getBestNeighbor((srcSs, permus)):
    nhbs = []
    for srcS, perms in zip(srcSs, permus):
        n = len(srcS)
        beta = {}
        delta = {}
        for i in range(n - 1):
            beta[i, i + 1] = 0
            for k in range(i, n):
                delta[i, i, k] = 0
                delta[i, k, k] = 0

        swap = [0, 0, 0]
        for w in range(n)[2:]:
            for i in range(n - w):
                k = i + w
                beta[i, k] = -10 ** 10
                for j in range(n)[i + 1:k]:
                    if [i, j, k] in perms:
                        if (i, j, k) not in delta:
                            delta = getDelta(srcS, i, j, k, delta)
                        bta = delta[i, j, k] + beta[i, j] + beta[j, k]
                        if bta >= beta[i, k]:
                            beta[i, k] = bta
                            swap = [i, j, k]
        print 'best swap', swap
        nhbs.append(getSwap(srcS, swap))
    return nhbs


def getDelta(srcS, i, j, k, delta):
    if (i, j, k - 1) not in delta:
        delta = getDelta(srcS, i, j, k - 1, delta)
    if (i + 1, j, k) not in delta:
        delta = getDelta(srcS, i + 1, j, k, delta)
    if (i + 1, j, k - 1) not in delta:
        delta = getDelta(srcS, i + 1, j, k - 1, delta)

    delta[i, j, k] = delta[i, j, k - 1] + delta[i + 1, j, k] - delta[i + 1, j, k - 1] + score(
        getSwap(srcS, [i, i + 1, k]), i + 1, k) - score(srcS, i + 1, k)
    return delta
    """
    da = getDelta(srcS,i,j,k-1)
    db = getDelta(srcS,i+1,j,k)
    dc = getDelta(srcS,i+1,j,k-1)
    dd = score(getSwap(srcS,[i,i+1,k]),i+1,k)
    df = score(srcS,i+1,k)

    return da+db-dc+dd-df
    """


def getSwap(src, swap):
    [i, j, k] = swap
    permS = []
    if sum(swap) is 0:
        return src
    permS.extend(src[:i + 1])
    permS.extend(src[j + 1:k + 1])
    permS.extend(src[i + 1:j + 1])
    permS.extend(src[k + 1:])
    return permS


def score(sen, l, r):
    if l > r:  # swap words
        print 'l to the right of r ...'
    d = r - l
    score = 0
    intervalVecs = []

    for i in range(len(sen[l:r])):
        for j in range(len(sen[l + 1:r + 1])):
            sampleFts = []
            for t in templates:
                feat = getFeat(sen, l + i, l + 1 + j, [templateFts[n] for n in t])
                sampleFts.append(feat)
                if d > 10:
                    d = 11
                elif d > 5:
                    d = 6
                feat += '_' + str(d)
                sampleFts.append(feat)
            vec = []
            for f in sampleFts:
                try:
                    i = features.index(f)
                    vec.append(i)
                except ValueError:
                    pass
            intervalVecs.append(vec)
    return sum(perceptron.predict(getVecs(intervalVecs, False)))


def getFeatsMP((srcS, refs)):
    vecs = []
    for src, refAlign in izip(srcS, refs):
        # srcP = permute(src)  # according to ITG neigbor
        refOrder = getReference(src, refAlign)
        vecs.extend(getFeats(src, refOrder))
    # print 'vecs', vecs
    return vecs


def getVecs(samples, train=True):
    X = []
    y = []
    for s in samples:
        x = [0 for i in range(len(features))]
        if train:
            sample = s[:-1]
        else:
            sample = s
        for f in sample:
            x[f] = 1
        X.append(x)
        if train:
            y.append(s[-1])
    if train:
        return csr_matrix(X), np.array(y)
    else:
        return csr_matrix(X)


# random reordering, must be replaced by ITG neigbor
def randomPermute(srcS, n):
    perms = []
    for i in range(n):
        perm = [randint(0, len(srcS)) for i in range(3)]
        perm.sort()
        perms.append(perm)
    return perms


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
def getFeats(src, refOrder):
    vecs = []
    for l in range(len(refOrder)):
        for i in range(len(refOrder) - (l + 1)):
            r = l + i + 1
            feats = []
            vec = []
            for t in templates:
                feat = getFeat(refOrder, l, r, [templateFts[n] for n in t])
                feats.append(feat)
                d = r - l
                if d > 10:
                    d = 11
                elif d > 5:
                    d = 6
                feat += '_' + str(d)
                feats.append(feat)

            for f in feats:
                try:
                    i = features.index(f)
                    vec.append(i)
                except ValueError:
                    pass
            # add label
            if src.index(refOrder[l]) < src.index(refOrder[r]):
                vec.append(1)
            # elif refOrder.index(srcP[l]) > refOrder.index(srcP[r]):
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
                for i in range(len(srcS) - (l + 1)):
                    r = l + i + 1
                    for t in templates:
                        feat = getFeat(srcS, l, r, [templateFts[n] for n in t])
                        feats.append(feat)
                        d = r - l
                        if d > 10:
                            d = 11
                        elif d > 5:
                            d = 6
                        feat += '_' + str(d)
                        feats.append(feat)

    return list(set(feats))


def getFeat(w, l, r, t):
    feat = ''
    for f in t:
        try:
            if f is 'tlm1' and l > 0:
                feat += w[l - 1].split('_')[1] + '_'
            if f is 'wl':
                feat += w[l].split('_')[0] + '_'
            if f is 'tl':
                feat += w[l].split('_')[1] + '_'
            if f is 'tlp1':
                feat += w[l + 1].split('_')[1] + '_'
            if f is 'tb':
                if r - l < 5:  # if farther apart then do not use this feature
                    for i in range(len(w)):
                        if i > l and i < r:
                            feat += w[i].split('_')[1] + '_'
            if f is 'trm1':
                feat += w[r - 1].split('_')[1] + '_'
            if f is 'wr':
                feat += w[r].split('_')[0] + '_'
            if f is 'tr':
                feat += w[r].split('_')[1] + '_'
            if f is 'trp1' and r < len(w) - 2:
                feat += w[r + 1].split('_')[1] + '_'
        except IndexError:
            pass
    return feat[:-1]


if __name__ == "__main__":
    main("data/training.tagged.en.test", "data/training.gdfa.test")

