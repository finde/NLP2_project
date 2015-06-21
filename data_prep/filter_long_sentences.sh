#!/usr/bin/env bash

echo "==============================================="
echo "    Filter training corpus sentence lengths    "
echo "==============================================="
${CDEC_CORPUS_TOOLS}/filter-length.pl -${MAX_LENGTH} ${DATA_FOLDER}/train.en-de | awk '!a[$0]++' | head -n ${MAX_LINES} > ${DATA_FOLDER}/training.en-de

echo "          done"
