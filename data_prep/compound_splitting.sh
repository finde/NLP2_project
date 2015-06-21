#!/usr/bin/env bash

echo "======================"
echo "    compound split    "
echo "======================"
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/tmp.en
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 2 ${DATA_FOLDER}/training.en-de | ${COMPOUND_SPLIT}/compound-split.pl --output 1best > ${DATA_FOLDER}/tmp.de

# get english/german sents only
${CDEC_CORPUS_TOOLS}/paste-files.pl ${DATA_FOLDER}/tmp.en ${DATA_FOLDER}/tmp.de > ${DATA_FOLDER}/training.en-de

rm -f ${DATA_FOLDER}/tmp.en
rm -f ${DATA_FOLDER}/tmp.de

echo "          done"