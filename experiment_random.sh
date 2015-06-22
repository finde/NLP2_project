#!/usr/bin/env bash

LANG=$1
N=$2
J=$3

echo "experiment with language ${LANG} on ${N} lines"

rm -rf data/caches/${LANG}.${N} 2> /dev/null
mkdir data/caches/${LANG}.${N}

echo "=== creating short sample set ==="
head -n ${N} data/training.tagged.${LANG} > data/training.tagged.${LANG}.${N}
head -n ${N} data/training.en-de.gdfa > data/training.en-de.gdfa.${N}

python reordering.py \
    -t data/training.tok.${LANG}.${N} \
    -s data/training.tagged.${LANG}.${N} \
    -a data/training.en-de.gdfa.${N} \
    -g data/itg.${LANG} \
    -c data/caches/${LANG}.${N} \
    -j ${J} > data/report_${N}_${LANG}_random