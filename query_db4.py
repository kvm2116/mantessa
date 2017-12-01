import MySQLdb as db
import pandas as pd
import datetime
import os
import sys
import string

date_dat = sys.argv[1]
yr = int(date_dat[0:4])
mo = int(date_dat[4:6])
dy = int(date_dat[6:8])
hr = int(date_dat[9:11])
mi = int(date_dat[12:14])
se = int(date_dat[15:17])
check_date = datetime.datetime(yr,mo,dy,hr,mi,se)


check_date_int = int(date_dat.replace('T','').replace('_',''))

print check_date_int

print " Do not press Ctl+C from here on!!"

con = db.connect(host="localhost",user="root",passwd="DNA@mantessa!",db="mantessa_db4");

with con:
    cursor = con.cursor()
    cursor.execute("DROP VIEW IF EXISTS wl_frac_" + str(date_dat) +";")
    cursor.execute("SELECT * FROM mantessa LIMIT 1;")
    head = cursor.description
    censys_dates = []
    for row in head[4:]:
        date = int(str(row).replace('T','').replace('_','').replace('Z',''))
        if date < check_date_int:
            censys_dates.append(str(row))
    runs = len(censys_dates)
    min = float(len(censys_dates))*.6
    sql = "CREATE VIEW wl_frac" + date_dat + " AS SELECT latitude, longitude, " + date_dat + "Z, " + "Z, ".join(censys_dates) + "Z, (" + "Z+".join(censys_dates) + "Z) AS run_counter, FROM mantessa;"
    cursor.execute(sql)
    cursor.execute("SELECT * FROM wl_frac" + date_dat + " LIMIT 2;")
    cursor.close()

newsql = "select latitude,longitude, c1 as Off, c2 as Total, c1/c2 as fraction from ((select latitude, longitude, count(*) as c1 from wl_frac" + str(check_date) + " where " + date_dat + "=0 and run_counter >= " + str(min) + " group by latitude,longitude)a natural join (select latitude, longitude, count(*) as c2 from wl_frac" + date_dat + " where run_counter >= " + str(min) + " group by latitude,longitude)b) order by fraction desc;"

os.system("mysql -e  " + newsql + "  -u root -p  mantessa_db4 | tr '\t' ',' > ../failure_data/new_test_" + date_dat + ".csv")

