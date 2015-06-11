#!/bin/bash

DATA_FOLDER="data"
CDEC_CORPUS_TOOLS="./cdec/corpus"
FAST_ALIGN="./fast_align-master/fast_align" # or FAST_ALIGN="./cdec/fast_align"
SYM_ALIGN="./cdec/build/utils/atools"
EXTRACTOR="./cdec/build/extractor"
COMPOUND_SPLIT="./cdec/build/compound-split"

# make sure every line ends with a '.' (needed for stanford POS tagger)
echo "================================================"
echo "    Compound splitting and merge data corpus    "
echo "================================================"
cat ${DATA_FOLDER}/train.en | sed 's/[^(?|!|.)]$/&./' > ${DATA_FOLDER}/train.clean.en
cat ${DATA_FOLDER}/train.de | sed 's/[^(?|!|.)]$/&./' | ${COMPOUND_SPLIT}/compound-split.pl --output 1best > ${DATA_FOLDER}/train.clean.de

paste -d '|' ${DATA_FOLDER}/train.en ${DATA_FOLDER}/train.clean.de > tmp
cat tmp | sed 's/\|/ ||| /g' > ${DATA_FOLDER}/train.en-de

echo "================================================"
echo "    Tokenize and lowercase the training data    "
echo "================================================"
${CDEC_CORPUS_TOOLS}/tokenize-anything.sh < ${DATA_FOLDER}/train.en-de | ${CDEC_CORPUS_TOOLS}/lowercase.pl > ${DATA_FOLDER}/train.tok.en-de
echo "done"

echo "==============================================="
echo "    Filter training corpus sentence lengths    "
echo "==============================================="
${CDEC_CORPUS_TOOLS}/filter-length.pl -40 ${DATA_FOLDER}/train.tok.en-de > ${DATA_FOLDER}/training.en-de
echo "done"

echo "=============================================="
echo "    Run word bidirectional word alignments    "
echo "=============================================="
${FAST_ALIGN} -i ${DATA_FOLDER}/training.en-de -d -v -o > ${DATA_FOLDER}/training.en-de.fwd_align
${FAST_ALIGN} -i ${DATA_FOLDER}/training.en-de -d -v -o -r > ${DATA_FOLDER}/training.en-de.rev_align
echo "done"

echo "=================================="
echo "    Symmetrize word alignments    "
echo "=================================="
${SYM_ALIGN} -i ${DATA_FOLDER}/training.en-de.fwd_align -j ${DATA_FOLDER}/training.en-de.rev_align -c grow-diag-final-and > ${DATA_FOLDER}/training.gdfa
echo "done"

echo "================================="
echo "    Compile the training data    "
echo "================================="
${EXTRACTOR}/sacompile -b ${DATA_FOLDER}/training.en-de -a ${DATA_FOLDER}/training.gdfa -c ${DATA_FOLDER}/extract.ini -o ${DATA_FOLDER}/training.sa
echo "done"

echo "========================"
echo "    Extract grammars    "
echo "========================"
${EXTRACTOR}/extract -c ${DATA_FOLDER}/extract.ini -g ${DATA_FOLDER}/grammars -t 8 < ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en-de.sgm
echo "done"

#get english sents only
cat ${DATA_FOLDER}/training.en-de | sed 's/|||.*//g' > ${DATA_FOLDER}/training.en

#download and unzip stanford basic POS tagger
cd stanford-postagger-2015-04-20/
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../${DATA_FOLDER}/training.en > ../${DATA_FOLDER}/training.tagged.en


