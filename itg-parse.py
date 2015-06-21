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


def main(args):
    if args.output_file:
        out_f = open(args.output_file, "w")
        out_f.close()
        out_f = open(args.output_file + '.raw', "w")
        out_f.close()

    if args.use_cache:
        map_file = args.use_cache + '/' + 'map.txt'
        map = open(map_file, "w")
        map.close()

        wcfg_file = args.use_cache + '/wcfg.cp'
        if os.path.isfile(wcfg_file):
            wcfg = cPickle.load(open(wcfg_file, 'r'))
        else:
            wcfg = WCFG(read_grammar_rules(args.grammar))
            cPickle.dump(wcfg, open(wcfg_file, 'w'))
    else:
        wcfg = WCFG(read_grammar_rules(args.grammar))

    # print 'GRAMMAR'
    # print wcfg

    for str_no, input_str in enumerate(args.input):

        if args.line:
            if int(str_no) < int(args.line) - 1:
                continue
            elif int(str_no) > int(args.line):
                return True

        if args.use_cache:
            forest_file = "%s/grammars.%s.cp" % (args.use_cache, str(str_no))

            if os.path.isfile(forest_file):
                # load cache
<<<<<<< HEAD
                forest_f = open(forest_file, 'r')
                forest = cPickle.load(forest_f)
                forest_f.close()
=======
                forest_file = open(forest_file, 'r')
                forest = cPickle.load(forest_file)
                forest_file.close()
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2
            else:
                forest = get_forest(input_str, wcfg)

                # store cache
<<<<<<< HEAD
                forest_f = open(forest_file, 'w')
                cPickle.dump(forest, forest_f)
                forest_f.close()
=======
                forest_file = open(forest_file, 'w')
                cPickle.dump(forest, forest_file)
                forest_file.close()
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2

            # store map
            map = open(map_file, "a")
            map.write("%s\t%s\n" % (str(str_no), input_str.replace("\n", "")))
            map.close()

        else:
            forest = get_forest(input_str, wcfg)

        if args.show_permutations:
            print '# PERMUTATIONS'
            counts = count_derivations(forest, '[GOAL]')
            total = 0
            for p, n in sorted(counts['p'].iteritems(), key=lambda (k, v): k):
                print 'permutation=(%s) derivations=%d' % (' '.join(str(i) for i in p), n)
                total += n
            print 'permutations=%d derivations=%d' % (len(counts['p'].keys()), total)
            print

        if args.best:
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

            tree = "# TREE\n%s\n\n" % '),\n['.join(derivation.__str__().split('), ['))

            if args.output_file:
                out_f = open(args.output_file, "a")
                out_f.write("%s\n" % sentence)
                out_f.close()

                out_f = open(args.output_file + '.raw', "a")
                out_f.write(tree)
                out_f.close()

<<<<<<< HEAD
                forest_f = open(forest_file + '.perm', 'w')
                for (words, p_score) in projection_score:
                    forest_f.write("%s\n" % ' '.join(words))
                forest_f.close()

=======
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2
            print sentence + " ||| " + str(p_score)
            print tree
        else:
            print '# FOREST'
            print forest
            print


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

    parser.add_argument('input', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input corpus (one sentence per line)')

    parser.add_argument('--grammar', '-g',
                        type=argparse.FileType('r'),
                        help='CFG rules')

    parser.add_argument('--show-permutations',
                        action='store_true',
                        help='dumps all permutations (use with caution)')

    parser.add_argument('--verbose', '-v',
                        action='store_true', default=True,
                        help='increase the verbosity level')

    parser.add_argument('--output-file', '-o',
                        type=str,
                        help='save output to file')

    parser.add_argument('--best', '-b',
                        action='store_true', default=False,
                        help='return best order')

    parser.add_argument('--line', '-l',
                        help='return best order')

    parser.add_argument('--use-cache', '-c',
                        default=False,
                        help='use caches for faster simulation')

    return parser


if __name__ == '__main__':
    main(argparser().parse_args())
