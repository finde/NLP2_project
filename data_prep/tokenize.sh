#!/usr/bin/env bash

echo "================================================"
echo "    Tokenize and lowercase the training data    "
echo "================================================"
${CDEC_CORPUS_TOOLS}/tokenize-anything.sh < ${DATA_FOLDER}/train.en-de | ${CDEC_CORPUS_TOOLS}/lowercase.pl > ${DATA_FOLDER}/train.tok.en-de
echo "          done"
