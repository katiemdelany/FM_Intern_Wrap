#!/bin/bash

######################
#Run exonerate hits with spades assemblies
######################


spades_path = $1
target_path = $2

for i in $spades_path; do 
	name=${i##*/}
	~/git/HybPiper/exonerate_hits.py ${target_path} $i/contigs.fasta --prefix $name
done

#make a genelist
grep ">" {target_path} | sed s/^.*\-// > genelist.txt

genelist=`cat genelist.txt`
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
