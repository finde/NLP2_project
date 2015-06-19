#!/bin/bash

DATA_FOLDER="data"
FAST_ALIGN="./fast_align-master/fast_align" # or FAST_ALIGN="./cdec/fast_align"
CDEC="./cdec"
CDEC_CORPUS_TOOLS="${CDEC}/corpus"
SYM_ALIGN="${CDEC}/build/utils/atools"
EXTRACTOR="${CDEC}/build/extractor"
COMPOUND_SPLIT="${CDEC}/build/compound-split"
N=10

if [ "$1" == "simple" ]
then
    N=$2
    DATA_FOLDER="data/simple_${N}"
    rm -rf ${DATA_FOLDER} 2> /dev/null
    mkdir ${DATA_FOLDER}
    head -n ${N} data/train.en > ${DATA_FOLDER}/train.en
    head -n ${N} data/train.de > ${DATA_FOLDER}/train.de
fi

# make sure every line ends with a '.' (needed for stanford POS tagger)
echo "================================================"
echo "    Compound splitting and merge data corpus    "
echo "================================================"
cat ${DATA_FOLDER}/train.en | sed 's/[^(?|!|.)]$/&./' > ${DATA_FOLDER}/train.clean.en
cat ${DATA_FOLDER}/train.de | sed 's/[^(?|!|.)]$/&./' | ${COMPOUND_SPLIT}/compound-split.pl --output 1best > ${DATA_FOLDER}/train.clean.de

paste -d '|' ${DATA_FOLDER}/train.en ${DATA_FOLDER}/train.clean.de > tmp
cat tmp | sed 's/\|/ ||| /g' > ${DATA_FOLDER}/train.en-de

echo "================================================"
echo "    Tokenize and lowercase the training data    "
echo "================================================"
${CDEC_CORPUS_TOOLS}/tokenize-anything.sh < ${DATA_FOLDER}/train.en-de | ${CDEC_CORPUS_TOOLS}/lowercase.pl > ${DATA_FOLDER}/train.tok.en-de
echo "done"

echo "==============================================="
echo "    Filter training corpus sentence lengths    "
echo "==============================================="
${CDEC_CORPUS_TOOLS}/filter-length.pl -40 ${DATA_FOLDER}/train.tok.en-de > ${DATA_FOLDER}/training.en-de
echo "done"

echo "=============================================="
echo "    Run word bidirectional word alignments    "
echo "=============================================="
${FAST_ALIGN} -i ${DATA_FOLDER}/training.en-de -d -v -o > ${DATA_FOLDER}/training.en-de.fwd_align
${FAST_ALIGN} -i ${DATA_FOLDER}/training.en-de -d -v -o -r > ${DATA_FOLDER}/training.en-de.rev_align
echo "done"

echo "=================================="
echo "    Symmetrize word alignments    "
echo "=================================="
${SYM_ALIGN} -i ${DATA_FOLDER}/training.en-de.fwd_align -j ${DATA_FOLDER}/training.en-de.rev_align -c grow-diag-final-and > ${DATA_FOLDER}/training.gdfa
echo "done"

echo "================================="
echo "    Compile the training data    "
echo "================================="
${EXTRACTOR}/sacompile -b ${DATA_FOLDER}/training.en-de -a ${DATA_FOLDER}/training.gdfa -c ${DATA_FOLDER}/extract.ini -o ${DATA_FOLDER}/training.sa
echo "done"

echo "========================"
echo "    Extract grammars    "
echo "========================"
${EXTRACTOR}/extract -c ${DATA_FOLDER}/extract.ini -g ${DATA_FOLDER}/grammars -t 8 < ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en-de.sgm

rm -f ${DATA_FOLDER}/itg.en 2> /dev/null
echo "[S] ||| [X] ||| 1.0" >> ${DATA_FOLDER}/itg.en
#echo "[X] ||| [X] ||| 0.5" >> ${DATA_FOLDER}/itg.en
f=${DATA_FOLDER}/grammars/grammar.*

cat ${f} \
    | awk '
        function get_number(x) {
            split(x,xright," CountEF=");
            split(xright[2], x," MaxLexFgivenE");
            return x[1]
        }
        BEGIN {}
        {
            split($0,a," [|][|][|] ");
            print a[1],"|||",a[2],"||| -==- ",get_number(a[4])
        }
        END{}
    ' \
    | sed -e 's/\[X,1\]/\[X\]/g' \
    | sed -e 's/\[X,2\]/\[X\]/g' \
    | sort -t '-' \
    | python merge_count.py \
    >> ${DATA_FOLDER}/itg.en

# get english sents only
${CDEC_CORPUS_TOOLS}/cut-corpus.pl 1 ${DATA_FOLDER}/training.en-de > ${DATA_FOLDER}/training.en

# get ITG FOREST
echo "======================"
echo "    Get ITG forest    "
echo "======================"
python ./pcfg-sampling/itg-parse.py ${DATA_FOLDER}/itg.en ${DATA_FOLDER}/training.en > ${DATA_FOLDER}/itg.forest.en

# download and unzip stanford basic POS tagger
cd stanford-postagger-2015-04-20/
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../${DATA_FOLDER}/training.en > ../${DATA_FOLDER}/training.tagged.en


