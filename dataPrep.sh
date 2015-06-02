#!/bin/bash

paste -d '|' data/train.en data/train.de > tmp
cat tmp | sed 's/\|/ ||| /g' > data/train.en-de
./cdec-2014-10-12/corpus/tokenize-anything.sh < data/train.en-de | ./cdec-2014-10-12/corpus/lowercase.pl > data/train.tok.en-de
./cdec-2014-10-12/corpus/filter-length.pl -40 data/train.tok.en-de > data/training.en-de

./fast_align-master/fast_align -i data/training.en-de -d -v -o > data/training.en-de.fwd_align
./fast_align-master/fast_align -i data/training.en-de -d -v -o -r > data/training.en-de.rev_align

./cdec-2014-10-12/utils/atools -i data/training.en-de.fwd_align -j data/training.en-de.rev_align -c grow-diag-final-and > data/training.gdfa
