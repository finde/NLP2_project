Data
===

You can use data made available by the WMT14 translation task
[http://www.statmt.org/wmt14/translation-task.html](http://www.statmt.org/wmt14/translation-task.html)

I would suggest Europarl for training. You probably want to clean up your data so that sentences are no longer than 40 words (that will make things run faster).


Word alignment
===

No need to use Giza++ (too old, too slow, too full of hacks). I would opt for fast_align (link below), which is very fast, easy to install and run:
[https://github.com/clab/fast_align](https://github.com/clab/fast_align)

You should run alignments in both directions and then symmetrise them.

There is a nice tutorial on data preparation and word alignment here: 
[http://www.cdec-decoder.org/guide/tutorial.html](http://www.cdec-decoder.org/guide/tutorial.html)

I heard some of you are struggling to get atools (a little part of cdec) to compile.
I’ve compiled it on both Ubuntu and iOS Darwin and you can download the binary directory from the links below:
[darwin](https://dl.dropboxusercontent.com/u/49398679/atools-darwin)
[ubuntu](https://dl.dropboxusercontent.com/u/49398679/atools-ubuntu)


If you are using German, you might want to consider preprocessing your data with a compound splitter:
[https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/compound-splitter.perl](https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/compound-splitter.perl)

Naive decoder
===

I suggest you write a simple decoder to use at the beginning, while getting your learning algorithm right. 
I give here an example of a randomised greedy decoder.

```
x = original sequence
for T iterations do:
   P = enumerate N random permutations of x
   x = best permutation in P according to the current model
```

This is a very simple decoder, which does not incorporate the ITG constraint, 
but will get you started (set T and N as a function of how much you are willing to wait). 
To get a random permutation of a sequence you can use any library you like. 
For instance, in python, random.suffle can do that for you.


ITG decoder
===

I have a python implementation of Earley’s algorithm that can parse a sentence and dump the ITG forest (chart) for you in text format.
[https://github.com/wilkeraziz/pcfg-sampling](https://github.com/wilkeraziz/pcfg-sampling)

From there, you would need to load this forest into a script that computes the recurrence formula presented in the paper 
(which you can accomplish by modifying the Inside algorithm slightly).