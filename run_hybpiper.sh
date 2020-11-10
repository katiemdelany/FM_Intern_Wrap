################################
#run HyPiper with blastx option#
#if target enrichment or de novo selected#
################################
target_file_path = $1
path_to_dataset = $2

git clone https://github.com/mossmatters/HybPiper.git

mkdir -p hybpiper_blastx
cd hybpiper_blastx

#runnning HybPiper main script on user input dataset
while read name;
do ../HybPiper/reads_first.py -b target_file_path -r path_to_dataset/$name*.fastq --prefix $name --cpu 6
done < ./namelist.txt

#Visualizing Results
python3 ../HybPiper/get_seq_lengths.py target_file_path namelist.txt aa > test_seq_lengths.txt
