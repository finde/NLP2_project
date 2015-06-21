#!/usr/bin/env bash

echo "================================================"
echo "    Tokenize and lowercase the training data    "
echo "================================================"
${CDEC_CORPUS_TOOLS}/tokenize-anything.sh < ${DATA_FOLDER}/training.en-de | ${CDEC_CORPUS_TOOLS}/lowercase.pl > ${DATA_FOLDER}/training.tok.en-de
echo "          done"
