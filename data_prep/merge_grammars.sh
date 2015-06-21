#!/usr/bin/env bash

echo "========================"
echo "    Merge grammars    "
echo "========================"
rm -f ${DATA_FOLDER}/itg.de 2> /dev/null
echo "[S] ||| [X] ||| 1.0" >> ${DATA_FOLDER}/itg.en
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
    | python ./merge_count.py \
    >> ${DATA_FOLDER}/itg.en

rm -f ${DATA_FOLDER}/itg.de 2> /dev/null
echo "[S] ||| [X] ||| 1.0" >> ${DATA_FOLDER}/itg.de
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
            print a[1],"|||",a[3],"||| -==- ",get_number(a[4])
        }
        END{}
    ' \
    | sed -e 's/\[X,1\]/\[X\]/g' \
    | sed -e 's/\[X,2\]/\[X\]/g' \
    | sort -t '-' \
    | python ./merge_count.py \
    >> ${DATA_FOLDER}/itg.de

echo "          done"