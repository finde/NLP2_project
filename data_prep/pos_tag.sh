#!/usr/bin/env bash

# download and unzip stanford basic POS tagger
python ./data_prep/pos_tag.py -i 'data/training.tok.de' -o 'data/training.tagged.de' -pi 'data/training.tok.en' -po 'data/training.tok2.en'