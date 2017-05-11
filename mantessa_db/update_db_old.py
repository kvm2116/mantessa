import MySQLdb
import pandas as pd
import datetime
import numpy as np
import sys

date_dat = sys.argv[1]
reader = pd.read_csv('../data/'+date_dat+'.csv',chunksize=10000)
#df2 = df.head()

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


start = datetime.datetime.now()
c= 0
try:
	for df in reader:
		df = df[df.location_latitude.apply(lambda x: np.isreal(x))]
		df = df[df.location_longitude.apply(lambda x: np.isreal(x))]
		df=df.values.tolist()
		#c += len(df)
		#print c
		for item in df:
			#print item[1], item[2], item[3]
			dbcursor.callproc('update_mantessa',('d_'+date_dat,item[0],item[1],item[2]))
			result = dbcursor.fetchall()

						
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e) 
	conn.rollback()
end = datetime.datetime.now()

print end-start
conn.close()
