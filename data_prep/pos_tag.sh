#!/usr/bin/env bash

# download and unzip stanford basic POS tagger
python ./data_prep/pos_tag.py -i 'data/training.tok.de' -o 'data/training.tagged.clean.de' \
                                -pi 'data/training.tok.en' -po 'data/training.tok.clean.en' \
                                -gi 'data/training.en-de.gdfa' -go 'data/training.en-de.clean.gdfa'