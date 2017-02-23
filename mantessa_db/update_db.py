import MySQLdb
import pandas as pd
import datetime

f_name = '20170208'
reader = pd.read_csv(f_name+'.csv',chunksize=10000)
#df2 = df.head()


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
		df=df.values.tolist()
		for item in df:
			#print item[1], item[2], item[3]
			dbcursor.callproc('update_mantessa',('d_'+f_name,item[1],item[2],item[3]))
			result = dbcursor.fetchall()
						
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e) 
	conn.rollback()
end = datetime.datetime.now()

print end-start
conn.close()
