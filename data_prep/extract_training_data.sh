#!/usr/bin/env bash

echo "============================="
echo "    Extract training data    "
echo "============================="
# get english/german sents only
<<<<<<< HEAD
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.tok.en-de > ${DATA_FOLDER}/training.tok.en
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 2 ${DATA_FOLDER}/training.tok.en-de | iconv -f utf-8 -t ascii --unicode-subst=? > ${DATA_FOLDER}/training.tok.de
=======
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 2 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.de
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2

echo "          done"