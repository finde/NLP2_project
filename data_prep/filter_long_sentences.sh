#!/usr/bin/env bash

echo "==============================================="
echo "    Filter training corpus sentence lengths    "
echo "==============================================="
${CDEC_CORPUS_TOOLS}/filter-length.pl -${MAX_LENGTH} ${DATA_FOLDER}/train.tok.en-de > ${DATA_FOLDER}/training.en-de

echo "          done"
