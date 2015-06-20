#!/usr/bin/env bash

echo "========================"
echo "    Extract best ITG    "
echo "========================"
python ./itg-parse.py ${DATA_FOLDER}/training.en -g ${DATA_FOLDER}/itg.en -c ${DATA_FOLDER}/caches -o ${DATA_FOLDER}/itg.best.en -b

echo "          done"