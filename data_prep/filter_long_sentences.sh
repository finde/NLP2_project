#!/usr/bin/env bash

echo "==============================================="
echo "    Filter training corpus sentence lengths    "
echo "==============================================="
${CDEC_CORPUS_TOOLS}/filter-length.pl -40 ${DATA_FOLDER}/train.tok.en-de > ${DATA_FOLDER}/training.en-de

echo "          done"
