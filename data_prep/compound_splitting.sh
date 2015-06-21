#!/usr/bin/env bash

# make sure every line ends with a '.' (needed for stanford POS tagger)
echo "================================================"
echo "    Compound splitting and merge data corpus    "
echo "================================================"
cat ${DATA_FOLDER}/train.en | sed 's/[^?!.]$/&./' | sed 's/p.m.$/p.m../g' | sed 's/a.m.$/a.m../g' > ${DATA_FOLDER}/train.clean.en
cat ${DATA_FOLDER}/train.de | sed 's/[^?!.]$/&./' | sed 's/p.m.$/p.m../g' | sed 's/a.m.$/a.m../g' | ${COMPOUND_SPLIT}/compound-split.pl --output 1best > ${DATA_FOLDER}/train.clean.de

paste -d '|' ${DATA_FOLDER}/train.clean.en ${DATA_FOLDER}/train.clean.de > tmp
cat tmp | sed 's/\|/ ||| /g' > ${DATA_FOLDER}/train.en-de

echo "          done"