#!/usr/bin/env bash

echo "=============================================="
echo "    Run word bidirectional word alignments    "
echo "=============================================="
<<<<<<< HEAD
${FAST_ALIGN} -i ${DATA_FOLDER}/training.tok.en-de -d -v -o > ${DATA_FOLDER}/training.tok.en-de.fwd_align
${FAST_ALIGN} -i ${DATA_FOLDER}/training.tok.en-de -d -v -o -r > ${DATA_FOLDER}/training.tok.en-de.rev_align
=======
${FAST_ALIGN} -i ${DATA_FOLDER}/training.en-de -d -v -o > ${DATA_FOLDER}/training.en-de.fwd_align
${FAST_ALIGN} -i ${DATA_FOLDER}/training.en-de -d -v -o -r > ${DATA_FOLDER}/training.en-de.rev_align
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2

echo "          done"

echo "=================================="
echo "    Symmetrize word alignments    "
echo "=================================="
<<<<<<< HEAD
${SYM_ALIGN} -i ${DATA_FOLDER}/training.tok.en-de.fwd_align -j ${DATA_FOLDER}/training.tok.en-de.rev_align -c grow-diag-final-and > ${DATA_FOLDER}/training.en-de.gdfa
=======
${SYM_ALIGN} -i ${DATA_FOLDER}/training.en-de.fwd_align -j ${DATA_FOLDER}/training.en-de.rev_align -c grow-diag-final-and > ${DATA_FOLDER}/training.gdfa
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2

echo "          done"