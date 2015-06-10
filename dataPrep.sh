#!/bin/bash

# make sure every line ends with a '.' (needed for stanford POS tagger)
cat data/train.en | sed 's/$/\. /g' | sed 's/\. \./\./g' > data/train.en
cat data/train.de | sed 's/$/\. /g' | sed 's/\. \./\./g' > data/train.de

paste -d '|' data/train.en data/train.de > tmp
cat tmp | sed 's/\|/ ||| /g' > data/train.en-de

./cdec-2014-10-12/corpus/tokenize-anything.sh < data/train.en-de | ./cdec-2014-10-12/corpus/lowercase.pl > data/train.tok.en-de
./cdec-2014-10-12/corpus/filter-length.pl -40 data/train.tok.en-de > data/training.en-de

./fast_align-master/fast_align -i data/training.en-de -d -v -o > data/training.en-de.fwd_align
./fast_align-master/fast_align -i data/training.en-de -d -v -o -r > data/training.en-de.rev_align

./cdec-2014-10-12/utils/atools -i data/training.en-de.fwd_align -j data/training.en-de.rev_align -c grow-diag-final-and > data/training.gdfa

#get english sents only 
cat data/training.en-de | sed 's/|||.*//g' > data/training.en

#dowload and unzip stanford basic POS tagger
cd stanford-postagger-2015-04-20/
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../data/training.en > ../data/training.tagged.en

# get ITG with cdec and forests with Wilker's tool
