import MySQLdb
import pandas as pd
import datetime
import numpy as np

f_name = '20170208'
reader = pd.read_csv(f_name+'.csv',chunksize=10000)
#df2 = df.head()

print " Do not press Ctl+C from here on!!"

conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="",
                  db="mantessa_db")
dbcursor = conn.cursor()


try:
	dbcursor.execute("alter table mantessa add d_"+f_name+" BOOLEAN DEFAULT 0")
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e)
	conn.rollback()

dbcursor = conn.cursor()


start = datetime.datetime.now()

try:
	for df in reader:
		df = df[df.location_latitude.apply(lambda x: np.isreal(x))]
		df = df[df.location_longitude.apply(lambda x: np.isreal(x))]
		df=df.values.tolist()
		print len(df)
		for item in df:
			#print item[1], item[2], item[3]
			dbcursor.callproc('update_mantessa',('d_'+f_name,item[0],item[1],item[2]))
			result = dbcursor.fetchall()

						
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e) 
	conn.rollback()
end = datetime.datetime.now()

print end-start
conn.close()
