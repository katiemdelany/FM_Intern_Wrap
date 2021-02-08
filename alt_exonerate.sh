#!/bin/bash

assembly_path = $1
target_path = $2

mkdir -p exonerate
cd exonerate

for i in ${assembly_path}; do 
	name=${i##*/}
	~/FM_Intern_Wrap/exonerate_alternate.py {target_path} $i/contigs.fasta --prefix $name
done

#make a genelist
grep ">" {target_path} | sed s/^.*\-// > genelist.txt

genelist=`cat genelist.txt`
for i in ${assembly_path}; do
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
