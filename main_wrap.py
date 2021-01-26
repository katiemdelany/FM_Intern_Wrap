'''
Main wrapper for running Hybpiper and subsequent analysis.
Input: Path to target enriched data, whole genome sequencing data, assembly data

'''
import re
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
    #To switch out file, change file name and upload new targets to github repo 
    path_to_target_dna = os.path.expanduser('~/FM_Intern_Wrap/Pseude_target_CDS.fasta')
    logging.info('Path to target DNA: '+path_to_target_dna)
    path_to_target_aa = os.path.expanduser('~/FM_Intern_Wrap/Pseude_target_CDS_translation.fasta')
    logging.info('Path to target Amino Acid: '+path_to_target_aa)
    
    
    #if user input is target enrichment data
    #set input dataset directory as variable
    path_to_sequences = args.target_enrichment_data
    if args.target_enrichment_data:
        logging.info('Path to TE data: '+path_to_sequences)
        logging.info('Created hybpiper directory in test sequence directory')
        os.chdir(path_to_sequences)
        
        #Get namelist.txt from dataset directory
        #This could potentially cause error later (see notes)
        namelist_cmd = 'python3 ~/FM_Intern_Wrap/getNameList.py'
        os.system(namelist_cmd)
        namelist = 'namelist.txt'
        path_to_namelist = os.path.join(path_to_sequences,namelist)
        
        #Make output directory
        out_dir = "hybpiper_TE"
        out_path = os.path.join(path_to_sequences,out_dir)
        os.mkdir(out_path)
        
        #change directory to output directory
        os.chdir(out_path)
        logging.info("Creating new directory for target enrichment hybpiper")
        logging.info('Running amino acid target script')
        #run blastx version of hybpiper
        AAscript = '~FM_Intern_Wrap/run_hybpiper.sh'
        runAAcmd = 'sh ~/FM_Intern_Wrap/run_hybpiper.sh ' + path_to_target_aa +' '+ path_to_sequences +' '+ path_to_namelist
        os.system(runAAcmd)
        logging.info("Running amino acid initial hybpiper scripts")
        os.chdir(out_path)
        #This will run mafft alignment
        logging.info("Running MSA with mafft")
        runMuscle = 'sh ~/FM_Intern_Wrap/runmuscle.sh'
        os.system(runMuscle)
        logging.info("MSA complete")
        #converts aligned fasta files to phylip (may not need this)
        logging.info("Converting aligned Fasta to Phylip")
        convert_cmd = 'sh ~/FM_Intern_Wrap/runConverter.sh'
        os.system(convert_cmd) 
        logging.info("Converted fasta files to phylip")
        #Add phylogenetic analysis scripts once tested
        
    #if argument is whole genome input data
    if args.whole_genome_data:
        path_to_sequences = args.whole_genome_data
        logging.info('Path to de novo data: '+path_to_sequences)
        logging.info('Created hybpiper directory in test sequence directory')
        os.chdir(path_to_sequences)
        
        #Get namelist.txt from dataset directory
        namelist_cmd = 'python3 ~/FM_Intern_Wrap/getNameList.py'
        os.system(namelist_cmd)
        namelist = 'namelist.txt'
        path_to_namelist = os.path.join(path_to_sequences,namelist)
        
        #Make output directory
        out_dir = "hybpiper_denovo"
        out_path = os.path.join(path_to_sequences,out_dir)
        os.mkdir(out_path)
        
        os.chdir(out_path)
        logging.info("Creating new directory for whole genome sequence input hybpiper")
        #os.system('../')
        logging.info('Running amino acid target script')
        #run blastx version of hybpiper
        AAscript = '~FM_Intern_Wrap/run_hybpiper.sh'
        runAAcmd = 'sh ~/FM_Intern_Wrap/run_hybpiper.sh ' + path_to_target_aa +' '+ path_to_sequences +' '+ path_to_namelist
        os.system(runAAcmd)
        logging.info("Running amino acid initial hybpiper scripts")
        os.chdir(out_path)
        #Run mafft
        logging.info("Running MSA with Mafft")
        runMuscle = 'sh ~/FM_Intern_Wrap/runmuscle.sh'
        os.system(runMuscle)
        logging.info("MSA complete")
        logging.info("Converting aligned Fasta to Phylip")
        #converts aligned fastas to phylip
        convert_cmd = 'sh ~/FM_Intern_Wrap/runConverter.sh'
        os.system(convert_cmd) 
        logging.info("Converted fasta files to phylip")
        #Add phylogenetic analysis scripts once tested
        
        
    #user input: assemblies
    if args.assemblies:
        path_to_assemblies = args.assemblies
        logging.info('Path to assemblies '+path_to_assemblies)
        logging.info('Created hybpiper directory in assembly sequence directory')
        os.chdir(path_to_assemblies)
        #namelist py program won't work here (COME BACK TO THIS - might not need)
        #namelist_cmd = 'python3 ../FM_Intern_Wrap/getNameList.py'
        #os.system(namelist_cmd)
        #if statement to determine spades or otherwise
        
        #Make output directory
        out_dir = "exonerate"
        out_path = os.path.join(path_to_assemblies,out_dir)
        os.mkdir(out_path)
        logging.info("Create new directory for exonerate hits")
        
        keyword = 'spades'
        for fname in os.listdir(path_to_assemblies):
            if keyword in fname:
                #if spades assembly, run exonerate_hits from HybPiper
                os.chdir(out_path)
                logging.info("Running HybPiper exonerate on assembly input data for "+fname)
                os.system('sh ~/FM_Intern_Wrap/spades_exonerate.sh {} {}'.format(path_to_assemblies,path_to_target_aa))
            elif keyword not in fname:
                os.chdir(out_path)
                logging.info("Running alternate exonerate script on assembly input data.")
                #Create alternate assembly script to run version of exonerate
                     
if __name__=='__main__':
    logger = logging.getLogger(__name__)
    logFormatter = '%(message)s'
    logging.basicConfig(filename='pipe_logger.log', format=logFormatter, level=logging.DEBUG)
    main()


