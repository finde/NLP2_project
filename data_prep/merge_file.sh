#!/usr/bin/env bash

# make sure every line ends with a '.' (needed for stanford POS tagger)
echo "========================="
echo "    merge data corpus    "
echo "========================="
cat ${DATA_FOLDER}/train.en | sed 's/[^?!.]$/&./' | sed 's/p.m.$/p.m../g' | sed 's/a.m.$/a.m../g' > ${DATA_FOLDER}/train.clean.en
cat ${DATA_FOLDER}/train.de | sed 's/[^?!.]$/&./' | sed 's/p.m.$/p.m../g' | sed 's/a.m.$/a.m../g' > ${DATA_FOLDER}/train.clean.de

${CDEC_CORPUS_TOOLS}/paste-files.pl ${DATA_FOLDER}/train.clean.en ${DATA_FOLDER}/train.clean.de > ${DATA_FOLDER}/train.en-de

rm -f ${DATA_FOLDER}/train.clean.en
rm -f ${DATA_FOLDER}/train.clean.de

echo "          done"