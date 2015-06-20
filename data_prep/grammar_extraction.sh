#!/usr/bin/env bash

echo "================================="
echo "    Compile the training data    "
echo "================================="
${EXTRACTOR}/sacompile -b ${DATA_FOLDER}/training.en-de -a ${DATA_FOLDER}/training.gdfa -c ${DATA_FOLDER}/extract.ini -o ${DATA_FOLDER}/training.sa
echo "          done"

echo "========================"
echo "    Extract grammars    "
echo "========================"
${EXTRACTOR}/extract -c ${DATA_FOLDER}/extract.ini -g ${DATA_FOLDER}/grammars -t 8 < ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en-de.sgm
echo "          done"