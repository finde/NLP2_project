#!/usr/bin/env bash

echo "==============================================="
echo "    Filter training corpus sentence lengths    "
echo "==============================================="
<<<<<<< HEAD
${CDEC_CORPUS_TOOLS}/filter-length.pl -${MAX_LENGTH} ${DATA_FOLDER}/train.en-de | awk '!a[$0]++' | head -n ${MAX_LINES} > ${DATA_FOLDER}/training.en-de
=======
${CDEC_CORPUS_TOOLS}/filter-length.pl -${MAX_LENGTH} ${DATA_FOLDER}/train.tok.en-de > ${DATA_FOLDER}/training.en-de
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2

echo "          done"
