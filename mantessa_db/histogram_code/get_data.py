import MySQLdb
import pandas as pd
import datetime
import os
import sys

date_dat = sys.argv[1]

print " Do not press Ctl+C from here on!!"
#os.system("mysql -e \"select ip,latitude,longitude  from mantessa where d_"+date_dat+" = 0 \" -u root  mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+".csv")
#os.system("mysql -e \"select longitude as lng, latitude as lat from mantessa where d_"+date_dat+" = 0 and counter > 6\" -u jmz2135 -p  mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+".csv")
os.system("mysql -e \"select count(*),d_"+date_dat+",counter from mantessa where latitude=38.5816000 and longitude=-121.4944000  group  by counter,d_"+date_dat+"  \" -u root -p  mantessa_db | tr '\t' ',' > d_"+date_dat+".csv")
#df = pd.read_csv("../failure_data/d_"+date_dat+".csv")
#print len(df)
