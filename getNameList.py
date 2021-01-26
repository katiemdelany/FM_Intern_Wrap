import os
from os import listdir
from os.path import isfile, join
##Need to edit paths out --> will set to current directory (whichever directory input fastq files are in (should be output of trimmomatic)
mypath = os.getcwd()
os.chdir(mypath) 

#Makes list of file names in current directory, set directory to input data
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

namelist = []
#Goes through list and finds the prefix "Name" of the file, must be unique sample name
#Adds to a list of names
for i in onlyfiles:
    _index = i.find('_PE')
    ## (position -1 of the string --> string not found) 
    if _index != -1:
    currname = (i[:_index])
    if currname not in namelist:
        namelist.append(currname)

sorted_namelist = sorted(namelist)
#os.chdir(outpath) ##in linux this will be cd ../
with open("namelist.txt",'w+') as f:
    f.write('\n'.join(sorted_namelist))
f.close()

