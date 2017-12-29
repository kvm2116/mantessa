#!/Bin/bash

# script to run the scans in the United States
# Author: Niloofar Bayat
# nb2776@columbia.edu

export PATH="/usr/local/bin:/usr/local/sbin:/opt/local/bin:/opt/local/sbin:/opt/local/bin:/opt/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/sbin:/usr/local/sbin"
cd /Users/niloofarbayat/Desktop/Dan/mantessa/USData
sudo zmap -B 15M --probe-module=icmp_echoscan  --whitelist-file="/Users/niloofarbayat/Desktop/Dan/mantessa/Scripts/CCCS_ranges_converted.csv" -o results3.csv
var=$(date +"20%y%m%dT%TZ" | sed 's/:/_/g')
#var=$(python rename.py $date_dat)
mv results3.csv "$var.csv"
echo "$var" >> DateDat 

gdrive upload --parent 1e1af9s1xqwHJCUR7sKY937tyxCghLdcA "$var.csv"
