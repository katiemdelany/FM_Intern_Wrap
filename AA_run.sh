#!/bin/bash

#Remove any previous runs
parallel rm -r {} :::: namelist.txt


#Run main HybPiper script with all available CPUs
while read i
do
python3 ../reads_first.py -r $i*.fastq -b RS_34_Alsophila_AA.fasta --prefix $i
done < namelist.txt

#Get the seq_lengths.txt file
python3 ../get_seq_lengths.py RS_34_Alsophila_AA.fasta namelist.txt aa > test_seq_lengths.txt

#Test for paralogs
while read i
do
python3 ../paralog_investigator.py $i
done < namelist.txt

#Run intronerate
while read i
do
python3 ../intronerate.py --prefix $i
done < namelist.txt
