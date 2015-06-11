#!/bin/bash

DATA_FOLDER="data"
CDEC_CORPUS_TOOLS="./cdec/corpus"
FAST_ALIGN="./fast_align-master/fast_align" # or FAST_ALIGN="./cdec/fast_align"
SYM_ALIGN="./cdec/build/utils/atools"
EXTRACTOR="./cdec/build/extractor"
COMPOUND_SPLIT="./cdec/build/compound-split"
ITG=${DATA_FOLDER}/itg.en.5

rm -f ${DATA_FOLDER}/itg.en.dirty 2> /dev/null
echo "[S] ||| [X] ||| 1.0" >> ${ITG}
tLen=$(ls -1 ${DATA_FOLDER}/grammars/grammar.* | wc -l)
for (( i=0; i<5; i++ ));
do
    f=${DATA_FOLDER}/grammars/grammar.${i}
    echo "Processing $f"
    # take action on each file. $f store current file name
    cat ${f} | awk '{split($0,a," [|][|][|] "); print a[1],"|||",a[2],"||| 0.1"}' | sed -e 's/\[X,1\]/\[X\]/g' | sed -e 's/\[X,2\]/\[X\]/g' | awk '!a[$0]++' >> ${DATA_FOLDER}/itg.en.dirty
done

cat ${DATA_FOLDER}/itg.en.dirty | awk '!a[$0]++' >> ${ITG} && rm -f ${DATA_FOLDER}/itg.en.dirty
python pcfg-sampling/itg-parse.py ${ITG} data/training.en.5 -v > data/itg.forest.en.5
