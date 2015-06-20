"""
@author wilkeraziz, finde
"""

import logging
import itertools
import argparse
import os
import sys
import hashlib

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
    if args.use_cache:
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

    for input_str in args.input:

        if args.use_cache:
            hashed_str = hashlib.md5(input_str.encode()).hexdigest()
            forest_file = args.use_cache + '/' + hashed_str + '.cp'
            map_file = args.use_cache + '/' + 'map.txt'

            if os.path.isfile(forest_file):
                # load cache
                forest_file = open(forest_file, 'r')
                forest = cPickle.load(forest_file)
                forest_file.close()
            else:
                forest = get_forest(input_str, wcfg)

                # store cache
                forest_file = open(forest_file, 'w')
                cPickle.dump(forest, forest_file)
                forest_file.close()

                # store map
                with open(map_file, "a") as map:
                    map.write("%s\t%s" % (hashed_str, input_str.replace("\n","")))
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
            print forest
        else:
            print '# FOREST'
            print forest
            print


def find_viterbi(forest):
    for rule in forest.split("\n"):
        if rule == 'NO PARSE FOUND':
            return 'NO PARSE FOUND'

        elif rule == '# FOREST':
            continue

        else:
            score = float(rule.split(' ')[-1].replace('(', '').replace(')', ''))
            rule_array = (' '.join(rule.split()[:-1])).split(' -> ')
            src = rule_array[0]
            tgt = rule_array[1]

            print rule, src, tgt

    pass


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
    parser.add_argument('--best', '-b',
                        default=False,
                        help='return best order')

    parser.add_argument('--use-cache', '-c',
                        default=False,
                        help='use caches for faster simulation')

    return parser


if __name__ == '__main__':
    main(argparser().parse_args())
