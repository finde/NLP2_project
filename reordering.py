from itertools import izip
from operator import itemgetter
from collections import deque
from multiprocessing import Pool
from random import randint
import argparse

import numpy as np
from nltk import tokenize
from sklearn.linear_model import Perceptron
from scipy.sparse import csr_matrix

from itg_parse import main as itg_parser, is_nonterminal



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


def generate_splits(n, split, A, B):
    return [(A[x * split:(x + 1) * split], B[x * split:(x + 1) * split]) for x in range(n)]


def get_itg_permutations(src, tree, max_perms):
    def rule_decoder(rule_str):
        perm = []
        lhs = rule_str[1:-1].split(',')[1].split('-')
        i = int(lhs[0])
        j = int(lhs[1])
        perm.extend([i])
        perm.extend([j])
        perm.sort()

        return perm

    if tree != 'NO PARSE FOUND':
        perms = []

        for rule in tree:
            if len(perms) < max_perms and len(rule.rhs) > 1 and sum(map(is_nonterminal, rule.rhs)) == 1:
                # transform lhs and rhs to (i, j, k)
                perm = rule_decoder(rule.lhs)
                rhs = filter(lambda x: x.startswith('[X,'), rule.rhs)[0]
                perm.extend(rule_decoder(rhs))
                perms.append(list(set(perm)))

        return perms

    else:
        return [[0, 0, 0]]


# main procedure
def main(args):
    sourceF = args.source_language
    sourceF_no_tags = args.source_language_without_tags
    aligns = args.alignments

    # todo: print settings

    toker = tokenize.RegexpTokenizer('\w+|\S+')
    global features
    features = setFeatures(sourceF)[:200000]  # up to 200000 features
    print 'nr.of feats: ', len(features)
    print 'permutation:', 'ITG' if args.itg else 'Random'
    trainVecs = []
    srcSs = []
    refs = []
    perms = []
    with open(sourceF) as srcF, open(aligns) as srcRef, open(sourceF_no_tags) as srcF_nt:
        for str_no, (_src, refAlign, sentence) in enumerate(izip(srcF, srcRef, srcF_nt)):
            src = toker.tokenize(_src)
            srcSs.append(src)
            refs.append(refAlign)

            # get permutation from ITG
            if args.itg:
                tree = itg_parser(use_cache=args.use_cache, grammar_file=args.grammar, input_str=sentence, best=True,
                                  key=str_no)
                perms.append(get_itg_permutations(src, tree, 5))
            else:
                perms.append(randomPermute(src, 5))

    # train 75% - test 25%
    ratio_train = .5
    split_index = int(np.floor(len(srcSs) * ratio_train))

    split = split_index / args.njobs

    # last batch for testing
    if ratio_train < 1:
        devSs = srcSs[:split_index]
        devPerms = srcSs[:split_index]
        testSs = srcSs[split_index:]
        testPerms = perms[split_index:]

    # testPerms.append([6, 7, 8])  # reasonable permutation, should (mostly) be chosen over random (for testing purposes)
    iters = 5  # until measure gives low error
    for i in range(iters):
        print '\n=== iteration %d ===' % (i + 1)

        # a = generate_splits(args.njobs, split, srcSs, perms)
        # print a

        p = Pool(args.njobs)
        if i > 0:
            print 'searching best neighbors'

            srcNBs = p.map(getBestNeighbor, generate_splits(args.njobs, split, srcSs, perms))
            srcSs = []
            for s in srcNBs:
                srcSs.extend(s)
                # print '--', s

        p = Pool(args.njobs)
        print 'building train vectors..'
        vecs = p.map(getFeatsMP, generate_splits(args.njobs, split, srcSs, refs))

        for v in vecs:
            trainVecs.extend(v)

        print 'training model..'
        X, y = getVecs(trainVecs)
        global perceptron
        perceptron = perceptron.fit(X, y)

    print '\n=== create dev n test ==='

    # dev
    args.njobs = 1
    split = len(devSs) / args.njobs
    p = Pool(args.njobs)
    bestNBs = p.map(getBestNeighbor, generate_splits(args.njobs, split, devSs, devPerms))

    resSs = []
    for s in bestNBs:
        resSs.extend(s)

    with open(sourceF + '.dev.src', 'w') as srcF, open(sourceF + '.dev.res', 'w') as resF:
        for src, res in zip(testSs[:len(resSs)], resSs):
            srcF.write(reduce(lambda x, y: x + ' ' + y, map(lambda x: x.split('_')[0], src)) + '\n')
            resF.write(reduce(lambda x, y: x + ' ' + y, map(lambda x: x.split('_')[0], res)) + '\n')

    # test
    args.njobs = 1
    split = len(testSs) / args.njobs
    p = Pool(args.njobs)
    bestNBs = p.map(getBestNeighbor, generate_splits(args.njobs, split, testSs, testPerms))

    resSs = []
    for s in bestNBs:
        resSs.extend(s)

    with open(sourceF + '.test.src', 'w') as srcF, open(sourceF + '.test.res', 'w') as resF:
        for src, res in zip(testSs[:len(resSs)], resSs):
            srcF.write(reduce(lambda x, y: x + ' ' + y, map(lambda x: x.split('_')[0], src)) + '\n')
            resF.write(reduce(lambda x, y: x + ' ' + y, map(lambda x: x.split('_')[0], res)) + '\n')


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

        after_swapped = getSwap(srcS, swap)
        print swap, '\t', srcS, '\t', after_swapped
        nhbs.append(after_swapped)
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
    permS.extend(src[:i])
    permS.extend(src[j:k])
    permS.extend(src[i:j])
    permS.extend(src[k:])
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


def argparser():
    """parse command line arguments"""

    parser = argparse.ArgumentParser(prog='parse')

    parser.description = 'Reordering'
    parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    parser.add_argument('--source-language', '-s',
                        type=str,
                        help='source language file path')

    parser.add_argument('--source-language-without-tags', '-t',
                        type=str,
                        help='source language without tags file path')

    parser.add_argument('--alignments', '-a',
                        type=str,
                        help='alignment file path')

    parser.add_argument('--itg',
                        action='store_true', default=False,
                        help='use itg instead of random permutation')

    parser.add_argument('--njobs', '-j',
                        type=int, default=1,
                        help='number of workers')

    parser.add_argument('--use-cache', '-c',
                        default=False,
                        help='use caches for faster simulation')

    parser.add_argument('--grammar', '-g',
                        type=str,
                        help='CFG rules')
    return parser


if __name__ == '__main__':
    main(argparser().parse_args())