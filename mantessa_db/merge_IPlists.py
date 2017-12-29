"""
An script to (supposedly) merge two set of IP addresses by taking the intersection of IPs

Author: Niloofar Bayat
nb2776@columbia.edu


"""


import MySQLdb
import pandas as pd
import datetime
import sys
from ip import *

#column_names = ['ip', 'latitude', 'longitude']
df2 = pd.read_csv('counties_wl-2.csv', sep=",")
'''
print(df2)
df2['ip'] = df2['ip'].apply(lambda x: ip2long(x))
df2 = df2[df2.ip.apply(lambda x: x!=-1)]
df2 = df2.sort_values('ip')
df2.to_csv('counties_wl-2.csv',index=False)
print(df2)
'''

print "Starting Pre-Processing"
date_dat = '20170712T20_30_25Z'
date_dat = date_dat.strip()
#date_dat = sys.argv[1]
column_names = ['ip']
df1 = pd.read_csv(date_dat.strip()+'.csv', sep="\s+", header = None, names = column_names)
#print(df1)
df1['ip'] = df1['ip'].apply(lambda x: ip2long(x))
#print(df1)
df1 = df1[df1.ip.apply(lambda x: x!=-1)]
df1 = df1.sort_values('ip')
df1.to_csv(date_dat+'_2.csv',index=False)
lst = [df1]

#result = pd.concat([df2, df1], axis=1, join='inner')
result = pd.merge(df1, df2, on='ip')
print(result)
result.to_csv('result.csv',index=False)


print "Pre-Processing done!"




### Code cleaning: delete from mantessa where ip = 0;
