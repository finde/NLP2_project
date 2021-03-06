#!/usr/bin/env bash

echo "============================="
echo "    Extract training data    "
echo "============================="
# get english/german sents only
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.tok.en-de > ${DATA_FOLDER}/training.tok.en
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 2 ${DATA_FOLDER}/training.tok.en-de | iconv -f utf-8 -t ascii --unicode-subst=a > ${DATA_FOLDER}/training.tok.de

# after ascii replacement
${CDEC_CORPUS_TOOLS}/paste-files.pl ${DATA_FOLDER}/training.tok.en ${DATA_FOLDER}/training.tok.de > ${DATA_FOLDER}/training.tok.en-de

echo "          done"