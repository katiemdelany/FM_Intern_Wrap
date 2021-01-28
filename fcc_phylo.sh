#potential work around for finding programs
#needs testing

#check MAFFT
if [ $(which mafft) ]
    then
      echo "MAFFT ...... OK"
      EXE_MAFFT=$(which mafft)
      DIR_MAFFT=${EXE_MAFFT%/*}
    else
      until [ -x $DIR_MAFFT/mafft ]
        do
          read -p "MAFFT is not found. Please input its installation directory (absolute path, e.g. /usr/bin):      " DIR_MAFFT
        done
      echo "MAFFT ...... OK"
fi

#check FASconCAT
until [ -s $DIR_FASconCAT/FASconCAT*.pl ]
    do
      read -p "DIR_FASconCAT is not found. Please input its installation directory (absolute path, e.g. /home/zf/install/FASconCAT-G):      " DIR_FASconCAT
    done
echo "FASconCAT ...... OK"

#Check the threads can be used
read -p "Please input the number of threads/cores (e.g. 8):      " THREADS
until [ $THREADS -gt 0 ]
    do
      read -p "Please input the correct integer for the number of threads/cores (e.g. 8):      " THREADS
    done

#change directory to .phy files
#copy fasconcat-g into directory
#run fasconcat-g
perl FASconCAT_v1.11.pl

#then use raxml
raxmlHPC-PTHREADS -n homologs -s FcC_smatrix.phy -m GTRGAMMA -f a -p 194955 -x 12345 -# 100 -T 10
