#!/bin/bash

######################
#Run exonerate hits with spades assemblies
######################


spades_path=$1
target_path=$2

for i in ${spades_path}; do 
	name=${i##*/}
	~/git/HybPiper/exonerate_hits.py ${target_path} $i/contigs.fasta --prefix $name
done

#make a genelist
#from target sequence
grep ">" ${target_path} | sed s/^.*\-// > genelist.txt

#directory hierarchy
#sample/gene/sample/sequences/

genelist=`cat ~/FM_Intern_Wrap/genelist.txt`
for i in ${spades_path}; do
        name=${i##*/}
        echo Working on $name
                for gene in $genelist; do
                        mkdir -p ./$name/$gene/$name/sequences/FNA
                        cp ./$name/sequences/FNA/$gene.FNA ./$name/$gene/$name/sequences/FNA
                        mkdir -p ./$name/$gene/$name/sequences/FAA
                        cp ./$name/sequences/FAA/$gene.FAA ./$name/$gene/$name/sequences/FAA
                done
        echo Done with $name
done

#create namelist for spades exonerate and add names to list
touch exonerate_namelist.txt
for i in ${spades_path}; do
	name=${i##*/}
	echo $name >> exonerate_namelist.txt
done

python3 ~/FM_Intern_Wrap/Hybpiper/get_seq_lengths.py ${target_path} exonerate_namelist.txt aa > test_seq_lengths.txt

python3 ~/FM_Intern_Wrap/Hybpiper/retrieve_sequences.py ${target_path} . aa
