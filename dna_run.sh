#!/bin/bash

#need to make variable to represent target file

#Remove any previous runs
parallel rm -r {} :::: namelist.txt


#Run main HybPiper script with all available CPUs
while read i
do
../reads_first.py -r $i*.fastq -b RS_34_Alsophila.fasta --prefix $i --bwa 
done < namelist.txt

#Get the seq_lengths.txt file
python3 ../get_seq_lengths.py RS_34_Alsophila.fasta namelist.txt supercontig > test_seq_lengths.txt

#Test for paralogs
#while read i
#do
#python3 ../paralog_investigator.py $i
#done < namelist.txt

#Run intronerate
while read i
do
python3 ../exonerate_hits.py --prefix $i
done < namelist.txt

#Retrieve sequences -- need to change supercontig for fungi
python3 ../retrieve_sequences.py RS_34_Alsophila.fasta . supercontig 

#identify longest supercontig fastas (length of list depending on how many have the same number
#outputs a file with "best" supercontigs
python3 findBest.py 

##Next we want to align (MUSCLE?)
##run muscle (runmuscle.sh)
##pick phylogenetic tree program (iqtree, raxml)
