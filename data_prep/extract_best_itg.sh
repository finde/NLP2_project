#!/usr/bin/env bash

echo "========================"
echo "    Extract best ITG    "
echo "========================"
python ./itg-parse.py ${DATA_FOLDER}/training.en -g ${DATA_FOLDER}/itg.en -c ${DATA_FOLDER}/caches -o ${DATA_FOLDER}/itg.best.en -b

echo "========================="
echo "    Extract best ITG    "
echo "========================"


# get the forest
# get the best tree
#python ./pcfg-sampling/itg-parse.py ${DATA_FOLDER}/itg.en ${DATA_FOLDER}/training.en > ${DATA_FOLDER}/itg.forest.en

echo "          done"