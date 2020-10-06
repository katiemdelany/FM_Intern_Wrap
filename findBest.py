#!/usr/bin/env python3
import os
import sys
from os import path
#path = "~/HybPiper/AA_run/supercontigs/"
#os.chdir(path) 

def countFasta(afasta):
    count = len([1 for line in open(afasta) if line.startswith(">")])
    return count


def getMax(adict):
    largest = [key for m in [max(adict.values())] 
            for key,val in adict.items() if val == m]
    return(largest)

def main():
    countdict = {}
    for filename in os.listdir():
        currcount = countFasta(filename)
        countdict[filename] = currcount
    result = getMax(countdict)
   #return top 5 longest fasta files (most records)
    for i in range(5):
        print(result[i])
   # sys.stdout.write("Hello")

if __name__ == '__main__':
    main()

