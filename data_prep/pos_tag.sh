#!/usr/bin/env bash

# download and unzip stanford basic POS tagger
cd stanford-postagger-2015-04-20/
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../${DATA_FOLDER}/training.en > ../${DATA_FOLDER}/training.tagged.en
