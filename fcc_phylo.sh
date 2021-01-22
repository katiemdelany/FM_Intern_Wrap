#potential work around for finding programs
#check FASconCAT
#until [ -s $DIR_FASconCAT/FASconCAT*.pl ]
#    do
#      read -p "DIR_FASconCAT is not found. Please input its installation directory (absolute path, e.g. /home/zf/install/FASconCAT-G):      " DIR_FASconCAT
#    done
#echo "FASconCAT ...... OK"

#change directory to .phy files
#copy fasconcat-g into directory
#run fasconcat-g
perl FASconCAT_v1.11.pl

#then use raxml
raxmlHPC-PTHREADS -n homologs -s FcC_smatrix.phy -m GTRGAMMA -f a -p 194955 -x 12345 -# 100 -T 10
