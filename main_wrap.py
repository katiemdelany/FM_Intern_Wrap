## Wrapper for running Hybpiper Analysis

import os
import sys
import argparse
import shlex
import subprocess
import logging
from os import path

def check_arg(args=None):
    ''' 
    Argument input for Wrapper: target enrichment data, assembly data, de novo data, AND target file path
    
    '''
    parser = argparse.ArgumentParser(description='Run Hybpiper for nucleotide or amino acid sequencing data')
    parser.add_argument('-target_enrichment_data',
                        help='path to target enriched data',
                        )
    parser.add_argument('-whole_genome_data',
                        help='Input path of de novo whole genome sequence data.'
                        )
    parser.add_argument('-assemblies',
                        help='Input path of assembled data',
                        )    

    return parser.parse_args(args)
args = check_arg(sys.argv[1:])


def main():
    
    #Clones hybpiper into current directory
    clone_hybpiper = 'git clone https://github.com/mossmatters/HybPiper.git'
    os.system(clone_hybpiper)
    logging.info("Hybpiper cloned")
    
    #Change the target file here
    path_to_target_dna = '~/FM_Intern_Wrap/Pseude_target_CDS.fasta'
    logging.info('Path to target DNA: '+path_to_target_dna)
    path_to_target_aa = '~/FM_Intern_Wrap/Pseude_target_CDS_translation.fasta'
    logging.info('Path to target Amino Acid: '+path_to_target_aa)
    
    
    #if user input is target enrichment data
    #run through hybpiper
    path_to_sequences = args.target_enrichment_data
    if args.target_enrichment_data:
        logging.info('Path to TE data: '+path_to_sequences)
        logging.info('Created hybpiper directory in test sequence directory')
        os.chdir(path_to_sequences)
        
        #Get namelist.txt from dataset directory
        namelist_cmd = 'python3 ~/FM_Intern_Wrap/getNameList.py'
        os.system(namelist_cmd)
        
        #Make output directory
        out_dir = "hybpiper_TE"
        out_path = os.path.join(path_to_sequences,out_dir)
        os.mkdir(out_path)
        
        #hyb_results = '/hybpiper_TE'
        #mk_results = 'mkdir /hybpiper_TE'
        #os.system(mk_results)
        os.chdir(out_path)
        logging.info("Creating new directory for target enrichment hybpiper")
        #os.system('../')
        logging.info('Running amino acid target script')
        #run blastx version of hybpiper
        #runAAcmd = '~FM_Intern_Wrap/run_hybpiper.sh ' + path_to_target_aa
        #os.system(runAAcmd)
        #runMuscle = 'sh ../runmuscle.sh'
        
    #if argument is whole genome input data
    #run through hybpiper
    #spades assembly
    #exonerate normal
    path_to_denovo = args.whole_genome_data 
    if args.whole_genome_data:
        logging.info('Path to whole genome '+path_to_denovo)
        logging.info('Created hybpiper directory in whole genome sequence directory')
        os.chdir(path_to_denovo)
        namelist_cmd = 'python3 ../FM_Intern_Wrap/getNameList.py'
        os.system(namelist_cmd)
        logging.info("Creating new directory for whole genome data run")
        de_novo = path_to_denovo+ '/de_novo'
        os.mkdir(de_novo)
        os.chdir(de_novo)
        logging.info('Running amino acid target script')
        runAAcmd = './run_hybpiper.sh ' + path_to_target_aa
        os.system(runAAcmd)
        
     #if user input is assembly
    #check if spades, run exonerate
    #if non-spades assembly, run Claudio's version of exonerate
    path_to_assemblies = args.assembly_data
    if args.assembly_data:
        logging.info('Path to assemblies '+path_to_assemblies)
        logging.info('Created hybpiper directory in assembly sequence directory')
        os.chdir(path_to_assemblies)
        namelist_cmd = 'python3 ../FM_Intern_Wrap/getNameList.py'
        os.system(namelist_cmd)
        #if statement to determine spades or otherwise
        logging.info("Create new directory for exonerate hits")
        assembly_out_path = 'exonerate/'
        os.system('mkdir {}.format(assembly_out_path)')
        os.system('cd {}.format(assembly_out_path)')
        logging.info("Running exonerate on assembly input data")
        os.system("./assembly_exonerate.sh {} {}.format(path_to_assemblies, path_to_target_aa)")
        
                     
if __name__=='__main__':
    logger = logging.getLogger(__name__)
    logFormatter = '%(message)s'
    logging.basicConfig(filename='pipe_logger.log', format=logFormatter, level=logging.DEBUG)
    main()


