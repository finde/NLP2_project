#!/usr/bin/env bash

echo "============================="
echo "    Extract training data    "
echo "============================="
# get english/german sents only
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 2 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.de

echo "          done"