#!/bin/bash

#align fasta files from HybPiper/retrieve_seqs.py
for $f in *.FAA;
do muscle -in $f -out $f.aligned.fas
done 

for f in *.FAA.aligned.fas; do
i = `cat $f | grep ">" | wc -l`
echo $f has $i taxa



