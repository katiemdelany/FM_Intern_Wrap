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
   #return longest fasta files (most records)
    top = [i for i in result]
   # sys.stdout.write("Hello")
    with open("tophits.txt","w") as outfile:
        outfile.write("\n".join(str(record) for record in top))
    return(top)

if __name__ == '__main__':
    main()

