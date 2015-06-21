#!/usr/bin/env bash

echo "================================="
echo "    Compile the training data    "
echo "================================="
<<<<<<< HEAD
${EXTRACTOR}/sacompile -b ${DATA_FOLDER}/training.tok.en-de -a ${DATA_FOLDER}/training.en-de.gdfa -c ${DATA_FOLDER}/extract.ini -o ${DATA_FOLDER}/training.sa
=======
${EXTRACTOR}/sacompile -b ${DATA_FOLDER}/training.en-de -a ${DATA_FOLDER}/training.gdfa -c ${DATA_FOLDER}/extract.ini -o ${DATA_FOLDER}/training.sa
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2
echo "          done"

echo "========================"
echo "    Extract grammars    "
echo "========================"
<<<<<<< HEAD
${EXTRACTOR}/extract -c ${DATA_FOLDER}/extract.ini -g ${DATA_FOLDER}/grammars -t 8 < ${DATA_FOLDER}/training.tok.en-de > ${DATA_FOLDER}/training.en-de.sgm
=======
${EXTRACTOR}/extract -c ${DATA_FOLDER}/extract.ini -g ${DATA_FOLDER}/grammars -t 8 < ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en-de.sgm
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2
echo "          done"