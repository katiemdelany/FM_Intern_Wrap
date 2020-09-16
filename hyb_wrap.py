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
    parser.add_argument('--dna',action='store_true', dest='dna', default=False, 
            help = 'Run BWA pipe if targets are nucleotide sequences')
    parser.add_argument('--AA', action='store_true', dest='AA', default=False, 
            help = 'Run BLASTX pipe if targets are amino acid sequences')
    parser.add_argument('--trim', action='store_true', default=False,
            help = 'Clean fastq data using trimmomatic')

    return parser.parse_args(args)
args = check_arg(sys.argv[1:])


def main():
## need to specify paths for each run eventually (mkdir --> chdir) 
    if args.trim:
        os.chdir("~/HybPiper/test_dataset/")
        logging.info('Trimming input reads')
        trim_cmd ='./trimmer.sh'
        os.system(trim_cmd)

    #if user input is dna
    if args.dna:
        logging.info("Creating new directory for dna target run")
        dna_path = '~/HybPiper/test_dataset/dna_run/'
        os.mkdir(dna_path)
        os.chdir(dna_path)
        logging.info('Running DNA target script')
        runDNAcmd = './run_DNA.sh'
        os.system(runDNAcmd) #adjust DNA shell as needed

    #if user input is AA 
    if args.AA:
        logging.info("Creating new directory for amino acid target run')
        aa_path = '~/HybPiper/test_dataset/aa_run/'
        os.mkdir(aa_path)
        os.chdir(aa_path)
        logging.info('Running amino acid target script')
        runAAcmd = './run_AA.sh'
        os.system(runAAcmd)

if __name__=='__main__':
    logger = logging.getLogger(__name__)
    logFormatter = '%(message)s'
    logging.basicConfig(filename='pipe_logger.log', format=logFormatter, level=logging.DEBUG)
    main()


