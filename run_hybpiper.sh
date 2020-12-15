#!/bin/bash

################################
#run HyPiper with blastx option#
#if target enrichment or de novo selected#
################################
target_file_path=$1
path_to_dataset=$2
path_to_namelist=$3


###
#mkdir -p hybpiper_blastx
#cd hybpiper_blastx
###

#running HybPiper main script on user input dataset
#must have name list with no space at end
while read name;
do ~/FM_Intern_Wrap/HybPiper/reads_first.py -b ${target_file_path} -r ${path_to_dataset}/$name*.fastq --prefix $name 
done < {path_to_namelist}

#Retrieve sequences
python3 ~/FM_Intern_Wrap/HybPiper/retrieve_sequences.py ${target_file_path} . aa

#Visualizing Results
#python3 ../HybPiper/get_seq_lengths.py target_file_path namelist.txt aa > test_seq_lengths.txt
