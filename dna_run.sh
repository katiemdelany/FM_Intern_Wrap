#!/bin/bash

#Remove any previous runs
parallel rm -r {} :::: namelist.txt


#Run main HybPiper script with all available CPUs
while read i
do
../reads_first.py -r $i*.fastq -b RS_34_Alsophila.fasta --prefix $i --bwa 
done < namelist.txt

#Get the seq_lengths.txt file
python3 ../get_seq_lengths.py RS_34_Alsophila.fasta namelist.txt dna > test_seq_lengths.txt

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
