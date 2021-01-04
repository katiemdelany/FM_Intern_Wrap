#!/bin/bash

for f in $(ls *.aligned.fas);
do 
	name=${f%%.aligned.fas}
        python3	~/FM_Intern_Wrap/fasTophy.py --in_fas $f --out_phy $name.aligned.phy

done
