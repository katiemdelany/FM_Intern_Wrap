#!/bin/bash

#align fasta files from HybPiper/retrieve_seqs.py
for f in *.FAA;
do muscle -in $f -out $f.aligned.fas
done 

#mkdir select_genes/
##Or with Mafft
for i in *.FAA;
do mafft --quiet $i > ${i%.FAA}.FAA.aligned.fas
done


for f in *.FAA.aligned.fas; do
i = `cat $f | grep ">" | wc -l`
echo $f has $i taxa
#if [$i -ge 9 taxa]; then
#cp $f select_genes/
#echo copied $f with $i sequences
#fi
done


