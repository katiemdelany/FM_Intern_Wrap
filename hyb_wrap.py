## Wrapper for running Hybpiper Analysis

import os
import sys
import argparse
import shlex
import subprocess
import logging
from os import path


#Argument input for Hybpiper. User input for dna, AA or both.
#KD- Check that it works for both (eventually)
def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Run Hybpiper for nucleotide or amino acid sequencing data')
    parser.add_argument('--target_enrichment_data', action = 'store_true',default =False,
            help = 'Input path of target enrichment data')
    parser.add_argument('--assembly_data', action='store_true', dest='assembly',default =False,
            help = 'Input path of assembly data')
    parser.add_argument('--whole_genome_data', actoion = 'store_true', default = True,
            help - 'Input path of whole genome sequence data.')
    
  #     parser.add_argument('--trim', action='store_true', default=False,
 #           help = 'Clean fastq data using trimmomatic')

    return parser.parse_args(args)
args = check_arg(sys.argv[1:])


def main():
    ## Get namelist.txt first
    ## Needs to be in directory of dataset (added dataset as required user input)

    #Get namelist.txt from dataset directory
    namelist_cmd = 'python3 ../FM_Intern_Wrap/getNameList.py'
    os.system(namelist_cmd)
    
    #Clones hybpiper one step out of current directory
    os.system('cd ../')
    clone_hybpiper = 'git clone https://github.com/mossmatters/HybPiper.git'
    os.system(clone_hybpiper)

    #if user input is target enrichment data
    if args.target_enrichment_data:
        logging.info("Creating new directory for amino acid target run")
        aa_path = '~/HybPiper/test_dataset/aa_run/'
        os.mkdir(aa_path)
        os.chdir(aa_path)
        logging.info('Running amino acid target script')
        runAAcmd = './run_AA.sh'
        os.system(runAAcmd)
        
    #if argument is whole genome input data
    #run through hybpiper
    #spades assembly
    #exonerate normal
    if arg.whole_genome_data:
        logging.info("Creating new directory for whole genome data run")
        aa_path = '~/HybPiper/test_dataset/aa_run/'
        os.mkdir(aa_path)
        os.chdir(aa_path)
        logging.info('Running amino acid target script')
        runAAcmd = './run_AA.sh'
        os.system(runAAcmd)
        
     #if user input is assembly
    if arg.assembly_data:
        #if statement to determine spades or otherwise
        logging.info("Create new directory for exonerate hits")
        assembly_out_path = 'exonerate/'
        os.system(mkdir {}.format(assembly_out_path))
        os.system(cd {}.format(assembly_out_path))
        logging.info("Running exonerate on assembly input data')
        
                     
if __name__=='__main__':
    logger = logging.getLogger(__name__)
    logFormatter = '%(message)s'
    logging.basicConfig(filename='pipe_logger.log', format=logFormatter, level=logging.DEBUG)
    main()


