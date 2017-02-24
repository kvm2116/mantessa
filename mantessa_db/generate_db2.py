import MySQLdb
import pandas as pd
import datetime

reader = pd.read_csv('20170207.csv',chunksize=10000)
#df2 = df.head()


conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="",
                  db="mantessa_db")
dbcursor = conn.cursor()
start = datetime.datetime.now()
stmt = "INSERT INTO mantessa VALUES (INET_ATON(%s),%s,%s,1,1)"
try:
	for df in reader:
		df=df.values.tolist()
		l = len(df)
		print df
		dbcursor.executemany(stmt,df)
			
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e) 
	conn.rollback()
end = datetime.datetime.now()
print end-start
conn.close()
