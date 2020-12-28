#!/bin/bash
FILES=*aligned.fas
CONVERSION=fastq2phylip
for f in $FILES
do
  echo "Processing $f file..."
  sbatch -c 1 bioconvert $CONVERSION $f  --force
done
