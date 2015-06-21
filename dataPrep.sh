#!/bin/bash

export DATA_FOLDER="data"
export FAST_ALIGN="./fast_align-master/fast_align" # or FAST_ALIGN="./cdec/fast_align"
export CDEC="./cdec"
export CDEC_CORPUS_TOOLS="${CDEC}/corpus"
export SYM_ALIGN="${CDEC}/build/utils/atools"
export EXTRACTOR="${CDEC}/build/extractor"
export COMPOUND_SPLIT="${CDEC}/build/compound-split"
export N=10
export MAX_LINES=1000
export MAX_LENGTH=10

if [ "$1" == "simple" ]
then
    export N=$2
    export DATA_FOLDER="data/simple_${N}"
    rm -rf ${DATA_FOLDER} 2> /dev/null
    mkdir ${DATA_FOLDER}
    mkdir ${DATA_FOLDER}/caches
    head -n ${N} data/train.en > ${DATA_FOLDER}/train.en
    head -n ${N} data/train.de > ${DATA_FOLDER}/train.de
fi

if [ "$1" == "short" ]
then
    export MAX_LENGTH=$2
    export DATA_FOLDER="data/short_${MAX_LENGTH}"
    rm -rf ${DATA_FOLDER} 2> /dev/null
    mkdir ${DATA_FOLDER}
    mkdir ${DATA_FOLDER}/caches
    cp data/train.en ${DATA_FOLDER}/train.en
    cp data/train.de ${DATA_FOLDER}/train.de
fi

./data_prep/merge_file.sh              # merge into en-de
./data_prep/filter_long_sentences.sh   # cut long sentence
./data_prep/compound_splitting.sh      # compound splitting
./data_prep/tokenize.sh                # tokenize
./data_prep/bidirectional_alignment.sh
./data_prep/extract_training_data.sh

# skip this
#./data_prep/grammar_extraction.sh
#./data_prep/merge_grammars.sh
#./data_prep/extract_best_itg.sh

./data_prep/pos_tag.sh

echo "=== creating short sample set ==="
head -n 30 ${DATA_FOLDER}/training.tagged.de > ${DATA_FOLDER}/training.tagged.de.10
head -n 30 ${DATA_FOLDER}/training.tagged.en > ${DATA_FOLDER}/training.tagged.en.10
head -n 30 ${DATA_FOLDER}/training.en-de.gdfa > ${DATA_FOLDER}/training.en-de.gdfa.10

