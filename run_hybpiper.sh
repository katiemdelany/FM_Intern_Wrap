#!/bin/bash

################################
#run HyPiper with blastx option#
#if target enrichment or de novo selected#
#Note: This is run in out_path created in main#
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
done < ${path_to_namelist}


#Get the seq_lengths.txt file
python3 ~/FM_Intern_Wrap/HybPiper/get_seq_lengths.py ${target_file_path} ${path_to_namelist} aa > test_seq_lengths.txt

#Generate heatmap (must be run after get_seq_lengths.py)
Rscript ~/FM_Intern_Wrap/gene_recovery_heatmap.R test_seq_lengths.txt


#Retrieve sequences
python3 ~/FM_Intern_Wrap/HybPiper/retrieve_sequences.py ${target_file_path} . aa

