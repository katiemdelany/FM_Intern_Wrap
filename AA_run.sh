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

#Retrieve sequences -- need to change supercontig for fungi
python3 ../retrieve_sequences.py RS_34_Alsophila_AA.fasta . supercontig 

#identify longest supercontig fastas (length of list depending on how many have the same number
#outputs a file with "best" supercontigs
python3 findBest.py 

##assembly and phylogenetic analysis
##run muscle (runmuscle.sh)
##pick phylogenetic tree program (iqtree, raxml)
