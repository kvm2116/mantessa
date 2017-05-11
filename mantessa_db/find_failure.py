import MySQLdb
import pandas as pd
import datetime
import sys
from ip import *

print "Starting Pre-Processing"

date_dat = sys.argv[1]
df1 = pd.read_csv('../data/'+date_dat+'.csv')
df1['ip'] = df1['ip'].apply(lambda x: ip2long(x))
df1 = df1[df1.ip.apply(lambda x: x!=-1)]
df1 = df1.sort_values('ip')
df1.to_csv('../data/'+date_dat+'.csv',index=False)
lst = [df1]
del df1
del lst

print "Pre-Processing done!"

reader = pd.read_csv('../data/'+date_dat+'.csv',chunksize=10000)

print " Do not press Ctl+C from here on!!"


conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="DNA@mantessa!",
                  db="mantessa_db")
dbcursor = conn.cursor()

try:
	dbcursor.execute("alter table mantessa add d_"+date_dat+" BOOLEAN DEFAULT 0")
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e)
	conn.rollback()

dbcursor = conn.cursor()
col= 'd_'+date_dat
start = datetime.datetime.now()
stmt = "UPDATE IGNORE  mantessa set "+col+"=1 where ip = %s and latitude = %s and longitude = %s;"
c = 0
try:
	for df in reader:
		df=df.values.tolist()
		#c+= len(df)
		#print c
		#print df
		dbcursor.executemany(stmt,df)
        conn.commit()
except Exception as e:
        print "Oops!! Something went wrong "+str(e)
        conn.rollback()
end = datetime.datetime.now()
print end-start
conn.close()
