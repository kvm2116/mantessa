import MySQLdb
import pandas as pd
import datetime
import sys

date_dat = sys.argv[1]
reader = pd.read_csv('../data/'+date_dat+'.csv',chunksize=10000)
#df2 = df.head()

print " Do not press Ctl+C from here on!!"


conn = MySQLdb.connect(host= "localhost",
                  user="ta2482",
                  passwd="ta2482@mantessa",
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
stmt = "INSERT IGNORE INTO mantessa VALUES (INET_ATON(%s),%s,%s,1,1)"
try:
	for df in reader:
		df=df.values.tolist()
		l = len(df)
		print l
		#print df
		dbcursor.executemany(stmt,df)
	stmt2 = "delete from mantessa where ip = 0;"	
	dbcursor.execute(stmt2)	
	conn.commit()
except Exception as e:
	print "Oops!! Something went wrong "+str(e) 
	conn.rollback()
end = datetime.datetime.now()
print end-start
conn.close()

### Code cleaning: delete from mantessa where ip = 0;
