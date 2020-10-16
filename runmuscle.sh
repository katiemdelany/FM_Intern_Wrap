#!/bin/bash

#this is from tophits, which should be in supercontig folder
while read i 
do 
muscle -in $i -out new_$i
done < tophits.txt


