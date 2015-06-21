#!/usr/bin/env bash

<<<<<<< HEAD
echo "======================"
echo "    compound split    "
echo "======================"
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/tmp.en
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 2 ${DATA_FOLDER}/training.en-de | ${COMPOUND_SPLIT}/compound-split.pl --output 1best > ${DATA_FOLDER}/tmp.de

# get english/german sents only
${CDEC_CORPUS_TOOLS}/paste-files.pl ${DATA_FOLDER}/tmp.en ${DATA_FOLDER}/tmp.de > ${DATA_FOLDER}/training.en-de

rm -f ${DATA_FOLDER}/tmp.en
rm -f ${DATA_FOLDER}/tmp.de
=======
# make sure every line ends with a '.' (needed for stanford POS tagger)
echo "================================================"
echo "    Compound splitting and merge data corpus    "
echo "================================================"
cat ${DATA_FOLDER}/train.en | sed 's/[^?!.]$/&./' | sed 's/p.m.$/p.m../g' | sed 's/a.m.$/a.m../g' > ${DATA_FOLDER}/train.clean.en
cat ${DATA_FOLDER}/train.de | sed 's/[^?!.]$/&./' | sed 's/p.m.$/p.m../g' | sed 's/a.m.$/a.m../g' | ${COMPOUND_SPLIT}/compound-split.pl --output 1best > ${DATA_FOLDER}/train.clean.de

paste -d '|' ${DATA_FOLDER}/train.clean.en ${DATA_FOLDER}/train.clean.de > tmp
cat tmp | sed 's/\|/ ||| /g' > ${DATA_FOLDER}/train.en-de
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2

echo "          done"