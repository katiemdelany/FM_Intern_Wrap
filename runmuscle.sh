#!/bin/bash

#align fasta files from HybPiper/retrieve_seqs.py
for $f in *.FAA;
do muscle -in $f -out $f.aligned.fas
done 




