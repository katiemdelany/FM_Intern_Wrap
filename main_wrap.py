#!/usr/bin/python3
'''
Main wrapper for running Hybpiper and subsequent analysis.
Input: Path to target enriched data, whole genome sequencing data, assembly data

'''
import shutil
import re
import os
import sys
import argparse
import shlex
import multiprocessing
import itertools
import subprocess
import logging
from os import path
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def run_exonerate_hits(file_, ref_seq_file):
	logging.info("Extracting genes from: " +file_)
	fline=open(file_).readline()
	regex_spades_header =re.search("^>NODE_[0-9]+_length_[0-9]+_cov_[0-9]+",fline)
	#if spades assembly, run exonerate_hits from HybPiper
	if regex_spades_header != None:
		os.system("python3 exonerate_hits.py {} --prefix {} {} ".format(ref_seq_file, file_.rstrip("\.fna"), file_))
	# else use the script version not using coverage information
	else:
		os.system("python3 exonerate_alt.py {} --prefix {} {} ".format(ref_seq_file, file_.rstrip("\.fna"), file_))
	return(file_)

def get_alignment(path_to_data):
	genes_list = []
	for root, dirs, files in os.walk(path_to_data, topdown=True):
		#append any gene to a list, make it a set to eliminate redundancy and then back to a list		
		for f in files:
			if f.endswith(".FAA"):
				genes_list.append(f.rstrip(".FAA"))
	genes_list = set(genes_list)
	genes_list = list(genes_list)
	print("List of genes found: ", genes_list)
	os.chdir(path_to_data)
	for g in genes_list:
		logging.info("Building nucleotide alignment for gene {}".format(g))
		with open("Alignment_" + g + "_nucleotide.FAS",'a+') as alignment:
			for root, dirs, files in os.walk(path_to_data, topdown=True):
				for f in files:
					if f == g + ".FNA":
						os.chdir(root)
						print("root" + root + f)
						with open(f, 'r') as gene:
							f_content = gene.read()
							os.chdir(path_to_data)
							print("pathtodata", path_to_data)
							alignment.write(f_content)	
	for g in genes_list:
		logging.info("Building aminoacid alignment for gene {}".format(g))
		with open("Alignment_" + g + "_protein.FAS",'a+') as alignment:
			for root, dirs, files in os.walk(path_to_data, topdown=True):
				for f in files:
					if f == g + ".FAA":
						os.chdir(root)
						print("root" + root + f)
						with open(f, 'r') as gene:
							f_content = gene.read()
							os.chdir(path_to_data)
							print("pathtodata", path_to_data)
							alignment.write(f_content)
	return()

def merge_alignments(path_to_assemblies, path_to_target_enrichment):
	output_path = path_to_target_enrichment + '../'
	if not os.path.exists('merged_alignments'):
		os.makedirs(output_path + 'alignments')
		os.makedirs(output_path + 'alignments_merged')
	output_path = output_path + 'alignments/'
	output_path_merged = output_path.rstrip("/") + "_merged/"
	#print(output_path)
	for filename in (os.listdir(path_to_assemblies)):
		if filename.endswith(".FAS"):
			os.rename(path_to_assemblies + filename , path_to_assemblies + filename.rstrip("FAS") + "assembly.FA")
	for filename in (os.listdir(path_to_target_enrichment)):
		if filename.endswith(".FAS"):
			os.rename(path_to_target_enrichment + filename , path_to_target_enrichment + filename.rstrip("FAS") + "targenrich.FA")
	for filename in (os.listdir(path_to_assemblies)):
		if filename.endswith("assembly.FA"):
			shutil.move(path_to_assemblies + filename , output_path + filename) 
	for filename in (os.listdir(path_to_target_enrichment)):
		if filename.endswith("targenrich.FA"):
			shutil.move(path_to_target_enrichment + filename , output_path + filename)
	file_list_total = os.listdir(output_path)
	for index, item in  enumerate(file_list_total):
		file_list_total[index] = (file_list_total[index]).replace(".targenrich.FA", "")
		file_list_total[index] = (file_list_total[index]).replace(".assembly.FA", "")	
	#print(file_list_total)
	file_list_total = list(set(file_list_total))
	print(file_list_total)
	for item in file_list_total:
		with open(output_path_merged + item + "_merged.fasta", 'a+') as f:
			for filename in os.listdir(output_path):
				regex = re.search('(^Alignement_[0-9]+at4890_\w+)\.\w+\.FA$', filename )
				if item == regex.group(1):
					my_file = open(output_path + filename, 'r')
					my_file_content = my_file.read()
					f.write(my_file_content)
	return()

def check_arg(args=None):
	''' 
	Argument input for Wrapper: target enrichment fastq files, assemblies fasta, WGS fasta AND target genes fasta 
	
	'''
	parser = argparse.ArgumentParser(description='Run the whole pipeline to raw data to phylogenetic tree')
	parser.add_argument('-b', '--target_markers', default= '',
						help=' Path to fasta files containg all the sequences used to design the bait set, MUST BE A PROTEIN FASTA'
						)
	parser.add_argument('-ch', '--hybpiper_cpu', default= '4',
						help='CPU number used by Hybpiper' 
						)				
	parser.add_argument('-ce', '--parallel_exonerate', default= 4,
						help='CPU number used to run exonerate in parallel on multiple assemblies' 
						)
parser.add_argument('-cm', '--parallel_mafft', default= '4',
						help=' Number of mafft alignments perfomed in parallel using each one thread'
						)										
	parser.add_argument('-t', '--target_enrichment_data', default= '',
						help='path to target enriched data',
						)
	parser.add_argument('-w', '--whole_genome_data', default= '',
						help='Input path of de novo whole genome sequence data.'
						)
	parser.add_argument('-a', '--assemblies', default= '',
						help='Input path of assembled data',
						)	
	parser.add_argument('-f', '--first_use', action= 'store_true', 
						help='Clones Hybpiper to your script directory from Github, use this argument only if is the first time you run the pipeline',
						)			
	return parser.parse_args(args)
args = check_arg(sys.argv[1:])


def main():
	#print(args)
	main_script_dir = os.path.realpath(__file__)
	main_script_dir = main_script_dir.rstrip("main_wrap.py")
	#print(main_script_dir)
	#print(args.target_enrichment_data)
	#print(args.assemblies)
	#Clones hybpiper into current directory
	if args.first_use == True:
		clone_hybpiper = 'git clone https://github.com/mossmatters/HybPiper.git'
		os.system(clone_hybpiper)
		logging.info("Hybpiper cloned")
		
	
	#if user input is target enrichment data
	#set input dataset directory as variable
	path_to_sequences = args.target_enrichment_data
	if args.target_enrichment_data:
		logging.info("***************************************************************************************")
		logging.info("* PERFORMING TARGET ENRICHMENT DATA ANALYSIS WITH Hybpiper  *")
		logging.info("***************************************************************************************")
		logging.info('Path to TE data: '+path_to_sequences)
		trimming_cmd = "python3 {}/trimmer.py -f {}".format(main_script_dir, args.target_enrichment_data)
		os.system(trimming_cmd)
		#Get namelist.txt from dataset directory
		namelist_cmd = 'python3 {}/getNameList.py -f {}'.format(main_script_dir, args.target_enrichment_data)
		os.system(namelist_cmd)
		namelist = 'namelist.txt'
		path_to_namelist = os.path.join(path_to_sequences,namelist)
		
		logging.info("Gunzipping paired reads trimmed fastq archives")
		gunzip_fastq =' parallel gunzip ::: {}*_paired.fastq.gz'.format(path_to_sequences) 
		os.system(gunzip_fastq)
		logging.info("Running Hybpiper on target enrichment data provided")
		os.chdir(path_to_sequences)
		with open(path_to_namelist, 'r') as f:
			for line in f:
				logging.info("Processing sample:" + line)
				sample_path = path_to_sequences + '/' + line.rstrip('\n') + '_R*.trimmed_paired.fastq'
				run_Hybpiper =  '{}HybPiper/reads_first.py -b {} -r {}  --prefix {} --cpu {} '.format(main_script_dir, args.target_markers, sample_path, line, args.hybpiper_cpu)
				os.system(run_Hybpiper)
		os.chdir(main_script_dir)			
	"""#if argument is whole genome input data
	if args.whole_genome_data:
		path_to_sequences = args.whole_genome_data
		logging.info('Path to de novo data: '+path_to_sequences)
		logging.info('Created hybpiper directory in test sequence directory')
		os.chdir(path_to_sequences)
		trimming_cmd = "python3 {}/trimmer.py -f {}".format(main_script_dir, args.whole_genome_data)
		os.system(trimming_cmd)
		
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
		#Add phylogenetic analysis scripts once tested"""
				
	#user input: assemblies
	if args.assemblies:
		path_to_assemblies = args.assemblies
		logging.info("*****************************************************************************")
		logging.info("* PERFORMING ASSEMBLIES DATA ANALYSIS WITH Exonerate  *")
		logging.info("*****************************************************************************")
		logging.info('Path to assemblies '+path_to_assemblies)
		#logging.info('Created hybpiper directory in assembly sequence directory')
		#os.chdir(path_to_assemblies)
		
		for root, dirs, files in os.walk(path_to_assemblies, topdown=True):
			for name in files:
				if name.startswith("GCA_") and name.endswith(".fna.gz"):
					os.system("gunzip " + name)	
		os.system("rm -r *.fna.gz")			
		pezizo_list = []	
		for root, dirs, files in os.walk(path_to_assemblies, topdown=True):
			for name in files:
				if name.startswith("GCA_") and name.endswith(".fna"):
					pezizo_list.append(root + name)
		#print("Samples are: ", pezizo_list)
		empty_list = []
		empty_list.append(args.target_markers)
		#print(empty_list)
		# product function from itertools does the cartesian product (lane * rows), it is like a nested for!!
		list_of_list = list(itertools.product(pezizo_list, empty_list))
		print(list_of_list)
		logging.info("Running exonerate using exonerate_hits.py script from Hybpiper..")	
		args.parallel_exonerate = int(args.parallel_exonerate)
		pool = multiprocessing.Pool(processes=args.parallel_exonerate)
		pool.starmap(run_exonerate_hits, list_of_list)
		
		logging.info("********************************")
		logging.info("* BUILDING FASTA FILES  *")
		logging.info("********************************")
		logging.info("Building alignments from assemblies data")
		get_alignment(args.assemblies)
		logging.info("Building alignments from target enrichment data")
		get_alignment(args.target_enrichment_data)
		merge_alignments(args.assemblies, args.target_enrichment_data)
		
		logging.info("*************************************************")
		logging.info("* PERFORMING ALIGNMENT WITH Mafft *")
		logging.info("*************************************************")
		path_to_merged_alignments = args.target_enrichment_data + '../alignments_merged/'
		#for item in os.listdir(path_to_merged_alignments):
		run_mafft_parallel = "find %s -type f -name '*_merged.fasta' | parallel -j %s mafft --maxiterate 1000 --localpair -thread 1 {} > {}_maffted.fas    ".format(path_to_merged_alignments, args.parallel_mafft)
		os.system(run_mafft_parallel)
		logging.info("******************************************************************")
		logging.info("* PERFORMING ALIGNMENT FILTERING WITH Gblocks *")
		logging.info("******************************************************************")
		logging.info("**************************************************************************")
		logging.info("* RECONSTRUCTING SINGLE MARKER TREES WITH RAxML *")
		logging.info("**************************************************************************")
		logging.info("******************************************************************************")
		logging.info("* PERFORMING ALIGNMENT CONCATENATION WITH Fasconcat  *")
		logging.info("******************************************************************************")
		logging.info("********************************************************************************************")
		logging.info("* RECONSTRUCTING SUPERMATRIX TREE WITH RAxML  *")
		logging.info("********************************************************************************************")
		logging.info("******************************************************************************************")
		logging.info("* RECONSTRUCTION SUPERTREE WITH ASTRAL *")
		logging.info("******************************************************************************************")
if __name__=='__main__':
	logger = logging.getLogger(__name__)
	logFormatter = '%(message)s'
	logging.basicConfig(filename='pipe_logger.log', format=logFormatter, level=logging.DEBUG)
	main()


