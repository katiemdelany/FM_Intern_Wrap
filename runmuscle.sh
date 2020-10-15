#!/bin/bash

while read i 
do 
muscle -in $i -out new_$i
done < tophits.txt


