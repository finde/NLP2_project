#!/usr/bin/env bash

# download and unzip stanford basic POS tagger
cd stanford-postagger-2015-04-20/
<<<<<<< HEAD
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../${DATA_FOLDER}/training.tok.en > ../${DATA_FOLDER}/training.tagged.en
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/german-fast.tagger -textFile ../${DATA_FOLDER}/training.tok.de > ../${DATA_FOLDER}/training.tagged.de
=======
java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile ../${DATA_FOLDER}/training.en > ../${DATA_FOLDER}/training.tagged.en
>>>>>>> d5ebffaf923b92583295862de609e9ef533d70d2
