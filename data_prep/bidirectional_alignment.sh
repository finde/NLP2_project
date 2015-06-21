#!/usr/bin/env bash

echo "=============================================="
echo "    Run word bidirectional word alignments    "
echo "=============================================="
${FAST_ALIGN} -i ${DATA_FOLDER}/training.tok.en-de -d -v -o > ${DATA_FOLDER}/training.tok.en-de.fwd_align
${FAST_ALIGN} -i ${DATA_FOLDER}/training.tok.en-de -d -v -o -r > ${DATA_FOLDER}/training.tok.en-de.rev_align

echo "          done"

echo "=================================="
echo "    Symmetrize word alignments    "
echo "=================================="
${SYM_ALIGN} -i ${DATA_FOLDER}/training.tok.en-de.fwd_align -j ${DATA_FOLDER}/training.tok.en-de.rev_align -c grow-diag-final-and > ${DATA_FOLDER}/training.en-de.gdfa

echo "          done"