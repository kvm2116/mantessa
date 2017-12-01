import MySQLdb as db
import pandas as pd
import datetime
import os
import sys
import csv

print " Do not press Ctl+C from here on!!"

con = db.connect(host="localhost", user="jmz2135", passwd="josh@mantessa", db="mantessa_db")

res = []

with open("/local/mantessa/zmap_scans/whitelist2.conf") as f:
    with con:
        cursor = con.cursor()
        for cur_ip in f:
            print cur_ip.replace(".","")
            cursor.execute("SELECT * FROM mantessa WHERE ip=\'" + cur_ip.replace(".","") + "\';")
            try:
                res.append(cursor.fetchall()[0])
            except IndexError:
                pass

print(res)

with open('whitelist-res.csv', 'wb') as out:
    csv_out=csv.writer(out)
    for row in res:
        csv_out.writerow(row)
#os.system("mysql -e \"select * from mantessa where ip=\'"+cur_ip.strip('.')+"\'\" -u jmz2135 -p  mantessa_db | tr '\t' ',' > whitelist_rows.csv")
