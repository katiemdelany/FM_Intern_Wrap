#!/bin/bash

# Bash script for trimming fastq reads
FILES=./*_R1_.fastq

for f in $FILES
do
	echo "Processing $f ..."
	# Adjust file format if needed
	file=${f%%_R1_.fastq}
	name=${file##*/}
	forward=${name}_R1_.fastq
	reverse=${name}_R2_.fastq
	echo "Forward $forward"
	echo "Reverse $reverse"

	#trimming of all read phred 10 or less
	# Adjust path to Trimmomatic
	java -jar /home/FM/kdelany/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 12 -phred33 ${forward} ${reverse} \
       	~/TestData/TrimmedSeqs/${name}_PEtrim_R1.fastq \
	~/TestData/TrimmedSeqs/${name}_PEtrim_R1un.fastq \
	~/TestData/TrimmedSeqs/${name}_PEtrim_R2.fastq \
	~/TestData/TrimmedSeqs/${name}_PEtrim_R2un.fastq \
	ILLUMINACLIP:/home/FM/kdelany/Trimmomatic-0.36/adaptors/TruSeq3-PE.fa:2:30:10 \
LEADING:10 TRAILING:10 SLIDINGWINDOW:4:15 MINLEN:25

done




