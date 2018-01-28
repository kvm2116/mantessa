"""
The most recent script to upate the existing database (called mantessa_db9) for the entire united states

The database includes: ip, latitude, longitude, zipCode, stateCode, cityName

Author: Niloofar Bayat
nb2776@columbia.edu
"""

import numpy as np
import MySQLdb
import pandas as pd
import datetime
import sys
from ip import *
import os.path

print "Starting Pre-Processing"
with open('../USData/DateDat', 'r') as input_file:
    for date_dat in input_file:
        #date_dat = sys.argv[1]
        date_dat = date_dat.strip()
        if not os.path.isfile('../USconverted/'+date_dat+'.csv') or os.path.isfile('../USData/'+date_dat+'_long.csv'):
            continue
        column_names = ['ip','latitude','longitude','zipCode','stateCode','cityName']
        df1 = pd.read_csv('../USconverted/'+date_dat+'.csv', sep=",", header = None, names = column_names)
  df1['ip'] = df1['ip'].apply(lambda x: ip2long(x))
        df1 = df1.drop(df1[df1.ip == -1].index)
  df1 = df1.sort_values('ip')
        '''
        tmp = df1.values.tolist()
        result = (pd.merge(df1, df2, how = 'inner', on='ip') for df2 in reader)
    
        result = pd.concat(result, ignore_index=True)
        #result = pd.merge(df1, df2, how = 'inner', on='ip')
        #print(len(result))     
        #print(result.head(), df1.head(), df2.head())
        #break
        '''
        df1.to_csv('../USData/'+date_dat+'_long.csv',index=False)
        print (date_dat,len(df1))
        lst = [df1]
        del df1

        print "Pre-Processing done!"

        reader = pd.read_csv('../USData/'+date_dat+'_long.csv', sep=",",chunksize=10000)

        print " Do not press Ctl+C from here on!!"


        conn = MySQLdb.connect(host= "localhost",
                          user="root",
                          passwd="DNA@mantessa!",
                          db="mantessa_db9")
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
        stmt = "INSERT IGNORE INTO mantessa (ip,latitude,longitude,zipCode,stateCode,cityName,"+col+") VALUES (%s,%s,%s,%s,%s,%s,1) ON DUPLICATE KEY UPDATE counter=counter+1 ,"+col+"=1;"
        c = 0
        try:
            for df in reader:
                df = df.replace(np.nan,'',regex=True)

                df=df.values.tolist()
                #c+= len(df)
                #print c
                #print df
                #print len(df)
                #print len(df[0])
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
  with open('db_config.py','w') as config:
    output = "COLUMN_NAME='"+date_dat+"'"
    config.write(output)
### Code cleaning: delete from mantessa where ip = 0;