#!/usr/bin/env bash

echo "================================================"
echo "    Tokenize and lowercase the training data    "
echo "================================================"
<<<<<<< HEAD
${CDEC_CORPUS_TOOLS}/tokenize-anything.sh < ${DATA_FOLDER}/training.en-de | ${CDEC_CORPUS_TOOLS}/lowercase.pl > ${DATA_FOLDER}/training.tok.en-de
=======
${CDEC_CORPUS_TOOLS}/tokenize-anything.sh < ${DATA_FOLDER}/train.en-de | ${CDEC_CORPUS_TOOLS}/lowercase.pl > ${DATA_FOLDER}/train.tok.en-de
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2
echo "          done"
