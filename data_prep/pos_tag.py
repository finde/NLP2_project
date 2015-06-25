import nltk
import nltk.tag
import nltk.tag.stanford
import argparse
from itertools import izip
import os

de_tagger = nltk.tag.stanford.POSTagger('../stanford-postagger-2015-04-20/models/german-fast.tagger',
                                        '../stanford-postagger-2015-04-20/stanford-postagger.jar')


def main(args):
    seq = 0
    with open(args.input, 'r') as i, open(args.output, 'w') as o, \
            open(args.parallel_input, 'r') as pi, open(args.parallel_output, 'w') as po, \
            open(args.gdfa_input, 'r') as gi, open(args.gdfa_output, 'w') as go:
        for _i, (f_s, p_s, g_s) in enumerate(izip(i, pi, gi)):
            tagged_f = de_tagger.tag(nltk.word_tokenize(f_s))

            if len(tagged_f[0]) == len(f_s.split(' ')) and len(f_s.split(' ')) > 1 and len(p_s.split(' ')) > 1:
                if seq != _i:
                    print seq, '<<', _i

                    os.rename('../data/caches/de/forest.' + str(_i) + '.cp',
                              '../data/caches/de/forest.' + str(seq) + '.cp')
                    os.rename('../data/caches/de/grammar.' + str(_i) + '.cp',
                              '../data/caches/de/grammar.' + str(seq) + '.cp')
                    os.rename('../data/caches/de/tree.' + str(_i) + '.cp',
                              '../data/caches/de/tree.' + str(seq) + '.cp')

                seq += 1
                print _i

                o.write(reduce(lambda x, y: x + ' ' + y, map(lambda x: '_'.join(x), tagged_f[0])) + '\n')
                po.write(p_s)
                go.write(g_s)


def argparser():
    """parse command line arguments"""

    parser = argparse.ArgumentParser(prog='parse')

    parser.description = 'POS Tagger'
    parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    parser.add_argument('--input', '-i',
                        type=str,
                        help='German sentences file')

    parser.add_argument('--output', '-o',
                        type=str,
                        help='Tagged german sentences file')

    parser.add_argument('--parallel-input', '-pi',
                        type=str)

    parser.add_argument('--parallel-output', '-po',
                        type=str)

    parser.add_argument('--gdfa-input', '-gi',
                        type=str)

    parser.add_argument('--gdfa-output', '-go',
                        type=str)

    return parser


if __name__ == '__main__':
    args = argparser().parse_args()

    # args.input = '../data/training.tok.de'
    # args.output = '../data/training.tagged.clean.de'
    # args.parallel_input = '../data/training.tok.en'
    # args.parallel_output = '../data/training.tok.clean.en'
    # args.gdfa_input = '../data/training.en-de.gdfa'
    # args.gdfa_output = '../data/training.en-de.clean.gdfa'

    main(args)
