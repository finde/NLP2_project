#!/bin/bash

export DATA_FOLDER="data"
export FAST_ALIGN="./fast_align-master/fast_align" # or FAST_ALIGN="./cdec/fast_align"
export CDEC="./cdec"
export CDEC_CORPUS_TOOLS="${CDEC}/corpus"
export SYM_ALIGN="${CDEC}/build/utils/atools"
export EXTRACTOR="${CDEC}/build/extractor"
export COMPOUND_SPLIT="${CDEC}/build/compound-split"
export N=10

if [ "$1" == "simple" ]
then
    export N=$2
    export DATA_FOLDER="data/simple_${N}"
    rm -rf ${DATA_FOLDER} 2> /dev/null
    mkdir ${DATA_FOLDER}
    head -n ${N} data/train.en > ${DATA_FOLDER}/train.en
    head -n ${N} data/train.de > ${DATA_FOLDER}/train.de
fi

#./data_prep/compound_splitting.sh
#./data_prep/tokenize.sh
#./data_prep/filter_long_sentences.sh
#./data_prep/bidirectional_alignment.sh
#./data_prep/grammar_extraction.sh
#./data_prep/merge_grammars.sh
#./data_prep/extract_training_data.sh
./data_prep/extract_best_itg.sh

# download and unzip stanford basic POS tagger
#cd stanford-postagger-2015-04-20/
#java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../${DATA_FOLDER}/training.en > ../${DATA_FOLDER}/training.tagged.en


