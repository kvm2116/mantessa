import MySQLdb
import pandas as pd
import datetime
import os
import sys

date_dat = sys.argv[1]

print " Do not press Ctl+C from here on!!"
os.system("mysql -e \"select ip,latitude,longitude,counter, d_"+date_dat+" from mantessa where latitude <42 and latitude>32 and longitude<-114 and longitude>-125\" -u root -p  mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+".csv")
#os.system("mysql -e \"select ip,latitude,longitude  from mantessa where d_"+date_dat+" = 0 \" -u root  mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+".csv")
#os.system("mysql -e \"select longitude as lng, latitude as lat from mantessa where d_"+date_dat+" = 0 and counter > 6\" -u jmz2135 -p  mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+".csv")

#os.system("mysql -e \"select latitude,longitude, c1 as Off, c2 as Total, c1/c2 as fraction from ((select latitude, longitude, count(*) as c1 from mantessa where counter>=30 and d_20170430=0 group by latitude,longitude)a natural join  (select latitude, longitude, count(*) as c2 from mantessa where counter>=30 group by latitude,longitude)b) order by fraction desc;\" -u jmz2135 -p mantessa_db | tr '\t' ',' > ../failure_data/d_"+date_dat+"_frac.csv")

# Fractional Distribution dump code
#os.system("mysql -e \"select latitude,longitude, c1 as Off, c2 as Total, c1/c2 as fraction from ((select latitude, longitude, count(*) as c1 from mantessa where d_20170123=0 and counter >= 50 group by latitude,longitude)a natural join  (select latitude, longitude, count(*) as c2 from mantessa where counter >=50 group by latitude,longitude)b) order by fraction desc;\"  -u root -p  mantessa_db | tr '\t' ',' > ../failure_data/sau_50t.csv");

#os.system("mysql -e \"select *  from mantessa where latitude = 38.5816000 and longitude = -121.4944000 \" -u root -p  mantessa_db | tr '\t' ',' > ../failure_data/sacramento.csv")
#df = pd.read_csv("../failure_data/d_"+date_dat+"_frac.csv")
#print len(df)
