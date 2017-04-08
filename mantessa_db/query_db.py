import MySQLdb
import pandas as pd
import datetime
import os
import sys

date_dat = sys.argv[1]

print " Do not press Ctl+C from here on!!"
os.system("mysql -e \"select ip,latitude,longitude  from mantessa where d_"+date_dat+" = 0 \" -u root  mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+".csv")

df = pd.read_csv("../failure_data/d_"+date_dat+".csv")
print len(df)