"""
@author wilkeraziz, finde
"""

import logging
import itertools
import argparse
import os
import sys
import hashlib
from collections import defaultdict, deque
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/pcfg-sampling')

from rule import Rule
from symbol import is_nonterminal, is_terminal
from wcfg import WCFG, read_grammar_rules, count_derivations
from wfsa import WDFSA, make_linear_fsa
from earley import Earley

import cPickle


def get_forest(input_str, wcfg):
    wfsa = make_linear_fsa(input_str)

    # print 'FSA'
    # print wfsa

    parser = Earley(wcfg, wfsa)
    forest = parser.do('[S]', '[GOAL]')
    if not forest:
        return 'NO PARSE FOUND'

    new_rules = []
    for rule in forest:
        if len(rule.rhs) > 1 and all(map(is_nonterminal, rule.rhs)):
            new_rules.append(Rule(rule.lhs, reversed(rule.rhs), rule.log_prob))
    [forest.add(rule) for rule in new_rules]

    return forest


def get_best_tree(forest, input_str):
    p_score = 0
    if forest == 'NO PARSE FOUND':
        sentence = input_str.replace("\n", "")
        derivation = 'NO PARSE FOUND'

    else:
        permutation_score = find_viterbi(forest, '[GOAL]')
        projection_score = sorted(permutation_score['p'].iteritems(), key=lambda (k, v): v, reverse=True)
        derivation_score = sorted(permutation_score['d'].iteritems(), key=lambda (k, v): v, reverse=True)
        (words, p_score) = projection_score[0]
        (derivation, d_score) = derivation_score[0]
        sentence = ' '.join(words)

    return sentence, derivation, p_score


def main(output_file=None, use_cache=None, grammar_file=None, input_str=None, best=False, key=0):
    if output_file:
        out_f = open(output_file, "w")
        out_f.close()
        out_f = open(output_file + '.raw', "w")
        out_f.close()

    grammar = open(grammar_file, 'r')

    if use_cache:
        # to improve the speed, only extract the grammar which contains text
        grammar_file = "%s/grammar.%s.cp" % (use_cache, str(key))

        if not os.path.isfile(grammar_file):
            # generate a shorter grammar
            grammar_f = open(grammar_file, 'w')
            for rule in grammar:

                if rule.startswith('[S] |||'):
                    grammar_f.write(rule)

                else:
                    rhs = rule.split(' ||| ')[1]
                    # remove token
                    rhs = ' '.join(filter(lambda x: not x.startswith('[X'), rhs.split(' ')))

                    if rhs.split() in input_str.split():
                        grammar_f.write(rule)
                    else:
                        if len(list(set(rhs.split()).difference(input_str.split()))) == 0:
                            grammar_f.write(rule)
                            # print rhs.split(), input_str.split(), list(set(rhs.split()).difference(input_str.split()))

            grammar_f.close()

        wcfg = WCFG(read_grammar_rules(open(grammar_file, 'r')))
    else:
        wcfg = WCFG(read_grammar_rules(grammar))

    grammar.close()

    # print 'GRAMMAR'
    # print wcfg

    if use_cache:
        forest_file = "%s/forest.%s.cp" % (use_cache, str(key))

        if os.path.isfile(forest_file):
            # load cache
            forest_f = open(forest_file, 'r')
            forest = cPickle.load(forest_f)
            forest_f.close()
        else:
            forest = get_forest(input_str, wcfg)

            # store cache
            forest_f = open(forest_file, 'w')
            cPickle.dump(forest, forest_f)
            forest_f.close()

    else:
        forest = get_forest(input_str, wcfg)

    if best:
        if use_cache:
            tree_file = "%s/tree.%s.cp" % (use_cache, str(key))

            if os.path.isfile(tree_file):
                # load cache
                tree_f = open(tree_file, 'r')
                tree = cPickle.load(tree_f)
                tree_f.close()
            else:
                sentence, tree, p_score = get_best_tree(forest, input_str)

                # store cache
                tree_f = open(tree_file, 'w')
                cPickle.dump(tree, tree_f)
                tree_f.close()

        else:
            sentence, tree, p_score = get_best_tree(forest, input_str)

        return tree

    else:
        # print '# FOREST'
        return forest


def find_viterbi(wcfg, root):
    def recursion(derivation, projection, Q, wcfg, scores):
        # print 'd:', '|'.join(str(r) for r in derivation)
        # print 'p:', projection
        # print 'Q:', Q
        if Q:
            sym = Q.popleft()
            # print ' pop:', sym
            if is_terminal(sym):
                recursion(derivation, [sym] + projection, Q, wcfg, scores)
            else:
                for rule in wcfg[sym]:
                    # print '  rule:', rule
                    QQ = deque(Q)
                    QQ.extendleft(rule.rhs)
                    recursion(derivation + [rule], projection, QQ, wcfg, scores)
        else:
            score = sum([r.log_prob for r in derivation])

            if scores['d'][tuple(derivation)] < score:
                scores['d'][tuple(derivation)] = score

            if scores['p'][tuple(projection)] < score:
                scores['p'][tuple(projection)] = score


    scores = {'d': defaultdict(float), 'p': defaultdict(float)}
    recursion([], [], deque([root]), wcfg, scores)
    return scores


def argparser():
    """parse command line arguments"""

    parser = argparse.ArgumentParser(prog='parse')

    parser.description = 'Earley parser'
    parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    parser.add_argument('--input_str', '-i',
                        type=str,
                        help='one sentence')

    parser.add_argument('--grammar', '-g',
                        type=str,
                        help='CFG rules')

    parser.add_argument('--output-file', '-o',
                        type=str,
                        help='save output to file')

    parser.add_argument('--key', '-k',
                        type=str,
                        help='key id of the input')

    parser.add_argument('--best', '-b',
                        action='store_true', default=False,
                        help='return best order')

    parser.add_argument('--use-cache', '-c',
                        default=False,
                        help='use caches for faster simulation')

    return parser


if __name__ == '__main__':
    args = argparser().parse_args()

    # todo: handle per sentences
    main(args)
